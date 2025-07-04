import re

def extract_title(mdFileContent: str) -> str:
    lines = mdFileContent.splitlines()
    for line in lines:
        result = re.match(r"^# (.+)", line)
        if result == None:
            continue
        return result.groups()[0]
    raise ValueError("Could not find title.")
