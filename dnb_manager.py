import argparse

import dnb_runners.ten_preparation as ten_preparation
import dnb_runners.select_parties as select_parties
from instruments.logger import logger, phase_logging





def dnb_manager(task_name, month):
    logger.info(f"Start DnB manager for task={task_name}, month={month}")

    dnb_process = {
        "ten_preparation": ten_preparation.TenPreparation(task_name, month),
        "select_parties": select_parties.SelectParties(task_name, month),
    }

    for phase_name, process in dnb_process.items():
        with phase_logging(phase_name, task_name):
            logger.info(f"Start phase: {phase_name}")

            output = process.runner()

            if output != 0:
                logger.error(f"Phase '{phase_name}' failed, stopping pipeline")
                break

            logger.info(f"Phase '{phase_name}' finished successfully")

    logger.info(f"Finish DnB manager for task={task_name}, month={month}")





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="DNB Manager Runner")
    parser.add_argument("-t", "--tusk", required=True)
    parser.add_argument("-m", "--month", required=True)

    args = parser.parse_args()
    dnb_manager(args.tusk, args.month)
