# PhotoOrganizer
## Description
This application allows to rename all pictures in specified directory basing on date when pictures were taken.

## Usage
To rename pictures in directory just run `main.py` in terminal with directory path as an argument.

Default mask of photos names is `(yyyy)_(mm)_(dd)_(H)h(MM)m(SS)s`. You can change it using `-m mask` argument.
Meaning of possible symbols in mask:
* (yyyy), (yy) - year
* (mm), (m) - month
* (dd), (d) - day
* (HH), (H) - hour
* (MM), (M) - minute
* (SS), (S) - second
Apliccation will not overwrite duplicates names by default (it will add number on the end of the photo name). You can change it using `-o` argument.

To rename photos in all subdirectories use `-R` argument

Use `-h` argument to see program manual