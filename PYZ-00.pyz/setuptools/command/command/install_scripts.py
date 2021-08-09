# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\setuptools-39.0.1-py3.6.egg\setuptools\command\install_scripts.py
from distutils import log
import distutils.command.install_scripts as orig, os, sys
from pkg_resources import Distribution, PathMetadata, ensure_directory

class install_scripts(orig.install_scripts):
    __doc__ = 'Do normal script install, plus any egg_info wrapper scripts'

    def initialize_options(self):
        orig.install_scripts.initialize_options(self)
        self.no_ep = False

    def run(self):
        import setuptools.command.easy_install as ei
        self.run_command('egg_info')
        if self.distribution.scripts:
            orig.install_scripts.run(self)
        else:
            self.outfiles = []
        if self.no_ep:
            return
        ei_cmd = self.get_finalized_command('egg_info')
        dist = Distribution(ei_cmd.egg_base, PathMetadata(ei_cmd.egg_base, ei_cmd.egg_info), ei_cmd.egg_name, ei_cmd.egg_version)
        bs_cmd = self.get_finalized_command('build_scripts')
        exec_param = getattr(bs_cmd, 'executable', None)
        bw_cmd = self.get_finalized_command('bdist_wininst')
        is_wininst = getattr(bw_cmd, '_is_running', False)
        writer = ei.ScriptWriter
        if is_wininst:
            exec_param = 'python.exe'
            writer = ei.WindowsScriptWriter
        if exec_param == sys.executable:
            exec_param = [
             exec_param]
        writer = writer.best()
        cmd = writer.command_spec_class.best().from_param(exec_param)
        for args in writer.get_args(dist, cmd.as_header()):
            (self.write_script)(*args)

    def write_script(self, script_name, contents, mode='t', *ignored):
        """Write an executable file to the scripts directory"""
        from setuptools.command.easy_install import chmod, current_umask
        log.info('Installing %s script to %s', script_name, self.install_dir)
        target = os.path.join(self.install_dir, script_name)
        self.outfiles.append(target)
        mask = current_umask()
        if not self.dry_run:
            ensure_directory(target)
            f = open(target, 'w' + mode)
            f.write(contents)
            f.close()
            chmod(target, 511 - mask)