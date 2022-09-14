from PIL import Image, ExifTags
from os import rename, unlink
from os.path import isfile
from datetime import datetime



class NoExifError(Exception):
    '''Exception raises when image has no EXIF data'''
    pass


class Photo:
    '''Getting time when photo was taken and renaming photo basing on mask'''

    def __init__(self, photo_path :str) -> None:
        self.__path = photo_path

        image_exif = Image.open(self.__path)._getexif()
        if image_exif:
            # Make a map with tag names
            exif = { ExifTags.TAGS[k]: v for k, v in image_exif.items() if k in ExifTags.TAGS and type(v) is not bytes }
            self.__date_obj = datetime.strptime(exif['DateTimeOriginal'], '%Y:%m:%d %H:%M:%S')
        else:
            self.__date_obj = None
    
    def rename(self, mask :str, overwrite :bool) -> str:
        '''
        Rename file basing on mask.
        Args:
            mask (str): mask of the name
            overwrite (bool): overwrite duplicate names if True or attach number to the file name if False
        Returns new file name
        '''
        new_name = NameMask(mask).create_name(self.taken_time, self.__path)
        base_name = new_name
        extension = ''
        if '.' in new_name:
            base_name = ''.join(x + '.' for x in new_name.split('.')[:-1])[:-1]
            extension = '.' + new_name.split('.')[-1]
        n = 0
        if not overwrite:
            while isfile(new_name):
                n += 1
                new_name = base_name + f' ({n})' + extension
        else:
            if isfile(new_name):
                unlink(new_name)
        rename(self.__path, new_name)
        return new_name
    
    @property
    def taken_time(self) -> datetime:
        '''Returns time when photo was taken in datetime format'''
        if self.__date_obj != None:
            return self.__date_obj
        else:
            raise NoExifError('No EXIF data in file')


class NameMask:

    def __init__(self, mask :str):
        '''
        Mask can contains:
        (yyyy), (yy) - year
        (mm), (m) - month
        (dd), (d) - day
        (HH), (H) - hour
        (MM), (M) - minute
        (SS), (S) - second
        '''
        self.__template = mask
    
    def create_name(self, date :datetime, original_name :str) -> str:
        '''Creates and returns filename basing on mask'''
        
        add_zero_prefix = lambda x : f'0{x}' if x < 10 else str(x)

        name = self.__template.replace('(d)', str(date.day)).replace('(m)', str(date.month)).replace('(yyyy)', str(date.year))
        name = name.replace('(H)', str(date.hour)).replace('(M)', str(date.minute)).replace('(S)', str(date.second))
        dd = add_zero_prefix(date.day)
        name = name.replace('(dd)', str(dd))

        name = name.replace('(yy)', str(date.year)[-2:])
        name = name.replace('(mm)', add_zero_prefix(date.month))
        name = name.replace('(SS)', add_zero_prefix(date.second))
        name = name.replace('(MM)', add_zero_prefix(date.minute))
        name = name.replace('(HH)', add_zero_prefix(date.hour))

        if '.' in original_name:
            extension = original_name.split('.')[-1]
            name += '.' + extension.lower()
        dir_loc = ''.join(x + '\\' for x in original_name.replace('/', '\\').split('\\')[:-1])
        name = dir_loc + name

        return name
