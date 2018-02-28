import os
import time
from utils import derypt_file
from utils import list_files_in_path
from utils import get_password
from utils import get_folder_path
from utils import delete_folder
from utils import get_file_sha256sum
from utils import get_hash_sum_path


if __name__ == "__main__":
    local_path, data_path = get_folder_path()
    hash_sum_path = get_hash_sum_path()
    failed_file = []
    for data_file in list_files_in_path(data_path):
        target_file = os.path.join(local_path, data_file.lstrip(data_path))
        hash_file = os.path.join(hash_sum_path, data_file.lstrip(data_path))
        folder = os.path.dirname(target_file)
        hash_folder = os.path.dirname(hash_file)
        os.makedirs(folder, exist_ok=True)
        os.makedirs(hash_folder, exist_ok=True)
        try:
            start_time = time.time()
            ret = derypt_file(data_file, target_file, get_password())
            end_time = time.time()
            if ret.exit == 0:
                print("Decrypt %s ok.... %ss" % (data_file, end_time - start_time))
                os.remove(data_file)
                sha256sum = get_file_sha256sum(target_file)
                with open(hash_file, "w") as f:
                    f.write(str(sha256sum))

            else:
                failed_file.append(data_file)
                print("Decrypt %s failed, output is: %s" % (data_file, ret.output))
        except Exception as e:
            print("Decrypt %s failed, exception: %s" % (data_file, e))
            failed_file.append(data_file)

    if failed_file:
        print("Failed encryt file:")
        for f in failed_file:
            print(f)
    else:
        delete_folder(data_path)
