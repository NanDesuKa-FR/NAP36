# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: webbrowser.py
"""Interfaces for launching and remotely controlling Web browsers."""
import os, shlex, shutil, sys, subprocess
__all__ = [
 'Error', 'open', 'open_new', 'open_new_tab', 'get', 'register']

class Error(Exception):
    pass


_browsers = {}
_tryorder = []

def register(name, klass, instance=None, update_tryorder=1):
    """Register a browser connector and, optionally, connection."""
    _browsers[name.lower()] = [
     klass, instance]
    if update_tryorder > 0:
        _tryorder.append(name)
    elif update_tryorder < 0:
        _tryorder.insert(0, name)


def get(using=None):
    """Return a browser launcher instance appropriate for the environment."""
    if using is not None:
        alternatives = [
         using]
    else:
        alternatives = _tryorder
    for browser in alternatives:
        if '%s' in browser:
            browser = shlex.split(browser)
            if browser[(-1)] == '&':
                return BackgroundBrowser(browser[:-1])
            else:
                return GenericBrowser(browser)
        else:
            try:
                command = _browsers[browser.lower()]
            except KeyError:
                command = _synthesize(browser)

            if command[1] is not None:
                return command[1]
            if command[0] is not None:
                return command[0]()

    raise Error('could not locate runnable browser')


def open(url, new=0, autoraise=True):
    for name in _tryorder:
        browser = get(name)
        if browser.open(url, new, autoraise):
            return True

    return False


def open_new(url):
    return open(url, 1)


def open_new_tab(url):
    return open(url, 2)


def _synthesize(browser, update_tryorder=1):
    """Attempt to synthesize a controller base on existing controllers.

    This is useful to create a controller when a user specifies a path to
    an entry in the BROWSER environment variable -- we can copy a general
    controller to operate using a specific installation of the desired
    browser in this way.

    If we can't create a controller in this way, or if there is no
    executable for the requested browser, return [None, None].

    """
    cmd = browser.split()[0]
    if not shutil.which(cmd):
        return [
         None, None]
    name = os.path.basename(cmd)
    try:
        command = _browsers[name.lower()]
    except KeyError:
        return [
         None, None]
    else:
        controller = command[1]
        if controller and name.lower() == controller.basename:
            import copy
            controller = copy.copy(controller)
            controller.name = browser
            controller.basename = os.path.basename(browser)
            register(browser, None, controller, update_tryorder)
            return [
             None, controller]
        else:
            return [
             None, None]


class BaseBrowser(object):
    __doc__ = 'Parent class for all browsers. Do not use directly.'
    args = [
     '%s']

    def __init__(self, name=''):
        self.name = name
        self.basename = name

    def open(self, url, new=0, autoraise=True):
        raise NotImplementedError

    def open_new(self, url):
        return self.open(url, 1)

    def open_new_tab(self, url):
        return self.open(url, 2)


class GenericBrowser(BaseBrowser):
    __doc__ = 'Class for all browsers started with a command\n       and without remote functionality.'

    def __init__(self, name):
        if isinstance(name, str):
            self.name = name
            self.args = ['%s']
        else:
            self.name = name[0]
            self.args = name[1:]
        self.basename = os.path.basename(self.name)

    def open(self, url, new=0, autoraise=True):
        cmdline = [
         self.name] + [arg.replace('%s', url) for arg in self.args]
        try:
            if sys.platform[:3] == 'win':
                p = subprocess.Popen(cmdline)
            else:
                p = subprocess.Popen(cmdline, close_fds=True)
            return not p.wait()
        except OSError:
            return False


class BackgroundBrowser(GenericBrowser):
    __doc__ = 'Class for all browsers which are to be started in the\n       background.'

    def open(self, url, new=0, autoraise=True):
        cmdline = [
         self.name] + [arg.replace('%s', url) for arg in self.args]
        try:
            if sys.platform[:3] == 'win':
                p = subprocess.Popen(cmdline)
            else:
                p = subprocess.Popen(cmdline, close_fds=True, start_new_session=True)
            return p.poll() is None
        except OSError:
            return False


class UnixBrowser(BaseBrowser):
    __doc__ = 'Parent class for all Unix browsers with remote functionality.'
    raise_opts = None
    background = False
    redirect_stdout = True
    remote_args = [
     '%action', '%s']
    remote_action = None
    remote_action_newwin = None
    remote_action_newtab = None

    def _invoke(self, args, remote, autoraise):
        raise_opt = []
        if remote:
            if self.raise_opts:
                autoraise = int(autoraise)
                opt = self.raise_opts[autoraise]
                if opt:
                    raise_opt = [
                     opt]
        else:
            cmdline = [
             self.name] + raise_opt + args
            if remote or self.background:
                inout = subprocess.DEVNULL
            else:
                inout = None
            p = subprocess.Popen(cmdline, close_fds=True, stdin=inout, stdout=(self.redirect_stdout and inout or None),
              stderr=inout,
              start_new_session=True)
            if remote:
                try:
                    rc = p.wait(5)
                    return not rc
                except subprocess.TimeoutExpired:
                    return True

            else:
                if self.background:
                    if p.poll() is None:
                        return True
                    else:
                        return False
                else:
                    return not p.wait()

    def open(self, url, new=0, autoraise=True):
        if new == 0:
            action = self.remote_action
        else:
            if new == 1:
                action = self.remote_action_newwin
            else:
                if new == 2:
                    if self.remote_action_newtab is None:
                        action = self.remote_action_newwin
                    else:
                        action = self.remote_action_newtab
                else:
                    raise Error("Bad 'new' parameter to open(); " + 'expected 0, 1, or 2, got %s' % new)
        args = [arg.replace('%s', url).replace('%action', action) for arg in self.remote_args]
        args = [arg for arg in args if arg]
        success = self._invoke(args, True, autoraise)
        if not success:
            args = [arg.replace('%s', url) for arg in self.args]
            return self._invoke(args, False, False)
        else:
            return True


class Mozilla(UnixBrowser):
    __doc__ = 'Launcher class for Mozilla browsers.'
    remote_args = [
     '%action', '%s']
    remote_action = ''
    remote_action_newwin = '-new-window'
    remote_action_newtab = '-new-tab'
    background = True


class Netscape(UnixBrowser):
    __doc__ = 'Launcher class for Netscape browser.'
    raise_opts = [
     '-noraise', '-raise']
    remote_args = ['-remote', 'openURL(%s%action)']
    remote_action = ''
    remote_action_newwin = ',new-window'
    remote_action_newtab = ',new-tab'
    background = True


class Galeon(UnixBrowser):
    __doc__ = 'Launcher class for Galeon/Epiphany browsers.'
    raise_opts = [
     '-noraise', '']
    remote_args = ['%action', '%s']
    remote_action = '-n'
    remote_action_newwin = '-w'
    background = True


class Chrome(UnixBrowser):
    __doc__ = 'Launcher class for Google Chrome browser.'
    remote_args = [
     '%action', '%s']
    remote_action = ''
    remote_action_newwin = '--new-window'
    remote_action_newtab = ''
    background = True


Chromium = Chrome

class Opera(UnixBrowser):
    __doc__ = 'Launcher class for Opera browser.'
    raise_opts = [
     '-noraise', '']
    remote_args = ['-remote', 'openURL(%s%action)']
    remote_action = ''
    remote_action_newwin = ',new-window'
    remote_action_newtab = ',new-page'
    background = True


class Elinks(UnixBrowser):
    __doc__ = 'Launcher class for Elinks browsers.'
    remote_args = [
     '-remote', 'openURL(%s%action)']
    remote_action = ''
    remote_action_newwin = ',new-window'
    remote_action_newtab = ',new-tab'
    background = False
    redirect_stdout = False


class Konqueror(BaseBrowser):
    __doc__ = 'Controller for the KDE File Manager (kfm, or Konqueror).\n\n    See the output of ``kfmclient --commands``\n    for more information on the Konqueror remote-control interface.\n    '

    def open(self, url, new=0, autoraise=True):
        if new == 2:
            action = 'newTab'
        else:
            action = 'openURL'
        devnull = subprocess.DEVNULL
        try:
            p = subprocess.Popen(['kfmclient', action, url], close_fds=True,
              stdin=devnull,
              stdout=devnull,
              stderr=devnull)
        except OSError:
            pass
        else:
            p.wait()
            return True
            try:
                p = subprocess.Popen(['konqueror', '--silent', url], close_fds=True,
                  stdin=devnull,
                  stdout=devnull,
                  stderr=devnull,
                  start_new_session=True)
            except OSError:
                pass
            else:
                if p.poll() is None:
                    return True
                try:
                    p = subprocess.Popen(['kfm', '-d', url], close_fds=True,
                      stdin=devnull,
                      stdout=devnull,
                      stderr=devnull,
                      start_new_session=True)
                except OSError:
                    return False
                else:
                    return p.poll() is None


class Grail(BaseBrowser):

    def _find_grail_rc(self):
        import glob, pwd, socket, tempfile
        tempdir = os.path.join(tempfile.gettempdir(), '.grail-unix')
        user = pwd.getpwuid(os.getuid())[0]
        filename = os.path.join(tempdir, user + '-*')
        maybes = glob.glob(filename)
        if not maybes:
            return
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        for fn in maybes:
            try:
                s.connect(fn)
            except OSError:
                try:
                    os.unlink(fn)
                except OSError:
                    pass

            else:
                return s

    def _remote(self, action):
        s = self._find_grail_rc()
        if not s:
            return 0
        else:
            s.send(action)
            s.close()
            return 1

    def open(self, url, new=0, autoraise=True):
        if new:
            ok = self._remote('LOADNEW ' + url)
        else:
            ok = self._remote('LOAD ' + url)
        return ok


def register_X_browsers():
    if shutil.which('xdg-open'):
        register('xdg-open', None, BackgroundBrowser('xdg-open'))
    else:
        if 'GNOME_DESKTOP_SESSION_ID' in os.environ:
            if shutil.which('gvfs-open'):
                register('gvfs-open', None, BackgroundBrowser('gvfs-open'))
            elif 'GNOME_DESKTOP_SESSION_ID' in os.environ:
                if shutil.which('gnome-open'):
                    register('gnome-open', None, BackgroundBrowser('gnome-open'))
                if 'KDE_FULL_SESSION' in os.environ:
                    if shutil.which('kfmclient'):
                        register('kfmclient', Konqueror, Konqueror('kfmclient'))
            else:
                if shutil.which('x-www-browser'):
                    register('x-www-browser', None, BackgroundBrowser('x-www-browser'))
                for browser in ('firefox', 'iceweasel', 'iceape', 'seamonkey'):
                    if shutil.which(browser):
                        register(browser, None, Mozilla(browser))

                for browser in ('mozilla-firefox', 'mozilla-firebird', 'firebird',
                                'mozilla', 'netscape'):
                    if shutil.which(browser):
                        register(browser, None, Netscape(browser))

                if shutil.which('kfm'):
                    register('kfm', Konqueror, Konqueror('kfm'))
                elif shutil.which('konqueror'):
                    register('konqueror', Konqueror, Konqueror('konqueror'))
            for browser in ('galeon', 'epiphany'):
                if shutil.which(browser):
                    register(browser, None, Galeon(browser))

            if shutil.which('skipstone'):
                register('skipstone', None, BackgroundBrowser('skipstone'))
        else:
            for browser in ('google-chrome', 'chrome', 'chromium', 'chromium-browser'):
                if shutil.which(browser):
                    register(browser, None, Chrome(browser))

            if shutil.which('opera'):
                register('opera', None, Opera('opera'))
            if shutil.which('mosaic'):
                register('mosaic', None, BackgroundBrowser('mosaic'))
        if shutil.which('grail'):
            register('grail', Grail, None)


if os.environ.get('DISPLAY'):
    register_X_browsers()
if os.environ.get('TERM'):
    if shutil.which('www-browser'):
        register('www-browser', None, GenericBrowser('www-browser'))
    else:
        if shutil.which('links'):
            register('links', None, GenericBrowser('links'))
        else:
            if shutil.which('elinks'):
                register('elinks', None, Elinks('elinks'))
            if shutil.which('lynx'):
                register('lynx', None, GenericBrowser('lynx'))
        if shutil.which('w3m'):
            register('w3m', None, GenericBrowser('w3m'))
if sys.platform[:3] == 'win':

    class WindowsDefault(BaseBrowser):

        def open(self, url, new=0, autoraise=True):
            try:
                os.startfile(url)
            except OSError:
                return False
            else:
                return True


    _tryorder = []
    _browsers = {}
    register('windows-default', WindowsDefault)
    iexplore = os.path.join(os.environ.get('PROGRAMFILES', 'C:\\Program Files'), 'Internet Explorer\\IEXPLORE.EXE')
    for browser in ('firefox', 'firebird', 'seamonkey', 'mozilla',
     'netscape', 'opera', iexplore):
        if shutil.which(browser):
            register(browser, None, BackgroundBrowser(browser))

if sys.platform == 'darwin':

    class MacOSX(BaseBrowser):
        __doc__ = 'Launcher class for Aqua browsers on Mac OS X\n\n        Optionally specify a browser name on instantiation.  Note that this\n        will not work for Aqua browsers if the user has moved the application\n        package after installation.\n\n        If no browser is specified, the default browser, as specified in the\n        Internet System Preferences panel, will be used.\n        '

        def __init__(self, name):
            self.name = name

        def open(self, url, new=0, autoraise=True):
            if not "'" not in url:
                raise AssertionError
            else:
                if ':' not in url:
                    url = 'file:' + url
                else:
                    new = int(bool(new))
                    if self.name == 'default':
                        script = 'open location "%s"' % url.replace('"', '%22')
                    else:
                        if self.name == 'OmniWeb':
                            toWindow = ''
                        else:
                            toWindow = 'toWindow %d' % (new - 1)
                cmd = 'OpenURL "%s"' % url.replace('"', '%22')
                script = 'tell application "%s"\n                                activate\n                                %s %s\n                            end tell' % (self.name, cmd, toWindow)
            osapipe = os.popen('osascript', 'w')
            if osapipe is None:
                return False
            else:
                osapipe.write(script)
                rc = osapipe.close()
                return not rc


    class MacOSXOSAScript(BaseBrowser):

        def __init__(self, name):
            self._name = name

        def open(self, url, new=0, autoraise=True):
            if self._name == 'default':
                script = 'open location "%s"' % url.replace('"', '%22')
            else:
                script = '\n                   tell application "%s"\n                       activate\n                       open location "%s"\n                   end\n                   ' % (self._name, url.replace('"', '%22'))
            osapipe = os.popen('osascript', 'w')
            if osapipe is None:
                return False
            else:
                osapipe.write(script)
                rc = osapipe.close()
                return not rc


    register('safari', None, MacOSXOSAScript('safari'), -1)
    register('firefox', None, MacOSXOSAScript('firefox'), -1)
    register('chrome', None, MacOSXOSAScript('chrome'), -1)
    register('MacOSX', None, MacOSXOSAScript('default'), -1)
if 'BROWSER' in os.environ:
    _userchoices = os.environ['BROWSER'].split(os.pathsep)
    _userchoices.reverse()
    for cmdline in _userchoices:
        if cmdline != '':
            cmd = _synthesize(cmdline, -1)
            if cmd[1] is None:
                register(cmdline, None, GenericBrowser(cmdline), -1)

    cmdline = None
    del cmdline
    del _userchoices

def main():
    import getopt
    usage = 'Usage: %s [-n | -t] url\n    -n: open new window\n    -t: open new tab' % sys.argv[0]
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'ntd')
    except getopt.error as msg:
        print(msg, file=(sys.stderr))
        print(usage, file=(sys.stderr))
        sys.exit(1)

    new_win = 0
    for o, a in opts:
        if o == '-n':
            new_win = 1
        else:
            if o == '-t':
                new_win = 2

    if len(args) != 1:
        print(usage, file=(sys.stderr))
        sys.exit(1)
    url = args[0]
    open(url, new_win)
    print('\x07')


if __name__ == '__main__':
    main()