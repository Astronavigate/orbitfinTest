import re

def reg_search(text):
    # 正则表达式字典，包含标的证券和换股期限的匹配规则
    regex_dict = {
        '标的证券': r'(\d{6}\.\b[a-zA-Z]{2})',  # 匹配股票代码
        '换股期限': r'(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日'  # 匹配日期格式（2023 年 6 月 2 日）
    }

    # 存储最终结果的字典
    result = {}

    # 对每个字段进行匹配
    for key, pattern in regex_dict.items():
        matches = re.findall(pattern, text)

        # 对匹配到的日期进行格式化
        if key == '换股期限' and matches:
            # 格式化为 yyyy-mm-dd 格式
            result[key] = [f"{match[0]}-{int(match[1]):02d}-{int(match[2]):02d}" for match in matches]
        else:
            result[key] = matches if matches else None

    # 格式化输出，确保符合要求
    formatted_result = "[{"

    # 遍历每个键值对并按要求格式化，最后去除多余的逗号
    formatted_result += "\n" + "\n".join([f"'{key}': {value}" for key, value in result.items()])

    # 添加结尾部分
    formatted_result += "\n}]"

    return formatted_result


if __name__ == '__main__':
    # 测试示例
    text = '''
    标的证券：本期发行的证券为可交换为发行人所持中国长江电力股份
    有限公司股票（股票代码：600900.SH，股票简称：长江电力）的可交换公司债
    券。
    换股期限：本期可交换公司债券换股期限自可交换公司债券发行结束
    之日满 12 个月后的第一个交易日起至可交换债券到期日止，即 2023 年 6 月 2
    日至 2027 年 6 月 1 日止。
    '''

    # 调用函数获取格式化后的结果
    formatted_result = reg_search(text)

    # 打印结果
    print(formatted_result)
