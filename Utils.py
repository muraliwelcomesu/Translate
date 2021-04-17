import os

# checks if the given file is available in a specific folder. Return true if file found, false otherwise.
def CheckFile(dir_name,file_name):
    os.chdir(dir_name)
    for p_filename in os.listdir():
        if file_name.upper() == p_filename.upper():
            return True
    return False

def is_srt_File(file_name):
    if file_name.endswith('.srt'):
        return True
    else:
        return False

def is_xlsx_File(file_name):
    if file_name.endswith('.xlsx'):
        return True
    else:
        return False
    
def GetFilesList(dir_name,extn):
    os.chdir(dir_name)
    files = filter(os.path.isfile, os.listdir(dir_name))
    if extn == 'srt':
        files = filter(is_srt_File, files)
    elif extn == 'xlsx':
        files = filter(is_xlsx_File, files)
    return files
