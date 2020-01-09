"""
skill Web Terminal
Copyright (C) 2020  Andreas Lorensen

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from mycroft import MycroftSkill, intent_file_handler
import os
from shutil import copyfile
import subprocess
import signal


class WebTerminal(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        self.SafePath = self.file_system.path
        self.SkillPath = self.root_dir
        if not self.settings.get("installed") or self.settings.get("installed") is None:
            self.install()
        if not self.pid_exists(self.settings.get("terminal_pid")):
            self.settings["terminal_pid"] = None
        if not self.pid_exists(self.settings.get("cli_pid")):
            self.settings["cli_pid"] = None
        if self.settings.get("terminal_enabled") and self.settings.get("terminal_pid") is None:
            self.run_terminal()
        if self.settings.get("cli_enabled") and self.settings.get("cli_pid") is None:
            self.run_cli()

    @intent_file_handler('terminal.start.intent')
    def handle_terminal_start(self, message):
        self.run_terminal()

    @intent_file_handler('terminal.stop.intent')
    def handle_terminal_stop(self, message):
        self.stop_terminal()

    @intent_file_handler('cli.start.intent')
    def handle_cli_start(self, message):
        self.run_cli()

    @intent_file_handler('cli.stop.intent')
    def handle_cli_stop(self, message):
        self.stop_cli()

    def run_terminal(self):
        if self.settings.get("terminal_pid)") is None:
            port = str(self.settings.get("terminal_port"))
            home = os.path.expanduser('~')
            proc = subprocess.Popen(self.SafePath + '/ttyd/build/ttyd -p '
                                    + port + ' bash --init-file '
                                    + self.SafePath + '/bashrc',
                                    cwd=home, preexec_fn=os.setsid, shell=True)
            self.settings["terminal_pid"] = proc.pid
            url = os.uname().nodename + ':' + port
            self.log.info('Terminal started - http://' + url)
            self.speak_dialog('terminal_started', data={"url": url})
            return True
        else:
            return False

    def run_cli(self):
        if self.settings.get("cli_pid)") is None:
            port = str(self.settings.get("cli_port"))
            home = os.path.expanduser('~')
            proc = subprocess.Popen(self.SafePath + '/ttyd/build/ttyd -p ' +
                                    port + ' mycroft-cli-client',
                                    cwd=home, preexec_fn=os.setsid, shell=True)
            self.settings["cli_pid"] = proc.pid
            url = os.uname().nodename + ':' + port
            self.log.info('CLI started - http://' + url)
            self.speak_dialog('cli_started', data={"url": url})
            return True
        else:
            return False

    def stop_terminal(self):
        self.log.info("Stopping web terminal")
        if self.settings.get("terminal_pid") is not None:
            os.killpg(self.settings.get("terminal_pid"), signal.SIGTERM)
            self.settings["terminal_pid"] = None
            self.speak_dialog('terminal_stoped')
            return True
        else:
            return False

    def stop_cli(self):
        self.log.info("Stopping mycroft-cli-client")
        if self.settings.get("cli_pid") is not None:
            os.killpg(self.settings.get("cli_pid"), signal.SIGTERM)
            self.settings["cli_pid"] = None
            self.speak_dialog('cli_stoped')
            return True
        else:
            return False

    def pid_exists(self, pid):
        try:
            os.kill(pid, 0)
            return True
        except Exception:
            return False

    def install(self):
        try:
            self.log.info("Installing Web Terminal...")
            proc = subprocess.Popen('git clone '
                                    + 'https://github.com/tsl0922/ttyd.git',
                                    cwd=self.SafePath, preexec_fn=os.setsid,
                                    shell=True)
            proc.wait()
            proc = subprocess.Popen('mkdir build', cwd=self.SafePath + '/ttyd',
                                    preexec_fn=os.setsid, shell=True)
            proc.wait()
            proc = subprocess.Popen('cmake ..', cwd=self.SafePath
                                    + '/ttyd/build',
                                    preexec_fn=os.setsid, shell=True)
            proc.wait()
            proc = subprocess.Popen('make', cwd=self.SafePath + '/ttyd/build',
                                    preexec_fn=os.setsid, shell=True)
            proc.wait()
            copyfile(self.SkillPath + '/bashrc', self.SafePath + '/bashrc')
            self.log.info("Installed OK")
            self.settings['installed'] = True
            return True
        except Exception:
            self.log.info("Web Terminal is not installed - something went wrong!")
            self.speak_dialog('installed_BAD')
            return False


def create_skill():
    return WebTerminal()
