from instruments import prepare_parameters as convert_absolut_path
import cmd_session.cmd_runner
import setup.setupenv_aps_ten as roots



class TenPreparation:
    def __init__(self, task_name, env_setup="aps_ten", month=None):
        self.input_path = f"{roots.TEN_SOURCES}/{task_name}"
        self.output_path = f"{roots.TEN_SOURCES}/{task_name}"

        self.convert_xls_to_csv = ["python", "-m", "drum_and_bass.convert_xls_to_csv", "-i", self.input_path]
        self.split_ten_invoices_per_week = ["python", "-m", "drum_and_bass.split_ten_invoices_per_week", "-i",
                                            self.input_path, "-o", self.output_path]

        self.time_check = None

    def runner(self):
        cmd_runner = cmd_session.cmd_runner.CmdRunner()

        try:
            convert_session_output = cmd_runner.run(self.convert_xls_to_csv)
        except Exception as e:
            cmd_runner.kill_session()
            return -1
        self.analyse_output(convert_session_output)

        try:
            split_session_output = cmd_runner.run(self.split_ten_invoices_per_week)
        except Exception as e:
            cmd_runner.kill_session()
            return -1
        self.analyse_output(split_session_output)

        return 0


    def analyse_output(self, output):
        # log + check
        pass