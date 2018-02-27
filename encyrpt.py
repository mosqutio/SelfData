import os
import time
from utils import list_files_in_path
from utils import get_password
from utils import enrypt_file
from utils import get_folder_path
from utils import delete_empty_folder


if __name__ == "__main__":
    local_path, data_path = get_folder_path()
    failed_file = []
    for data_file in list_files_in_path(local_path):
        target_file = os.path.join(data_path, data_file.lstrip(local_path))
        folder = os.path.dirname(target_file)
        os.makedirs(folder, exist_ok=True)
        try:
            start_time = time.time()
            ret = enrypt_file(data_file, target_file, get_password())
            end_time = time.time()
            if ret.exit == 0:
                print("Encrypt %s ok.... %ss" % (data_file, end_time - start_time))
                os.remove(data_file)
            else:
                failed_file.append(data_file)
                print("Encrypt %s failed, output is: %s" % ret.output)
        except Exception as e:
            print("Encrypt %s failed, exception: %s" % (data_file, e))
            failed_file.append(data_file)

    if failed_file:
        print("Failed encryt file:")
        for f in failed_file:
            print(f)
    else:
        delete_empty_folder(local_path)


"""
可以指定文件加解密
"""