# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\cffi\cparser.py
from . import model
from .commontypes import COMMON_TYPES, resolve_common_type
from .error import FFIError, CDefError
try:
    from . import _pycparser as pycparser
except ImportError:
    import pycparser

import weakref, re, sys
try:
    if sys.version_info < (3, ):
        import thread as _thread
    else:
        import _thread
    lock = _thread.allocate_lock()
except ImportError:
    lock = None

CDEF_SOURCE_STRING = '<cdef source string>'
_r_comment = re.compile('/\\*.*?\\*/|//([^\\n\\\\]|\\\\.)*?$', re.DOTALL | re.MULTILINE)
_r_define = re.compile('^\\s*#\\s*define\\s+([A-Za-z_][A-Za-z_0-9]*)\\b((?:[^\\n\\\\]|\\\\.)*?)$', re.DOTALL | re.MULTILINE)
_r_partial_enum = re.compile('=\\s*\\.\\.\\.\\s*[,}]|\\.\\.\\.\\s*\\}')
_r_enum_dotdotdot = re.compile('__dotdotdot\\d+__$')
_r_partial_array = re.compile('\\[\\s*\\.\\.\\.\\s*\\]')
_r_words = re.compile('\\w+|\\S')
_parser_cache = None
_r_int_literal = re.compile('-?0?x?[0-9a-f]+[lu]*$', re.IGNORECASE)
_r_stdcall1 = re.compile('\\b(__stdcall|WINAPI)\\b')
_r_stdcall2 = re.compile('[(]\\s*(__stdcall|WINAPI)\\b')
_r_cdecl = re.compile('\\b__cdecl\\b')
_r_extern_python = re.compile('\\bextern\\s*"(Python|Python\\s*\\+\\s*C|C\\s*\\+\\s*Python)"\\s*.')
_r_star_const_space = re.compile('[*]\\s*((const|volatile|restrict)\\b\\s*)+')
_r_int_dotdotdot = re.compile('(\\b(int|long|short|signed|unsigned|char)\\s*)+\\.\\.\\.')
_r_float_dotdotdot = re.compile('\\b(double|float)\\s*\\.\\.\\.')

def _get_parser():
    global _parser_cache
    if _parser_cache is None:
        _parser_cache = pycparser.CParser()
    return _parser_cache


def _workaround_for_old_pycparser(csource):
    parts = []
    while True:
        match = _r_star_const_space.search(csource)
        if not match:
            break
        parts.append(csource[:match.start()])
        parts.append('(')
        closing = ')'
        parts.append(match.group())
        endpos = match.end()
        if csource.startswith('*', endpos):
            parts.append('(')
            closing += ')'
        level = 0
        i = endpos
        while i < len(csource):
            c = csource[i]
            if c == '(':
                level += 1
            else:
                if c == ')':
                    if level == 0:
                        break
                    level -= 1
                else:
                    if c in ',;=':
                        if level == 0:
                            break
            i += 1

        csource = csource[endpos:i] + closing + csource[i:]

    parts.append(csource)
    return ''.join(parts)


def _preprocess_extern_python(csource):
    parts = []
    while True:
        match = _r_extern_python.search(csource)
        if not match:
            break
        endpos = match.end() - 1
        parts.append(csource[:match.start()])
        if 'C' in match.group(1):
            parts.append('void __cffi_extern_python_plus_c_start; ')
        else:
            parts.append('void __cffi_extern_python_start; ')
        if csource[endpos] == '{':
            closing = csource.find('}', endpos)
            if closing < 0:
                raise CDefError('\'extern "Python" {\': no \'}\' found')
            if csource.find('{', endpos + 1, closing) >= 0:
                raise NotImplementedError('cannot use { } inside a block \'extern "Python" { ... }\'')
            parts.append(csource[endpos + 1:closing])
            csource = csource[closing + 1:]
        else:
            semicolon = csource.find(';', endpos)
            if semicolon < 0:
                raise CDefError('\'extern "Python": no \';\' found')
            parts.append(csource[endpos:semicolon + 1])
            csource = csource[semicolon + 1:]
        parts.append(' void __cffi_extern_python_stop;')

    parts.append(csource)
    return ''.join(parts)


def _preprocess(csource):
    csource = _r_comment.sub(' ', csource)
    macros = {}
    for match in _r_define.finditer(csource):
        macroname, macrovalue = match.groups()
        macrovalue = macrovalue.replace('\\\n', '').strip()
        macros[macroname] = macrovalue

    csource = _r_define.sub('', csource)
    if pycparser.__version__ < '2.14':
        csource = _workaround_for_old_pycparser(csource)
    csource = _r_stdcall2.sub(' volatile volatile const(', csource)
    csource = _r_stdcall1.sub(' volatile volatile const ', csource)
    csource = _r_cdecl.sub(' ', csource)
    csource = _preprocess_extern_python(csource)
    csource = _r_partial_array.sub('[__dotdotdotarray__]', csource)
    matches = list(_r_partial_enum.finditer(csource))
    for number, match in enumerate(reversed(matches)):
        p = match.start()
        if csource[p] == '=':
            p2 = csource.find('...', p, match.end())
            assert p2 > p
            csource = '%s,__dotdotdot%d__ %s' % (csource[:p], number,
             csource[p2 + 3:])
        else:
            assert csource[p:p + 3] == '...'
            csource = '%s __dotdotdot%d__ %s' % (csource[:p], number,
             csource[p + 3:])

    csource = _r_int_dotdotdot.sub(' __dotdotdotint__ ', csource)
    csource = _r_float_dotdotdot.sub(' __dotdotdotfloat__ ', csource)
    return (
     csource.replace('...', ' __dotdotdot__ '), macros)


def _common_type_names(csource):
    look_for_words = set(COMMON_TYPES)
    look_for_words.add(';')
    look_for_words.add(',')
    look_for_words.add('(')
    look_for_words.add(')')
    look_for_words.add('typedef')
    words_used = set()
    is_typedef = False
    paren = 0
    previous_word = ''
    for word in _r_words.findall(csource):
        if word in look_for_words:
            if word == ';':
                if is_typedef:
                    words_used.discard(previous_word)
                    look_for_words.discard(previous_word)
                    is_typedef = False
            else:
                if word == 'typedef':
                    is_typedef = True
                    paren = 0
                else:
                    if word == '(':
                        paren += 1
                    else:
                        if word == ')':
                            paren -= 1
                        else:
                            if word == ',':
                                if is_typedef:
                                    if paren == 0:
                                        words_used.discard(previous_word)
                                        look_for_words.discard(previous_word)
                            else:
                                words_used.add(word)
        previous_word = word

    return words_used


class Parser(object):

    def __init__(self):
        self._declarations = {}
        self._included_declarations = set()
        self._anonymous_counter = 0
        self._structnode2type = weakref.WeakKeyDictionary()
        self._options = {}
        self._int_constants = {}
        self._recomplete = []
        self._uses_new_feature = None

    def _parse(self, csource):
        csource, macros = _preprocess(csource)
        ctn = _common_type_names(csource)
        typenames = []
        for name in sorted(self._declarations):
            if name.startswith('typedef '):
                name = name[8:]
                typenames.append(name)
                ctn.discard(name)

        typenames += sorted(ctn)
        csourcelines = []
        csourcelines.append('# 1 "<cdef automatic initialization code>"')
        for typename in typenames:
            csourcelines.append('typedef int %s;' % typename)

        csourcelines.append('typedef int __dotdotdotint__, __dotdotdotfloat__, __dotdotdot__;')
        csourcelines.append('# 1 "%s"' % (CDEF_SOURCE_STRING,))
        csourcelines.append(csource)
        fullcsource = '\n'.join(csourcelines)
        if lock is not None:
            lock.acquire()
        try:
            try:
                ast = _get_parser().parse(fullcsource)
            except pycparser.c_parser.ParseError as e:
                self.convert_pycparser_error(e, csource)

        finally:
            if lock is not None:
                lock.release()

        return (
         ast, macros, csource)

    def _convert_pycparser_error(self, e, csource):
        line = None
        msg = str(e)
        match = re.match('%s:(\\d+):' % (CDEF_SOURCE_STRING,), msg)
        if match:
            linenum = int(match.group(1), 10)
            csourcelines = csource.splitlines()
            if 1 <= linenum <= len(csourcelines):
                line = csourcelines[(linenum - 1)]
        return line

    def convert_pycparser_error(self, e, csource):
        line = self._convert_pycparser_error(e, csource)
        msg = str(e)
        if line:
            msg = 'cannot parse "%s"\n%s' % (line.strip(), msg)
        else:
            msg = 'parse error\n%s' % (msg,)
        raise CDefError(msg)

    def parse(self, csource, override=False, packed=False, dllexport=False):
        prev_options = self._options
        try:
            self._options = {'override':override, 
             'packed':packed, 
             'dllexport':dllexport}
            self._internal_parse(csource)
        finally:
            self._options = prev_options

    def _internal_parse(self, csource):
        ast, macros, csource = self._parse(csource)
        self._process_macros(macros)
        iterator = iter(ast.ext)
        for decl in iterator:
            if decl.name == '__dotdotdot__':
                break
        else:
            assert 0

        current_decl = None
        try:
            self._inside_extern_python = '__cffi_extern_python_stop'
            for decl in iterator:
                current_decl = decl
                if isinstance(decl, pycparser.c_ast.Decl):
                    self._parse_decl(decl)
                elif isinstance(decl, pycparser.c_ast.Typedef):
                    if not decl.name:
                        raise CDefError('typedef does not declare any name', decl)
                    else:
                        quals = 0
                        if isinstance(decl.type.type, pycparser.c_ast.IdentifierType):
                            if decl.type.type.names[(-1)].startswith('__dotdotdot'):
                                realtype = self._get_unknown_type(decl)
                        elif isinstance(decl.type, pycparser.c_ast.PtrDecl) and isinstance(decl.type.type, pycparser.c_ast.TypeDecl) and isinstance(decl.type.type.type, pycparser.c_ast.IdentifierType) and decl.type.type.type.names[(-1)].startswith('__dotdotdot'):
                            realtype = self._get_unknown_ptr_type(decl)
                        else:
                            realtype, quals = self._get_type_and_quals((decl.type),
                              name=(decl.name), partial_length_ok=True)
                    self._declare(('typedef ' + decl.name), realtype, quals=quals)
                elif decl.__class__.__name__ == 'Pragma':
                    pass
                else:
                    raise CDefError('unexpected <%s>: this construct is valid C but not valid in cdef()' % decl.__class__.__name__, decl)

        except CDefError as e:
            if len(e.args) == 1:
                e.args = e.args + (current_decl,)
            raise
        except FFIError as e:
            msg = self._convert_pycparser_error(e, csource)
            if msg:
                e.args = (
                 e.args[0] + '\n    *** Err: %s' % msg,)
            raise

    def _add_constants(self, key, val):
        if key in self._int_constants:
            if self._int_constants[key] == val:
                return
            raise FFIError('multiple declarations of constant: %s' % (key,))
        self._int_constants[key] = val

    def _add_integer_constant(self, name, int_str):
        int_str = int_str.lower().rstrip('ul')
        neg = int_str.startswith('-')
        if neg:
            int_str = int_str[1:]
        if int_str.startswith('0'):
            if int_str != '0':
                if not int_str.startswith('0x'):
                    int_str = '0o' + int_str[1:]
        pyvalue = int(int_str, 0)
        if neg:
            pyvalue = -pyvalue
        self._add_constants(name, pyvalue)
        self._declare('macro ' + name, pyvalue)

    def _process_macros(self, macros):
        for key, value in macros.items():
            value = value.strip()
            if _r_int_literal.match(value):
                self._add_integer_constant(key, value)
            else:
                if value == '...':
                    self._declare('macro ' + key, value)
                else:
                    raise CDefError('only supports one of the following syntax:\n  #define %s ...     (literally dot-dot-dot)\n  #define %s NUMBER  (with NUMBER an integer constant, decimal/hex/octal)\ngot:\n  #define %s %s' % (
                     key, key, key, value))

    def _declare_function(self, tp, quals, decl):
        tp = self._get_type_pointer(tp, quals)
        if self._options.get('dllexport'):
            tag = 'dllexport_python '
        else:
            if self._inside_extern_python == '__cffi_extern_python_start':
                tag = 'extern_python '
            else:
                if self._inside_extern_python == '__cffi_extern_python_plus_c_start':
                    tag = 'extern_python_plus_c '
                else:
                    tag = 'function '
        self._declare(tag + decl.name, tp)

    def _parse_decl(self, decl):
        node = decl.type
        if isinstance(node, pycparser.c_ast.FuncDecl):
            tp, quals = self._get_type_and_quals(node, name=(decl.name))
            assert isinstance(tp, model.RawFunctionType)
            self._declare_function(tp, quals, decl)
        else:
            if isinstance(node, pycparser.c_ast.Struct):
                self._get_struct_union_enum_type('struct', node)
            else:
                if isinstance(node, pycparser.c_ast.Union):
                    self._get_struct_union_enum_type('union', node)
                else:
                    if isinstance(node, pycparser.c_ast.Enum):
                        self._get_struct_union_enum_type('enum', node)
                    else:
                        if not decl.name:
                            raise CDefError('construct does not declare any variable', decl)
        if decl.name:
            tp, quals = self._get_type_and_quals(node, partial_length_ok=True)
            if tp.is_raw_function:
                self._declare_function(tp, quals, decl)
            elif tp.is_integer_type():
                if hasattr(decl, 'init'):
                    if hasattr(decl.init, 'value'):
                        if _r_int_literal.match(decl.init.value):
                            self._add_integer_constant(decl.name, decl.init.value)
            elif tp.is_integer_type():
                if isinstance(decl.init, pycparser.c_ast.UnaryOp):
                    if decl.init.op == '-':
                        if hasattr(decl.init.expr, 'value'):
                            if _r_int_literal.match(decl.init.expr.value):
                                self._add_integer_constant(decl.name, '-' + decl.init.expr.value)
            elif tp is model.void_type:
                if decl.name.startswith('__cffi_extern_python_'):
                    self._inside_extern_python = decl.name
            elif self._inside_extern_python != '__cffi_extern_python_stop':
                raise CDefError('cannot declare constants or variables with \'extern "Python"\'')
            elif quals & model.Q_CONST and not tp.is_array_type:
                self._declare(('constant ' + decl.name), tp, quals=quals)
            else:
                self._declare(('variable ' + decl.name), tp, quals=quals)

    def parse_type(self, cdecl):
        return self.parse_type_and_quals(cdecl)[0]

    def parse_type_and_quals(self, cdecl):
        ast, macros = self._parse('void __dummy(\n%s\n);' % cdecl)[:2]
        assert not macros
        exprnode = ast.ext[(-1)].type.args.params[0]
        if isinstance(exprnode, pycparser.c_ast.ID):
            raise CDefError("unknown identifier '%s'" % (exprnode.name,))
        return self._get_type_and_quals(exprnode.type)

    def _declare(self, name, obj, included=False, quals=0):
        if name in self._declarations:
            prevobj, prevquals = self._declarations[name]
            if prevobj is obj:
                if prevquals == quals:
                    return
        else:
            if not self._options.get('override'):
                raise FFIError('multiple declarations of %s (for interactive usage, try cdef(xx, override=True))' % (
                 name,))
            elif not '__dotdotdot__' not in name.split():
                raise AssertionError
            self._declarations[name] = (
             obj, quals)
            if included:
                self._included_declarations.add(obj)

    def _extract_quals(self, type):
        quals = 0
        if isinstance(type, (pycparser.c_ast.TypeDecl,
         pycparser.c_ast.PtrDecl)):
            if 'const' in type.quals:
                quals |= model.Q_CONST
            else:
                if 'volatile' in type.quals:
                    quals |= model.Q_VOLATILE
                if 'restrict' in type.quals:
                    quals |= model.Q_RESTRICT
        return quals

    def _get_type_pointer(self, type, quals, declname=None):
        if isinstance(type, model.RawFunctionType):
            return type.as_function_pointer()
        else:
            if isinstance(type, model.StructOrUnionOrEnum):
                if type.name.startswith('$'):
                    if type.name[1:].isdigit():
                        if type.forcename is None:
                            if declname is not None:
                                return model.NamedPointerType(type, declname, quals)
            return model.PointerType(type, quals)

    def _get_type_and_quals(self, typenode, name=None, partial_length_ok=False):
        if isinstance(typenode, pycparser.c_ast.TypeDecl):
            if isinstance(typenode.type, pycparser.c_ast.IdentifierType):
                if len(typenode.type.names) == 1:
                    if 'typedef ' + typenode.type.names[0] in self._declarations:
                        tp, quals = self._declarations[('typedef ' + typenode.type.names[0])]
                        quals |= self._extract_quals(typenode)
                        return (
                         tp, quals)
                if isinstance(typenode, pycparser.c_ast.ArrayDecl):
                    if typenode.dim is None:
                        length = None
                    else:
                        length = self._parse_constant((typenode.dim),
                          partial_length_ok=partial_length_ok)
                    tp, quals = self._get_type_and_quals((typenode.type), partial_length_ok=partial_length_ok)
                    return (model.ArrayType(tp, length), quals)
                if isinstance(typenode, pycparser.c_ast.PtrDecl):
                    itemtype, itemquals = self._get_type_and_quals(typenode.type)
                    tp = self._get_type_pointer(itemtype, itemquals, declname=name)
                    quals = self._extract_quals(typenode)
                    return (tp, quals)
            else:
                if isinstance(typenode, pycparser.c_ast.TypeDecl):
                    quals = self._extract_quals(typenode)
                    type = typenode.type
                    if isinstance(type, pycparser.c_ast.IdentifierType):
                        names = list(type.names)
                        if names != ['signed', 'char']:
                            prefixes = {}
                            while names:
                                name = names[0]
                                if name in ('short', 'long', 'signed', 'unsigned'):
                                    prefixes[name] = prefixes.get(name, 0) + 1
                                    del names[0]
                                else:
                                    break

                            newnames = []
                            for prefix in ('unsigned', 'short', 'long'):
                                for i in range(prefixes.get(prefix, 0)):
                                    newnames.append(prefix)

                            if not names:
                                names = [
                                 'int']
                            if names == ['int']:
                                if 'short' in prefixes or 'long' in prefixes:
                                    names = []
                            names = newnames + names
                        ident = ' '.join(names)
                        if ident == 'void':
                            return (model.void_type, quals)
                        else:
                            if ident == '__dotdotdot__':
                                raise FFIError(':%d: bad usage of "..."' % typenode.coord.line)
                            tp0, quals0 = resolve_common_type(self, ident)
                            return (
                             tp0, quals | quals0)
                    if isinstance(type, pycparser.c_ast.Struct):
                        tp = self._get_struct_union_enum_type('struct', type, name)
                        return (tp, quals)
                    if isinstance(type, pycparser.c_ast.Union):
                        tp = self._get_struct_union_enum_type('union', type, name)
                        return (tp, quals)
                    if isinstance(type, pycparser.c_ast.Enum):
                        tp = self._get_struct_union_enum_type('enum', type, name)
                        return (tp, quals)
            if isinstance(typenode, pycparser.c_ast.FuncDecl):
                return (self._parse_function_type(typenode, name), 0)
        else:
            if isinstance(typenode, pycparser.c_ast.Struct):
                return (self._get_struct_union_enum_type('struct', typenode, name, nested=True), 0)
            if isinstance(typenode, pycparser.c_ast.Union):
                return (self._get_struct_union_enum_type('union', typenode, name, nested=True), 0)
        raise FFIError(':%d: bad or unsupported type declaration' % typenode.coord.line)

    def _parse_function_type(self, typenode, funcname=None):
        params = list(getattr(typenode.args, 'params', []))
        for i, arg in enumerate(params):
            if not hasattr(arg, 'type'):
                raise CDefError("%s arg %d: unknown type '%s' (if you meant to use the old C syntax of giving untyped arguments, it is not supported)" % (
                 funcname or 'in expression', i + 1,
                 getattr(arg, 'name', '?')))

        ellipsis = len(params) > 0 and isinstance(params[(-1)].type, pycparser.c_ast.TypeDecl) and isinstance(params[(-1)].type.type, pycparser.c_ast.IdentifierType) and params[(-1)].type.type.names == ['__dotdotdot__']
        if ellipsis:
            params.pop()
            if not params:
                raise CDefError("%s: a function with only '(...)' as argument is not correct C" % (funcname or 'in expression'))
        args = [(self._as_func_arg)(*self._get_type_and_quals(argdeclnode.type)) for argdeclnode in params]
        if not ellipsis:
            if args == [model.void_type]:
                args = []
        result, quals = self._get_type_and_quals(typenode.type)
        abi = None
        if hasattr(typenode.type, 'quals'):
            if typenode.type.quals[-3:] == ['volatile', 'volatile', 'const']:
                abi = '__stdcall'
        return model.RawFunctionType(tuple(args), result, ellipsis, abi)

    def _as_func_arg(self, type, quals):
        if isinstance(type, model.ArrayType):
            return model.PointerType(type.item, quals)
        else:
            if isinstance(type, model.RawFunctionType):
                return type.as_function_pointer()
            return type

    def _get_struct_union_enum_type(self, kind, type, name=None, nested=False):
        try:
            return self._structnode2type[type]
        except KeyError:
            pass

        force_name = name
        name = type.name
        if name is None:
            if force_name is not None:
                explicit_name = '$%s' % force_name
            else:
                self._anonymous_counter += 1
                explicit_name = '$%d' % self._anonymous_counter
            tp = None
        else:
            explicit_name = name
            key = '%s %s' % (kind, name)
            tp, _ = self._declarations.get(key, (None, None))
        if tp is None:
            if kind == 'struct':
                tp = model.StructType(explicit_name, None, None, None)
            else:
                if kind == 'union':
                    tp = model.UnionType(explicit_name, None, None, None)
                else:
                    if kind == 'enum':
                        if explicit_name == '__dotdotdot__':
                            raise CDefError('Enums cannot be declared with ...')
                        tp = self._build_enum_type(explicit_name, type.values)
                    else:
                        raise AssertionError('kind = %r' % (kind,))
            if name is not None:
                self._declare(key, tp)
        else:
            if kind == 'enum':
                if type.values is not None:
                    raise NotImplementedError("enum %s: the '{}' declaration should appear on the first time the enum is mentioned, not later" % explicit_name)
        if not tp.forcename:
            tp.force_the_name(force_name)
        if tp.forcename:
            if '$' in tp.name:
                self._declare('anonymous %s' % tp.forcename, tp)
        self._structnode2type[type] = tp
        if kind == 'enum':
            return tp
        if type.decls is None:
            return tp
        else:
            if tp.fldnames is not None:
                raise CDefError('duplicate declaration of struct %s' % name)
            else:
                fldnames = []
                fldtypes = []
                fldbitsize = []
                fldquals = []
                for decl in type.decls:
                    if isinstance(decl.type, pycparser.c_ast.IdentifierType):
                        if ''.join(decl.type.names) == '__dotdotdot__':
                            self._make_partial(tp, nested)
                            continue
                        else:
                            if decl.bitsize is None:
                                bitsize = -1
                            else:
                                bitsize = self._parse_constant(decl.bitsize)
                        self._partial_length = False
                        type, fqual = self._get_type_and_quals((decl.type), partial_length_ok=True)
                        if self._partial_length:
                            self._make_partial(tp, nested)
                    else:
                        if isinstance(type, model.StructType):
                            if type.partial:
                                self._make_partial(tp, nested)
                    fldnames.append(decl.name or '')
                    fldtypes.append(type)
                    fldbitsize.append(bitsize)
                    fldquals.append(fqual)

                tp.fldnames = tuple(fldnames)
                tp.fldtypes = tuple(fldtypes)
                tp.fldbitsize = tuple(fldbitsize)
                tp.fldquals = tuple(fldquals)
                if fldbitsize != [-1] * len(fldbitsize):
                    if isinstance(tp, model.StructType):
                        if tp.partial:
                            raise NotImplementedError("%s: using both bitfields and '...;'" % (
                             tp,))
                tp.packed = self._options.get('packed')
                if tp.completed:
                    tp.completed = 0
                    self._recomplete.append(tp)
            return tp

    def _make_partial(self, tp, nested):
        if not isinstance(tp, model.StructOrUnion):
            raise CDefError('%s cannot be partial' % (tp,))
        if not tp.has_c_name():
            if not nested:
                raise NotImplementedError('%s is partial but has no C name' % (tp,))
        tp.partial = True

    def _parse_constant(self, exprnode, partial_length_ok=False):
        if isinstance(exprnode, pycparser.c_ast.Constant):
            s = exprnode.value
            if s.startswith('0'):
                if s.startswith('0x') or s.startswith('0X'):
                    return int(s, 16)
                else:
                    return int(s, 8)
            else:
                if '1' <= s[0] <= '9':
                    return int(s, 10)
                if s[0] == "'":
                    if s[(-1)] == "'":
                        if len(s) == 3 or len(s) == 4 and s[1] == '\\':
                            return ord(s[(-2)])
                    raise CDefError('invalid constant %r' % (s,))
                elif isinstance(exprnode, pycparser.c_ast.UnaryOp):
                    if exprnode.op == '+':
                        return self._parse_constant(exprnode.expr)
            if isinstance(exprnode, pycparser.c_ast.UnaryOp):
                if exprnode.op == '-':
                    return -self._parse_constant(exprnode.expr)
            if isinstance(exprnode, pycparser.c_ast.ID):
                if exprnode.name in self._int_constants:
                    return self._int_constants[exprnode.name]
            if isinstance(exprnode, pycparser.c_ast.ID):
                if exprnode.name == '__dotdotdotarray__':
                    if partial_length_ok:
                        self._partial_length = True
                        return '...'
                    raise FFIError(":%d: unsupported '[...]' here, cannot derive the actual array length in this context" % exprnode.coord.line)
            if isinstance(exprnode, pycparser.c_ast.BinaryOp):
                if exprnode.op == '+':
                    return self._parse_constant(exprnode.left) + self._parse_constant(exprnode.right)
        else:
            if isinstance(exprnode, pycparser.c_ast.BinaryOp):
                if exprnode.op == '-':
                    return self._parse_constant(exprnode.left) - self._parse_constant(exprnode.right)
        raise FFIError(':%d: unsupported expression: expected a simple numeric constant' % exprnode.coord.line)

    def _build_enum_type(self, explicit_name, decls):
        if decls is not None:
            partial = False
            enumerators = []
            enumvalues = []
            nextenumvalue = 0
            for enum in decls.enumerators:
                if _r_enum_dotdotdot.match(enum.name):
                    partial = True
                else:
                    if enum.value is not None:
                        nextenumvalue = self._parse_constant(enum.value)
                    enumerators.append(enum.name)
                    enumvalues.append(nextenumvalue)
                    self._add_constants(enum.name, nextenumvalue)
                    nextenumvalue += 1

            enumerators = tuple(enumerators)
            enumvalues = tuple(enumvalues)
            tp = model.EnumType(explicit_name, enumerators, enumvalues)
            tp.partial = partial
        else:
            tp = model.EnumType(explicit_name, (), ())
        return tp

    def include(self, other):
        for name, (tp, quals) in other._declarations.items():
            if name.startswith('anonymous $enum_$'):
                pass
            else:
                kind = name.split(' ', 1)[0]
                if kind in ('struct', 'union', 'enum', 'anonymous', 'typedef'):
                    self._declare(name, tp, included=True, quals=quals)

        for k, v in other._int_constants.items():
            self._add_constants(k, v)

    def _get_unknown_type(self, decl):
        typenames = decl.type.type.names
        if typenames == ['__dotdotdot__']:
            return model.unknown_type(decl.name)
        if typenames == ['__dotdotdotint__']:
            if self._uses_new_feature is None:
                self._uses_new_feature = "'typedef int... %s'" % decl.name
            return model.UnknownIntegerType(decl.name)
        if typenames == ['__dotdotdotfloat__']:
            if self._uses_new_feature is None:
                self._uses_new_feature = "'typedef float... %s'" % decl.name
            return model.UnknownFloatType(decl.name)
        raise FFIError(':%d: unsupported usage of "..." in typedef' % decl.coord.line)

    def _get_unknown_ptr_type(self, decl):
        if decl.type.type.type.names == ['__dotdotdot__']:
            return model.unknown_ptr_type(decl.name)
        raise FFIError(':%d: unsupported usage of "..." in typedef' % decl.coord.line)