import os


def get_lambda_name(counter):
    return "<lambda{}>".format(counter)


def get_dict_name(counter):
    return "<dict{}>".format(counter)


def get_list_name(counter):
    return "<list{}>".format(counter)


def get_int_name(counter):
    return "<int{}>".format(counter)


def join_ns(*args):
    return ".".join([arg for arg in args])


def to_mod_name(name, package=None):
    return os.path.splitext(name)[0].replace("/", ".")


def equal_attribute(method1, method2):
    if method1 == method2:
        return True
    md1 = method1.replace("\\", ".")
    md2 = method2.replace("\\", ".")

    if md1 in md2:
        long = md2
        short = md1
    elif md2 in md1:
        long = md1
        short = md2
    else:
        return False
    
    if long.split(short)[-1] == '' and long.split(short)[0][-1] == '.':
        return True
    else:
        return False



def is_method_node(candidate, methodset):

    if candidate in methodset:
        return True

    for method in methodset:
        m1 = candidate.split("\\")[-1]
        m2 = method.split("\\")[-1]

        if m1 in m2:
            return True
        
        if m2 in m1 and m1.split(m2)[-1] == '':
            return True
    
    return False
