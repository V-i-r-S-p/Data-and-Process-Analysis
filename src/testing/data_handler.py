import subprocess
import os
from glob import glob
from shutil import copy2
import re

from datagen.utils.path_helper import PathHelper

def copy_files_with_mask(source_dir, destination_dir, mask='*.txt'):
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    files_to_copy = glob(os.path.join(source_dir, mask))

    counter = 0
    for file in files_to_copy:
        new_location = os.path.join(destination_dir, os.path.basename(file))
        copy2(file, new_location)
        counter+=1

    print(f'Files {counter} copy: {', '.join(files_to_copy)}')

def run_and_save(script_name, output_file):
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            result = subprocess.run(
                ['.\\..\\..\\.venv\\Scripts\\python.exe', script_name],
                encoding='utf-8',
                stdout=file,
                stderr=subprocess.STDOUT,
            )

        return result.returncode

    except Exception as e:
        print(f'Error: {e}')

def parse_file_to_dict_with_mask(file_path, mask=None):
    result = {}

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if ': ' not in line:
                continue

            key, value = line.split(": ", 1)
            key = key.strip()
            value = value.strip()

            if mask is None or re.match(mask, key):
                result[key] = value

    return result

def parse_files_to_dict_with_mask(folder_path, mask=None):
    files_dict = {}

    search_path = os.path.join(folder_path, mask)

    for file_path in glob(search_path):
        file_name = os.path.basename(file_path)

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                files_dict[file_name] = content.strip()
        except UnicodeDecodeError as e:
            print(f"Error {file_name}: {e}")

    return files_dict

def data2test_img(folder_data, folder_test_img, prefix='external_'):
    def name_generator(file_path: str) -> str:
        return f'{prefix}{PathHelper.filename(file_path)}'
    PathHelper.flatten_directory(PathHelper.path(folder_data, 'images'), folder_test_img, name_generator=name_generator)
    PathHelper.flatten_directory(PathHelper.path(folder_data, 'labels'), folder_test_img, name_generator=name_generator)

def setup_data():
    if not PathHelper.exists('./datagen/build'):
        import datagen.main

    if not PathHelper.exists('./test_images'):
        PathHelper.flatten_directory("./datagen/build", "./test_images")

    copy_files_with_mask('../model/', './', '*.py')
    copy_files_with_mask('../model/', './', '*.pth')

    if PathHelper.exists('./data'):
        print('External data detected')
        data2test_img('./data', "./test_images")

    if run_and_save('predict.py','out.txt'):
        raise Exception('predict.py end with error')

def filter_latex_files(folder_name: str, prefix: str, tokens_universe: set, extend: str = '.tex') -> dict:
    latex_dict = parse_files_to_dict_with_mask(folder_name, f'{prefix}*')

    result = {}

    for key, value in latex_dict.items():
        normalized_key = key
        if key.startswith(prefix):
            normalized_key = key[len(prefix):]
        if normalized_key.endswith(extend):
            normalized_key = normalized_key[:-len(extend)]
        remaining_chars = value

        for token in sorted(tokens_universe, key=len, reverse=True):
            remaining_chars = remaining_chars.replace(token, '')

        if not remaining_chars.strip():
            result[normalized_key] = value

    return result

def filter_png_files(folder_name: str, prefix: str) -> dict:
    png_dict = parse_file_to_dict_with_mask(folder_name, f'{prefix}*')

    result = {}

    for key, value in png_dict.items():
        normalized_key = key
        if key.startswith(prefix):
            normalized_key = key[len(prefix):]
        else:
            continue
        if normalized_key.endswith('.png') or normalized_key.endswith('.jpg'):
            normalized_key = normalized_key[:-4]
        else:
            continue
        remaining_chars = value
        result[normalized_key] = remaining_chars.strip()

    return result
