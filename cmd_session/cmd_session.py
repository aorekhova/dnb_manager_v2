import shlex
import subprocess
import threading
from instruments.logger import logger
import sys




def _reader(pipe, buffer, invisible, is_err=False):
    try:
        for line in iter(pipe.readline, ''):
            buffer.append(line)

            if not invisible:
                text = line.rstrip("\n")
                if is_err:
                    logger.error(text)
                    # или print(text, file=sys.stderr)
                else:
                    logger.info(text)
                    # или print(text)
    finally:
        pipe.close()




class CmdSession:
    def __init__(self):
        self.cmd_session = None
        self.stdout_lines = []
        self.stderr_lines = []

    def run(self, parameters, timeout=900, invisible=False):
        logger.info(f"[CmdSession] Start process: {parameters}, timeout={timeout}, invisible={invisible}")

        self.cmd_session = subprocess.Popen(
            parameters,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8"
        )

        session_out = threading.Thread(
            target=_reader,
            args=(self.cmd_session.stdout, self.stdout_lines, invisible, False),
            daemon=True
        )
        session_err = threading.Thread(
            target=_reader,
            args=(self.cmd_session.stderr, self.stderr_lines, invisible, True),
            daemon=True
        )

        session_out.start()
        session_err.start()

        try:
            self.cmd_session.wait(timeout=timeout)
            status = "finished"
        except subprocess.TimeoutExpired:
            logger.error("[CmdSession] TimeoutExpired, killing process")
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

        logger.info(
            f"[CmdSession] End process: status={status}, returncode={returncode}, "
            f"stdout_len={len(stdout)}, stderr_len={len(stderr)}"
        )

        return {
            "status": status,
            "stdout": stdout,
            "stderr": stderr,
            "returncode": returncode,
        }

    def kill_session(self):
        if self.cmd_session is not None and self.cmd_session.poll() is None:
            logger.warning("[CmdSession] Killing running process")
            try:
                self.cmd_session.kill()
            except Exception:
                logger.exception("[CmdSession] Error while killing process")

        self.cmd_session = None
        self.stdout_lines = []
        self.stderr_lines = []
