import csv
import os
import shutil
import sys
import pandas as pd

def check(dir):
    """
    :param dir: 输入路径
    :return: 输出每一个机型对应的内参外参png数据以及csv数据，写在字典里
    """
    list1 = os.listdir(dir)
    remdic = {} #创建一个字典记录每一个手机对应的png文件数量
    num = 0
    deallist = [] #创建一个输出要处理的机型列表
    print("开始处理数据，请等待...")
    for phone in list1:
        if "DS_Store" not in phone:
            num = num + 1
            print(f"已处理 {phone} ...")
            try:
                data_png_n = os.listdir(f"{dir}/{phone}/cam-imu/cam/mav0/cam0/data")  # 读取内参的png数据
                # print(f'手机型号是{phone} 数据量是：{len(data_png_n)}')
                # 读取内参的csv文件
                n_csv = csv_read(f"{dir}/{phone}/cam-imu/cam/mav0/cam0/data.csv")  # 读取的内参csv文件行数
                info_n_csv = {f'{phone}_n_csv': n_csv}
                info_n = {f'{phone}_n': len(data_png_n)}
                remdic.update(info_n)
                remdic.update(info_n_csv)
                data_png_w = os.listdir(f"{dir}/{phone}/cam-imu/cam-imu/mav0/cam0/data")  # 读取外参的png数据
                # 读取外参的csv文件
                w_csv = csv_read(f"{dir}/{phone}/cam-imu/cam-imu/mav0/cam0/data.csv")
                info_w_csv = {f'{phone}_w_csv': w_csv}
                info_w = {f'{phone}_w': len(data_png_w)}

                remdic.update(info_w)
                remdic.update(info_w_csv)
                if len(data_png_n) == n_csv and len(data_png_w) == w_csv:
                    pass
                else:
                    deallist.append(phone)
            except FileNotFoundError:
                print(f'找不到文件异常 {phone}')
            except NotADirectoryError:
                print(f'文件异常 {phone}')

        info_num = {'info_num':num}
        remdic.update(info_num)

    # print(remdic)
    print(f"共处理文件 {num} 个\n")
    print(f"需要处理的机型如下:")
    for ph in deallist:
        print(ph)
    print('\n')
    return deallist

def deal(dir,data):
    """
    :return: 输入为data的列表，将其中的所有数据做处理
    """
    for phone in data:
        data_png_n = os.listdir(f"{dir}/{phone}/cam-imu/cam/mav0/cam0/data")  # 读取内参的png数据
        n_csv = csv_read(f"{dir}/{phone}/cam-imu/cam/mav0/cam0/data.csv")
        data_png_w = os.listdir(f"{dir}/{phone}/cam-imu/cam-imu/mav0/cam0/data")  # 读取外参的png数据
        w_csv = csv_read(f"{dir}/{phone}/cam-imu/cam-imu/mav0/cam0/data.csv")
        if len(data_png_n) > n_csv:  #如果图片数量大于csv数量则删除最新的一张图片
            dir2 = f"{dir}/{phone}/cam-imu/cam/mav0/cam0/data"
            data_png_n.sort(key=lambda f: os.path.getmtime(dir2 + '/' + f))
            delete_path = os.path.join(dir2,data_png_n[-1])
            os.remove(delete_path)
            print(f'删除成功，文件是 {delete_path}')
        elif len(data_png_n) < n_csv: #若csv数量大于图片则删除多余的csv数据
            del_csv(f"{dir}/{phone}/cam-imu/cam/mav0/cam0/data.csv",len(data_png_n))
            print(f'处理的文件是 {dir}/{phone}/cam-imu/cam/mav0/cam0/data.csv')
        elif int(len(data_png_w)) > int(w_csv):
            dir2 = f"{dir}/{phone}/cam-imu/cam-imu/mav0/cam0/data"
            data_png_w.sort(key=lambda f: os.path.getmtime(dir2 + '/' + f))
            delete_path = os.path.join(dir2, data_png_w[-1])
            os.remove(delete_path)
            print(f'删除成功，文件是 {delete_path}')
        elif len(data_png_w) < w_csv:
            del_csv(f"{dir}/{phone}/cam-imu/cam-imu/mav0/cam0/data.csv",len(data_png_w))
            print(f'已处理的文件是 {dir}/{phone}/cam-imu/cam-imu/mav0/cam0/data.csv')

def test(dir):
    list = os.listdir(dir)
    # print(list[-1]) #读取的最后一个并非是文件路径下的最后一个
    for name in list:
        print(name)

def new_file(path):
    lists = os.listdir(path)
    lists.sort(key= lambda f: os.path.getmtime(path + '/' + f))
    file_path = os.path.join(path, lists[-1])
    print(file_path)
    return file_path

def delete():
    # shutil.rmtree('/Users/jackrechard/Desktop/change_test/OPPO_A11X_PCHM30/cam-imu/cam/mav0/cam0/data/1636704704961349010的副本2.png')
    os.remove('/Users/jackrechard/Desktop/change_test/OPPO_A11X_PCHM30/cam-imu/cam/mav0/cam0/data/1636704704961349010的副本2.png')
    print('删除成功')

def deletecsv(csvdir):
    df = pd.read_csv(csvdir)
    # data_new = df.drop(columns=["234"])
    data_new = df.drop(444)
    # data_new = df.drop(1010)
    data_new.to_csv(csvdir, index=0)
    print('删除成功')

def csv_read(csvdir):
    """
    :param csvdir: csv文件路径
    :return: 输出csv的行数
    """
    with open(csvdir) as f:
        rows = csv.reader(f) #reader返回一个可迭代的对象，按行
        rrr = 0 #定义行数
        for row in rows:
            # print(row)
            rrr = rrr +1
    # print(rrr)
    return rrr

def del_csv(csvdir,num):
    """
    :param csvdir: 传入要处理的csv路径
    :param num: 传入希望输出的行数
    :return:会修改输入的csv文件
    """
    with open(csvdir) as f:
        # test = ['header1', 'header2', 'header3', 'header4', 'header5']
        # test2 = [
        #     [1, 'xiaoming', 'male', 168, 23],
        #     [2, 'xiaohong', 'female', 162, 22],
        #     [3, 'xiaozhang', 'female', 163, 21],
        # ]
        # test3 = [['1.64E+18', '1636704671404999971.png'],
        #          ['1.64E+18', '1636704671438366890.png'],
        #          ['1.64E+18', '1636704671471809864.png']]
        rows = csv.reader(f)
        rows_new = []
        i = 0
        for row in rows:
            i = i + 1
            if i <= num :
                rows_new.append(row)

    with open(csvdir, 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(rows_new)
    # print('del_csv处理完成')
    # print(rows_new)

if __name__ == '__main__':
    # test('/Users/jackrechard/Desktop/change_test/OPPO_A11X_PCHM30/cam-imu/cam/mav0/cam0/data')
    # new_file('/Users/jackrechard/Desktop/change_test/OPPO_A11X_PCHM30/cam-imu/cam/mav0/cam0/data')
    # delete('/Users/jackrechard/Desktop/change_test/OPPO_A11X_PCHM30/cam-imu/cam/mav0/cam0/data.csv')

    # data = check('/Volumes/calibration/第二批已转换png/已好')
    # csv_read('/Users/jackrechard/Desktop/change_test/OPPO_A11X_PCHM30/cam-imu/cam/mav0/cam0/data.csv')
    # del_csv('/Users/jackrechard/Desktop/change_test/OPPO_A11X_PCHM30/cam-imu/cam/mav0/cam0/dataddd.csv',1007)
    # deletecsv('/Users/jackrechard/Desktop/change_test/OPPO_A11X_PCHM30/cam-imu/cam/mav0/cam0/data.csv')
    """
    编译运行
    """
    # data = check('/Users/jackrechard/Desktop/change_test')
    # deal('/Users/jackrechard/Desktop/change_test',data)

    """
    命令行运行
    """
    path = sys.argv[1]
    data = check(path)
    deal(path, data)