# 打开txt文件，去除重复的magnet值
# 然后按原始循序保存新列表到txt文件中

with open('babes.txt', 'r', encoding='utf-8') as f:
    content = f.readlines()
    print(content)
    print(len(content))
    list_new = sorted(set(content), key=content.index)
    print(len(list_new))

with open('new_111.txt', 'w', encoding='utf-8') as f:
    for i in list_new:
        f.write(i)


