import json
import argparse
import os

def clean_folder(folder, inplace=True, remove_errors=False):
    files = os.listdir(folder)
    for file in files:
        if len(file) <= 6 or file[-6:] != '.ipynb': # gets only the .ipynb
            if os.path.isdir(folder + '/' + file): # cleans subfolders too
                clean_folder(folder + '/' + file)
            continue
        print("cleaning: ", file)
        clean(os.path.join(folder, file), inplace=True, remove_errors=remove_errors)

def clean(filename, inplace=True, remove_errors=False):
    with open(filename) as f:
        ipynb_file = json.load(f)
        count = 0
        for cell in range(len(ipynb_file['cells'])):
            if ipynb_file['cells'][cell]['cell_type'] != 'code': # must be "code" cell
                continue
            if ipynb_file['cells'][cell]['execution_count'] is None: # cell must be run
                continue
            ipynb_file['cells'][cell]['execution_count'] = count + 1
            if len(ipynb_file['cells'][cell]['outputs']) > 0:
                if 'execution_count' in ipynb_file['cells'][cell]['outputs'][0]:
                    ipynb_file['cells'][cell]['outputs'][0]['execution_count'] = count + 1
                # removing errors
                if remove_errors and ipynb_file['cells'][cell]['outputs'][0]['output_type'] == 'error':
                    ipynb_file['cells'][cell]['outputs'] = []
            count += 1
        cleaned = json.dumps(ipynb_file)
        new = None
        if inplace:
            new = open(filename, 'w')
        else:
            new = open('cleaned.ipynb', 'w')
        new.write(cleaned)
        new.close()

# example
# clean('training.ipynb', inplace=True)
# command line:
# python clean.py <FOLDER_NAME> --remove_errors=True
parser = argparse.ArgumentParser(description='Jupyter File cleaner CLI interface')
parser.add_argument('target', type=str, help='File or folder you want cleaned')
parser.add_argument('--remove_errors', type=bool, help='True/False whether you want to remove error prints', default=False, required=False)

if __name__ == '__main__':
    args = parser.parse_args()
    target = args.target
    remove_errors = args.remove_errors

    if os.path.isfile(target):
        if len(target) <= 6 or target[-6:] != '.ipynb': # makes sure file is a jupyter file
            raise ValueError('Not an ipynb file')
        clean(target, inplace=True, remove_errors=remove_errors)
    elif os.path.isdir(target):
        clean_folder(target, inplace=True, remove_errors=remove_errors)
    else:
        raise ValueError('Given target is not a file or a directory')

