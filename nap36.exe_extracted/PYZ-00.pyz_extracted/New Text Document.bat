import os
import uncompyle6
your_directory = 'C:\Users\MUHAM\Desktop\New folder (3)\nap36.exe_extracted\PYZ-00.pyz_extracted'
for dirpath, b, filenames in os.walk(your_directory):
    for filename in filenames:
        if not filename.endswith('.pyc'):
            continue

        filepath = dirpath + '/' + filename
        original_filename = filename.split('.')[0]
        original_filepath = dirpath + '/' + original_filename + '.py'
        with open(original_filepath, 'w') as f:
            uncompyle6.decompile_file(filepath, f)