# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: uuid.py
r"""UUID objects (universally unique identifiers) according to RFC 4122.

This module provides immutable UUID objects (class UUID) and the functions
uuid1(), uuid3(), uuid4(), uuid5() for generating version 1, 3, 4, and 5
UUIDs as specified in RFC 4122.

If all you want is a unique ID, you should probably call uuid1() or uuid4().
Note that uuid1() may compromise privacy since it creates a UUID containing
the computer's network address.  uuid4() creates a random UUID.

Typical usage:

    >>> import uuid

    # make a UUID based on the host ID and current time
    >>> uuid.uuid1()    # doctest: +SKIP
    UUID('a8098c1a-f86e-11da-bd1a-00112444be1e')

    # make a UUID using an MD5 hash of a namespace UUID and a name
    >>> uuid.uuid3(uuid.NAMESPACE_DNS, 'python.org')
    UUID('6fa459ea-ee8a-3ca4-894e-db77e160355e')

    # make a random UUID
    >>> uuid.uuid4()    # doctest: +SKIP
    UUID('16fd2706-8baf-433b-82eb-8c7fada847da')

    # make a UUID using a SHA-1 hash of a namespace UUID and a name
    >>> uuid.uuid5(uuid.NAMESPACE_DNS, 'python.org')
    UUID('886313e1-3b8a-5372-9b90-0c9aee199e5d')

    # make a UUID from a string of hex digits (braces and hyphens ignored)
    >>> x = uuid.UUID('{00010203-0405-0607-0809-0a0b0c0d0e0f}')

    # convert a UUID to a string of hex digits in standard form
    >>> str(x)
    '00010203-0405-0607-0809-0a0b0c0d0e0f'

    # get the raw 16 bytes of the UUID
    >>> x.bytes
    b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'

    # make a UUID from a 16-byte string
    >>> uuid.UUID(bytes=x.bytes)
    UUID('00010203-0405-0607-0809-0a0b0c0d0e0f')
"""
import os
__author__ = 'Ka-Ping Yee <ping@zesty.ca>'
RESERVED_NCS, RFC_4122, RESERVED_MICROSOFT, RESERVED_FUTURE = [
 'reserved for NCS compatibility', 'specified in RFC 4122',
 'reserved for Microsoft compatibility', 'reserved for future definition']
int_ = int
bytes_ = bytes

class UUID(object):
    __doc__ = "Instances of the UUID class represent UUIDs as specified in RFC 4122.\n    UUID objects are immutable, hashable, and usable as dictionary keys.\n    Converting a UUID to a string with str() yields something in the form\n    '12345678-1234-1234-1234-123456789abc'.  The UUID constructor accepts\n    five possible forms: a similar string of hexadecimal digits, or a tuple\n    of six integer fields (with 32-bit, 16-bit, 16-bit, 8-bit, 8-bit, and\n    48-bit values respectively) as an argument named 'fields', or a string\n    of 16 bytes (with all the integer fields in big-endian order) as an\n    argument named 'bytes', or a string of 16 bytes (with the first three\n    fields in little-endian order) as an argument named 'bytes_le', or a\n    single 128-bit integer as an argument named 'int'.\n\n    UUIDs have these read-only attributes:\n\n        bytes       the UUID as a 16-byte string (containing the six\n                    integer fields in big-endian byte order)\n\n        bytes_le    the UUID as a 16-byte string (with time_low, time_mid,\n                    and time_hi_version in little-endian byte order)\n\n        fields      a tuple of the six integer fields of the UUID,\n                    which are also available as six individual attributes\n                    and two derived attributes:\n\n            time_low                the first 32 bits of the UUID\n            time_mid                the next 16 bits of the UUID\n            time_hi_version         the next 16 bits of the UUID\n            clock_seq_hi_variant    the next 8 bits of the UUID\n            clock_seq_low           the next 8 bits of the UUID\n            node                    the last 48 bits of the UUID\n\n            time                    the 60-bit timestamp\n            clock_seq               the 14-bit sequence number\n\n        hex         the UUID as a 32-character hexadecimal string\n\n        int         the UUID as a 128-bit integer\n\n        urn         the UUID as a URN as specified in RFC 4122\n\n        variant     the UUID variant (one of the constants RESERVED_NCS,\n                    RFC_4122, RESERVED_MICROSOFT, or RESERVED_FUTURE)\n\n        version     the UUID version number (1 through 5, meaningful only\n                    when the variant is RFC_4122)\n    "

    def __init__(self, hex=None, bytes=None, bytes_le=None, fields=None, int=None, version=None):
        r"""Create a UUID from either a string of 32 hexadecimal digits,
        a string of 16 bytes as the 'bytes' argument, a string of 16 bytes
        in little-endian order as the 'bytes_le' argument, a tuple of six
        integers (32-bit time_low, 16-bit time_mid, 16-bit time_hi_version,
        8-bit clock_seq_hi_variant, 8-bit clock_seq_low, 48-bit node) as
        the 'fields' argument, or a single 128-bit integer as the 'int'
        argument.  When a string of hex digits is given, curly braces,
        hyphens, and a URN prefix are all optional.  For example, these
        expressions all yield the same UUID:

        UUID('{12345678-1234-5678-1234-567812345678}')
        UUID('12345678123456781234567812345678')
        UUID('urn:uuid:12345678-1234-5678-1234-567812345678')
        UUID(bytes='\x12\x34\x56\x78'*4)
        UUID(bytes_le='\x78\x56\x34\x12\x34\x12\x78\x56' +
                      '\x12\x34\x56\x78\x12\x34\x56\x78')
        UUID(fields=(0x12345678, 0x1234, 0x5678, 0x12, 0x34, 0x567812345678))
        UUID(int=0x12345678123456781234567812345678)

        Exactly one of 'hex', 'bytes', 'bytes_le', 'fields', or 'int' must
        be given.  The 'version' argument is optional; if given, the resulting
        UUID will have its variant and version set according to RFC 4122,
        overriding the given 'hex', 'bytes', 'bytes_le', 'fields', or 'int'.
        """
        if [
         hex, bytes, bytes_le, fields, int].count(None) != 4:
            raise TypeError('one of the hex, bytes, bytes_le, fields, or int arguments must be given')
        else:
            if hex is not None:
                hex = hex.replace('urn:', '').replace('uuid:', '')
                hex = hex.strip('{}').replace('-', '')
                if len(hex) != 32:
                    raise ValueError('badly formed hexadecimal UUID string')
                int = int_(hex, 16)
            elif bytes_le is not None:
                if len(bytes_le) != 16:
                    raise ValueError('bytes_le is not a 16-char string')
                bytes = bytes_le[3::-1] + bytes_le[5:3:-1] + bytes_le[7:5:-1] + bytes_le[8:]
            else:
                if bytes is not None:
                    if len(bytes) != 16:
                        raise ValueError('bytes is not a 16-char string')
                    elif not isinstance(bytes, bytes_):
                        raise AssertionError(repr(bytes))
                    int = int_.from_bytes(bytes, byteorder='big')
                if fields is not None:
                    if len(fields) != 6:
                        raise ValueError('fields is not a 6-tuple')
                    else:
                        time_low, time_mid, time_hi_version, clock_seq_hi_variant, clock_seq_low, node = fields
                        if not 0 <= time_low < 4294967296:
                            raise ValueError('field 1 out of range (need a 32-bit value)')
                        if not 0 <= time_mid < 65536:
                            raise ValueError('field 2 out of range (need a 16-bit value)')
                        if not 0 <= time_hi_version < 65536:
                            raise ValueError('field 3 out of range (need a 16-bit value)')
                        if not 0 <= clock_seq_hi_variant < 256:
                            raise ValueError('field 4 out of range (need an 8-bit value)')
                        if not 0 <= clock_seq_low < 256:
                            raise ValueError('field 5 out of range (need an 8-bit value)')
                        raise 0 <= node < 281474976710656 or ValueError('field 6 out of range (need a 48-bit value)')
                    clock_seq = clock_seq_hi_variant << 8 | clock_seq_low
                    int = time_low << 96 | time_mid << 80 | time_hi_version << 64 | clock_seq << 48 | node
                if int is not None:
                    raise 0 <= int < 340282366920938463463374607431768211456 or ValueError('int is out of range (need a 128-bit value)')
            if version is not None:
                if not 1 <= version <= 5:
                    raise ValueError('illegal version number')
                int &= -13835058055282163713
                int |= 9223372036854775808
                int &= -1133367955888714851287041
                int |= version << 76
        self.__dict__['int'] = int

    def __eq__(self, other):
        if isinstance(other, UUID):
            return self.int == other.int
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, UUID):
            return self.int < other.int
        else:
            return NotImplemented

    def __gt__(self, other):
        if isinstance(other, UUID):
            return self.int > other.int
        else:
            return NotImplemented

    def __le__(self, other):
        if isinstance(other, UUID):
            return self.int <= other.int
        else:
            return NotImplemented

    def __ge__(self, other):
        if isinstance(other, UUID):
            return self.int >= other.int
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.int)

    def __int__(self):
        return self.int

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, str(self))

    def __setattr__(self, name, value):
        raise TypeError('UUID objects are immutable')

    def __str__(self):
        hex = '%032x' % self.int
        return '%s-%s-%s-%s-%s' % (
         hex[:8], hex[8:12], hex[12:16], hex[16:20], hex[20:])

    @property
    def bytes(self):
        return self.int.to_bytes(16, 'big')

    @property
    def bytes_le(self):
        bytes = self.bytes
        return bytes[3::-1] + bytes[5:3:-1] + bytes[7:5:-1] + bytes[8:]

    @property
    def fields(self):
        return (self.time_low, self.time_mid, self.time_hi_version,
         self.clock_seq_hi_variant, self.clock_seq_low, self.node)

    @property
    def time_low(self):
        return self.int >> 96

    @property
    def time_mid(self):
        return self.int >> 80 & 65535

    @property
    def time_hi_version(self):
        return self.int >> 64 & 65535

    @property
    def clock_seq_hi_variant(self):
        return self.int >> 56 & 255

    @property
    def clock_seq_low(self):
        return self.int >> 48 & 255

    @property
    def time(self):
        return (self.time_hi_version & 4095) << 48 | self.time_mid << 32 | self.time_low

    @property
    def clock_seq(self):
        return (self.clock_seq_hi_variant & 63) << 8 | self.clock_seq_low

    @property
    def node(self):
        return self.int & 281474976710655

    @property
    def hex(self):
        return '%032x' % self.int

    @property
    def urn(self):
        return 'urn:uuid:' + str(self)

    @property
    def variant(self):
        if not self.int & 9223372036854775808:
            return RESERVED_NCS
        else:
            if not self.int & 4611686018427387904:
                return RFC_4122
            if not self.int & 2305843009213693952:
                return RESERVED_MICROSOFT
            return RESERVED_FUTURE

    @property
    def version(self):
        if self.variant == RFC_4122:
            return int(self.int >> 76 & 15)


def _popen(command, *args):
    import os, shutil, subprocess
    executable = shutil.which(command)
    if executable is None:
        path = os.pathsep.join(('/sbin', '/usr/sbin'))
        executable = shutil.which(command, path=path)
        if executable is None:
            return
    env = dict(os.environ)
    env['LC_ALL'] = 'C'
    proc = subprocess.Popen(((executable,) + args), stdout=(subprocess.PIPE),
      stderr=(subprocess.DEVNULL),
      env=env)
    return proc


def _find_mac(command, args, hw_identifiers, get_index):
    try:
        proc = _popen(command, *args.split())
        if not proc:
            return
        with proc:
            for line in proc.stdout:
                words = line.lower().rstrip().split()
                for i in range(len(words)):
                    if words[i] in hw_identifiers:
                        try:
                            word = words[get_index(i)]
                            mac = int(word.replace(b':', b''), 16)
                            if mac:
                                return mac
                        except (ValueError, IndexError):
                            pass

    except OSError:
        pass


def _ifconfig_getnode():
    """Get the hardware address on Unix by running ifconfig."""
    for args in ('', '-a', '-av'):
        mac = _find_mac('ifconfig', args, [b'hwaddr', b'ether'], lambda i: i + 1)
        if mac:
            return mac


def _ip_getnode():
    """Get the hardware address on Unix by running ip."""
    mac = _find_mac('ip', 'link list', [b'link/ether'], lambda i: i + 1)
    if mac:
        return mac


def _arp_getnode():
    """Get the hardware address on Unix by running arp."""
    import os, socket
    try:
        ip_addr = socket.gethostbyname(socket.gethostname())
    except OSError:
        return
    else:
        return _find_mac('arp', '-an', [os.fsencode(ip_addr)], lambda i: -1)


def _lanscan_getnode():
    """Get the hardware address on Unix by running lanscan."""
    return _find_mac('lanscan', '-ai', [b'lan0'], lambda i: 0)


def _netstat_getnode():
    """Get the hardware address on Unix by running netstat."""
    try:
        proc = _popen('netstat', '-ia')
        if not proc:
            return
        with proc:
            words = proc.stdout.readline().rstrip().split()
            try:
                i = words.index(b'Address')
            except ValueError:
                return
            else:
                for line in proc.stdout:
                    try:
                        words = line.rstrip().split()
                        word = words[i]
                        if len(word) == 17:
                            if word.count(b':') == 5:
                                mac = int(word.replace(b':', b''), 16)
                                if mac:
                                    return mac
                    except (ValueError, IndexError):
                        pass

    except OSError:
        pass


def _ipconfig_getnode():
    """Get the hardware address on Windows by running ipconfig.exe."""
    import os, re
    dirs = [
     '', 'c:\\windows\\system32', 'c:\\winnt\\system32']
    try:
        import ctypes
        buffer = ctypes.create_string_buffer(300)
        ctypes.windll.kernel32.GetSystemDirectoryA(buffer, 300)
        dirs.insert(0, buffer.value.decode('mbcs'))
    except:
        pass

    for dir in dirs:
        try:
            pipe = os.popen(os.path.join(dir, 'ipconfig') + ' /all')
        except OSError:
            continue

        with pipe:
            for line in pipe:
                value = line.split(':')[(-1)].strip().lower()
                if re.match('([0-9a-f][0-9a-f]-){5}[0-9a-f][0-9a-f]', value):
                    return int(value.replace('-', ''), 16)


def _netbios_getnode():
    """Get the hardware address on Windows using NetBIOS calls.
    See http://support.microsoft.com/kb/118623 for details."""
    import win32wnet, netbios
    ncb = netbios.NCB()
    ncb.Command = netbios.NCBENUM
    ncb.Buffer = adapters = netbios.LANA_ENUM()
    adapters._pack()
    if win32wnet.Netbios(ncb) != 0:
        return
    adapters._unpack()
    for i in range(adapters.length):
        ncb.Reset()
        ncb.Command = netbios.NCBRESET
        ncb.Lana_num = ord(adapters.lana[i])
        if win32wnet.Netbios(ncb) != 0:
            pass
        else:
            ncb.Reset()
            ncb.Command = netbios.NCBASTAT
            ncb.Lana_num = ord(adapters.lana[i])
            ncb.Callname = '*'.ljust(16)
            ncb.Buffer = status = netbios.ADAPTER_STATUS()
            if win32wnet.Netbios(ncb) != 0:
                pass
            else:
                status._unpack()
                bytes = status.adapter_address[:6]
                if len(bytes) != 6:
                    continue
                return int.from_bytes(bytes, 'big')


_uuid_generate_time = _UuidCreate = None
try:
    import ctypes, ctypes.util, sys
    _libnames = [
     'uuid']
    if not sys.platform.startswith('win'):
        _libnames.append('c')
    for libname in _libnames:
        try:
            lib = ctypes.CDLL(ctypes.util.find_library(libname))
        except Exception:
            continue

        if hasattr(lib, 'uuid_generate_time'):
            _uuid_generate_time = lib.uuid_generate_time
            break

    del _libnames
    if sys.platform == 'darwin':
        if int(os.uname().release.split('.')[0]) >= 9:
            _uuid_generate_time = None
    try:
        lib = ctypes.windll.rpcrt4
    except:
        lib = None

    _UuidCreate = getattr(lib, 'UuidCreateSequential', getattr(lib, 'UuidCreate', None))
except:
    pass

def _unixdll_getnode():
    """Get the hardware address on Unix using ctypes."""
    _buffer = ctypes.create_string_buffer(16)
    _uuid_generate_time(_buffer)
    return UUID(bytes=(bytes_(_buffer.raw))).node


def _windll_getnode():
    """Get the hardware address on Windows using ctypes."""
    _buffer = ctypes.create_string_buffer(16)
    if _UuidCreate(_buffer) == 0:
        return UUID(bytes=(bytes_(_buffer.raw))).node


def _random_getnode():
    """Get a random node ID, with eighth bit set as suggested by RFC 4122."""
    import random
    return random.getrandbits(48) | 1099511627776


_node = None

def getnode():
    """Get the hardware address as a 48-bit positive integer.

    The first time this runs, it may launch a separate program, which could
    be quite slow.  If all attempts to obtain the hardware address fail, we
    choose a random 48-bit number with its eighth bit set to 1 as recommended
    in RFC 4122.
    """
    global _node
    if _node is not None:
        return _node
    else:
        import sys
        if sys.platform == 'win32':
            getters = [
             _windll_getnode, _netbios_getnode, _ipconfig_getnode]
        else:
            getters = [
             _unixdll_getnode, _ifconfig_getnode, _ip_getnode,
             _arp_getnode, _lanscan_getnode, _netstat_getnode]
    for getter in getters + [_random_getnode]:
        try:
            _node = getter()
        except:
            continue

        if _node is not None:
            return _node


_last_timestamp = None

def uuid1(node=None, clock_seq=None):
    """Generate a UUID from a host ID, sequence number, and the current time.
    If 'node' is not given, getnode() is used to obtain the hardware
    address.  If 'clock_seq' is given, it is used as the sequence number;
    otherwise a random 14-bit sequence number is chosen."""
    global _last_timestamp
    if _uuid_generate_time and node is clock_seq is None:
        _buffer = ctypes.create_string_buffer(16)
        _uuid_generate_time(_buffer)
        return UUID(bytes=(bytes_(_buffer.raw)))
    else:
        import time
        nanoseconds = int(time.time() * 1000000000.0)
        timestamp = int(nanoseconds / 100) + 122192928000000000
        if _last_timestamp is not None:
            if timestamp <= _last_timestamp:
                timestamp = _last_timestamp + 1
        _last_timestamp = timestamp
        if clock_seq is None:
            import random
            clock_seq = random.getrandbits(14)
        time_low = timestamp & 4294967295
        time_mid = timestamp >> 32 & 65535
        time_hi_version = timestamp >> 48 & 4095
        clock_seq_low = clock_seq & 255
        clock_seq_hi_variant = clock_seq >> 8 & 63
        if node is None:
            node = getnode()
        return UUID(fields=(time_low, time_mid, time_hi_version,
         clock_seq_hi_variant, clock_seq_low, node),
          version=1)


def uuid3(namespace, name):
    """Generate a UUID from the MD5 hash of a namespace UUID and a name."""
    from hashlib import md5
    hash = md5(namespace.bytes + bytes(name, 'utf-8')).digest()
    return UUID(bytes=(hash[:16]), version=3)


def uuid4():
    """Generate a random UUID."""
    return UUID(bytes=(os.urandom(16)), version=4)


def uuid5(namespace, name):
    """Generate a UUID from the SHA-1 hash of a namespace UUID and a name."""
    from hashlib import sha1
    hash = sha1(namespace.bytes + bytes(name, 'utf-8')).digest()
    return UUID(bytes=(hash[:16]), version=5)


NAMESPACE_DNS = UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')
NAMESPACE_URL = UUID('6ba7b811-9dad-11d1-80b4-00c04fd430c8')
NAMESPACE_OID = UUID('6ba7b812-9dad-11d1-80b4-00c04fd430c8')
NAMESPACE_X500 = UUID('6ba7b814-9dad-11d1-80b4-00c04fd430c8')