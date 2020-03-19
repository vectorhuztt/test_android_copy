#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/10/31 16:33
# -----------------------------------------


def dict_slice(split_dict, start=None, end=None):
    result_dict = {}
    keys = list(split_dict.keys())
    if start is None:
        start_index = 0
    else:
        start_index = start

    if end is None:
        end_index = len(split_dict)
    else:
        end_index = end

    for k in keys[start_index:end_index]:
        result_dict[k] = split_dict[k]
    return result_dict
