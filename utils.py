import os
import command
import hashlib


def list_files_in_path(root_path, prefix=None, postfix=None):
    if not os.path.exists(root_path):
        raise Exception("path not found")
    for root, sub_dirs, files in os.walk(root_path):
        for special_file in files:
            if postfix or prefix:
                if postfix and not special_file.endswith(postfix):
                    continue
                if prefix and not special_file.startswith(prefix):
                    continue
                yield os.path.join(root, special_file)
            yield os.path.join(root, special_file)

        for sub_dir in sub_dirs:
            list_files_in_path(os.path.join(root, sub_dir), prefix=prefix, postfix=postfix)


def get_password():
    cmd = [
        'ip address | grep link | grep -v inet6'
    ]
    ret = os.popen(" ".join(cmd))
    pwd = ret.read().replace("\n", "").replace(":", "").replace(" ", "").replace("/", "").strip()
    pwd = hashlib.sha256(pwd.encode("utf-8")).hexdigest()
    return pwd


def enrypt_file(infile, outfile, password):
    cmd = [
        'openssl enc -e -aes-256-cbc',
        '-in', infile,
        '-out', outfile,
        '-pass pass:%s' % password,
        '-base64'
    ]
    # print(" ".join(cmd))
    return command.run(" ".join(cmd).split(" "))


def derypt_file(infile, outfile, password):
    cmd = [
        'openssl enc -d -aes-256-cbc',
        '-in', infile,
        '-out', outfile,
        '-pass pass:%s' % password,
        '-base64'
    ]
    # print(" ".join(cmd))
    return command.run(" ".join(cmd).split(" "))


def get_folder_path():
    data_folder = "data"
    local_folder = "local_folder"
    local_path = os.path.curdir + os.path.sep + local_folder
    data_path = os.path.curdir + os.path.sep + data_folder

    return local_path, data_path
