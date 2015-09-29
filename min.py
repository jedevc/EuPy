#Build a single file containing all of eupy!

import re

def main():
    #Find all the files to concentrate
    files = []
    with open("euphoria/__init__.py", 'r') as f:
        lines = f.read().split('\n')
        for l in lines:
            matches = re.search("from \. import (\S*)", l)
            if matches:
                files.append(matches.group(1))

    #Find all the imports
    imports = [x for x in files]
    for filename  in files:
        with open("euphoria/%s.py" % filename, 'r') as f:
            contents = f.read().split('\n')
            for c in contents:
                matches = re.search("import (\S*)", c)
                if matches:
                    if matches.group(1) not in imports:
                        imports.append(matches.group(1))
                        print(matches.group(0))

    #Open the files individually and output them
    for filename in files:
        with open("euphoria/%s.py" % filename, 'r') as f:
            contents = f.read().split('\n')
            print("class %s:" % filename)
            for c in contents:
                if not re.search("import (\S*)", c):
                    print(4 * " " + c)

if __name__ == "__main__":
    main()
