import os
import time
from utils import derypt_file
from utils import list_files_in_path
from utils import get_password
from utils import get_folder_path


if __name__ == "__main__":
    local_path, data_path = get_folder_path()
    for data_file in list_files_in_path(data_path):
        target_file = os.path.join(local_path, data_file.lstrip(data_path))
        folder = os.path.dirname(target_file)
        os.makedirs(folder, exist_ok=True)
        try:
            start_time = time.time()
            ret = derypt_file(data_file, target_file, get_password())
            end_time = time.time()
            if ret.exit == 0:
                print("Decrypt %s ok.... %ss" % (data_file, end_time - start_time))
            else:
                print("Decrypt %s failed, output is: %s" % (data_file, ret.output))
        except Exception as e:
            print("Decrypt %s failed, exception: %s" % (data_file, e))
