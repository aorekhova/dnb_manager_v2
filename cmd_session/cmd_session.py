import shlex
import subprocess
import threading
import time
import sys




def _reader(pipe, buffer, invisible, is_err=False):
    try:
        for line in iter(pipe.readline, ''):
            if not invisible:
                continue
            buffer.append(line)
            if not is_err:
                print(line, end='')
    finally:
        pipe.close()




class CmdSession:
    def __init__(self):
        self.cmd_session = None
        self.stdout_lines = []
        self.stderr_lines = []



    def run(self, parameters, timeout=900, invisible=False):
        self.cmd_session = subprocess.Popen(parameters,
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE,
                                            text=True,
                                            encoding="utf-8")

        # create streams for session out/errors
        session_out = threading.Thread(target=_reader,
                                        args=(self.cmd_session.stdout, self.stdout_lines, invisible, False),
                                        daemon=True)
        session_err = threading.Thread(target=_reader,
                                        args=(self.cmd_session.stderr, self.stderr_lines, invisible, True),
                                        daemon=True)

        session_out.start()
        session_err.start()

        try:
            self.cmd_session.wait(timeout=timeout)
            status = "finished"
        except subprocess.TimeoutExpired:
            self.cmd_session.kill()
            status = "timeout"

        session_out.join(timeout=1)
        session_err.join(timeout=1)

        stdout = "".join(self.stdout_lines)
        stderr = "".join(self.stderr_lines)

        # clean
        self.stdout_lines = []
        self.stderr_lines = []
        returncode = self.cmd_session.returncode if status == "finished" else -1
        self.cmd_session = None


        return {"status": status, "stdout": stdout,
                "stderr": stderr, "returncode": returncode}



    def kill_session(self):
        if self.cmd_session is not None and self.cmd_session.poll() is None:
            try:
                self.cmd_session.kill()
            except Exception:
                pass

        self.cmd_session = None
        self.stdout_lines = []
        self.stderr_lines = []