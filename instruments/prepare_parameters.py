import uuid, os, re
import setup.setupenv_aps_ten as env_setup




def pars_bat_setup(bat_path, return_type="all"):
    rewrite_vars, output_vars = [], []

    pattern = re.compile(r"^\s*set\s+([A-Z0-9_]+)=(.*)$", re.IGNORECASE)

    with open(bat_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            match = pattern.match(line)
            if match:
                var_name = match.group(1).strip()
                var_value = match.group(2).strip()

                if var_name.upper().startswith("OUTPUT"):
                    output_vars.append((var_name, var_value))
                else:
                    rewrite_vars.append((var_name, var_value))

    if return_type == "output_vars":
        return output_vars
    elif return_type == "rewrite_vars":
        return rewrite_vars
    return output_vars, rewrite_vars



def convert_absolute_path(path_template, task_name, month=""):

    result = path_template
    variables = re.findall(r"%([A-Z0-9_]+)%", result)

    for var in variables:
        placeholder = f"%{var}%"

        if hasattr(env_setup, var):
            value = getattr(env_setup, var)
            result = result.replace(placeholder, value)
            continue

        if var == "TASK_NAME":
            result = result.replace(placeholder, task_name)
            continue

        if var == "MONTH":
            result = result.replace(placeholder, month)
            continue

    return result


def convert_parameters(param_names, param_path, task_name, month=""):
    sort_parameters = {}
    for name, value in zip(param_names, param_path):
        sort_parameters[name] = convert_absolute_path(value, task_name, month)
    return sort_parameters