import dnb_runners.ten_preparation as ten_preparation
import dnb_runners.select_parties as select_parties
from instruments.logger import logger




def dnb_manager(task_name, month):

    logger.info(f"Start DnB manager for task={task_name}, month={month}")

    dnb_process = {
        "ten preparation": ten_preparation.TenPreparation(task_name, month),
        "select parties": select_parties.SelectParties(task_name, month)
    }


    for process_name, process in dnb_process.items():
        logger.info(f"Start process: {process_name}")

        output = process.runner()

        if output == -1:
            logger.error(f"Process '{process_name}' failed, stopping pipeline")
            break


        logger.info(f"Finish DnB manager for task={task_name}, month={month}")
