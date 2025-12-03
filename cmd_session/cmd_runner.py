import cmd_session
import instruments.handle_files




class CmdRunner:
    def __init__(self):
        self.cmd_session = cmd_session.CmdSession()

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

        if session_output["status"] == "timeout":
            return TimeoutError
        elif session_output["returncode"] == -1:
            return TypeError
        return session_output


    def kill_session(self):
        self.cmd_session.kill_session()
