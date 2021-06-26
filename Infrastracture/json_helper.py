import json


def load_json(path):
    lines = []  # 第一步：定义一个列表， 打开文件
    with open(path, encoding='utf-8') as f:
        for row in f.readlines():  # 第二步：读取文件内容
            if row.strip().startswith("//"):   # 第三步：对每一行进行过滤
                continue
            lines.append(row)                   # 第四步：将过滤后的行添加到列表中.
    # 将列表中的每个字符串用某一个符号拼接为一整个字符串，用json.loads()函数加载，这样就大功告成啦！！
    return json.loads("\n".join(lines))
