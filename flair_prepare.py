import os
import keyword

import tokenize


ROOT_FOLDER = 'data'
REPOS_FOLDER = os.path.join(ROOT_FOLDER, 'repos')
PROCESSED_FOLDER = os.path.join(ROOT_FOLDER, 'processed')
STRIPPED_FOLDER = os.path.join(ROOT_FOLDER, 'stripped')
TOKENIZED_FOLDER = os.path.join(ROOT_FOLDER, 'tokenized')
TRAIN_FILE = os.path.join(ROOT_FOLDER, 'train.txt')

def find_type_hint(filename, token):
    _string = token.string
    # print(_string)
    _line = token.line
    if _string == 'utf-8':
        return 'O'
    if _line.replace('\r', '').replace('\n', '').strip() == '':
        return 'O'

    # return the known type for each token that is known
    target_file = os.path.join(PROCESSED_FOLDER, filename)
    with open(target_file, 'r', encoding="ISO-8859-1") as f:
        lines = f.readlines()
        line_index = token.start[0]-1
        line = lines[line_index]
        # print(f'line: {line}')
        # print(f'token.line: {_line}')
        split_stripped_line = _line.replace('(', ' ').replace(')', ' ').split()
        split_line = line.replace('(', ' ').replace(')', ' ').split()
        # print(f'split_stripped_line: {split_stripped_line}')
        try:
            token_idx = split_stripped_line.index(_string)
        except:
            return 'O'
        # print(f'token: {token.string}, {split_stripped_line[token_idx]}')
        if len(split_stripped_line) < 2 or len(split_line) < 2:
            return 'O'    
        # find function return type
        if split_stripped_line[0] == 'def':
            if token_idx == 0:
                # skip `def`
                return 'O'
            if _string == split_stripped_line[1]:
                func_end_idx = -1
                count = -1
                while func_end_idx == -1:
                    count += 1
                    new_index = line_index + count
                    new_line = lines[new_index]
                    new_split_line = new_line.replace('(', ' ').replace(')', ' ').split()
                    # print(f'new_line: {new_line}')
                    # print(f'new_split_line: {new_split_line}')
                    breakers = ['return', 'class', 'def', 'pass', 'raise']
                    if any(breaker in new_split_line for breaker in breakers):
                        break
                    for idx, val in enumerate(new_split_line):
                        if val == '->':
                            func_end_idx = idx
                
                return split_line[func_end_idx+1]
        
        # print(split_line)
        # print(split_stripped_line)
        # print(token_idx)
        if ':' in split_line[token_idx]:
            if split_line[token_idx].replace(':', '') == split_stripped_line[token_idx]:
                # found potential type suggestion
                # print(f'type_hint: {split_line[token_idx+1]}')
                try:
                    return split_line[token_idx+1]
                except:
                    # this happens for lines that end in `:`, like `except OSError:`
                    return 'O'

    # return unknown character 'O' when a type is unknown
    return 'O'

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
        if count < 2057:
            count += 1
            continue
        total += 1
        count += 1
        target_file = os.path.join(dir_name, py_file)
        print(target_file)
        with open(target_file, 'rb') as f:
            out_file = os.path.join(TOKENIZED_FOLDER, py_file)
            with open(out_file, 'w', encoding='utf-8') as out:
                # parse each python file without hints so that each token is on a new line
                for five_tuple in tokenize.tokenize(f.readline):
                    _string = five_tuple.string
                    _type = tokenize.tok_name[five_tuple.type]
                    _exact_type = tokenize.tok_name[five_tuple.exact_type]
                    # print(five_tuple)
                    if _type == 'NEWLINE':
                        continue
                    if _string.strip() == '':
                        # get rid of whitespace
                        continue
                    if keyword.iskeyword(_string):
                        # label keywords
                        _exact_type = 'KEYWORD'
                    if _type == 'OP':
                        # remove operators
                        continue
                    _type_hint = find_type_hint(py_file, five_tuple)
                    print_str = f'{_string} {_type} {_exact_type} {_type_hint}'
                    # print(print_str)
                    # print(f'start: {five_tuple.start}')
                    # print(f'end: {five_tuple.end}')
                    # print(f'line: {five_tuple.line}')
                    print(print_str, file=out)

print(f'total: {total}')
print(f'total typed lines: {total_typed_tokens}')
print(f'total lines: {total_tokens}')