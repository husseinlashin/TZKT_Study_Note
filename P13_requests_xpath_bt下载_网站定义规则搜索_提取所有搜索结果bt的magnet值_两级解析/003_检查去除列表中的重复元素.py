

with open('tushy.txt', 'r', encoding='utf-8') as f:
    content = f.readlines()
    print(content)
    print(len(content))
    list_new = sorted(set(content), key=content.index)
    print(len(list_new))
