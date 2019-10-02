import json
import argparse
import os

# clean folder code
def clean_folder(folder, inplace=True):
    files = os.listdir(folder)
    for file in files:
        if len(file) <= 6 or file[-6:] != '.ipynb': # gets only the .ipynb
            continue
        print("cleaning: ", file)
        clean(os.path.join(folder, file), inplace=True)

# clean file code
def clean(filename, inplace=True):
    with open(filename) as f:
        ipynb_file = json.load(f)
        count = 0
        for cell in range(len(ipynb_file['cells'])):
            if ipynb_file['cells'][cell]['cell_type'] != 'code': # must be "code" cell
                continue
            if ipynb_file['cells'][cell]['execution_count'] is None: # cell must be run
                continue
            ipynb_file['cells'][cell]['execution_count'] = count + 1
            if len(ipynb_file['cells'][cell]['outputs']) > 0 and 'execution_count' in ipynb_file['cells'][cell]['outputs'][0]:
                ipynb_file['cells'][cell]['outputs'][0]['execution_count'] = count + 1
            count += 1
        cleaned = json.dumps(ipynb_file)
        new = None
        if inplace:
            new = open(filename, 'w')
        else:
            new = open('cleaned.ipynb', 'w')
        new.write(cleaned)
        new.close()

# example usage
# clean('training.ipynb', inplace=True)

# command line usage
# python clean.py [PATH TO DIRECTORY]
parser = argparse.ArgumentParser(description='Jupyter File cleaner CLI interface')
parser.add_argument('target', type=str, help='File or folder you want cleaned')

if __name__ == '__main__':
    args = parser.parse_args()
    target = args.target
    if os.path.isfile(target):
        if len(target) <= 6 or target[-6:] != '.ipynb': # makes sure file is a jupyter file
            raise ValueError('Not an ipynb file')
        clean(target, inplace=True)
    elif os.path.isdir(target):
        clean_folder(target, inplace=True)
    else:
        raise ValueError('Given target is not a file or a directory')

