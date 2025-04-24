import os 

PATH_PROBA="proba"
for path, dirs, files in os.walk(PATH_PROBA):
    print (len(files))