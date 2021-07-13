'''數量平分後隨機分配數據'''
import random


def subset(alist, idxs):
    '''
        用法：根据下标idxs取出列表alist的子集
        alist: list
        idxs: list
    '''
    sub_list = []
    for idx in idxs:
        sub_list.append(alist[idx])

    return sub_list


def split_list_below(alist, group_num=4, shuffle=True, retain_left=False):
    '''
        用法：将alist切分成group个子列表，每个子列表里面有len(alist)//group个元素
        shuffle: 表示是否要随机切分列表，默认为True
        retain_left: 若将列表alist分成group_num个子列表后还要剩余，是否将剩余的元素单独作为一组
    '''

    length = len(alist)
    index = list(range(length))  # 保留下标

    # 是否打乱列表
    if shuffle:
        random.shuffle(index)

    elem_num = length // group_num  # 每一个子列表所含有的元素数量
    sub_lists = {}

    # 取出每一个子列表所包含的元素，存入字典中
    for idx in range(group_num):
        start, end = idx * elem_num, (idx + 1) * elem_num
        sub_lists['set' + str(idx)] = subset(alist, index[start:end])

    # 是否将最后剩余的元素作为单独的一组
    if retain_left and group_num * elem_num != len(index):  # 列表元素数量未能整除子列表数，需要将最后那一部分元素单独作为新的列表
        sub_lists['set' + str(idx + 1)] = subset(alist, index[end:])

    return sub_lists


def split_list_above(alist,user_list,group_num,shuffle=True, shortage="空", shortage_exist=True):
    '''
    將 alist 切分成 group_name個子列表， 每个子列表里面有len(alist)//group个元素。
    多餘的元素重新隨機再分配到這些子列表中，沒分到的添加補充字段
    :param shortage: 補缺字段
    :param shortage_exist: True 保留 shortage 字段， False: 不保留
    :return:
    '''
    import math
    length = len(alist)
    index = list(range(length))  # 保留下标


    if len(alist) % group_num != 0:
        much = math.ceil(length / group_num) * group_num - length
        alist = list(alist) + much * [shortage]
        length = length + much
        index = list(range(length))

    # 是否打乱列表
    if shuffle:
        random.shuffle(index)

    elem_num = length // group_num  # 每一个子列表所含有的元素数量
    sub_lists = {}

    # 判斷是否需要保留補缺字段
    # 取出每一个子列表所包含的元素，存入字典中
    if shortage_exist:
        for idx in range(group_num):
            start, end = idx * elem_num, (idx + 1) * elem_num
            sub_lists[user_list[idx]] = subset(alist, index[start:end])
    else:
        for idx in range(group_num):
            start, end = idx * elem_num, (idx + 1) * elem_num
            sub_lists[user_list[idx]] = list(filter(lambda x: x != shortage, subset(alist, index[start:end])))

    return sub_lists


if __name__ == '__main__':
    user=["a","b","c","d"]
    print(split_list_above(range(50), user_list=user,group_num=4, shuffle=True, shortage="None", shortage_exist=False))
