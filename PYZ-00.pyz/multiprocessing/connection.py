# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: multiprocessing\connection.py
__all__ = [
 'Client', 'Listener', 'Pipe', 'wait']
import io, os, sys, socket, struct, time, tempfile, itertools, _multiprocessing
from . import util
from . import AuthenticationError, BufferTooShort
from .context import reduction
_ForkingPickler = reduction.ForkingPickler
try:
    import _winapi
    from _winapi import WAIT_OBJECT_0, WAIT_ABANDONED_0, WAIT_TIMEOUT, INFINITE
except ImportError:
    if sys.platform == 'win32':
        raise
    _winapi = None

BUFSIZE = 8192
CONNECTION_TIMEOUT = 20.0
_mmap_counter = itertools.count()
default_family = 'AF_INET'
families = ['AF_INET']
if hasattr(socket, 'AF_UNIX'):
    default_family = 'AF_UNIX'
    families += ['AF_UNIX']
if sys.platform == 'win32':
    default_family = 'AF_PIPE'
    families += ['AF_PIPE']

def _init_timeout(timeout=CONNECTION_TIMEOUT):
    return time.time() + timeout


def _check_timeout(t):
    return time.time() > t


def arbitrary_address(family):
    """
    Return an arbitrary free address for the given family
    """
    if family == 'AF_INET':
        return ('localhost', 0)
    else:
        if family == 'AF_UNIX':
            return tempfile.mktemp(prefix='listener-', dir=(util.get_temp_dir()))
        if family == 'AF_PIPE':
            return tempfile.mktemp(prefix=('\\\\.\\pipe\\pyc-%d-%d-' % (
             os.getpid(), next(_mmap_counter))),
              dir='')
    raise ValueError('unrecognized family')


def _validate_family(family):
    """
    Checks if the family is valid for the current environment.
    """
    if sys.platform != 'win32':
        if family == 'AF_PIPE':
            raise ValueError('Family %s is not recognized.' % family)
    if sys.platform == 'win32':
        if family == 'AF_UNIX':
            if not hasattr(socket, family):
                raise ValueError('Family %s is not recognized.' % family)


def address_type(address):
    """
    Return the types of the address

    This can be 'AF_INET', 'AF_UNIX', or 'AF_PIPE'
    """
    if type(address) == tuple:
        return 'AF_INET'
    else:
        if type(address) is str:
            if address.startswith('\\\\'):
                return 'AF_PIPE'
        if type(address) is str:
            return 'AF_UNIX'
    raise ValueError('address type of %r unrecognized' % address)


class _ConnectionBase:
    _handle = None

    def __init__(self, handle, readable=True, writable=True):
        handle = handle.__index__()
        if handle < 0:
            raise ValueError('invalid handle')
        if not readable:
            if not writable:
                raise ValueError('at least one of `readable` and `writable` must be True')
        self._handle = handle
        self._readable = readable
        self._writable = writable

    def __del__(self):
        if self._handle is not None:
            self._close()

    def _check_closed(self):
        if self._handle is None:
            raise OSError('handle is closed')

    def _check_readable(self):
        if not self._readable:
            raise OSError('connection is write-only')

    def _check_writable(self):
        if not self._writable:
            raise OSError('connection is read-only')

    def _bad_message_length(self):
        if self._writable:
            self._readable = False
        else:
            self.close()
        raise OSError('bad message length')

    @property
    def closed(self):
        """True if the connection is closed"""
        return self._handle is None

    @property
    def readable(self):
        """True if the connection is readable"""
        return self._readable

    @property
    def writable(self):
        """True if the connection is writable"""
        return self._writable

    def fileno(self):
        """File descriptor or handle of the connection"""
        self._check_closed()
        return self._handle

    def close(self):
        """Close the connection"""
        if self._handle is not None:
            try:
                self._close()
            finally:
                self._handle = None

    def send_bytes(self, buf, offset=0, size=None):
        """Send the bytes data from a bytes-like object"""
        self._check_closed()
        self._check_writable()
        m = memoryview(buf)
        if m.itemsize > 1:
            m = memoryview(bytes(m))
        n = len(m)
        if offset < 0:
            raise ValueError('offset is negative')
        if n < offset:
            raise ValueError('buffer length < offset')
        if size is None:
            size = n - offset
        else:
            if size < 0:
                raise ValueError('size is negative')
            else:
                if offset + size > n:
                    raise ValueError('buffer length < offset + size')
        self._send_bytes(m[offset:offset + size])

    def send(self, obj):
        """Send a (picklable) object"""
        self._check_closed()
        self._check_writable()
        self._send_bytes(_ForkingPickler.dumps(obj))

    def recv_bytes(self, maxlength=None):
        """
        Receive bytes data as a bytes object.
        """
        self._check_closed()
        self._check_readable()
        if maxlength is not None:
            if maxlength < 0:
                raise ValueError('negative maxlength')
        buf = self._recv_bytes(maxlength)
        if buf is None:
            self._bad_message_length()
        return buf.getvalue()

    def recv_bytes_into(self, buf, offset=0):
        """
        Receive bytes data into a writeable bytes-like object.
        Return the number of bytes read.
        """
        self._check_closed()
        self._check_readable()
        with memoryview(buf) as (m):
            itemsize = m.itemsize
            bytesize = itemsize * len(m)
            if offset < 0:
                raise ValueError('negative offset')
            else:
                if offset > bytesize:
                    raise ValueError('offset too large')
            result = self._recv_bytes()
            size = result.tell()
            if bytesize < offset + size:
                raise BufferTooShort(result.getvalue())
            result.seek(0)
            result.readinto(m[offset // itemsize:(offset + size) // itemsize])
            return size

    def recv(self):
        """Receive a (picklable) object"""
        self._check_closed()
        self._check_readable()
        buf = self._recv_bytes()
        return _ForkingPickler.loads(buf.getbuffer())

    def poll(self, timeout=0.0):
        """Whether there is any input available to be read"""
        self._check_closed()
        self._check_readable()
        return self._poll(timeout)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()


if _winapi:

    class PipeConnection(_ConnectionBase):
        __doc__ = '\n        Connection class based on a Windows named pipe.\n        Overlapped I/O is used, so the handles must have been created\n        with FILE_FLAG_OVERLAPPED.\n        '
        _got_empty_message = False

        def _close(self, _CloseHandle=_winapi.CloseHandle):
            _CloseHandle(self._handle)

        def _send_bytes(self, buf):
            ov, err = _winapi.WriteFile((self._handle), buf, overlapped=True)
            try:
                try:
                    if err == _winapi.ERROR_IO_PENDING:
                        waitres = _winapi.WaitForMultipleObjects([
                         ov.event], False, INFINITE)
                        if not waitres == WAIT_OBJECT_0:
                            raise AssertionError
                except:
                    ov.cancel()
                    raise

            finally:
                nwritten, err = ov.GetOverlappedResult(True)

            if not err == 0:
                raise AssertionError
            elif not nwritten == len(buf):
                raise AssertionError

        def _recv_bytes(self, maxsize=None):
            if self._got_empty_message:
                self._got_empty_message = False
                return io.BytesIO()
            bsize = 128 if maxsize is None else min(maxsize, 128)
            try:
                ov, err = _winapi.ReadFile((self._handle), bsize, overlapped=True)
                try:
                    try:
                        if err == _winapi.ERROR_IO_PENDING:
                            waitres = _winapi.WaitForMultipleObjects([
                             ov.event], False, INFINITE)
                            if not waitres == WAIT_OBJECT_0:
                                raise AssertionError
                    except:
                        ov.cancel()
                        raise

                finally:
                    nread, err = ov.GetOverlappedResult(True)
                    if err == 0:
                        f = io.BytesIO()
                        f.write(ov.getbuffer())
                        return f
                    if err == _winapi.ERROR_MORE_DATA:
                        return self._get_more_data(ov, maxsize)

            except OSError as e:
                if e.winerror == _winapi.ERROR_BROKEN_PIPE:
                    raise EOFError
                else:
                    raise

            raise RuntimeError("shouldn't get here; expected KeyboardInterrupt")

        def _poll(self, timeout):
            if self._got_empty_message or _winapi.PeekNamedPipe(self._handle)[0] != 0:
                return True
            else:
                return bool(wait([self], timeout))

        def _get_more_data(self, ov, maxsize):
            buf = ov.getbuffer()
            f = io.BytesIO()
            f.write(buf)
            left = _winapi.PeekNamedPipe(self._handle)[1]
            if not left > 0:
                raise AssertionError
            else:
                if maxsize is not None:
                    if len(buf) + left > maxsize:
                        self._bad_message_length()
                else:
                    ov, err = _winapi.ReadFile((self._handle), left, overlapped=True)
                    rbytes, err = ov.GetOverlappedResult(True)
                    assert err == 0
                assert rbytes == left
            f.write(ov.getbuffer())
            return f


else:

    class Connection(_ConnectionBase):
        __doc__ = '\n    Connection class based on an arbitrary file descriptor (Unix only), or\n    a socket handle (Windows).\n    '
        if _winapi:

            def _close(self, _close=_multiprocessing.closesocket):
                _close(self._handle)

            _write = _multiprocessing.send
            _read = _multiprocessing.recv
        else:

            def _close(self, _close=os.close):
                _close(self._handle)

            _write = os.write
            _read = os.read

        def _send(self, buf, write=_write):
            remaining = len(buf)
            while True:
                n = write(self._handle, buf)
                remaining -= n
                if remaining == 0:
                    break
                buf = buf[n:]

        def _recv(self, size, read=_read):
            buf = io.BytesIO()
            handle = self._handle
            remaining = size
            while remaining > 0:
                chunk = read(handle, remaining)
                n = len(chunk)
                if n == 0:
                    if remaining == size:
                        raise EOFError
                    else:
                        raise OSError('got end of file during message')
                buf.write(chunk)
                remaining -= n

            return buf

        def _send_bytes(self, buf):
            n = len(buf)
            header = struct.pack('!i', n)
            if n > 16384:
                self._send(header)
                self._send(buf)
            else:
                self._send(header + buf)

        def _recv_bytes(self, maxsize=None):
            buf = self._recv(4)
            size, = struct.unpack('!i', buf.getvalue())
            if maxsize is not None:
                if size > maxsize:
                    return
            return self._recv(size)

        def _poll(self, timeout):
            r = wait([self], timeout)
            return bool(r)


    class Listener(object):
        __doc__ = "\n    Returns a listener object.\n\n    This is a wrapper for a bound socket which is 'listening' for\n    connections, or for a Windows named pipe.\n    "

        def __init__(self, address=None, family=None, backlog=1, authkey=None):
            family = family or address and address_type(address) or default_family
            address = address or arbitrary_address(family)
            _validate_family(family)
            if family == 'AF_PIPE':
                self._listener = PipeListener(address, backlog)
            else:
                self._listener = SocketListener(address, family, backlog)
            if authkey is not None:
                if not isinstance(authkey, bytes):
                    raise TypeError('authkey should be a byte string')
            self._authkey = authkey

        def accept(self):
            """
        Accept a connection on the bound socket or named pipe of `self`.

        Returns a `Connection` object.
        """
            if self._listener is None:
                raise OSError('listener is closed')
            c = self._listener.accept()
            if self._authkey:
                deliver_challenge(c, self._authkey)
                answer_challenge(c, self._authkey)
            return c

        def close(self):
            """
        Close the bound socket or named pipe of `self`.
        """
            listener = self._listener
            if listener is not None:
                self._listener = None
                listener.close()

        address = property(lambda self: self._listener._address)
        last_accepted = property(lambda self: self._listener._last_accepted)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, exc_tb):
            self.close()


    def Client(address, family=None, authkey=None):
        """
    Returns a connection to the address of a `Listener`
    """
        family = family or address_type(address)
        _validate_family(family)
        if family == 'AF_PIPE':
            c = PipeClient(address)
        else:
            c = SocketClient(address)
        if authkey is not None:
            if not isinstance(authkey, bytes):
                raise TypeError('authkey should be a byte string')
        if authkey is not None:
            answer_challenge(c, authkey)
            deliver_challenge(c, authkey)
        return c


    if sys.platform != 'win32':

        def Pipe(duplex=True):
            """
        Returns pair of connection objects at either end of a pipe
        """
            if duplex:
                s1, s2 = socket.socketpair()
                s1.setblocking(True)
                s2.setblocking(True)
                c1 = Connection(s1.detach())
                c2 = Connection(s2.detach())
            else:
                fd1, fd2 = os.pipe()
                c1 = Connection(fd1, writable=False)
                c2 = Connection(fd2, readable=False)
            return (c1, c2)


    else:

        def Pipe(duplex=True):
            """
        Returns pair of connection objects at either end of a pipe
        """
            address = arbitrary_address('AF_PIPE')
            if duplex:
                openmode = _winapi.PIPE_ACCESS_DUPLEX
                access = _winapi.GENERIC_READ | _winapi.GENERIC_WRITE
                obsize, ibsize = BUFSIZE, BUFSIZE
            else:
                openmode = _winapi.PIPE_ACCESS_INBOUND
                access = _winapi.GENERIC_WRITE
                obsize, ibsize = 0, BUFSIZE
            h1 = _winapi.CreateNamedPipe(address, openmode | _winapi.FILE_FLAG_OVERLAPPED | _winapi.FILE_FLAG_FIRST_PIPE_INSTANCE, _winapi.PIPE_TYPE_MESSAGE | _winapi.PIPE_READMODE_MESSAGE | _winapi.PIPE_WAIT, 1, obsize, ibsize, _winapi.NMPWAIT_WAIT_FOREVER, _winapi.NULL)
            h2 = _winapi.CreateFile(address, access, 0, _winapi.NULL, _winapi.OPEN_EXISTING, _winapi.FILE_FLAG_OVERLAPPED, _winapi.NULL)
            _winapi.SetNamedPipeHandleState(h2, _winapi.PIPE_READMODE_MESSAGE, None, None)
            overlapped = _winapi.ConnectNamedPipe(h1, overlapped=True)
            _, err = overlapped.GetOverlappedResult(True)
            assert err == 0
            c1 = PipeConnection(h1, writable=duplex)
            c2 = PipeConnection(h2, readable=duplex)
            return (
             c1, c2)


    class SocketListener(object):
        __doc__ = '\n    Representation of a socket which is bound to an address and listening\n    '

        def __init__(self, address, family, backlog=1):
            self._socket = socket.socket(getattr(socket, family))
            try:
                if os.name == 'posix':
                    self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self._socket.setblocking(True)
                self._socket.bind(address)
                self._socket.listen(backlog)
                self._address = self._socket.getsockname()
            except OSError:
                self._socket.close()
                raise

            self._family = family
            self._last_accepted = None
            if family == 'AF_UNIX':
                self._unlink = util.Finalize(self,
                  (os.unlink), args=(address,), exitpriority=0)
            else:
                self._unlink = None

        def accept(self):
            s, self._last_accepted = self._socket.accept()
            s.setblocking(True)
            return Connection(s.detach())

        def close(self):
            try:
                self._socket.close()
            finally:
                unlink = self._unlink
                if unlink is not None:
                    self._unlink = None
                    unlink()


    def SocketClient(address):
        """
    Return a connection object connected to the socket given by `address`
    """
        family = address_type(address)
        with socket.socket(getattr(socket, family)) as (s):
            s.setblocking(True)
            s.connect(address)
            return Connection(s.detach())


    if sys.platform == 'win32':

        class PipeListener(object):
            __doc__ = '\n        Representation of a named pipe\n        '

            def __init__(self, address, backlog=None):
                self._address = address
                self._handle_queue = [self._new_handle(first=True)]
                self._last_accepted = None
                util.sub_debug('listener created with address=%r', self._address)
                self.close = util.Finalize(self,
                  (PipeListener._finalize_pipe_listener), args=(
                 self._handle_queue, self._address),
                  exitpriority=0)

            def _new_handle(self, first=False):
                flags = _winapi.PIPE_ACCESS_DUPLEX | _winapi.FILE_FLAG_OVERLAPPED
                if first:
                    flags |= _winapi.FILE_FLAG_FIRST_PIPE_INSTANCE
                return _winapi.CreateNamedPipe(self._address, flags, _winapi.PIPE_TYPE_MESSAGE | _winapi.PIPE_READMODE_MESSAGE | _winapi.PIPE_WAIT, _winapi.PIPE_UNLIMITED_INSTANCES, BUFSIZE, BUFSIZE, _winapi.NMPWAIT_WAIT_FOREVER, _winapi.NULL)

            def accept(self):
                self._handle_queue.append(self._new_handle())
                handle = self._handle_queue.pop(0)
                try:
                    ov = _winapi.ConnectNamedPipe(handle, overlapped=True)
                except OSError as e:
                    if e.winerror != _winapi.ERROR_NO_DATA:
                        raise
                else:
                    try:
                        try:
                            res = _winapi.WaitForMultipleObjects([
                             ov.event], False, INFINITE)
                        except:
                            ov.cancel()
                            _winapi.CloseHandle(handle)
                            raise

                    finally:
                        _, err = ov.GetOverlappedResult(True)
                        assert err == 0

                return PipeConnection(handle)

            @staticmethod
            def _finalize_pipe_listener(queue, address):
                util.sub_debug('closing listener with address=%r', address)
                for handle in queue:
                    _winapi.CloseHandle(handle)


        def PipeClient(address):
            """
        Return a connection object connected to the pipe given by `address`
        """
            t = _init_timeout()
            while 1:
                try:
                    _winapi.WaitNamedPipe(address, 1000)
                    h = _winapi.CreateFile(address, _winapi.GENERIC_READ | _winapi.GENERIC_WRITE, 0, _winapi.NULL, _winapi.OPEN_EXISTING, _winapi.FILE_FLAG_OVERLAPPED, _winapi.NULL)
                except OSError as e:
                    if e.winerror not in (_winapi.ERROR_SEM_TIMEOUT,
                     _winapi.ERROR_PIPE_BUSY) or _check_timeout(t):
                        raise
                else:
                    break
            else:
                raise

            _winapi.SetNamedPipeHandleState(h, _winapi.PIPE_READMODE_MESSAGE, None, None)
            return PipeConnection(h)


    MESSAGE_LENGTH = 20
    CHALLENGE = b'#CHALLENGE#'
    WELCOME = b'#WELCOME#'
    FAILURE = b'#FAILURE#'

    def deliver_challenge(connection, authkey):
        import hmac
        if not isinstance(authkey, bytes):
            raise AssertionError
        else:
            message = os.urandom(MESSAGE_LENGTH)
            connection.send_bytes(CHALLENGE + message)
            digest = hmac.new(authkey, message, 'md5').digest()
            response = connection.recv_bytes(256)
            if response == digest:
                connection.send_bytes(WELCOME)
            else:
                connection.send_bytes(FAILURE)
                raise AuthenticationError('digest received was wrong')


    def answer_challenge(connection, authkey):
        import hmac
        if not isinstance(authkey, bytes):
            raise AssertionError
        else:
            message = connection.recv_bytes(256)
            assert message[:len(CHALLENGE)] == CHALLENGE, 'message = %r' % message
        message = message[len(CHALLENGE):]
        digest = hmac.new(authkey, message, 'md5').digest()
        connection.send_bytes(digest)
        response = connection.recv_bytes(256)
        if response != WELCOME:
            raise AuthenticationError('digest sent was rejected')


    class ConnectionWrapper(object):

        def __init__(self, conn, dumps, loads):
            self._conn = conn
            self._dumps = dumps
            self._loads = loads
            for attr in ('fileno', 'close', 'poll', 'recv_bytes', 'send_bytes'):
                obj = getattr(conn, attr)
                setattr(self, attr, obj)

        def send(self, obj):
            s = self._dumps(obj)
            self._conn.send_bytes(s)

        def recv(self):
            s = self._conn.recv_bytes()
            return self._loads(s)


    def _xml_dumps(obj):
        return xmlrpclib.dumps((obj,), None, None, None, 1).encode('utf-8')


    def _xml_loads(s):
        (obj,), method = xmlrpclib.loads(s.decode('utf-8'))
        return obj


    class XmlListener(Listener):

        def accept(self):
            global xmlrpclib
            import xmlrpc.client as xmlrpclib
            obj = Listener.accept(self)
            return ConnectionWrapper(obj, _xml_dumps, _xml_loads)


    def XmlClient(*args, **kwds):
        global xmlrpclib
        import xmlrpc.client as xmlrpclib
        return ConnectionWrapper(Client(*args, **kwds), _xml_dumps, _xml_loads)


    if sys.platform == 'win32':

        def _exhaustive_wait(handles, timeout):
            L = list(handles)
            ready = []
            while L:
                res = _winapi.WaitForMultipleObjects(L, False, timeout)
                if res == WAIT_TIMEOUT:
                    break
                else:
                    if WAIT_OBJECT_0 <= res < WAIT_OBJECT_0 + len(L):
                        res -= WAIT_OBJECT_0
                    else:
                        if WAIT_ABANDONED_0 <= res < WAIT_ABANDONED_0 + len(L):
                            res -= WAIT_ABANDONED_0
                        else:
                            raise RuntimeError('Should not get here')
                ready.append(L[res])
                L = L[res + 1:]
                timeout = 0

            return ready


        _ready_errors = {
         _winapi.ERROR_BROKEN_PIPE, _winapi.ERROR_NETNAME_DELETED}

        def wait(object_list, timeout=None):
            """
        Wait till an object in object_list is ready/readable.

        Returns list of those objects in object_list which are ready/readable.
        """
            if timeout is None:
                timeout = INFINITE
            else:
                if timeout < 0:
                    timeout = 0
                else:
                    timeout = int(timeout * 1000 + 0.5)
            object_list = list(object_list)
            waithandle_to_obj = {}
            ov_list = []
            ready_objects = set()
            ready_handles = set()
            try:
                for o in object_list:
                    try:
                        fileno = getattr(o, 'fileno')
                    except AttributeError:
                        waithandle_to_obj[o.__index__()] = o
                    else:
                        try:
                            ov, err = _winapi.ReadFile(fileno(), 0, True)
                        except OSError as e:
                            ov, err = None, e.winerror
                            if err not in _ready_errors:
                                raise

                    if err == _winapi.ERROR_IO_PENDING:
                        ov_list.append(ov)
                        waithandle_to_obj[ov.event] = o
                    else:
                        if ov:
                            if sys.getwindowsversion()[:2] >= (6, 2):
                                try:
                                    _, err = ov.GetOverlappedResult(False)
                                except OSError as e:
                                    err = e.winerror

                                if not err:
                                    if hasattr(o, '_got_empty_message'):
                                        o._got_empty_message = True
                        ready_objects.add(o)
                        timeout = 0

                ready_handles = _exhaustive_wait(waithandle_to_obj.keys(), timeout)
            finally:
                for ov in ov_list:
                    ov.cancel()

                for ov in ov_list:
                    try:
                        _, err = ov.GetOverlappedResult(True)
                    except OSError as e:
                        err = e.winerror
                        if err not in _ready_errors:
                            raise

                    if err != _winapi.ERROR_OPERATION_ABORTED:
                        o = waithandle_to_obj[ov.event]
                        ready_objects.add(o)
                        if err == 0 and hasattr(o, '_got_empty_message'):
                            o._got_empty_message = True

            ready_objects.update(waithandle_to_obj[h] for h in ready_handles)
            return [o for o in object_list if o in ready_objects]


    else:
        import selectors
        if hasattr(selectors, 'PollSelector'):
            _WaitSelector = selectors.PollSelector
        else:
            _WaitSelector = selectors.SelectSelector

        def wait(object_list, timeout=None):
            """
        Wait till an object in object_list is ready/readable.

        Returns list of those objects in object_list which are ready/readable.
        """
            with _WaitSelector() as (selector):
                for obj in object_list:
                    selector.register(obj, selectors.EVENT_READ)

                if timeout is not None:
                    deadline = time.time() + timeout
                while 1:
                    ready = selector.select(timeout)
                    if ready:
                        return [key.fileobj for key, events in ready]
                    if timeout is not None:
                        timeout = deadline - time.time()
                        if timeout < 0:
                            return ready


    if sys.platform == 'win32':

        def reduce_connection(conn):
            handle = conn.fileno()
            with socket.fromfd(handle, socket.AF_INET, socket.SOCK_STREAM) as (s):
                from . import resource_sharer
                ds = resource_sharer.DupSocket(s)
                return (rebuild_connection, (ds, conn.readable, conn.writable))


        def rebuild_connection(ds, readable, writable):
            sock = ds.detach()
            return Connection(sock.detach(), readable, writable)


        reduction.register(Connection, reduce_connection)

        def reduce_pipe_connection(conn):
            access = (_winapi.FILE_GENERIC_READ if conn.readable else 0) | (_winapi.FILE_GENERIC_WRITE if conn.writable else 0)
            dh = reduction.DupHandle(conn.fileno(), access)
            return (rebuild_pipe_connection, (dh, conn.readable, conn.writable))


        def rebuild_pipe_connection(dh, readable, writable):
            handle = dh.detach()
            return PipeConnection(handle, readable, writable)


        reduction.register(PipeConnection, reduce_pipe_connection)
    else:

        def reduce_connection(conn):
            df = reduction.DupFd(conn.fileno())
            return (rebuild_connection, (df, conn.readable, conn.writable))


        def rebuild_connection(df, readable, writable):
            fd = df.detach()
            return Connection(fd, readable, writable)


        reduction.register(Connection, reduce_connection)