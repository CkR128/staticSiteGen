import re
import sys
import os
from os.path import isdir
import shutil

from markdown_handler import markdown_to_html
from page_hander import extract_title

source="static"
target="docs"

def deletePublic(target: str):
    if os.path.exists(f"./{target}"):
        print(f"Cleaning existing {target} directory.")
        shutil.rmtree(f"./{target}")

def copyDirectory(source, target, relativePath: str = ""):
    if os.path.exists(target + relativePath) == False:
        os.mkdir(target + relativePath)

    path = source + relativePath
    items = os.listdir(path)
    for item in items:
        itemPath = relativePath + f"/{item}"
        if os.path.isdir(source + itemPath):
            copyDirectory(source, target, itemPath)

        if os.path.isfile(source + itemPath):
            shutil.copy(source + itemPath, target + itemPath)

def generate_page(from_path, template_path, dest_path, rootWebPath=""):
    print(f"Generating page from {from_path} to {dest_path}, using {template_path}")

    if os.path.exists(from_path) == False:
        raise ValueError(f"from_path does not exist.")

    if os.path.exists(template_path) == False:
        os.makedirs(template_path)

    if os.path.exists(dest_path):
        raise ValueError(f"dest_path {dest_path} already exists")

    file = open(from_path, 'r')
    content = file.read()
    file.close() 

    template_file = open(template_path, 'r')
    template_content = template_file.read()
    template_file.close()

    html = markdown_to_html(content)
    htmlString = html.to_html()

    title = extract_title(content)
    final_content = re.sub(r"{{ Title }}", title, template_content)
    final_content = re.sub(r"{{ Content }}", htmlString, final_content)

    if rootWebPath != "":
        rootWebPath = f"{rootWebPath}/"
        final_content = final_content.replace(f"href=\"/", f"href=\"/{rootWebPath}")
        final_content = final_content.replace(f"src=\"/", f"src=\"/{rootWebPath}")

    file = open(dest_path, 'w')
    file.write(final_content)
    file.close()

def generate_pages_recursive(source, template_path, target, rootWebPath=""):
    def recurse(relativePath: str = ""):
        if os.path.exists(target + relativePath) == False:
            os.mkdir(target + relativePath)

        path = source + relativePath

        items = os.listdir(path)
        for item in items:
            itemPath = relativePath + f"/{item}"
            if os.path.isdir(source + itemPath):
                recurse(itemPath)

            result = re.match(r"(.+)\.md", item)
            if os.path.isfile(source + itemPath) and result:
                targetItem = f"{result.groups()[0]}.html"
                generate_page(source+itemPath, template_path, target+relativePath+"/"+targetItem, rootWebPath)

    recurse()

if __name__ == '__main__':
    rootWebPath = ""
    if len(sys.argv) > 1:
        rootWebPath = sys.argv[1]

    deletePublic(target)
    os.mkdir(f"{target}")
    copyDirectory(f"./{source}", f"./{target}")
    generate_pages_recursive("content", "template.html", target, rootWebPath)
