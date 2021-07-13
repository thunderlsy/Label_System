import re


def strQ2B(ustring):
    """中文特殊符号转英文特殊符号"""
    # 中文特殊符号批量识别

    pattern = re.compile('[，。：“”【】《》？；、（）‘’『』「」﹃﹄〔〕—·]')

    # re.compile: 编译一个正则表达式模式，返回一个模式（匹配模式）对象。
    # [...]用于定义待转换的中文特殊符号字符集

    fps = re.findall(pattern, ustring)

    # re.findall: 搜索string，以列表形式返回全部能匹配的子串。

    # 对有中文特殊符号的文本进行符号替换
    #
    if len(fps) > 0:
        ustring = ustring.replace('，', ',')
        ustring = ustring.replace('。', '.')
        ustring = ustring.replace('：', ':')
        ustring = ustring.replace('“', '"')
        ustring = ustring.replace('”', '"')
        ustring = ustring.replace('【', '[')
        ustring = ustring.replace('】', ']')
        ustring = ustring.replace('《', '<')
        ustring = ustring.replace('》', '>')
        ustring = ustring.replace('？', '?')
        ustring = ustring.replace('；', ':')
        ustring = ustring.replace('、', ',')
        ustring = ustring.replace('（', '(')
        ustring = ustring.replace('）', ')')
        ustring = ustring.replace('‘', "'")
        ustring = ustring.replace('’', "'")
        ustring = ustring.replace('’', "'")
        ustring = ustring.replace('『', "[")
        ustring = ustring.replace('』', "]")
        ustring = ustring.replace('「', "[")
        ustring = ustring.replace('」', "]")
        ustring = ustring.replace('﹃', "[")
        ustring = ustring.replace('﹄', "]")
        ustring = ustring.replace('〔', "{")
        ustring = ustring.replace('〕', "}")
        ustring = ustring.replace('—', "-")
        ustring = ustring.replace('·', ".")

    """半角转全角"""
    # 转换说明：
    # 全角字符unicode编码从65281~65374 （十六进制 0xFF01 ~ 0xFF5E）
    # 半角字符unicode编码从33~126 （十六进制 0x21~ 0x7E）
    # 空格比较特殊，全角为 12288（0x3000），半角为 32（0x20）
    # 除空格外，全角/半角按unicode编码排序在顺序上是对应的（半角 + 0x7e= 全角）,所以可以直接通过用+-法来处理非空格数据，对空格单独处理。
    # 48--57 是半角數字範圍, 65--90 是半角大寫字母, 97--122 是半角小寫字母

    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 32:  # 半角空格直接转换
            inside_code = 12288
        elif (inside_code >= 123 and inside_code <= 126):  # 半角字符（除空格\數字和字母）根据关系转化
            inside_code += 65248
        elif (65296 <= inside_code <= 65307 or 65315 <= inside_code <= 65338 or 65345 <= inside_code <= 65370): # 全角字符轉化
            inside_code -= 65248
        rstring += chr(inside_code)
    return rstring