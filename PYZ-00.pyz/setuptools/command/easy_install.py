# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\setuptools-39.0.1-py3.6.egg\setuptools\command\easy_install.py
"""
Easy Install
------------

A tool for doing automatic download/extract/build of distutils-based Python
packages.  For detailed documentation, see the accompanying EasyInstall.txt
file, or visit the `EasyInstall home page`__.

__ https://setuptools.readthedocs.io/en/latest/easy_install.html

"""
from glob import glob
from distutils.util import get_platform
from distutils.util import convert_path, subst_vars
from distutils.errors import DistutilsArgError, DistutilsOptionError, DistutilsError, DistutilsPlatformError
from distutils.command.install import INSTALL_SCHEMES, SCHEME_KEYS
from distutils import log, dir_util
from distutils.command.build_scripts import first_line_re
from distutils.spawn import find_executable
import sys, os, zipimport, shutil, tempfile, zipfile, re, stat, random, textwrap, warnings, site, struct, contextlib, subprocess, shlex, io
from setuptools.extern import six
from setuptools.extern.six.moves import configparser, map
from setuptools import Command
from setuptools.sandbox import run_setup
from setuptools.py31compat import get_path, get_config_vars
from setuptools.py27compat import rmtree_safe
from setuptools.command import setopt
from setuptools.archive_util import unpack_archive
from setuptools.package_index import PackageIndex, parse_requirement_arg, URL_SCHEME
from setuptools.command import bdist_egg, egg_info
from setuptools.wheel import Wheel
from pkg_resources import yield_lines, normalize_path, resource_string, ensure_directory, get_distribution, find_distributions, Environment, Requirement, Distribution, PathMetadata, EggMetadata, WorkingSet, DistributionNotFound, VersionConflict, DEVELOP_DIST
import pkg_resources.py31compat
warnings.filterwarnings('default', category=(pkg_resources.PEP440Warning))
__all__ = [
 'samefile', 'easy_install', 'PthDistributions', 'extract_wininst_cfg',
 'main', 'get_exe_prefixes']

def is_64bit():
    return struct.calcsize('P') == 8


def samefile(p1, p2):
    """
    Determine if two paths reference the same file.

    Augments os.path.samefile to work on Windows and
    suppresses errors if the path doesn't exist.
    """
    both_exist = os.path.exists(p1) and os.path.exists(p2)
    use_samefile = hasattr(os.path, 'samefile') and both_exist
    if use_samefile:
        return os.path.samefile(p1, p2)
    else:
        norm_p1 = os.path.normpath(os.path.normcase(p1))
        norm_p2 = os.path.normpath(os.path.normcase(p2))
        return norm_p1 == norm_p2


if six.PY2:

    def _to_ascii(s):
        return s


    def isascii(s):
        try:
            six.text_type(s, 'ascii')
            return True
        except UnicodeError:
            return False


else:

    def _to_ascii(s):
        return s.encode('ascii')


    def isascii(s):
        try:
            s.encode('ascii')
            return True
        except UnicodeError:
            return False


_one_liner = lambda text: textwrap.dedent(text).strip().replace('\n', '; ')

class easy_install(Command):
    __doc__ = 'Manage a download/build/install process'
    description = 'Find/get/install Python packages'
    command_consumes_arguments = True
    user_options = [
     ('prefix=', None, 'installation prefix'),
     ('zip-ok', 'z', 'install package as a zipfile'),
     ('multi-version', 'm', 'make apps have to require() a version'),
     ('upgrade', 'U', 'force upgrade (searches PyPI for latest versions)'),
     ('install-dir=', 'd', 'install package to DIR'),
     ('script-dir=', 's', 'install scripts to DIR'),
     ('exclude-scripts', 'x', "Don't install scripts"),
     ('always-copy', 'a', 'Copy all needed packages to install dir'),
     ('index-url=', 'i', 'base URL of Python Package Index'),
     ('find-links=', 'f', 'additional URL(s) to search for packages'),
     ('build-directory=', 'b', 'download/extract/build in DIR; keep the results'),
     ('optimize=', 'O', 'also compile with optimization: -O1 for "python -O", -O2 for "python -OO", and -O0 to disable [default: -O0]'),
     ('record=', None, 'filename in which to record list of installed files'),
     ('always-unzip', 'Z', "don't install as a zipfile, no matter what"),
     ('site-dirs=', 'S', 'list of directories where .pth files work'),
     ('editable', 'e', 'Install specified packages in editable form'),
     ('no-deps', 'N', "don't install dependencies"),
     ('allow-hosts=', 'H', 'pattern(s) that hostnames must match'),
     ('local-snapshots-ok', 'l', 'allow building eggs from local checkouts'),
     ('version', None, 'print version information and exit'),
     ('no-find-links', None, "Don't load find-links defined in packages being installed")]
    boolean_options = [
     'zip-ok', 'multi-version', 'exclude-scripts', 'upgrade', 'always-copy',
     'editable',
     'no-deps', 'local-snapshots-ok', 'version']
    if site.ENABLE_USER_SITE:
        help_msg = "install in user site-package '%s'" % site.USER_SITE
        user_options.append(('user', None, help_msg))
        boolean_options.append('user')
    negative_opt = {'always-unzip': 'zip-ok'}
    create_index = PackageIndex

    def initialize_options(self):
        self.user = 0
        self.zip_ok = self.local_snapshots_ok = None
        self.install_dir = self.script_dir = self.exclude_scripts = None
        self.index_url = None
        self.find_links = None
        self.build_directory = None
        self.args = None
        self.optimize = self.record = None
        self.upgrade = self.always_copy = self.multi_version = None
        self.editable = self.no_deps = self.allow_hosts = None
        self.root = self.prefix = self.no_report = None
        self.version = None
        self.install_purelib = None
        self.install_platlib = None
        self.install_headers = None
        self.install_lib = None
        self.install_scripts = None
        self.install_data = None
        self.install_base = None
        self.install_platbase = None
        if site.ENABLE_USER_SITE:
            self.install_userbase = site.USER_BASE
            self.install_usersite = site.USER_SITE
        else:
            self.install_userbase = None
            self.install_usersite = None
        self.no_find_links = None
        self.package_index = None
        self.pth_file = self.always_copy_from = None
        self.site_dirs = None
        self.installed_projects = {}
        self.sitepy_installed = False
        self._dry_run = None
        self.verbose = self.distribution.verbose
        self.distribution._set_command_options(self, self.distribution.get_option_dict('easy_install'))

    def delete_blockers(self, blockers):
        extant_blockers = (filename for filename in blockers if os.path.exists(filename) or os.path.islink(filename))
        list(map(self._delete_path, extant_blockers))

    def _delete_path(self, path):
        log.info('Deleting %s', path)
        if self.dry_run:
            return
        is_tree = os.path.isdir(path) and not os.path.islink(path)
        remover = rmtree if is_tree else os.unlink
        remover(path)

    @staticmethod
    def _render_version():
        """
        Render the Setuptools version and installation details, then exit.
        """
        ver = sys.version[:3]
        dist = get_distribution('setuptools')
        tmpl = 'setuptools {dist.version} from {dist.location} (Python {ver})'
        print((tmpl.format)(**locals()))
        raise SystemExit()

    def finalize_options(self):
        self.version and self._render_version()
        py_version = sys.version.split()[0]
        prefix, exec_prefix = get_config_vars('prefix', 'exec_prefix')
        self.config_vars = {'dist_name':self.distribution.get_name(), 
         'dist_version':self.distribution.get_version(), 
         'dist_fullname':self.distribution.get_fullname(), 
         'py_version':py_version, 
         'py_version_short':py_version[0:3], 
         'py_version_nodot':py_version[0] + py_version[2], 
         'sys_prefix':prefix, 
         'prefix':prefix, 
         'sys_exec_prefix':exec_prefix, 
         'exec_prefix':exec_prefix, 
         'abiflags':getattr(sys, 'abiflags', '')}
        if site.ENABLE_USER_SITE:
            self.config_vars['userbase'] = self.install_userbase
            self.config_vars['usersite'] = self.install_usersite
        self._fix_install_dir_for_user_site()
        self.expand_basedirs()
        self.expand_dirs()
        self._expand('install_dir', 'script_dir', 'build_directory', 'site_dirs')
        if self.script_dir is None:
            self.script_dir = self.install_dir
        if self.no_find_links is None:
            self.no_find_links = False
        self.set_undefined_options('install_lib', ('install_dir', 'install_dir'))
        self.set_undefined_options('install_scripts', ('install_dir', 'script_dir'))
        if self.user:
            if self.install_purelib:
                self.install_dir = self.install_purelib
                self.script_dir = self.install_scripts
        self.set_undefined_options('install', ('record', 'record'))
        normpath = map(normalize_path, sys.path)
        self.all_site_dirs = get_site_dirs()
        if self.site_dirs is not None:
            site_dirs = [os.path.expanduser(s.strip()) for s in self.site_dirs.split(',')]
            for d in site_dirs:
                if not os.path.isdir(d):
                    log.warn('%s (in --site-dirs) does not exist', d)
                else:
                    if normalize_path(d) not in normpath:
                        raise DistutilsOptionError(d + ' (in --site-dirs) is not on sys.path')
                    else:
                        self.all_site_dirs.append(normalize_path(d))

        if not self.editable:
            self.check_site_dir()
        else:
            self.index_url = self.index_url or 'https://pypi.python.org/simple'
            self.shadow_path = self.all_site_dirs[:]
            for path_item in (self.install_dir, normalize_path(self.script_dir)):
                if path_item not in self.shadow_path:
                    self.shadow_path.insert(0, path_item)

            if self.allow_hosts is not None:
                hosts = [s.strip() for s in self.allow_hosts.split(',')]
            else:
                hosts = [
                 '*']
            if self.package_index is None:
                self.package_index = self.create_index((self.index_url),
                  search_path=(self.shadow_path), hosts=hosts)
            self.local_index = Environment(self.shadow_path + sys.path)
            if self.find_links is not None:
                if isinstance(self.find_links, six.string_types):
                    self.find_links = self.find_links.split()
            else:
                self.find_links = []
        if self.local_snapshots_ok:
            self.package_index.scan_egg_links(self.shadow_path + sys.path)
        if not self.no_find_links:
            self.package_index.add_find_links(self.find_links)
        self.set_undefined_options('install_lib', ('optimize', 'optimize'))
        if not isinstance(self.optimize, int):
            try:
                self.optimize = int(self.optimize)
                if not 0 <= self.optimize <= 2:
                    raise ValueError
            except ValueError:
                raise DistutilsOptionError('--optimize must be 0, 1, or 2')

        if self.editable:
            if not self.build_directory:
                raise DistutilsArgError('Must specify a build directory (-b) when using --editable')
        if not self.args:
            raise DistutilsArgError('No urls, filenames, or requirements specified (see --help)')
        self.outputs = []

    def _fix_install_dir_for_user_site(self):
        """
        Fix the install_dir if "--user" was used.
        """
        if not self.user or not site.ENABLE_USER_SITE:
            return
        self.create_home_path()
        if self.install_userbase is None:
            msg = 'User base directory is not specified'
            raise DistutilsPlatformError(msg)
        self.install_base = self.install_platbase = self.install_userbase
        scheme_name = os.name.replace('posix', 'unix') + '_user'
        self.select_scheme(scheme_name)

    def _expand_attrs(self, attrs):
        for attr in attrs:
            val = getattr(self, attr)
            if val is not None:
                if os.name == 'posix' or os.name == 'nt':
                    val = os.path.expanduser(val)
                val = subst_vars(val, self.config_vars)
                setattr(self, attr, val)

    def expand_basedirs(self):
        """Calls `os.path.expanduser` on install_base, install_platbase and
        root."""
        self._expand_attrs(['install_base', 'install_platbase', 'root'])

    def expand_dirs(self):
        """Calls `os.path.expanduser` on install dirs."""
        dirs = [
         'install_purelib',
         'install_platlib',
         'install_lib',
         'install_headers',
         'install_scripts',
         'install_data']
        self._expand_attrs(dirs)

    def run(self):
        if self.verbose != self.distribution.verbose:
            log.set_verbosity(self.verbose)
        try:
            for spec in self.args:
                self.easy_install(spec, not self.no_deps)

            if self.record:
                outputs = self.outputs
                if self.root:
                    root_len = len(self.root)
                    for counter in range(len(outputs)):
                        outputs[counter] = outputs[counter][root_len:]

                from distutils import file_util
                self.execute(file_util.write_file, (self.record, outputs), "writing list of installed files to '%s'" % self.record)
            self.warn_deprecated_options()
        finally:
            log.set_verbosity(self.distribution.verbose)

    def pseudo_tempname(self):
        """Return a pseudo-tempname base in the install directory.
        This code is intentionally naive; if a malicious party can write to
        the target directory you're already in deep doodoo.
        """
        try:
            pid = os.getpid()
        except Exception:
            pid = random.randint(0, sys.maxsize)

        return os.path.join(self.install_dir, 'test-easy-install-%s' % pid)

    def warn_deprecated_options(self):
        pass

    def check_site_dir(self):
        """Verify that self.install_dir is .pth-capable dir, if needed"""
        instdir = normalize_path(self.install_dir)
        pth_file = os.path.join(instdir, 'easy-install.pth')
        is_site_dir = instdir in self.all_site_dirs
        if not is_site_dir:
            if not self.multi_version:
                is_site_dir = self.check_pth_processing()
            else:
                testfile = self.pseudo_tempname() + '.write-test'
                test_exists = os.path.exists(testfile)
                try:
                    if test_exists:
                        os.unlink(testfile)
                    open(testfile, 'w').close()
                    os.unlink(testfile)
                except (OSError, IOError):
                    self.cant_write_to_target()

        elif not is_site_dir:
            if not self.multi_version:
                raise DistutilsError(self.no_default_version_msg())
        else:
            if is_site_dir:
                if self.pth_file is None:
                    self.pth_file = PthDistributions(pth_file, self.all_site_dirs)
            else:
                self.pth_file = None
        if instdir not in map(normalize_path, _pythonpath()):
            self.sitepy_installed = True
        else:
            if self.multi_version:
                if not os.path.exists(pth_file):
                    self.sitepy_installed = True
                    self.pth_file = None
        self.install_dir = instdir

    _easy_install__cant_write_msg = textwrap.dedent("\n        can't create or remove files in install directory\n\n        The following error occurred while trying to add or remove files in the\n        installation directory:\n\n            %s\n\n        The installation directory you specified (via --install-dir, --prefix, or\n        the distutils default setting) was:\n\n            %s\n        ").lstrip()
    _easy_install__not_exists_id = textwrap.dedent('\n        This directory does not currently exist.  Please create it and try again, or\n        choose a different installation directory (using the -d or --install-dir\n        option).\n        ').lstrip()
    _easy_install__access_msg = textwrap.dedent('\n        Perhaps your account does not have write access to this directory?  If the\n        installation directory is a system-owned directory, you may need to sign in\n        as the administrator or "root" account.  If you do not have administrative\n        access to this machine, you may wish to choose a different installation\n        directory, preferably one that is listed in your PYTHONPATH environment\n        variable.\n\n        For information on other options, you may wish to consult the\n        documentation at:\n\n          https://setuptools.readthedocs.io/en/latest/easy_install.html\n\n        Please make the appropriate changes for your system and try again.\n        ').lstrip()

    def cant_write_to_target(self):
        msg = self._easy_install__cant_write_msg % (sys.exc_info()[1], self.install_dir)
        if not os.path.exists(self.install_dir):
            msg += '\n' + self._easy_install__not_exists_id
        else:
            msg += '\n' + self._easy_install__access_msg
        raise DistutilsError(msg)

    def check_pth_processing(self):
        """Empirically verify whether .pth files are supported in inst. dir"""
        instdir = self.install_dir
        log.info('Checking .pth file support in %s', instdir)
        pth_file = self.pseudo_tempname() + '.pth'
        ok_file = pth_file + '.ok'
        ok_exists = os.path.exists(ok_file)
        tmpl = _one_liner("\n            import os\n            f = open({ok_file!r}, 'w')\n            f.write('OK')\n            f.close()\n            ") + '\n'
        try:
            if ok_exists:
                os.unlink(ok_file)
            dirname = os.path.dirname(ok_file)
            pkg_resources.py31compat.makedirs(dirname, exist_ok=True)
            f = open(pth_file, 'w')
        except (OSError, IOError):
            self.cant_write_to_target()
        else:
            try:
                f.write((tmpl.format)(**locals()))
                f.close()
                f = None
                executable = sys.executable
                if os.name == 'nt':
                    dirname, basename = os.path.split(executable)
                    alt = os.path.join(dirname, 'pythonw.exe')
                    use_alt = basename.lower() == 'python.exe' and os.path.exists(alt)
                    if use_alt:
                        executable = alt
                from distutils.spawn import spawn
                spawn([executable, '-E', '-c', 'pass'], 0)
                if os.path.exists(ok_file):
                    log.info('TEST PASSED: %s appears to support .pth files', instdir)
                    return True
            finally:
                if f:
                    f.close()
                else:
                    if os.path.exists(ok_file):
                        os.unlink(ok_file)
                    if os.path.exists(pth_file):
                        os.unlink(pth_file)

        if not self.multi_version:
            log.warn('TEST FAILED: %s does NOT support .pth files', instdir)
        return False

    def install_egg_scripts(self, dist):
        """Write all the scripts for `dist`, unless scripts are excluded"""
        if not self.exclude_scripts:
            if dist.metadata_isdir('scripts'):
                for script_name in dist.metadata_listdir('scripts'):
                    if dist.metadata_isdir('scripts/' + script_name):
                        pass
                    else:
                        self.install_script(dist, script_name, dist.get_metadata('scripts/' + script_name))

        self.install_wrapper_scripts(dist)

    def add_output(self, path):
        if os.path.isdir(path):
            for base, dirs, files in os.walk(path):
                for filename in files:
                    self.outputs.append(os.path.join(base, filename))

        else:
            self.outputs.append(path)

    def not_editable(self, spec):
        if self.editable:
            raise DistutilsArgError("Invalid argument %r: you can't use filenames or URLs with --editable (except via the --find-links option)." % (
             spec,))

    def check_editable(self, spec):
        if not self.editable:
            return
        if os.path.exists(os.path.join(self.build_directory, spec.key)):
            raise DistutilsArgError("%r already exists in %s; can't do a checkout there" % (
             spec.key, self.build_directory))

    @contextlib.contextmanager
    def _tmpdir(self):
        tmpdir = tempfile.mkdtemp(prefix=(six.u('easy_install-')))
        try:
            yield str(tmpdir)
        finally:
            os.path.exists(tmpdir) and rmtree(rmtree_safe(tmpdir))

    def easy_install(self, spec, deps=False):
        if not self.editable:
            self.install_site_py()
        with self._tmpdir() as (tmpdir):
            if not isinstance(spec, Requirement):
                if URL_SCHEME(spec):
                    self.not_editable(spec)
                    dl = self.package_index.download(spec, tmpdir)
                    return self.install_item(None, dl, tmpdir, deps, True)
                if os.path.exists(spec):
                    self.not_editable(spec)
                    return self.install_item(None, spec, tmpdir, deps, True)
                spec = parse_requirement_arg(spec)
            else:
                self.check_editable(spec)
                dist = self.package_index.fetch_distribution(spec, tmpdir, self.upgrade, self.editable, not self.always_copy, self.local_index)
                if dist is None:
                    msg = 'Could not find suitable distribution for %r' % spec
                    if self.always_copy:
                        msg += ' (--always-copy skips system and development eggs)'
                    raise DistutilsError(msg)
                else:
                    if dist.precedence == DEVELOP_DIST:
                        self.process_distribution(spec, dist, deps, 'Using')
                        return dist
                    else:
                        return self.install_item(spec, dist.location, tmpdir, deps)

    def install_item(self, spec, download, tmpdir, deps, install_needed=False):
        install_needed = install_needed or self.always_copy
        install_needed = install_needed or os.path.dirname(download) == tmpdir
        install_needed = install_needed or not download.endswith('.egg')
        install_needed = install_needed or self.always_copy_from is not None and os.path.dirname(normalize_path(download)) == normalize_path(self.always_copy_from)
        if spec:
            if not install_needed:
                for dist in self.local_index[spec.project_name]:
                    if dist.location == download:
                        break
                else:
                    install_needed = True

        else:
            log.info('Processing %s', os.path.basename(download))
            if install_needed:
                dists = self.install_eggs(spec, download, tmpdir)
                for dist in dists:
                    self.process_distribution(spec, dist, deps)

            else:
                dists = [
                 self.egg_distribution(download)]
                self.process_distribution(spec, dists[0], deps, 'Using')
        if spec is not None:
            for dist in dists:
                if dist in spec:
                    return dist

    def select_scheme(self, name):
        """Sets the install directories by applying the install schemes."""
        scheme = INSTALL_SCHEMES[name]
        for key in SCHEME_KEYS:
            attrname = 'install_' + key
            if getattr(self, attrname) is None:
                setattr(self, attrname, scheme[key])

    def process_distribution(self, requirement, dist, deps=True, *info):
        self.update_pth(dist)
        self.package_index.add(dist)
        if dist in self.local_index[dist.key]:
            self.local_index.remove(dist)
        self.local_index.add(dist)
        self.install_egg_scripts(dist)
        self.installed_projects[dist.key] = dist
        log.info((self.installation_report)(requirement, dist, *info))
        if dist.has_metadata('dependency_links.txt'):
            if not self.no_find_links:
                self.package_index.add_find_links(dist.get_metadata_lines('dependency_links.txt'))
        if not deps:
            if not self.always_copy:
                return
        if requirement is not None:
            if dist.key != requirement.key:
                log.warn('Skipping dependencies for %s', dist)
                return
        if requirement is None or dist not in requirement:
            distreq = dist.as_requirement()
            requirement = Requirement(str(distreq))
        log.info('Processing dependencies for %s', requirement)
        try:
            distros = WorkingSet([]).resolve([
             requirement], self.local_index, self.easy_install)
        except DistributionNotFound as e:
            raise DistutilsError(str(e))
        except VersionConflict as e:
            raise DistutilsError(e.report())

        if self.always_copy or self.always_copy_from:
            for dist in distros:
                if dist.key not in self.installed_projects:
                    self.easy_install(dist.as_requirement())

        log.info('Finished processing dependencies for %s', requirement)

    def should_unzip(self, dist):
        if self.zip_ok is not None:
            return not self.zip_ok
        else:
            if dist.has_metadata('not-zip-safe'):
                return True
            if not dist.has_metadata('zip-safe'):
                return True
            return False

    def maybe_move(self, spec, dist_filename, setup_base):
        dst = os.path.join(self.build_directory, spec.key)
        if os.path.exists(dst):
            msg = '%r already exists in %s; build directory %s will not be kept'
            log.warn(msg, spec.key, self.build_directory, setup_base)
            return setup_base
        else:
            if os.path.isdir(dist_filename):
                setup_base = dist_filename
            else:
                if os.path.dirname(dist_filename) == setup_base:
                    os.unlink(dist_filename)
                contents = os.listdir(setup_base)
            if len(contents) == 1:
                dist_filename = os.path.join(setup_base, contents[0])
                if os.path.isdir(dist_filename):
                    setup_base = dist_filename
            ensure_directory(dst)
            shutil.move(setup_base, dst)
            return dst

    def install_wrapper_scripts(self, dist):
        if self.exclude_scripts:
            return
        for args in ScriptWriter.best().get_args(dist):
            (self.write_script)(*args)

    def install_script(self, dist, script_name, script_text, dev_path=None):
        """Generate a legacy script wrapper and install it"""
        spec = str(dist.as_requirement())
        is_script = is_python_script(script_text, script_name)
        if is_script:
            body = self._load_template(dev_path) % locals()
            script_text = ScriptWriter.get_header(script_text) + body
        self.write_script(script_name, _to_ascii(script_text), 'b')

    @staticmethod
    def _load_template(dev_path):
        """
        There are a couple of template scripts in the package. This
        function loads one of them and prepares it for use.
        """
        name = 'script.tmpl'
        if dev_path:
            name = name.replace('.tmpl', ' (dev).tmpl')
        raw_bytes = resource_string('setuptools', name)
        return raw_bytes.decode('utf-8')

    def write_script(self, script_name, contents, mode='t', blockers=()):
        """Write an executable file to the scripts directory"""
        self.delete_blockers([os.path.join(self.script_dir, x) for x in blockers])
        log.info('Installing %s script to %s', script_name, self.script_dir)
        target = os.path.join(self.script_dir, script_name)
        self.add_output(target)
        if self.dry_run:
            return
        mask = current_umask()
        ensure_directory(target)
        if os.path.exists(target):
            os.unlink(target)
        with open(target, 'w' + mode) as (f):
            f.write(contents)
        chmod(target, 511 - mask)

    def install_eggs(self, spec, dist_filename, tmpdir):
        if dist_filename.lower().endswith('.egg'):
            return [self.install_egg(dist_filename, tmpdir)]
        else:
            if dist_filename.lower().endswith('.exe'):
                return [
                 self.install_exe(dist_filename, tmpdir)]
            else:
                if dist_filename.lower().endswith('.whl'):
                    return [
                     self.install_wheel(dist_filename, tmpdir)]
                else:
                    setup_base = tmpdir
                    if os.path.isfile(dist_filename):
                        if not dist_filename.endswith('.py'):
                            unpack_archive(dist_filename, tmpdir, self.unpack_progress)
                    if os.path.isdir(dist_filename):
                        setup_base = os.path.abspath(dist_filename)
                    if setup_base.startswith(tmpdir):
                        if self.build_directory:
                            if spec is not None:
                                setup_base = self.maybe_move(spec, dist_filename, setup_base)
                    setup_script = os.path.join(setup_base, 'setup.py')
                    setups = os.path.exists(setup_script) or glob(os.path.join(setup_base, '*', 'setup.py'))
                    if not setups:
                        raise DistutilsError("Couldn't find a setup script in %s" % os.path.abspath(dist_filename))
                    if len(setups) > 1:
                        raise DistutilsError('Multiple setup scripts in %s' % os.path.abspath(dist_filename))
                    setup_script = setups[0]
                if self.editable:
                    log.info(self.report_editable(spec, setup_script))
                    return []
            return self.build_and_install(setup_script, setup_base)

    def egg_distribution(self, egg_path):
        if os.path.isdir(egg_path):
            metadata = PathMetadata(egg_path, os.path.join(egg_path, 'EGG-INFO'))
        else:
            metadata = EggMetadata(zipimport.zipimporter(egg_path))
        return Distribution.from_filename(egg_path, metadata=metadata)

    def install_egg(self, egg_path, tmpdir):
        destination = os.path.join(self.install_dir, os.path.basename(egg_path))
        destination = os.path.abspath(destination)
        if not self.dry_run:
            ensure_directory(destination)
        dist = self.egg_distribution(egg_path)
        if samefile(egg_path, destination) or os.path.isdir(destination) and not os.path.islink(destination):
            dir_util.remove_tree(destination, dry_run=(self.dry_run))
        else:
            if os.path.exists(destination):
                self.execute(os.unlink, (
                 destination,), 'Removing ' + destination)
        try:
            new_dist_is_zipped = False
            if os.path.isdir(egg_path):
                if egg_path.startswith(tmpdir):
                    f, m = shutil.move, 'Moving'
                else:
                    f, m = shutil.copytree, 'Copying'
            else:
                if self.should_unzip(dist):
                    self.mkpath(destination)
                    f, m = self.unpack_and_compile, 'Extracting'
                else:
                    new_dist_is_zipped = True
                    if egg_path.startswith(tmpdir):
                        f, m = shutil.move, 'Moving'
                    else:
                        f, m = shutil.copy2, 'Copying'
                self.execute(f, (
                 egg_path, destination), (m + ' %s to %s') % (
                 os.path.basename(egg_path),
                 os.path.dirname(destination)))
                update_dist_caches(destination,
                  fix_zipimporter_caches=new_dist_is_zipped)
        except Exception:
            update_dist_caches(destination, fix_zipimporter_caches=False)
            raise

        self.add_output(destination)
        return self.egg_distribution(destination)

    def install_exe(self, dist_filename, tmpdir):
        cfg = extract_wininst_cfg(dist_filename)
        if cfg is None:
            raise DistutilsError('%s is not a valid distutils Windows .exe' % dist_filename)
        dist = Distribution(None,
          project_name=(cfg.get('metadata', 'name')),
          version=(cfg.get('metadata', 'version')),
          platform=(get_platform()))
        egg_path = os.path.join(tmpdir, dist.egg_name() + '.egg')
        dist.location = egg_path
        egg_tmp = egg_path + '.tmp'
        _egg_info = os.path.join(egg_tmp, 'EGG-INFO')
        pkg_inf = os.path.join(_egg_info, 'PKG-INFO')
        ensure_directory(pkg_inf)
        dist._provider = PathMetadata(egg_tmp, _egg_info)
        self.exe_to_egg(dist_filename, egg_tmp)
        if not os.path.exists(pkg_inf):
            f = open(pkg_inf, 'w')
            f.write('Metadata-Version: 1.0\n')
            for k, v in cfg.items('metadata'):
                if k != 'target_version':
                    f.write('%s: %s\n' % (k.replace('_', '-').title(), v))

            f.close()
        script_dir = os.path.join(_egg_info, 'scripts')
        self.delete_blockers([os.path.join(script_dir, args[0]) for args in ScriptWriter.get_args(dist)])
        bdist_egg.make_zipfile(egg_path,
          egg_tmp, verbose=(self.verbose), dry_run=(self.dry_run))
        return self.install_egg(egg_path, tmpdir)

    def exe_to_egg(self, dist_filename, egg_tmp):
        """Extract a bdist_wininst to the directories an egg would use"""
        prefixes = get_exe_prefixes(dist_filename)
        to_compile = []
        native_libs = []
        top_level = {}

        def process(src, dst):
            s = src.lower()
            for old, new in prefixes:
                if s.startswith(old):
                    src = new + src[len(old):]
                    parts = src.split('/')
                    dst = (os.path.join)(egg_tmp, *parts)
                    dl = dst.lower()
                    if dl.endswith('.pyd') or dl.endswith('.dll'):
                        parts[-1] = bdist_egg.strip_module(parts[(-1)])
                        top_level[os.path.splitext(parts[0])[0]] = 1
                        native_libs.append(src)
                    else:
                        if dl.endswith('.py'):
                            if old != 'SCRIPTS/':
                                top_level[os.path.splitext(parts[0])[0]] = 1
                                to_compile.append(dst)
                        return dst

            if not src.endswith('.pth'):
                log.warn("WARNING: can't process %s", src)

        unpack_archive(dist_filename, egg_tmp, process)
        stubs = []
        for res in native_libs:
            if res.lower().endswith('.pyd'):
                parts = res.split('/')
                resource = parts[(-1)]
                parts[-1] = bdist_egg.strip_module(parts[(-1)]) + '.py'
                pyfile = (os.path.join)(egg_tmp, *parts)
                to_compile.append(pyfile)
                stubs.append(pyfile)
                bdist_egg.write_stub(resource, pyfile)

        self.byte_compile(to_compile)
        bdist_egg.write_safety_flag(os.path.join(egg_tmp, 'EGG-INFO'), bdist_egg.analyze_egg(egg_tmp, stubs))
        for name in ('top_level', 'native_libs'):
            if locals()[name]:
                txt = os.path.join(egg_tmp, 'EGG-INFO', name + '.txt')
                if not os.path.exists(txt):
                    f = open(txt, 'w')
                    f.write('\n'.join(locals()[name]) + '\n')
                    f.close()

    def install_wheel(self, wheel_path, tmpdir):
        wheel = Wheel(wheel_path)
        assert wheel.is_compatible()
        destination = os.path.join(self.install_dir, wheel.egg_name())
        destination = os.path.abspath(destination)
        if not self.dry_run:
            ensure_directory(destination)
        if os.path.isdir(destination):
            if not os.path.islink(destination):
                dir_util.remove_tree(destination, dry_run=(self.dry_run))
        if os.path.exists(destination):
            self.execute(os.unlink, (
             destination,), 'Removing ' + destination)
        try:
            self.execute(wheel.install_as_egg, (
             destination,), 'Installing %s to %s' % (
             os.path.basename(wheel_path),
             os.path.dirname(destination)))
        finally:
            update_dist_caches(destination, fix_zipimporter_caches=False)

        self.add_output(destination)
        return self.egg_distribution(destination)

    _easy_install__mv_warning = textwrap.dedent('\n        Because this distribution was installed --multi-version, before you can\n        import modules from this package in an application, you will need to\n        \'import pkg_resources\' and then use a \'require()\' call similar to one of\n        these examples, in order to select the desired version:\n\n            pkg_resources.require("%(name)s")  # latest installed version\n            pkg_resources.require("%(name)s==%(version)s")  # this exact version\n            pkg_resources.require("%(name)s>=%(version)s")  # this version or higher\n        ').lstrip()
    _easy_install__id_warning = textwrap.dedent("\n        Note also that the installation directory must be on sys.path at runtime for\n        this to work.  (e.g. by being the application's script directory, by being on\n        PYTHONPATH, or by being added to sys.path by your code.)\n        ")

    def installation_report(self, req, dist, what='Installed'):
        """Helpful installation message for display to package users"""
        msg = '\n%(what)s %(eggloc)s%(extras)s'
        if self.multi_version:
            if not self.no_report:
                msg += '\n' + self._easy_install__mv_warning
                if self.install_dir not in map(normalize_path, sys.path):
                    msg += '\n' + self._easy_install__id_warning
        eggloc = dist.location
        name = dist.project_name
        version = dist.version
        extras = ''
        return msg % locals()

    _easy_install__editable_msg = textwrap.dedent('\n        Extracted editable version of %(spec)s to %(dirname)s\n\n        If it uses setuptools in its setup script, you can activate it in\n        "development" mode by going to that directory and running::\n\n            %(python)s setup.py develop\n\n        See the setuptools documentation for the "develop" command for more info.\n        ').lstrip()

    def report_editable(self, spec, setup_script):
        dirname = os.path.dirname(setup_script)
        python = sys.executable
        return '\n' + self._easy_install__editable_msg % locals()

    def run_setup(self, setup_script, setup_base, args):
        sys.modules.setdefault('distutils.command.bdist_egg', bdist_egg)
        sys.modules.setdefault('distutils.command.egg_info', egg_info)
        args = list(args)
        if self.verbose > 2:
            v = 'v' * (self.verbose - 1)
            args.insert(0, '-' + v)
        else:
            if self.verbose < 2:
                args.insert(0, '-q')
        if self.dry_run:
            args.insert(0, '-n')
        log.info('Running %s %s', setup_script[len(setup_base) + 1:], ' '.join(args))
        try:
            run_setup(setup_script, args)
        except SystemExit as v:
            raise DistutilsError('Setup script exited with %s' % (v.args[0],))

    def build_and_install(self, setup_script, setup_base):
        args = ['bdist_egg', '--dist-dir']
        dist_dir = tempfile.mkdtemp(prefix='egg-dist-tmp-',
          dir=(os.path.dirname(setup_script)))
        try:
            self._set_fetcher_options(os.path.dirname(setup_script))
            args.append(dist_dir)
            self.run_setup(setup_script, setup_base, args)
            all_eggs = Environment([dist_dir])
            eggs = []
            for key in all_eggs:
                for dist in all_eggs[key]:
                    eggs.append(self.install_egg(dist.location, setup_base))

            if not eggs:
                if not self.dry_run:
                    log.warn('No eggs found in %s (setup script problem?)', dist_dir)
            return eggs
        finally:
            rmtree(dist_dir)
            log.set_verbosity(self.verbose)

    def _set_fetcher_options(self, base):
        """
        When easy_install is about to run bdist_egg on a source dist, that
        source dist might have 'setup_requires' directives, requiring
        additional fetching. Ensure the fetcher options given to easy_install
        are available to that command as well.
        """
        ei_opts = self.distribution.get_option_dict('easy_install').copy()
        fetch_directives = ('find_links', 'site_dirs', 'index_url', 'optimize', 'site_dirs',
                            'allow_hosts')
        fetch_options = {}
        for key, val in ei_opts.items():
            if key not in fetch_directives:
                pass
            else:
                fetch_options[key.replace('_', '-')] = val[1]

        settings = dict(easy_install=fetch_options)
        cfg_filename = os.path.join(base, 'setup.cfg')
        setopt.edit_config(cfg_filename, settings)

    def update_pth(self, dist):
        if self.pth_file is None:
            return
        else:
            for d in self.pth_file[dist.key]:
                if self.multi_version or d.location != dist.location:
                    log.info('Removing %s from easy-install.pth file', d)
                    self.pth_file.remove(d)
                    if d.location in self.shadow_path:
                        self.shadow_path.remove(d.location)

            if not self.multi_version:
                if dist.location in self.pth_file.paths:
                    log.info('%s is already the active version in easy-install.pth', dist)
                else:
                    log.info('Adding %s to easy-install.pth file', dist)
                    self.pth_file.add(dist)
                    if dist.location not in self.shadow_path:
                        self.shadow_path.append(dist.location)
            if not self.dry_run:
                self.pth_file.save()
                if dist.key == 'setuptools':
                    filename = os.path.join(self.install_dir, 'setuptools.pth')
                    if os.path.islink(filename):
                        os.unlink(filename)
                    f = open(filename, 'wt')
                    f.write(self.pth_file.make_relative(dist.location) + '\n')
                    f.close()

    def unpack_progress(self, src, dst):
        log.debug('Unpacking %s to %s', src, dst)
        return dst

    def unpack_and_compile(self, egg_path, destination):
        to_compile = []
        to_chmod = []

        def pf(src, dst):
            if dst.endswith('.py'):
                if not src.startswith('EGG-INFO/'):
                    to_compile.append(dst)
            if dst.endswith('.dll') or dst.endswith('.so'):
                to_chmod.append(dst)
            self.unpack_progress(src, dst)
            return not self.dry_run and dst or None

        unpack_archive(egg_path, destination, pf)
        self.byte_compile(to_compile)
        if not self.dry_run:
            for f in to_chmod:
                mode = (os.stat(f)[stat.ST_MODE] | 365) & 4077
                chmod(f, mode)

    def byte_compile(self, to_compile):
        if sys.dont_write_bytecode:
            return
        from distutils.util import byte_compile
        try:
            log.set_verbosity(self.verbose - 1)
            byte_compile(to_compile, optimize=0, force=1, dry_run=(self.dry_run))
            if self.optimize:
                byte_compile(to_compile,
                  optimize=(self.optimize), force=1, dry_run=(self.dry_run))
        finally:
            log.set_verbosity(self.verbose)

    _easy_install__no_default_msg = textwrap.dedent('\n        bad install directory or PYTHONPATH\n\n        You are attempting to install a package to a directory that is not\n        on PYTHONPATH and which Python does not read ".pth" files from.  The\n        installation directory you specified (via --install-dir, --prefix, or\n        the distutils default setting) was:\n\n            %s\n\n        and your PYTHONPATH environment variable currently contains:\n\n            %r\n\n        Here are some of your options for correcting the problem:\n\n        * You can choose a different installation directory, i.e., one that is\n          on PYTHONPATH or supports .pth files\n\n        * You can add the installation directory to the PYTHONPATH environment\n          variable.  (It must then also be on PYTHONPATH whenever you run\n          Python and want to use the package(s) you are installing.)\n\n        * You can set up the installation directory to support ".pth" files by\n          using one of the approaches described here:\n\n          https://setuptools.readthedocs.io/en/latest/easy_install.html#custom-installation-locations\n\n\n        Please make the appropriate changes for your system and try again.').lstrip()

    def no_default_version_msg(self):
        template = self._easy_install__no_default_msg
        return template % (self.install_dir, os.environ.get('PYTHONPATH', ''))

    def install_site_py(self):
        """Make sure there's a site.py in the target dir, if needed"""
        if self.sitepy_installed:
            return
        else:
            sitepy = os.path.join(self.install_dir, 'site.py')
            source = resource_string('setuptools', 'site-patch.py')
            source = source.decode('utf-8')
            current = ''
            if os.path.exists(sitepy):
                log.debug('Checking existing site.py in %s', self.install_dir)
                with io.open(sitepy) as (strm):
                    current = strm.read()
                if not current.startswith('def __boot():'):
                    raise DistutilsError('%s is not a setuptools-generated site.py; please remove it.' % sitepy)
            if current != source:
                log.info('Creating %s', sitepy)
                if not self.dry_run:
                    ensure_directory(sitepy)
                    with io.open(sitepy, 'w', encoding='utf-8') as (strm):
                        strm.write(source)
                self.byte_compile([sitepy])
        self.sitepy_installed = True

    def create_home_path(self):
        """Create directories under ~."""
        if not self.user:
            return
        home = convert_path(os.path.expanduser('~'))
        for name, path in six.iteritems(self.config_vars):
            if path.startswith(home) and not os.path.isdir(path):
                self.debug_print("os.makedirs('%s', 0o700)" % path)
                os.makedirs(path, 448)

    INSTALL_SCHEMES = dict(posix=dict(install_dir='$base/lib/python$py_version_short/site-packages',
      script_dir='$base/bin'))
    DEFAULT_SCHEME = dict(install_dir='$base/Lib/site-packages',
      script_dir='$base/Scripts')

    def _expand(self, *attrs):
        config_vars = self.get_finalized_command('install').config_vars
        if self.prefix:
            config_vars = config_vars.copy()
            config_vars['base'] = self.prefix
            scheme = self.INSTALL_SCHEMES.get(os.name, self.DEFAULT_SCHEME)
            for attr, val in scheme.items():
                if getattr(self, attr, None) is None:
                    setattr(self, attr, val)

        from distutils.util import subst_vars
        for attr in attrs:
            val = getattr(self, attr)
            if val is not None:
                val = subst_vars(val, config_vars)
                if os.name == 'posix':
                    val = os.path.expanduser(val)
                setattr(self, attr, val)


def _pythonpath():
    items = os.environ.get('PYTHONPATH', '').split(os.pathsep)
    return filter(None, items)


def get_site_dirs():
    """
    Return a list of 'site' dirs
    """
    sitedirs = []
    sitedirs.extend(_pythonpath())
    prefixes = [
     sys.prefix]
    if sys.exec_prefix != sys.prefix:
        prefixes.append(sys.exec_prefix)
    for prefix in prefixes:
        if prefix:
            if sys.platform in ('os2emx', 'riscos'):
                sitedirs.append(os.path.join(prefix, 'Lib', 'site-packages'))
            else:
                if os.sep == '/':
                    sitedirs.extend([
                     os.path.join(prefix, 'lib', 'python' + sys.version[:3], 'site-packages'),
                     os.path.join(prefix, 'lib', 'site-python')])
                else:
                    sitedirs.extend([
                     prefix,
                     os.path.join(prefix, 'lib', 'site-packages')])
            if sys.platform == 'darwin' and 'Python.framework' in prefix:
                home = os.environ.get('HOME')
                if home:
                    home_sp = os.path.join(home, 'Library', 'Python', sys.version[:3], 'site-packages')
                    sitedirs.append(home_sp)

    lib_paths = (
     get_path('purelib'), get_path('platlib'))
    for site_lib in lib_paths:
        if site_lib not in sitedirs:
            sitedirs.append(site_lib)

    if site.ENABLE_USER_SITE:
        sitedirs.append(site.USER_SITE)
    try:
        sitedirs.extend(site.getsitepackages())
    except AttributeError:
        pass

    sitedirs = list(map(normalize_path, sitedirs))
    return sitedirs


def expand_paths(inputs):
    """Yield sys.path directories that might contain "old-style" packages"""
    seen = {}
    for dirname in inputs:
        dirname = normalize_path(dirname)
        if dirname in seen:
            pass
        else:
            seen[dirname] = 1
            if not os.path.isdir(dirname):
                pass
            else:
                files = os.listdir(dirname)
                yield (dirname, files)
                for name in files:
                    if not name.endswith('.pth'):
                        pass
                    else:
                        if name in ('easy-install.pth', 'setuptools.pth'):
                            pass
                        else:
                            f = open(os.path.join(dirname, name))
                            lines = list(yield_lines(f))
                            f.close()
                            for line in lines:
                                if not line.startswith('import'):
                                    line = normalize_path(line.rstrip())
                                    if line not in seen:
                                        seen[line] = 1
                                        if not os.path.isdir(line):
                                            pass
                                        else:
                                            yield (
                                             line, os.listdir(line))


def extract_wininst_cfg(dist_filename):
    """Extract configuration data from a bdist_wininst .exe

    Returns a configparser.RawConfigParser, or None
    """
    f = open(dist_filename, 'rb')
    try:
        endrec = zipfile._EndRecData(f)
        if endrec is None:
            return
        prepended = endrec[9] - endrec[5] - endrec[6]
        if prepended < 12:
            return
        f.seek(prepended - 12)
        tag, cfglen, bmlen = struct.unpack('<iii', f.read(12))
        if tag not in (305419898, 305419899):
            return
        f.seek(prepended - (12 + cfglen))
        init = {'version':'',  'target_version':''}
        cfg = configparser.RawConfigParser(init)
        try:
            part = f.read(cfglen)
            config = part.split(b'\x00', 1)[0]
            config = config.decode(sys.getfilesystemencoding())
            cfg.readfp(six.StringIO(config))
        except configparser.Error:
            return

        if not cfg.has_section('metadata') or not cfg.has_section('Setup'):
            return
        return cfg
    finally:
        f.close()


def get_exe_prefixes(exe_filename):
    """Get exe->egg path translations for a given .exe file"""
    prefixes = [
     ('PURELIB/', ''),
     ('PLATLIB/pywin32_system32', ''),
     ('PLATLIB/', ''),
     ('SCRIPTS/', 'EGG-INFO/scripts/'),
     ('DATA/lib/site-packages', '')]
    z = zipfile.ZipFile(exe_filename)
    try:
        for info in z.infolist():
            name = info.filename
            parts = name.split('/')
            if len(parts) == 3:
                if parts[2] == 'PKG-INFO':
                    if parts[1].endswith('.egg-info'):
                        prefixes.insert(0, ('/'.join(parts[:2]), 'EGG-INFO/'))
                        break
            if not len(parts) != 2:
                if not name.endswith('.pth'):
                    pass
                else:
                    if name.endswith('-nspkg.pth'):
                        pass
                    elif parts[0].upper() in ('PURELIB', 'PLATLIB'):
                        contents = z.read(name)
                        if six.PY3:
                            contents = contents.decode()
                        for pth in yield_lines(contents):
                            pth = pth.strip().replace('\\', '/')
                            if not pth.startswith('import'):
                                prefixes.append(('%s/%s/' % (parts[0], pth), ''))

    finally:
        z.close()

    prefixes = [(x.lower(), y) for x, y in prefixes]
    prefixes.sort()
    prefixes.reverse()
    return prefixes


class PthDistributions(Environment):
    __doc__ = 'A .pth file with Distribution paths in it'
    dirty = False

    def __init__(self, filename, sitedirs=()):
        self.filename = filename
        self.sitedirs = list(map(normalize_path, sitedirs))
        self.basedir = normalize_path(os.path.dirname(self.filename))
        self._load()
        Environment.__init__(self, [], None, None)
        for path in yield_lines(self.paths):
            list(map(self.add, find_distributions(path, True)))

    def _load(self):
        self.paths = []
        saw_import = False
        seen = dict.fromkeys(self.sitedirs)
        if os.path.isfile(self.filename):
            f = open(self.filename, 'rt')
            for line in f:
                if line.startswith('import'):
                    saw_import = True
                else:
                    path = line.rstrip()
                    self.paths.append(path)
                    if not not path.strip():
                        if path.strip().startswith('#'):
                            pass
                        else:
                            path = self.paths[-1] = normalize_path(os.path.join(self.basedir, path))
                            if not os.path.exists(path) or path in seen:
                                self.paths.pop()
                                self.dirty = True
                                continue
                            seen[path] = 1

            f.close()
        if self.paths:
            if not saw_import:
                self.dirty = True
        while self.paths and not self.paths[(-1)].strip():
            self.paths.pop()

    def save(self):
        """Write changed .pth file back to disk"""
        if not self.dirty:
            return
        rel_paths = list(map(self.make_relative, self.paths))
        if rel_paths:
            log.debug('Saving %s', self.filename)
            lines = self._wrap_lines(rel_paths)
            data = '\n'.join(lines) + '\n'
            if os.path.islink(self.filename):
                os.unlink(self.filename)
            with open(self.filename, 'wt') as (f):
                f.write(data)
        else:
            if os.path.exists(self.filename):
                log.debug('Deleting empty %s', self.filename)
                os.unlink(self.filename)
            self.dirty = False

    @staticmethod
    def _wrap_lines(lines):
        return lines

    def add(self, dist):
        """Add `dist` to the distribution map"""
        new_path = dist.location not in self.paths and (dist.location not in self.sitedirs or dist.location == os.getcwd())
        if new_path:
            self.paths.append(dist.location)
            self.dirty = True
        Environment.add(self, dist)

    def remove(self, dist):
        """Remove `dist` from the distribution map"""
        while dist.location in self.paths:
            self.paths.remove(dist.location)
            self.dirty = True

        Environment.remove(self, dist)

    def make_relative(self, path):
        npath, last = os.path.split(normalize_path(path))
        baselen = len(self.basedir)
        parts = [last]
        sep = os.altsep == '/' and '/' or os.sep
        while len(npath) >= baselen:
            if npath == self.basedir:
                parts.append(os.curdir)
                parts.reverse()
                return sep.join(parts)
            npath, last = os.path.split(npath)
            parts.append(last)
        else:
            return path


class RewritePthDistributions(PthDistributions):

    @classmethod
    def _wrap_lines(cls, lines):
        yield cls.prelude
        for line in lines:
            yield line

        yield cls.postlude

    prelude = _one_liner('\n        import sys\n        sys.__plen = len(sys.path)\n        ')
    postlude = _one_liner("\n        import sys\n        new = sys.path[sys.__plen:]\n        del sys.path[sys.__plen:]\n        p = getattr(sys, '__egginsert', 0)\n        sys.path[p:p] = new\n        sys.__egginsert = p + len(new)\n        ")


if os.environ.get('SETUPTOOLS_SYS_PATH_TECHNIQUE', 'raw') == 'rewrite':
    PthDistributions = RewritePthDistributions
else:

    def _first_line_re():
        """
    Return a regular expression based on first_line_re suitable for matching
    strings.
    """
        if isinstance(first_line_re.pattern, str):
            return first_line_re
        else:
            return re.compile(first_line_re.pattern.decode())


    def auto_chmod(func, arg, exc):
        if func in [os.unlink, os.remove]:
            if os.name == 'nt':
                chmod(arg, stat.S_IWRITE)
                return func(arg)
        et, ev, _ = sys.exc_info()
        six.reraise(et, (ev[0], ev[1] + ' %s %s' % (func, arg)))


    def update_dist_caches(dist_path, fix_zipimporter_caches):
        """
    Fix any globally cached `dist_path` related data

    `dist_path` should be a path of a newly installed egg distribution (zipped
    or unzipped).

    sys.path_importer_cache contains finder objects that have been cached when
    importing data from the original distribution. Any such finders need to be
    cleared since the replacement distribution might be packaged differently,
    e.g. a zipped egg distribution might get replaced with an unzipped egg
    folder or vice versa. Having the old finders cached may then cause Python
    to attempt loading modules from the replacement distribution using an
    incorrect loader.

    zipimport.zipimporter objects are Python loaders charged with importing
    data packaged inside zip archives. If stale loaders referencing the
    original distribution, are left behind, they can fail to load modules from
    the replacement distribution. E.g. if an old zipimport.zipimporter instance
    is used to load data from a new zipped egg archive, it may cause the
    operation to attempt to locate the requested data in the wrong location -
    one indicated by the original distribution's zip archive directory
    information. Such an operation may then fail outright, e.g. report having
    read a 'bad local file header', or even worse, it may fail silently &
    return invalid data.

    zipimport._zip_directory_cache contains cached zip archive directory
    information for all existing zipimport.zipimporter instances and all such
    instances connected to the same archive share the same cached directory
    information.

    If asked, and the underlying Python implementation allows it, we can fix
    all existing zipimport.zipimporter instances instead of having to track
    them down and remove them one by one, by updating their shared cached zip
    archive directory information. This, of course, assumes that the
    replacement distribution is packaged as a zipped egg.

    If not asked to fix existing zipimport.zipimporter instances, we still do
    our best to clear any remaining zipimport.zipimporter related cached data
    that might somehow later get used when attempting to load data from the new
    distribution and thus cause such load operations to fail. Note that when
    tracking down such remaining stale data, we can not catch every conceivable
    usage from here, and we clear only those that we know of and have found to
    cause problems if left alive. Any remaining caches should be updated by
    whomever is in charge of maintaining them, i.e. they should be ready to
    handle us replacing their zip archives with new distributions at runtime.

    """
        normalized_path = normalize_path(dist_path)
        _uncache(normalized_path, sys.path_importer_cache)
        if fix_zipimporter_caches:
            _replace_zip_directory_cache_data(normalized_path)
        else:
            _remove_and_clear_zip_directory_cache_data(normalized_path)


    def _collect_zipimporter_cache_entries(normalized_path, cache):
        """
    Return zipimporter cache entry keys related to a given normalized path.

    Alternative path spellings (e.g. those using different character case or
    those using alternative path separators) related to the same path are
    included. Any sub-path entries are included as well, i.e. those
    corresponding to zip archives embedded in other zip archives.

    """
        result = []
        prefix_len = len(normalized_path)
        for p in cache:
            np = normalize_path(p)
            if np.startswith(normalized_path) and np[prefix_len:prefix_len + 1] in (os.sep, ''):
                result.append(p)

        return result


    def _update_zipimporter_cache(normalized_path, cache, updater=None):
        """
    Update zipimporter cache data for a given normalized path.

    Any sub-path entries are processed as well, i.e. those corresponding to zip
    archives embedded in other zip archives.

    Given updater is a callable taking a cache entry key and the original entry
    (after already removing the entry from the cache), and expected to update
    the entry and possibly return a new one to be inserted in its place.
    Returning None indicates that the entry should not be replaced with a new
    one. If no updater is given, the cache entries are simply removed without
    any additional processing, the same as if the updater simply returned None.

    """
        for p in _collect_zipimporter_cache_entries(normalized_path, cache):
            old_entry = cache[p]
            del cache[p]
            new_entry = updater and updater(p, old_entry)
            if new_entry is not None:
                cache[p] = new_entry


    def _uncache(normalized_path, cache):
        _update_zipimporter_cache(normalized_path, cache)


    def _remove_and_clear_zip_directory_cache_data(normalized_path):

        def clear_and_remove_cached_zip_archive_directory_data(path, old_entry):
            old_entry.clear()

        _update_zipimporter_cache(normalized_path,
          (zipimport._zip_directory_cache), updater=clear_and_remove_cached_zip_archive_directory_data)


    if '__pypy__' in sys.builtin_module_names:
        _replace_zip_directory_cache_data = _remove_and_clear_zip_directory_cache_data
    else:

        def _replace_zip_directory_cache_data(normalized_path):

            def replace_cached_zip_archive_directory_data(path, old_entry):
                old_entry.clear()
                zipimport.zipimporter(path)
                old_entry.update(zipimport._zip_directory_cache[path])
                return old_entry

            _update_zipimporter_cache(normalized_path,
              (zipimport._zip_directory_cache), updater=replace_cached_zip_archive_directory_data)


def is_python(text, filename='<string>'):
    """Is this string a valid Python script?"""
    try:
        compile(text, filename, 'exec')
    except (SyntaxError, TypeError):
        return False
    else:
        return True


def is_sh(executable):
    """Determine if the specified executable is a .sh (contains a #! line)"""
    try:
        with io.open(executable, encoding='latin-1') as (fp):
            magic = fp.read(2)
    except (OSError, IOError):
        return executable
    else:
        return magic == '#!'


def nt_quote_arg(arg):
    """Quote a command line argument according to Windows parsing rules"""
    return subprocess.list2cmdline([arg])


def is_python_script(script_text, filename):
    """Is this text, as a whole, a Python script? (as opposed to shell/bat/etc.
    """
    if filename.endswith('.py') or filename.endswith('.pyw'):
        return True
    else:
        if is_python(script_text, filename):
            return True
        if script_text.startswith('#!'):
            return 'python' in script_text.splitlines()[0].lower()
        return False


try:
    from os import chmod as _chmod
except ImportError:

    def _chmod(*args):
        pass


def chmod(path, mode):
    log.debug('changing mode of %s to %o', path, mode)
    try:
        _chmod(path, mode)
    except os.error as e:
        log.debug('chmod failed: %s', e)


class CommandSpec(list):
    __doc__ = '\n    A command spec for a #! header, specified as a list of arguments akin to\n    those passed to Popen.\n    '
    options = []
    split_args = dict()

    @classmethod
    def best(cls):
        """
        Choose the best CommandSpec class based on environmental conditions.
        """
        return cls

    @classmethod
    def _sys_executable(cls):
        _default = os.path.normpath(sys.executable)
        return os.environ.get('__PYVENV_LAUNCHER__', _default)

    @classmethod
    def from_param(cls, param):
        """
        Construct a CommandSpec from a parameter to build_scripts, which may
        be None.
        """
        if isinstance(param, cls):
            return param
        else:
            if isinstance(param, list):
                return cls(param)
            if param is None:
                return cls.from_environment()
            return cls.from_string(param)

    @classmethod
    def from_environment(cls):
        return cls([cls._sys_executable()])

    @classmethod
    def from_string(cls, string):
        """
        Construct a command spec from a simple string representing a command
        line parseable by shlex.split.
        """
        items = (shlex.split)(string, **cls.split_args)
        return cls(items)

    def install_options(self, script_text):
        self.options = shlex.split(self._extract_options(script_text))
        cmdline = subprocess.list2cmdline(self)
        if not isascii(cmdline):
            self.options[:0] = [
             '-x']

    @staticmethod
    def _extract_options(orig_script):
        """
        Extract any options from the first line of the script.
        """
        first = (orig_script + '\n').splitlines()[0]
        match = _first_line_re().match(first)
        options = match.group(1) or '' if match else ''
        return options.strip()

    def as_header(self):
        return self._render(self + list(self.options))

    @staticmethod
    def _strip_quotes(item):
        _QUOTES = '"\''
        for q in _QUOTES:
            if item.startswith(q):
                if item.endswith(q):
                    return item[1:-1]

        return item

    @staticmethod
    def _render(items):
        cmdline = subprocess.list2cmdline(CommandSpec._strip_quotes(item.strip()) for item in items)
        return '#!' + cmdline + '\n'


sys_executable = CommandSpec._sys_executable()

class WindowsCommandSpec(CommandSpec):
    split_args = dict(posix=False)


class ScriptWriter(object):
    __doc__ = '\n    Encapsulates behavior around writing entry point scripts for console and\n    gui apps.\n    '
    template = textwrap.dedent("\n        # EASY-INSTALL-ENTRY-SCRIPT: %(spec)r,%(group)r,%(name)r\n        __requires__ = %(spec)r\n        import re\n        import sys\n        from pkg_resources import load_entry_point\n\n        if __name__ == '__main__':\n            sys.argv[0] = re.sub(r'(-script\\.pyw?|\\.exe)?$', '', sys.argv[0])\n            sys.exit(\n                load_entry_point(%(spec)r, %(group)r, %(name)r)()\n            )\n    ").lstrip()
    command_spec_class = CommandSpec

    @classmethod
    def get_script_args(cls, dist, executable=None, wininst=False):
        warnings.warn('Use get_args', DeprecationWarning)
        writer = (WindowsScriptWriter if wininst else ScriptWriter).best()
        header = cls.get_script_header('', executable, wininst)
        return writer.get_args(dist, header)

    @classmethod
    def get_script_header(cls, script_text, executable=None, wininst=False):
        warnings.warn('Use get_header', DeprecationWarning)
        if wininst:
            executable = 'python.exe'
        cmd = cls.command_spec_class.best().from_param(executable)
        cmd.install_options(script_text)
        return cmd.as_header()

    @classmethod
    def get_args(cls, dist, header=None):
        """
        Yield write_script() argument tuples for a distribution's
        console_scripts and gui_scripts entry points.
        """
        if header is None:
            header = cls.get_header()
        spec = str(dist.as_requirement())
        for type_ in ('console', 'gui'):
            group = type_ + '_scripts'
            for name, ep in dist.get_entry_map(group).items():
                cls._ensure_safe_name(name)
                script_text = cls.template % locals()
                args = cls._get_script_args(type_, name, header, script_text)
                for res in args:
                    yield res

    @staticmethod
    def _ensure_safe_name(name):
        """
        Prevent paths in *_scripts entry point names.
        """
        has_path_sep = re.search('[\\\\/]', name)
        if has_path_sep:
            raise ValueError('Path separators not allowed in script names')

    @classmethod
    def get_writer(cls, force_windows):
        warnings.warn('Use best', DeprecationWarning)
        if force_windows:
            return WindowsScriptWriter.best()
        else:
            return cls.best()

    @classmethod
    def best(cls):
        """
        Select the best ScriptWriter for this environment.
        """
        if sys.platform == 'win32' or os.name == 'java' and os._name == 'nt':
            return WindowsScriptWriter.best()
        else:
            return cls

    @classmethod
    def _get_script_args(cls, type_, name, header, script_text):
        yield (
         name, header + script_text)

    @classmethod
    def get_header(cls, script_text='', executable=None):
        """Create a #! line, getting options (if any) from script_text"""
        cmd = cls.command_spec_class.best().from_param(executable)
        cmd.install_options(script_text)
        return cmd.as_header()


class WindowsScriptWriter(ScriptWriter):
    command_spec_class = WindowsCommandSpec

    @classmethod
    def get_writer(cls):
        warnings.warn('Use best', DeprecationWarning)
        return cls.best()

    @classmethod
    def best(cls):
        """
        Select the best ScriptWriter suitable for Windows
        """
        writer_lookup = dict(executable=WindowsExecutableLauncherWriter,
          natural=cls)
        launcher = os.environ.get('SETUPTOOLS_LAUNCHER', 'executable')
        return writer_lookup[launcher]

    @classmethod
    def _get_script_args(cls, type_, name, header, script_text):
        """For Windows, add a .py extension"""
        ext = dict(console='.pya', gui='.pyw')[type_]
        if ext not in os.environ['PATHEXT'].lower().split(';'):
            msg = ('{ext} not listed in PATHEXT; scripts will not be recognized as executables.'.format)(**locals())
            warnings.warn(msg, UserWarning)
        old = [
         '.pya', '.py', '-script.py', '.pyc', '.pyo', '.pyw', '.exe']
        old.remove(ext)
        header = cls._adjust_header(type_, header)
        blockers = [name + x for x in old]
        yield (name + ext, header + script_text, 't', blockers)

    @classmethod
    def _adjust_header(cls, type_, orig_header):
        """
        Make sure 'pythonw' is used for gui and and 'python' is used for
        console (regardless of what sys.executable is).
        """
        pattern = 'pythonw.exe'
        repl = 'python.exe'
        if type_ == 'gui':
            pattern, repl = repl, pattern
        pattern_ob = re.compile(re.escape(pattern), re.IGNORECASE)
        new_header = pattern_ob.sub(string=orig_header, repl=repl)
        if cls._use_header(new_header):
            return new_header
        else:
            return orig_header

    @staticmethod
    def _use_header(new_header):
        """
        Should _adjust_header use the replaced header?

        On non-windows systems, always use. On
        Windows systems, only use the replaced header if it resolves
        to an executable on the system.
        """
        clean_header = new_header[2:-1].strip('"')
        return sys.platform != 'win32' or find_executable(clean_header)


class WindowsExecutableLauncherWriter(WindowsScriptWriter):

    @classmethod
    def _get_script_args(cls, type_, name, header, script_text):
        """
        For Windows, add a .py extension and an .exe launcher
        """
        if type_ == 'gui':
            launcher_type = 'gui'
            ext = '-script.pyw'
            old = ['.pyw']
        else:
            launcher_type = 'cli'
            ext = '-script.py'
            old = ['.py', '.pyc', '.pyo']
        hdr = cls._adjust_header(type_, header)
        blockers = [name + x for x in old]
        yield (name + ext, hdr + script_text, 't', blockers)
        yield (
         name + '.exe', get_win_launcher(launcher_type),
         'b')
        if not is_64bit():
            m_name = name + '.exe.manifest'
            yield (m_name, load_launcher_manifest(name), 't')


get_script_args = ScriptWriter.get_script_args
get_script_header = ScriptWriter.get_script_header

def get_win_launcher(type):
    """
    Load the Windows launcher (executable) suitable for launching a script.

    `type` should be either 'cli' or 'gui'

    Returns the executable as a byte string.
    """
    launcher_fn = '%s.exe' % type
    if is_64bit():
        launcher_fn = launcher_fn.replace('.', '-64.')
    else:
        launcher_fn = launcher_fn.replace('.', '-32.')
    return resource_string('setuptools', launcher_fn)


def load_launcher_manifest(name):
    manifest = pkg_resources.resource_string(__name__, 'launcher manifest.xml')
    if six.PY2:
        return manifest % vars()
    else:
        return manifest.decode('utf-8') % vars()


def rmtree(path, ignore_errors=False, onerror=auto_chmod):
    return shutil.rmtree(path, ignore_errors, onerror)


def current_umask():
    tmp = os.umask(18)
    os.umask(tmp)
    return tmp


def bootstrap():
    import setuptools
    argv0 = os.path.dirname(setuptools.__path__[0])
    sys.argv[0] = argv0
    sys.argv.append(argv0)
    main()


def main(argv=None, **kw):
    from setuptools import setup
    from setuptools.dist import Distribution

    class DistributionWithoutHelpCommands(Distribution):
        common_usage = ''

        def _show_help(self, *args, **kw):
            with _patch_usage():
                (Distribution._show_help)(self, *args, **kw)

    if argv is None:
        argv = sys.argv[1:]
    with _patch_usage():
        setup(script_args=[
 '-q', 'easy_install', '-v'] + argv, 
         script_name=sys.argv[0] or 'easy_install', 
         distclass=DistributionWithoutHelpCommands, **kw)


@contextlib.contextmanager
def _patch_usage():
    import distutils.core
    USAGE = textwrap.dedent('\n        usage: %(script)s [options] requirement_or_url ...\n           or: %(script)s --help\n        ').lstrip()

    def gen_usage(script_name):
        return USAGE % dict(script=(os.path.basename(script_name)))

    saved = distutils.core.gen_usage
    distutils.core.gen_usage = gen_usage
    try:
        yield
    finally:
        distutils.core.gen_usage = saved