from read_roi import read_roi_file
import os
import shutil

file_path = "0001_03_pl.roi"
file = "0001_01_pl.roi"
src = 'D:/waste_data/roi/hoil/'
dir = 'D:/waste_data/roi/nr/'

# for file in os.listdir(src):
# shutil.move(src + file_path, dir + file)

# roi = read_roi_file(dir + file)
# print(roi)
count = 15052
a = ''
# for a in os.listdir(src):
#     file_name = os.listdir(src+a)
#     file_ma = src+a+'/'
#     print(file_ma)
for file in os.listdir(src):
    if file.endswith('.roi'):
        if a == file.split('_')[0]:
            if count < 10:
                file_path = '0000' + str(count-1) + '_' + file.split('_')[1] + '_' + file.split('_')[2]
            elif count < 100:
                file_path = '000' + str(count-1) + '_' + file.split('_')[1] + '_' + file.split('_')[2]
            elif count < 1000:
                file_path = '00' + str(count-1) + '_' + file.split('_')[1] + '_' + file.split('_')[2]
            elif count < 10000:
                file_path = '0' + str(count-1) + '_' + file.split('_')[1] + '_' + file.split('_')[2]
            else:
                file_path = str(count-1) + '_' + file.split('_')[1] + '_' + file.split('_')[2]
        else:
            if count < 10:
                file_path = '0000' + str(count) + '_' + file.split('_')[1] + '_' + file.split('_')[2]
            elif count < 100:
                file_path = '000' + str(count) + '_' + file.split('_')[1] + '_' + file.split('_')[2]
            elif count < 1000:
                file_path = '00' + str(count) + '_' + file.split('_')[1] + '_' + file.split('_')[2]
            elif count < 10000:
                file_path = '0' + str(count) + '_' + file.split('_')[1] + '_' + file.split('_')[2]
            else:
                file_path = str(count) + '_' + file.split('_')[1] + '_' + file.split('_')[2]
    elif file.endswith('.jpg'):
        a = file.split('.')[0]
        if count < 10:
            file_path = '0000' + str(count) + '.jpg'
        elif count < 100:
            file_path = '000' + str(count) + '.jpg'
        elif count < 1000:
            file_path = '00' + str(count) + '.jpg'
        elif count < 10000:
            file_path = '0' + str(count) + '.jpg'
        else:
            file_path = str(count) + '.jpg'
        count += 1
    shutil.move(src + file, dir + file_path)
    # elif file.endswith('.jpg'):
    #     print(file)