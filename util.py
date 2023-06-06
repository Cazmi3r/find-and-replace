import tomllib
import pathlib


def load_config(file: pathlib.Path) -> dict:
    with file.open(mode='rb') as file:
        return tomllib.load(file)
def write_string_to_file(file: pathlib.Path, data: str):
    with file.open(mode='w') as file:
        file.write(data)
def read_str_from_file(path: pathlib.Path) -> str:
    with path.open(mode='r') as file:
        return file.read()
def create_empty_file(path: pathlib.Path) -> None: 
    with path.open(mode="w") as file:
        return
def replace_all(string: str, replace_dic: dict) -> str:
     output = string
     for key, value in replace_dic.items():
        output = output.replace(key, value)
     return output