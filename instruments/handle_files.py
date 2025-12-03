
import uuid, os, re



def add_folder(base_paths):
    if base_paths is not list:
        os.makedirs(base_paths, exist_ok=True)
        print(f"Created {base_paths}")
    else:
        for path in base_paths:
            os.makedirs(path, exist_ok=True)
            print(f"Created {path}")


