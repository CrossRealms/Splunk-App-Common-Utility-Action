import os
from datetime import datetime
import hashlib


# Debug function
def list_files(startpath, max_level=5):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)

        if level > max_level:
            continue

        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))


def str_to_boolean(value_in_str: str):
    value_in_str = str(value_in_str).lower()
    if value_in_str in ("false", "f", "0"):
        return False
    return True


def get_input(name):
    val = os.getenv(f"SPLUNK_{name}")
    if not val or val == 'NONE':
        return None
    return val


def test_set_input(name, value):
    os.environ["SPLUNK_{}".format(name)] = value


def set_env(name, value):
    # os.environ[name] = value   # this does not work with github action
    # ret_code = os.system('export {}={}'.format(name, value))   # this does not work with github action
    ret_code = os.system('echo "{}={}" >> $GITHUB_ENV'.format(name, value))
    print("ret_code for setting env variable. {}".format(ret_code))


def set_output(name, value):
    print(f"::set-output name={name}::{_escape_data(value)}")


def format_message(message):
    timestamp = datetime.now().strftime("%H:%M:%S.%f")
    return "{} | {}".format(timestamp, message)


def debug(message):
    message = format_message(message)
    print(f"::debug::{_escape_data(message)}")


def info(message):
    message = format_message(message)
    print(f"{_escape_data(message)}")


def warning(message):
    message = format_message(message)
    print(f"::warning::{_escape_data(message)}")


def error(message):
    message = format_message(message)
    print(f"::error::{_escape_data(message)}")


def group(title):
    print(f"::group::{title}")


def end_group():
    print(f"::endgroup::")


def add_mask(value):
    print(f"::add-mask::{_escape_data(value)}")


def stop_commands():
    print(f"::stop-commands::pause-commands")


def resume_commands():
    print(f"::pause-commands::")


def save_state(name, value):
    print(f"::save-state name={name}::{_escape_data(value)}")


def _escape_data(value: str):
    return value.replace("%", "%25").replace("\r", "%0D")
    # .replace("\n", "%0A")


def get_file_hash(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()