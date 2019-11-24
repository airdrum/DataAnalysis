directory = "/home/sy/Backup Data/Compressed Files"

import os
dir_list = os.listdir(directory)
compressed_list= []
for i in dir_list:
    if "samet_2019" in i:
        compressed_list.append(i)

compressed_list.sort()
print("***************************")
for i in compressed_list:
    print(i)