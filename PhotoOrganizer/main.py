from argparse import ArgumentParser
from os import listdir
from os.path import isfile, basename, abspath

from photo import Photo, NoExifError
from filesystem import list_dir_r



def main() -> None:
    parser = ArgumentParser()

    DEFAULT_MASK = '(yyyy)_(mm)_(dd)_(H)h(MM)m(SS)s'
    MASK_HELP = 'Mask defines file name basing on date and time when photo was taken. Meaning of symbols in mask: (yyyy), (yy) - year; '
    MASK_HELP += f'(mm), (m) - month; (dd), (d) - day; (HH), (H) - hour; (MM), (M) - minute; (SS), (S) - second. Default: {DEFAULT_MASK}'

    parser.add_argument('directory', action='store', help="Path to the photos directory", metavar=('directory'))
    parser.add_argument('-m', '--mask', action='store', help=MASK_HELP, default=DEFAULT_MASK, metavar=('mask'))
    parser.add_argument('-o', '--overwrite', action='store_true', help='overwrite duplicated names (default: rename duplicates)')
    parser.add_argument('-R', '--recursive', action='store_true', help='rename photos in all subdirectories (recursively)')
    
    args = vars(parser.parse_args())

    dir, mask, overwrite, recursive = args['directory'], args['mask'], args['overwrite'], args['recursive']
    
    dir_content = listdir(dir)
    total_elements = len(dir_content)
    done = 0

    files = list_dir_r(dir, recursive)

    for file_path in files:
        done += 1
        filename = basename(file_path)
        if not isfile(file_path):
            continue
        
        try:
            new_path = Photo(file_path).rename(mask, overwrite)
        except NoExifError: # no exif data
            new_path = filename + ' (NO EXIF DATA)'
        except IOError: # file is not a photo
            continue

        new_name = new_path.replace('/', '\\').split('\\')[-1]
        percentage = round(done / total_elements * 100, 2)
        print(f'[{percentage}%] {abspath(file_path)} => {new_name}')


if __name__ == '__main__':
    main()
