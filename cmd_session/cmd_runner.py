from cmd_session.cmd_session import CmdSession
import instruments.handle_files
from instruments.logger import logger




class CmdRunner:
    def __init__(self):
        self.cmd_session = CmdSession()

    def prepare_env(self, type_prepare, input_path=None, output_path=None):
        if type_prepare == "add folder":
            instruments.handle_files.add_folder(output_path)
        elif type_prepare == "merge":
            pass
        elif type_prepare == "delete":
            pass


    def run(self, parameters, timeout=None, invisible=False):
        session_output = self.cmd_session.run(parameters, timeout, invisible)

        # log: finish {session_output.status}, if returncode == "-1" --> print(session.std_err)
        logger.info(
            f"[CmdRunner] Finished command: status={session_output['status']}, "
            f"returncode={session_output['returncode']}")

        if session_output["status"] == "timeout":
            logger.error(f"[CmdRunner] Timeout error. stderr:\n{session_output['stderr']}")
            return TimeoutError
        elif session_output["returncode"] == -1:
            logger.error(f"[CmdRunner] Process failed with returncode -1. stderr:\n{session_output['stderr']}")
            return TypeError
        return session_output


    def kill_session(self):
        logger.warning("[CmdRunner] Kill session requested")
        self.cmd_session.kill_session()
