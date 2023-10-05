import subprocess
import threading


class CMDProcess(threading.Thread):
    def __init__(self, args, callback):
        threading.Thread.__init__(self)
        self.args = args
        self.callback = callback
        self.cwd = "./"

    def run(self):
        self.proc = subprocess.Popen(
            self.args,
            bufsize=1,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=self.cwd,
        )

        while self.proc.poll() is None:
            line = self.proc.stdout.readline()
            self.proc.stdout.flush()
            if self.callback:
                self.callback(line)
