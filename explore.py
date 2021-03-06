import os
import shutil 


ROOT_FOLDER = 'data'
REPOS_FOLDER = os.path.join(ROOT_FOLDER, 'repos')
PROCESSED_FOLDER = os.path.join(ROOT_FOLDER, 'processed')

FILE_ID = 0
count = 0
type_1_count = 0
type_2_count = 0
total_lines = 0
total_typed_lines = 0
total = 0
for dir_name, subdir_list, file_list in os.walk(REPOS_FOLDER):
    py_file_list = [py_file for py_file in file_list if py_file.lower().endswith('.py')]
    for py_file in py_file_list:
        total += 1
        count += 1
        target_file = os.path.join(dir_name, py_file)
        with open(target_file, 'r', encoding="ISO-8859-1") as curr_file:
            lines = curr_file.readlines()
            total_lines += len(lines)
            import_1 = 'import typing'
            import_2 = 'from typing import'
            match_1 = next((s for s in lines if import_1 in s), None) # returns 'abc123'
            if match_1:
                total_typed_lines += len(lines)
                type_1_count += 1
                new_dest = f'{FILE_ID}_{py_file}'
                shutil.copy2(target_file, os.path.join(PROCESSED_FOLDER, new_dest))
                FILE_ID += 1
                continue
            match_2 = next((s for s in lines if import_2 in s), None)
            if match_2:
                total_typed_lines += len(lines)
                type_2_count += 1
                new_dest = f'{FILE_ID}_{py_file}'
                shutil.copy2(target_file, os.path.join(PROCESSED_FOLDER, new_dest))
                FILE_ID += 1
                continue
            

print(f'total: {total}')
print(f'`import typing` count: {type_1_count}')
print(f'`from typing import ...` count: {type_2_count}')
print(f'total typed: {type_1_count + type_2_count}')
print(f'total typed lines: {total_typed_lines}')
print(f'total lines: {total_lines}')