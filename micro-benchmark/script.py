import subprocess
import json

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def compare_json(file1, file2):
    json1 = load_json(file1)
    json2 = load_json(file2)
    return json1 == json2


def sort_values(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, list):
                data[key] = sorted(value)
            elif isinstance(value, dict):
                sort_values(value)
    elif isinstance(data, list):
        for item in data:
            sort_values(item)

def compare_json_files(file1_path, file2_path):
    # 读取第一个JSON文件
    with open(file1_path, 'r', encoding='utf-8') as file1:
        data1 = json.load(file1)

    # 读取第二个JSON文件
    with open(file2_path, 'r', encoding='utf-8') as file2:
        data2 = json.load(file2)

    #sorted_data1 = json.dumps(data1, sort_keys=True)
    #sorted_data2 = json.dumps(data2, sort_keys=True)

    sort_values(data1)
    sort_values(data2)

    # 检查键值对是否完全相同
    return data1 == data2
    #if sorted_data1 == sorted_data2:
    #    print("两个JSON文件的内容完全相同。")
    #else:
    #    print("两个JSON文件的内容不相同。")


test_path = "C:\\Users\\misty\\OneDrive\\桌面\\NewPyCG\\micro-benchmark\\args\\assigned_call"
test_file = test_path + "\main.py"
file1_path = "C:/Users/misty/OneDrive/桌面/NewPyCG/cg.json"
file2_path = "C:/Users/misty/OneDrive/桌面/NewPyCG/cg2.json"
file3_path = test_path + "\callgraph.json"


# 定义命令行命令
command = [
    "python",             # Python解释器
    "C:/Users/misty/OneDrive/桌面/NewPyCG/pycg/__main__.py",  # 要执行的脚本路径
    test_file,  # 参数1
    "--package",          # 参数2
    test_path,  # 参数3
    "-o",                 # 参数4
    "cg.json"             # 参数5
]

command2 = [
    "python",             # Python解释器
    "C:/Users/misty/OneDrive/桌面/设备SDK/PyCG-main/PyCG-main/pycg/__main__.py",  # 要执行的脚本路径
    test_file,  # 参数1
    "--package",          # 参数2
    test_path,  # 参数3
    "-o",                 # 参数4
    "cg2.json"             # 参数5
]

# 执行命令
try:
    result = subprocess.run(command, check=True)
    result2 = subprocess.run(command2, check=True)
    print("命令执行成功")
except subprocess.CalledProcessError as e:
    print("命令执行失败:", e)


result1 = compare_json_files(file1_path, file2_path)
if result1:
    print("PyDECG与PyCG结果相同")
else:
    print("PyDECG与PyCG结果不同")

print("_________________")
result2 = compare_json_files(file2_path, file3_path)
if result2:
    print("PyCG与GroundTruth结果相同")
else:
    print("PyCG与GroundTruth结果不同")

print("_________________")
result1 = compare_json_files(file1_path, file3_path)
if result1:
    print("PyDECG与GroundTruth结果相同")
else:
    print("PyDECG与GroundTruth结果不同")

print("_________________")