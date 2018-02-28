import os
import time
from utils import list_files_in_path
from utils import get_password
from utils import enrypt_file
from utils import get_folder_path
from utils import delete_folder
from utils import get_hash_sum_path
from utils import get_file_sha256sum


if __name__ == "__main__":
    local_path, data_path = get_folder_path()
    hash_sum_path = get_hash_sum_path()
    failed_file = []
    for data_file in list_files_in_path(local_path):
        target_file = os.path.join(data_path, data_file.lstrip(local_path))
        hash_file = os.path.join(hash_sum_path, data_file.lstrip(local_path))
        folder = os.path.dirname(target_file)
        os.makedirs(folder, exist_ok=True)
        try:
            sha256sum = get_file_sha256sum(data_file)
            old_sha256sum = None
            if os.path.exists(hash_file):
                with open(hash_file, "r") as f:
                    old_sha256sum = f.read()

            if str(old_sha256sum) != str(sha256sum):
                start_time = time.time()
                ret = enrypt_file(data_file, target_file, get_password())
                end_time = time.time()
                if ret.exit == 0:
                    print("Encrypt %s ok.... %ss" % (data_file, end_time - start_time))
                    os.remove(data_file)
                else:
                    failed_file.append(data_file)
                    print("Encrypt %s failed, output is: %s" % ret.output)
            else:
                print("File %s not changed, skip..." % data_file)
                os.remove(data_file)

        except Exception as e:
            print("Encrypt %s failed, exception: %s" % (data_file, e))
            failed_file.append(data_file)

    if failed_file:
        print("Failed encryt file:")
        for f in failed_file:
            print(f)
    else:
        delete_folder(local_path)
        delete_folder(hash_sum_path, delete_file=True)


"""
可以指定文件加解密
"""