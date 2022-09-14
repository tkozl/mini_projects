from os import listdir
from os.path import isdir, isfile



def list_dir_r(dir :str, recursive :bool) -> list[str]:
    '''
    Listing directory content.
    Args:
        dir (str): path to directory
        recursive (bool): use recursive mode - returns files in all subdirectories
    Returns list of files patches
    '''

    dir_content = listdir(dir)
    files = []
    for item in dir_content:
        path = f'{dir}\\{item}'
        if isdir(path):
            if recursive:
                files += list_dir_r(path, recursive)
        elif isfile(path):
            files.append(path)

    return files
