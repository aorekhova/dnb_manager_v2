import dnb_runners.ten_preparation as ten_preparation
import dnb_runners.select_parties as select_parties




def dnb_manager(task_name, month):

    dnb_process = {"ten preparation": ten_preparation.TenPreparation(task_name, month),
                    "select parties": select_parties.SelectParties(task_name, month)}


    for process_name, process in dnb_process.items():
        output = process.runner()
        if output == -1:
            break
