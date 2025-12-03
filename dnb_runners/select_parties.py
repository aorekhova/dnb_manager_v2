import setup.setupenv_aps_ten as roots
from instruments import prepare_parameters as preparation
import cmd_session.cmd_runner





class SelectParties:
    def __init__(self, task_name, month, env_setup="aps_ten"):

        self.aps_input_path, self.aps_output_path = (f"{roots.APS_SOURCES}/{task_name}",
                                                    f"{roots.APS_SELECTED_PARTIES}/{task_name}")
        self.ten_input_path, self.ten_output_path = (f"{roots.TEN_SOURCES}/{task_name}",
                                                    f"{roots.TEN_SELECTED_PARTIES}/{task_name}")

        self.aps_parameters = [ "python", "-m", "drum_and_bass.select_parties", "-i", self.aps_input_path,
                                "--buyers-output", f"{self.aps_output_path}/APS-buyers-{month}.csv",
                                "--suppliers-output", f"{self.aps_output_path}/APS-suppliers-{month}.csv",
                                "-d", f"{roots.DNB_DATABASE}",
                                "--country-map", f"{roots.COUNTRY_MAP}/country-map.csv",
                                "-p", "APS", "--delimiter", ";" ]

        self.ten_parameters = [ "python", "-m", "drum_and_bass.select_parties", "-i", self.ten_input_path,
                                "--buyers-output", f"{self.ten_output_path}/TEN-buyers-{month}.csv",
                                "--suppliers-output", f"{self.ten_output_path}/TEN-suppliers-{month}.csv",
                                "-d", f"{roots.DNB_DATABASE}",
                                "--country-map", f"{roots.COUNTRY_MAP}/country-map.csv",
                                "-p", "TEN", "--delimiter", "," ]


    def runner(self):
        cmd_runner = cmd_session.cmd_runner.CmdRunner()

        try:
            cmd_runner.prepare_env("add folder", output_path=self.aps_output_path)
            aps_select_output = cmd_runner.run(self.aps_parameters)
        except Exception as e:
            cmd_runner.kill_session()
            return -1
        # checkPont("select parties")
        self.analyse_output(aps_select_output)

        try:
            cmd_runner.prepare_env("add folder", output_path=self.ten_output_path)
            ten_select_output = cmd_runner.run(self.ten_parameters)
        except Exception as e:
            cmd_runner.kill_session()
            return -1
        self.analyse_output(ten_select_output)


    def analyse_output(self, output):
        pass

