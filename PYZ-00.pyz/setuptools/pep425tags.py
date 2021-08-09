# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\setuptools-39.0.1-py3.6.egg\setuptools\pep425tags.py
"""Generate and work with PEP 425 Compatibility Tags."""
from __future__ import absolute_import
import distutils.util, platform, re, sys, sysconfig, warnings
from collections import OrderedDict
from . import glibc
_osx_arch_pat = re.compile('(.+)_(\\d+)_(\\d+)_(.+)')

def get_config_var(var):
    try:
        return sysconfig.get_config_var(var)
    except IOError as e:
        warnings.warn('{}'.format(e), RuntimeWarning)
        return


def get_abbr_impl():
    """Return abbreviated implementation name."""
    if hasattr(sys, 'pypy_version_info'):
        pyimpl = 'pp'
    else:
        if sys.platform.startswith('java'):
            pyimpl = 'jy'
        else:
            if sys.platform == 'cli':
                pyimpl = 'ip'
            else:
                pyimpl = 'cp'
    return pyimpl


def get_impl_ver():
    """Return implementation version."""
    impl_ver = get_config_var('py_version_nodot')
    if not impl_ver or get_abbr_impl() == 'pp':
        impl_ver = ''.join(map(str, get_impl_version_info()))
    return impl_ver


def get_impl_version_info():
    """Return sys.version_info-like tuple for use in decrementing the minor
    version."""
    if get_abbr_impl() == 'pp':
        return (
         sys.version_info[0], sys.pypy_version_info.major,
         sys.pypy_version_info.minor)
    else:
        return (
         sys.version_info[0], sys.version_info[1])


def get_impl_tag():
    """
    Returns the Tag for this specific implementation.
    """
    return '{}{}'.format(get_abbr_impl(), get_impl_ver())


def get_flag(var, fallback, expected=True, warn=True):
    """Use a fallback method for determining SOABI flags if the needed config
    var is unset or unavailable."""
    val = get_config_var(var)
    if val is None:
        if warn:
            warnings.warn("Config variable '{0}' is unset, Python ABI tag may be incorrect".format(var), RuntimeWarning, 2)
        return fallback()
    else:
        return val == expected


def get_abi_tag():
    """Return the ABI tag based on SOABI (if available) or emulate SOABI
    (CPython 2, PyPy)."""
    soabi = get_config_var('SOABI')
    impl = get_abbr_impl()
    if not soabi:
        if impl in frozenset({'pp', 'cp'}):
            if hasattr(sys, 'maxunicode'):
                d = ''
                m = ''
                u = ''
                if get_flag('Py_DEBUG', (lambda : hasattr(sys, 'gettotalrefcount')),
                  warn=(impl == 'cp')):
                    d = 'd'
                if get_flag('WITH_PYMALLOC', (lambda : impl == 'cp'),
                  warn=(impl == 'cp')):
                    m = 'm'
                if get_flag('Py_UNICODE_SIZE', (lambda : sys.maxunicode == 1114111),
                  expected=4,
                  warn=(impl == 'cp' and sys.version_info < (3, 3))):
                    if sys.version_info < (3, 3):
                        u = 'u'
                abi = '%s%s%s%s%s' % (impl, get_impl_ver(), d, m, u)
    if soabi and soabi.startswith('cpython-'):
        abi = 'cp' + soabi.split('-')[1]
    else:
        if soabi:
            abi = soabi.replace('.', '_').replace('-', '_')
        else:
            abi = None
    return abi


def _is_running_32bit():
    return sys.maxsize == 2147483647


def get_platform():
    """Return our platform name 'win32', 'linux_x86_64'"""
    if sys.platform == 'darwin':
        release, _, machine = platform.mac_ver()
        split_ver = release.split('.')
        if machine == 'x86_64':
            if _is_running_32bit():
                machine = 'i386'
        if machine == 'ppc64':
            if _is_running_32bit():
                machine = 'ppc'
        return 'macosx_{}_{}_{}'.format(split_ver[0], split_ver[1], machine)
    else:
        result = distutils.util.get_platform().replace('.', '_').replace('-', '_')
        if result == 'linux_x86_64':
            if _is_running_32bit():
                result = 'linux_i686'
        return result


def is_manylinux1_compatible():
    if get_platform() not in frozenset({'linux_x86_64', 'linux_i686'}):
        return False
    else:
        try:
            import _manylinux
            return bool(_manylinux.manylinux1_compatible)
        except (ImportError, AttributeError):
            pass

        return glibc.have_compatible_glibc(2, 5)


def get_darwin_arches(major, minor, machine):
    """Return a list of supported arches (including group arches) for
    the given major, minor and machine architecture of an macOS machine.
    """
    arches = []

    def _supports_arch(major, minor, arch):
        if arch == 'ppc':
            return (major, minor) <= (10, 5)
        else:
            if arch == 'ppc64':
                return (
                 major, minor) == (10, 5)
            else:
                if arch == 'i386':
                    return (
                     major, minor) >= (10, 4)
                if arch == 'x86_64':
                    return (
                     major, minor) >= (10, 5)
                if arch in groups:
                    for garch in groups[arch]:
                        if _supports_arch(major, minor, garch):
                            return True

            return False

    groups = OrderedDict([
     ('fat', ('i386', 'ppc')),
     ('intel', ('x86_64', 'i386')),
     ('fat64', ('x86_64', 'ppc64')),
     ('fat32', ('x86_64', 'i386', 'ppc'))])
    if _supports_arch(major, minor, machine):
        arches.append(machine)
    for garch in groups:
        if machine in groups[garch] and _supports_arch(major, minor, garch):
            arches.append(garch)

    arches.append('universal')
    return arches


def get_supported(versions=None, noarch=False, platform=None, impl=None, abi=None):
    """Return a list of supported tags for each version specified in
    `versions`.

    :param versions: a list of string versions, of the form ["33", "32"],
        or None. The first version will be assumed to support our ABI.
    :param platform: specify the exact platform you want valid
        tags for, or None. If None, use the local system platform.
    :param impl: specify the exact implementation you want valid
        tags for, or None. If None, use the local interpreter impl.
    :param abi: specify the exact abi you want valid
        tags for, or None. If None, use the local interpreter abi.
    """
    supported = []
    if versions is None:
        versions = []
        version_info = get_impl_version_info()
        major = version_info[:-1]
        for minor in range(version_info[(-1)], -1, -1):
            versions.append(''.join(map(str, major + (minor,))))

    impl = impl or get_abbr_impl()
    abis = []
    abi = abi or get_abi_tag()
    if abi:
        abis[0:0] = [
         abi]
    abi3s = set()
    import imp
    for suffix in imp.get_suffixes():
        if suffix[0].startswith('.abi'):
            abi3s.add(suffix[0].split('.', 2)[1])

    abis.extend(sorted(list(abi3s)))
    abis.append('none')
    if not noarch:
        arch = platform or get_platform()
        if arch.startswith('macosx'):
            match = _osx_arch_pat.match(arch)
            if match:
                name, major, minor, actual_arch = match.groups()
                tpl = '{}_{}_%i_%s'.format(name, major)
                arches = []
                for m in reversed(range(int(minor) + 1)):
                    for a in get_darwin_arches(int(major), m, actual_arch):
                        arches.append(tpl % (m, a))

            else:
                arches = [
                 arch]
        elif platform is None:
            if is_manylinux1_compatible():
                arches = [
                 arch.replace('linux', 'manylinux1'), arch]
        else:
            arches = [
             arch]
        for abi in abis:
            for arch in arches:
                supported.append(('%s%s' % (impl, versions[0]), abi, arch))

        for version in versions[1:]:
            if version in frozenset({'31', '30'}):
                break
            for abi in abi3s:
                for arch in arches:
                    supported.append(('%s%s' % (impl, version), abi, arch))

        for arch in arches:
            supported.append(('py%s' % versions[0][0], 'none', arch))

    supported.append(('%s%s' % (impl, versions[0]), 'none', 'any'))
    supported.append(('%s%s' % (impl, versions[0][0]), 'none', 'any'))
    for i, version in enumerate(versions):
        supported.append(('py%s' % (version,), 'none', 'any'))
        if i == 0:
            supported.append(('py%s' % version[0], 'none', 'any'))

    return supported


implementation_tag = get_impl_tag()