import os


#directory = 'C:/Users/40382/Desktop/NewPyCG/scripts/test' 
directory = "C:/Users/40382/Desktop/NewPyCG/SDK_dataset/pymystrom"


def remove_await_in_files(directory):

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)

                with open(file_path, 'r', encoding="utf-8") as f:
                    file_content = f.read()
                file_content = file_content.replace('await ', '')

                with open(file_path, 'w', encoding="utf-8") as f:
                    f.write(file_content)


remove_await_in_files(directory)