import os
import temp_dict
from filer import LinkFile
my_path = r'D:\python_home\python_full_course\to_rename'

json_links_file = 'links.json'
link_range = input('file range: ')
range_start = int(link_range.split('-')[0]) - 1
range_end = int(link_range.split('-')[1])

link_dict = LinkFile.read_links(json_links_file)
link_dict_range = link_dict["links"][range_start:range_end]


list_of_files = os.listdir(my_path)
print(list_of_files)

match_count = 0
for file in list_of_files:
    full_file = file
    file = file.split('.')[0]
    match_per_file = 0
    for dict_item in link_dict_range:
        if file == dict_item[0].replace(':', '').replace('.', '').replace('?', ''):
            vid_num = dict_item[1].split('-video')[1][:-1]
            print(f'{file} | {dict_item[0]} | {dict_item[1]} | {vid_num}')
            file1 = os.path.join(my_path, full_file)
            new_file = f'{vid_num}_{full_file}'.replace(' ','_')
            file2 = os.path.join(my_path, new_file)
            print(file1)
            print(file2)
            #os.rename(file1, file2)
            match_per_file += 1
            match_count += 1

        if match_per_file > 1:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    if match_per_file == 0:
        print(f'>>>>> "{file}" was not recognized')

print(len(list_of_files))
print(match_count)