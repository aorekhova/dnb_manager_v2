import setup.setupenv_aps_ten as roots
from instruments import prepare_parameters as preparation
import cmd_session.cmd_runner
from instruments.logger import logger
import check_points.check_point_manager as check_points





class SelectParties:
    def __init__(self, task_name, month, env_setup="aps_ten"):
        self.checking = check_points.CheckPoint(phase="select parties", inf="All number of read invoices:")

        self.aps_input_path, self.aps_output_path = (f"{roots.APS_SOURCES}/{task_name}",
                                                    f"{roots.APS_SELECTED_PARTIES}/{task_name}")
        self.ten_input_path, self.ten_output_path = (f"{roots.TEN_SOURCES}/{task_name}",
                                                    f"{roots.TEN_SELECTED_PARTIES}/{task_name}")

        self.aps_parameters = [ "python", "-u", "-m", "drum_and_bass.select_parties", "-i", self.aps_input_path,
                                "--buyers-output", f"{self.aps_output_path}/APS-buyers-{month}.csv",
                                "--suppliers-output", f"{self.aps_output_path}/APS-suppliers-{month}.csv",
                                "-d", f"{roots.DNB_DATABASE}",
                                "--country-map", f"{roots.COUNTRY_MAP}/country-map.csv",
                                "-p", "APS", "--delimiter", ";" ]

        self.ten_parameters = [ "python", "-u", "-m", "drum_and_bass.select_parties", "-i", self.ten_input_path,
                                "--buyers-output", f"{self.ten_output_path}/TEN-buyers-{month}.csv",
                                "--suppliers-output", f"{self.ten_output_path}/TEN-suppliers-{month}.csv",
                                "-d", f"{roots.DNB_DATABASE}",
                                "--country-map", f"{roots.COUNTRY_MAP}/country-map.csv",
                                "-p", "TEN", "--delimiter", "," ]


    def runner(self):
        cmd_runner = cmd_session.cmd_runner.CmdRunner()

        try:
            logger.info(f"[SelectParties] Prepare APS env: create folder {self.aps_output_path}")
            cmd_runner.prepare_env("add folder", output_path=self.aps_output_path)
            aps_select_output = cmd_runner.run(self.aps_parameters)

        except Exception as e:
            logger.exception(f"[SelectParties] APS step failed with exception: {e}")
            cmd_runner.kill_session()
            return -1

        # checkPont("select parties")
        self.checking.give_new_stat(cmd_runner.return_prepare_inf())
        self.analyse_output(aps_select_output, label="APS")


        try:
            logger.info(f"[SelectParties] Prepare TeN env: create folder {self.ten_output_path}")
            cmd_runner.prepare_env("add folder", output_path=self.ten_output_path)
            ten_select_output = cmd_runner.run(self.ten_parameters)

        except Exception as e:
            logger.exception(f"[SelectParties] TeN step failed with exception: {e}")
            cmd_runner.kill_session()
            return -1

        self.analyse_output(ten_select_output, label="TEN")
        logger.info(f"[SelectParties] Finished successfully")
        return 0



    def analyse_output(self, output, label):
        if output == TimeoutError:
            logger.error(f"[SelectParties][{label}] Timeout during execution")
        elif output == TypeError:
            logger.error(f"[SelectParties][{label}] Process finished with returncode -1")
        else:
            logger.info(f"[SelectParties][{label}] status={output['status']}, returncode={output['returncode']}")
            if output["stderr"]:
                logger.warning(f"[SelectParties][{label}] stderr not empty:\n{output['stderr']}")


