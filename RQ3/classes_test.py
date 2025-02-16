import subprocess
from compare import compare_json_files

def DECG_run(source_path, test_file, test_category):
    command = [
        "python",         
        source_path,  
        test_file,  
        "--package",         
        test_category,  
        "-o",                 
        "RQ3\cg.json"             
    ]
    return command

def PyCG_run(source_path, test_file, test_category):
    command = [
        "python",            
        source_path, 
        test_file,  
        "--package",          
        test_category,  
        "-o",                
        "RQ3\cg2.json"         
    ]
    return command

if __name__ == "__main__":

    DECG_path = r'AID\__main__.py'
    PyCG_path = r'pycg\__main__.py'
    test_path = r'micro-benchmark\classes'
    categories = [r'\assigned_call', r'\assigned_self_call', r'\base_class_attr', r'\base_class_calls_child', r'\call', r'\direct_call',
                  r'\imported_attr_access', r'\imported_call', r'\imported_call_without_init', r'\imported_nested_attr_access', r'\instance', r'\nested_call',
                  r'\nested_class_calls', r'\parameter_call', r'\return_call', r'\return_call_direct', r'\self_assign_func', r'\self_assignment',
                  r'\self_call', r'\static_method_call', r'\super_class_return', r'\tuple_assignment']

    DECG_accuracy = 0
    PyCG_accuracy = 0

    for category in categories:
        
        test_category = test_path + category

        test_file = test_category + r'\main.py'
        
        file1_path = r'RQ3\cg.json'
        file2_path = r'RQ3\cg2.json'
        file3_path = test_category + r'\callgraph.json'

        result = subprocess.run(DECG_run(DECG_path, test_file, test_category), check=True)
        result2 = subprocess.run(PyCG_run(PyCG_path, test_file, test_category), check=True)

        result1 = compare_json_files(file1_path, file3_path)
        if result1:
            DECG_accuracy += 1

        result2 = compare_json_files(file2_path, file3_path)
        if result2:
            PyCG_accuracy += 1
        print("Testing: " + test_path + category)
        print("DECG Accuracy: " + str(DECG_accuracy) + "/" + str(len(categories)))
        print("PyCG Accuracy: " + str(PyCG_accuracy) + "/" + str(len(categories)))
        print("_________________")


    