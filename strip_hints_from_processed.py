import os

import strip_hints

ROOT_FOLDER = '../../../python_typing/'
REPOS_FOLDER = os.path.join(ROOT_FOLDER, 'repos')
PROCESSED_FOLDER = os.path.join(ROOT_FOLDER, 'processed')
STRIPPED_FOLDER = os.path.join(ROOT_FOLDER, 'stripped')

for dir_name, subdir_list, file_list in os.walk(PROCESSED_FOLDER):
    print(f'---{dir_name}---')
    print(subdir_list)
    py_file_list = [py_file for py_file in file_list if py_file.lower().endswith('.py')]
    # print(f'py_file_list: {py_file_list}')
    for filename in py_file_list:
        full_path = os.path.join(dir_name, filename)
        code_string = strip_hints.strip_file_to_string(full_path, no_ast=True)
        # print(code_string)
        target_file = os.path.join(STRIPPED_FOLDER, filename)
        with open(target_file, 'w', encoding="utf-8") as curr_file:
            print(code_string, file=curr_file)