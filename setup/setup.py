DNBPhases  = {
    "TeN preparation": None,
    # "add track id": None, # ?????
    "select parties": "CheckPointManager",
    # "improve L2L4": None,
    "match data to dnb": "CheckPointManager",
    "merge dnb match result": None,
    "compact db": None,
    "verify db": None,
    "generate reports": "CheckPointManager"
}



APS_TeN_BAT_ROOT = r"C:\analytics_scripts\scripts"
AS_NA_BAT_ROOT = "C:/reports/test_samples"
ENV_SETUP = "setupenv.bat"

DNBBats  = {
    "TeN preparation": "ten_preparation.bat",
    # "add track id": "add_track_id.bat", # ?????
    "select parties": "select_parties.bat",
    "improve L2L4": None,
    "match data to dnb": "match_data_to_dnb.bat",
    "merge dnb match result": "merge_from_dnb.bat",
    "compact db": "compact_db.bat",
    "verify db": "verify_db.bat",
    "generate reports": "generate_reports.bat"
}


DNBEnv = {
    "TeN preparation": [None, None],
    # "add track id": "add_track_id.bat", # ?????
    "select parties": ["_add_", None],
    "improve L2L4": [None, "_transfer_"],
    "match data to dnb": [None, None],
    "merge dnb match result": [None, None],
    "compact db": [None, None],
    "verify db": [None, None],
    "generate reports": ["_add_", None]
}



















