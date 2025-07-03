import os
from os.path import isdir
import shutil

source="static"
target="public"

def deletePublic():
    if os.path.exists(f"./{target}"):
        print("Cleaning existing public directory.")
        shutil.rmtree(f"./{target}")

def copyDirectory(source, target, relativePath: str = ""):
    if os.path.exists(target + relativePath) == False:
        os.mkdir(target + relativePath)

    path = source + relativePath
    items = os.listdir(path)
    for item in items:
        itemPath = relativePath + f"/{item}"
        print(source + itemPath)
        if os.path.isdir(source + itemPath):
            print(f"iterating on {source + itemPath}")
            copyDirectory(source, target, itemPath)

        if os.path.isfile(source + itemPath):
            print(f"copying {source + itemPath} to {target + itemPath}")
            shutil.copy(source + itemPath, target + itemPath)


if __name__ == '__main__':
    deletePublic()
    os.mkdir(f"{target}")
    copyDirectory(f"./{source}", f"./{target}")
    
