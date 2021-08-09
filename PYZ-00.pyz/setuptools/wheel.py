# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\setuptools-39.0.1-py3.6.egg\setuptools\wheel.py
"""Wheels support."""
from distutils.util import get_platform
import email, itertools, os, re, zipfile
from pkg_resources import Distribution, PathMetadata, parse_version
from setuptools.extern.six import PY3
from setuptools import Distribution as SetuptoolsDistribution
from setuptools import pep425tags
from setuptools.command.egg_info import write_requirements
WHEEL_NAME = re.compile('^(?P<project_name>.+?)-(?P<version>\\d.*?)\n    ((-(?P<build>\\d.*?))?-(?P<py_version>.+?)-(?P<abi>.+?)-(?P<platform>.+?)\n    )\\.whl$', re.VERBOSE).match
NAMESPACE_PACKAGE_INIT = "try:\n    __import__('pkg_resources').declare_namespace(__name__)\nexcept ImportError:\n    __path__ = __import__('pkgutil').extend_path(__path__, __name__)\n"

def unpack(src_dir, dst_dir):
    """Move everything under `src_dir` to `dst_dir`, and delete the former."""
    for dirpath, dirnames, filenames in os.walk(src_dir):
        subdir = os.path.relpath(dirpath, src_dir)
        for f in filenames:
            src = os.path.join(dirpath, f)
            dst = os.path.join(dst_dir, subdir, f)
            os.renames(src, dst)

        for n, d in reversed(list(enumerate(dirnames))):
            src = os.path.join(dirpath, d)
            dst = os.path.join(dst_dir, subdir, d)
            if not os.path.exists(dst):
                os.renames(src, dst)
                del dirnames[n]

    for dirpath, dirnames, filenames in os.walk(src_dir, topdown=True):
        assert not filenames
        os.rmdir(dirpath)


class Wheel(object):

    def __init__(self, filename):
        match = WHEEL_NAME(os.path.basename(filename))
        if match is None:
            raise ValueError('invalid wheel name: %r' % filename)
        self.filename = filename
        for k, v in match.groupdict().items():
            setattr(self, k, v)

    def tags(self):
        """List tags (py_version, abi, platform) supported by this wheel."""
        return itertools.product(self.py_version.split('.'), self.abi.split('.'), self.platform.split('.'))

    def is_compatible(self):
        """Is the wheel is compatible with the current platform?"""
        supported_tags = pep425tags.get_supported()
        return next((True for t in self.tags() if t in supported_tags), False)

    def egg_name(self):
        return Distribution(project_name=(self.project_name),
          version=(self.version),
          platform=(None if self.platform == 'any' else get_platform())).egg_name() + '.egg'

    def install_as_egg(self, destination_eggdir):
        """Install wheel as an egg directory."""
        with zipfile.ZipFile(self.filename) as (zf):
            dist_basename = '%s-%s' % (self.project_name, self.version)
            dist_info = '%s.dist-info' % dist_basename
            dist_data = '%s.data' % dist_basename

            def get_metadata(name):
                with zf.open('%s/%s' % (dist_info, name)) as (fp):
                    value = fp.read().decode('utf-8') if PY3 else fp.read()
                    return email.parser.Parser().parsestr(value)

            wheel_metadata = get_metadata('WHEEL')
            dist_metadata = get_metadata('METADATA')
            wheel_version = parse_version(wheel_metadata.get('Wheel-Version'))
            if not parse_version('1.0') <= wheel_version < parse_version('2.0dev0'):
                raise ValueError('unsupported wheel format version: %s' % wheel_version)
            os.mkdir(destination_eggdir)
            zf.extractall(destination_eggdir)
            dist_info = os.path.join(destination_eggdir, dist_info)
            dist = Distribution.from_location(destination_eggdir,
              dist_info, metadata=(PathMetadata(destination_eggdir, dist_info)))

            def raw_req(req):
                req.marker = None
                return str(req)

            install_requires = list(sorted(map(raw_req, dist.requires())))
            extras_require = {extra:list(sorted(req for req in map(raw_req, dist.requires((extra,))) if req not in install_requires)) for extra in dist.extras}
            egg_info = os.path.join(destination_eggdir, 'EGG-INFO')
            os.rename(dist_info, egg_info)
            os.rename(os.path.join(egg_info, 'METADATA'), os.path.join(egg_info, 'PKG-INFO'))
            setup_dist = SetuptoolsDistribution(attrs=dict(install_requires=install_requires,
              extras_require=extras_require))
            write_requirements(setup_dist.get_command_obj('egg_info'), None, os.path.join(egg_info, 'requires.txt'))
            dist_data = os.path.join(destination_eggdir, dist_data)
            dist_data_scripts = os.path.join(dist_data, 'scripts')
            if os.path.exists(dist_data_scripts):
                egg_info_scripts = os.path.join(destination_eggdir, 'EGG-INFO', 'scripts')
                os.mkdir(egg_info_scripts)
                for entry in os.listdir(dist_data_scripts):
                    if entry.endswith('.pyc'):
                        os.unlink(os.path.join(dist_data_scripts, entry))
                    else:
                        os.rename(os.path.join(dist_data_scripts, entry), os.path.join(egg_info_scripts, entry))

                os.rmdir(dist_data_scripts)
            for subdir in filter(os.path.exists, (os.path.join(dist_data, d) for d in ('data',
                                                                                       'headers',
                                                                                       'purelib',
                                                                                       'platlib'))):
                unpack(subdir, destination_eggdir)

            if os.path.exists(dist_data):
                os.rmdir(dist_data)
            namespace_packages = os.path.join(egg_info, 'namespace_packages.txt')
            if os.path.exists(namespace_packages):
                with open(namespace_packages) as (fp):
                    namespace_packages = fp.read().split()
                for mod in namespace_packages:
                    mod_dir = (os.path.join)(destination_eggdir, *mod.split('.'))
                    mod_init = os.path.join(mod_dir, '__init__.py')
                    if os.path.exists(mod_dir) and not os.path.exists(mod_init):
                        with open(mod_init, 'w') as (fp):
                            fp.write(NAMESPACE_PACKAGE_INIT)