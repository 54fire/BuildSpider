import threading

from setting import KEYWORDS

def keywords_juste(sentences, keywords=KEYWORDS):
    '''
    函数的主要功能，判断 =句子= 中是否包含有 "关键词"
    :param keywords: 关键词
    :param sentences: 需要判断的句子
    :return: 如果句子中包含关键词就返回true，反之返回false
    '''
    if not keywords:
        return True
    for keyword in keywords:
        if keyword in sentences:
            return True
    return False
