import re

def processo_existe(numero):
    padrao = r'^\d{7}-\d{2}\.\d{4}\.\d{1}\.\d{2}\.\d{4}$'
    if re.match(padrao, numero):
        return True
    else:
        return False

def get_tribunal(url):
    return url[13:17]