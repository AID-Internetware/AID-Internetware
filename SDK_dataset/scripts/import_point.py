import os

#C:/Users/40382/Desktop/NewPyCG/pycg/examples/inherit
#C:\Users/40382\Desktop\NewPyCG\pycg\examples\jaraco.abode-5.1.0\jaraco\abode
directory = "C:/Users/40382/Desktop/NewPyCG/SDK_dataset/pymystrom"



def process_file(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        lines = file.readlines()

    modified = False
    new_lines = []
    for line in lines:

        if 'from .' in line and '. ' not in line:
            modified_line = line.replace('...','.').replace('..','.').replace('from .', 'from ')
            new_lines.append(modified_line)
            modified = True

        elif 'from . ' in line and '. ' in line:
            modified_line = line.replace('from .... ', '').replace('from ... ', '').replace('from .. ', '').replace('from . ', '')
            new_lines.append(modified_line)
            modified = True
        else:
            new_lines.append(line)



    if modified:
        with open(file_path, 'w', encoding="utf-8") as file:
            file.writelines(new_lines)

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                process_file(file_path)

if __name__ == '__main__':
    process_directory(directory)


