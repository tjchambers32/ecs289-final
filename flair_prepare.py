import os
from io import BytesIO

import tokenize
# parse each python file without hints so that each token is on a new line
# then, add in the known types for each token that is known
# then, add in unknown (O) when a type is unknown


ROOT_FOLDER = 'data'
REPOS_FOLDER = os.path.join(ROOT_FOLDER, 'repos')
PROCESSED_FOLDER = os.path.join(ROOT_FOLDER, 'processed')
STRIPPED_FOLDER = os.path.join(ROOT_FOLDER, 'stripped')
TOKENIZED_FOLDER = os.path.join(ROOT_FOLDER, 'tokenized')
TRAIN_FILE = os.path.join(ROOT_FOLDER, 'train.txt')

FILE_ID = 0
count = 0
total_tokens = 0
total_typed_tokens = 0
total = 0
for dir_name, subdir_list, file_list in os.walk(STRIPPED_FOLDER):
    # print(f'---{dir_name}---')
    # print(subdir_list)
    # print(file_list)
    py_file_list = [py_file for py_file in file_list if py_file.lower().endswith('.py')]
    # print(f'py_file_list: {py_file_list}')
    if count > 0: break
    for py_file in py_file_list:
        if count > 0: break
        total += 1
        count += 1
        target_file = os.path.join(dir_name, py_file)
        print(target_file)
        with open(target_file, 'rb') as f:
            out_file = os.path.join(TOKENIZED_FOLDER, py_file)
            with open(out_file, 'w') as out:
                for five_tuple in tokenize.tokenize(f.readline):
                    if five_tuple.string.strip() == '':
                        # get rid of whitespace
                        continue
                    print(f'type: {tokenize.tok_name[five_tuple.type]}')
                    print(f'string: {five_tuple.string}')
                    # print(f'start: {five_tuple.start}')
                    # print(f'end: {five_tuple.end}')
                    # print(f'line: {five_tuple.line}')
                    print(five_tuple.string, file=out)

print(f'total: {total}')
print(f'total typed lines: {total_typed_tokens}')
print(f'total lines: {total_tokens}')