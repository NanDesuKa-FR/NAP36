# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: importlib\abc.py
"""Abstract base classes related to import."""
from . import _bootstrap
from . import _bootstrap_external
from . import machinery
try:
    import _frozen_importlib
except ImportError as exc:
    if exc.name != '_frozen_importlib':
        raise
    _frozen_importlib = None

try:
    import _frozen_importlib_external
except ImportError as exc:
    _frozen_importlib_external = _bootstrap_external

import abc

def _register(abstract_cls, *classes):
    for cls in classes:
        abstract_cls.register(cls)
        if _frozen_importlib is not None:
            try:
                frozen_cls = getattr(_frozen_importlib, cls.__name__)
            except AttributeError:
                frozen_cls = getattr(_frozen_importlib_external, cls.__name__)

            abstract_cls.register(frozen_cls)


class Finder(metaclass=abc.ABCMeta):
    __doc__ = 'Legacy abstract base class for import finders.\n\n    It may be subclassed for compatibility with legacy third party\n    reimplementations of the import system.  Otherwise, finder\n    implementations should derive from the more specific MetaPathFinder\n    or PathEntryFinder ABCs.\n    '

    @abc.abstractmethod
    def find_module(self, fullname, path=None):
        """An abstract method that should find a module.
        The fullname is a str and the optional path is a str or None.
        Returns a Loader object or None.
        """
        pass


class MetaPathFinder(Finder):
    __doc__ = 'Abstract base class for import finders on sys.meta_path.'

    def find_module(self, fullname, path):
        """Return a loader for the module.

        If no module is found, return None.  The fullname is a str and
        the path is a list of strings or None.

        This method is deprecated in favor of finder.find_spec(). If find_spec()
        exists then backwards-compatible functionality is provided for this
        method.

        """
        if not hasattr(self, 'find_spec'):
            return
        found = self.find_spec(fullname, path)
        if found is not None:
            return found.loader

    def invalidate_caches(self):
        """An optional method for clearing the finder's cache, if any.
        This method is used by importlib.invalidate_caches().
        """
        pass


_register(MetaPathFinder, machinery.BuiltinImporter, machinery.FrozenImporter, machinery.PathFinder, machinery.WindowsRegistryFinder)

class PathEntryFinder(Finder):
    __doc__ = 'Abstract base class for path entry finders used by PathFinder.'

    def find_loader(self, fullname):
        """Return (loader, namespace portion) for the path entry.

        The fullname is a str.  The namespace portion is a sequence of
        path entries contributing to part of a namespace package. The
        sequence may be empty.  If loader is not None, the portion will
        be ignored.

        The portion will be discarded if another path entry finder
        locates the module as a normal module or package.

        This method is deprecated in favor of finder.find_spec(). If find_spec()
        is provided than backwards-compatible functionality is provided.

        """
        if not hasattr(self, 'find_spec'):
            return (None, [])
        else:
            found = self.find_spec(fullname)
            if found is not None:
                if not found.submodule_search_locations:
                    portions = []
                else:
                    portions = found.submodule_search_locations
                return (
                 found.loader, portions)
            return (None, [])

    find_module = _bootstrap_external._find_module_shim

    def invalidate_caches(self):
        """An optional method for clearing the finder's cache, if any.
        This method is used by PathFinder.invalidate_caches().
        """
        pass


_register(PathEntryFinder, machinery.FileFinder)

class Loader(metaclass=abc.ABCMeta):
    __doc__ = 'Abstract base class for import loaders.'

    def create_module(self, spec):
        """Return a module to initialize and into which to load.

        This method should raise ImportError if anything prevents it
        from creating a new module.  It may return None to indicate
        that the spec should create the new module.
        """
        pass

    def load_module(self, fullname):
        """Return the loaded module.

        The module must be added to sys.modules and have import-related
        attributes set properly.  The fullname is a str.

        ImportError is raised on failure.

        This method is deprecated in favor of loader.exec_module(). If
        exec_module() exists then it is used to provide a backwards-compatible
        functionality for this method.

        """
        if not hasattr(self, 'exec_module'):
            raise ImportError
        return _bootstrap._load_module_shim(self, fullname)

    def module_repr(self, module):
        """Return a module's repr.

        Used by the module type when the method does not raise
        NotImplementedError.

        This method is deprecated.

        """
        raise NotImplementedError


class ResourceLoader(Loader):
    __doc__ = 'Abstract base class for loaders which can return data from their\n    back-end storage.\n\n    This ABC represents one of the optional protocols specified by PEP 302.\n\n    '

    @abc.abstractmethod
    def get_data(self, path):
        """Abstract method which when implemented should return the bytes for
        the specified path.  The path must be a str."""
        raise IOError


class InspectLoader(Loader):
    __doc__ = 'Abstract base class for loaders which support inspection about the\n    modules they can load.\n\n    This ABC represents one of the optional protocols specified by PEP 302.\n\n    '

    def is_package(self, fullname):
        """Optional method which when implemented should return whether the
        module is a package.  The fullname is a str.  Returns a bool.

        Raises ImportError if the module cannot be found.
        """
        raise ImportError

    def get_code(self, fullname):
        """Method which returns the code object for the module.

        The fullname is a str.  Returns a types.CodeType if possible, else
        returns None if a code object does not make sense
        (e.g. built-in module). Raises ImportError if the module cannot be
        found.
        """
        source = self.get_source(fullname)
        if source is None:
            return
        else:
            return self.source_to_code(source)

    @abc.abstractmethod
    def get_source(self, fullname):
        """Abstract method which should return the source code for the
        module.  The fullname is a str.  Returns a str.

        Raises ImportError if the module cannot be found.
        """
        raise ImportError

    @staticmethod
    def source_to_code(data, path='<string>'):
        """Compile 'data' into a code object.

        The 'data' argument can be anything that compile() can handle. The'path'
        argument should be where the data was retrieved (when applicable)."""
        return compile(data, path, 'exec', dont_inherit=True)

    exec_module = _bootstrap_external._LoaderBasics.exec_module
    load_module = _bootstrap_external._LoaderBasics.load_module


_register(InspectLoader, machinery.BuiltinImporter, machinery.FrozenImporter)

class ExecutionLoader(InspectLoader):
    __doc__ = 'Abstract base class for loaders that wish to support the execution of\n    modules as scripts.\n\n    This ABC represents one of the optional protocols specified in PEP 302.\n\n    '

    @abc.abstractmethod
    def get_filename(self, fullname):
        """Abstract method which should return the value that __file__ is to be
        set to.

        Raises ImportError if the module cannot be found.
        """
        raise ImportError

    def get_code(self, fullname):
        """Method to return the code object for fullname.

        Should return None if not applicable (e.g. built-in module).
        Raise ImportError if the module cannot be found.
        """
        source = self.get_source(fullname)
        if source is None:
            return
        try:
            path = self.get_filename(fullname)
        except ImportError:
            return self.source_to_code(source)
        else:
            return self.source_to_code(source, path)


_register(ExecutionLoader, machinery.ExtensionFileLoader)

class FileLoader(_bootstrap_external.FileLoader, ResourceLoader, ExecutionLoader):
    __doc__ = 'Abstract base class partially implementing the ResourceLoader and\n    ExecutionLoader ABCs.'


_register(FileLoader, machinery.SourceFileLoader, machinery.SourcelessFileLoader)

class SourceLoader(_bootstrap_external.SourceLoader, ResourceLoader, ExecutionLoader):
    __doc__ = 'Abstract base class for loading source code (and optionally any\n    corresponding bytecode).\n\n    To support loading from source code, the abstractmethods inherited from\n    ResourceLoader and ExecutionLoader need to be implemented. To also support\n    loading from bytecode, the optional methods specified directly by this ABC\n    is required.\n\n    Inherited abstractmethods not implemented in this ABC:\n\n        * ResourceLoader.get_data\n        * ExecutionLoader.get_filename\n\n    '

    def path_mtime(self, path):
        """Return the (int) modification time for the path (str)."""
        if self.path_stats.__func__ is SourceLoader.path_stats:
            raise IOError
        return int(self.path_stats(path)['mtime'])

    def path_stats(self, path):
        """Return a metadata dict for the source pointed to by the path (str).
        Possible keys:
        - 'mtime' (mandatory) is the numeric timestamp of last source
          code modification;
        - 'size' (optional) is the size in bytes of the source code.
        """
        if self.path_mtime.__func__ is SourceLoader.path_mtime:
            raise IOError
        return {'mtime': self.path_mtime(path)}

    def set_data(self, path, data):
        """Write the bytes to the path (if possible).

        Accepts a str path and data as bytes.

        Any needed intermediary directories are to be created. If for some
        reason the file cannot be written because of permissions, fail
        silently.
        """
        pass


_register(SourceLoader, machinery.SourceFileLoader)