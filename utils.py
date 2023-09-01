import re
from fastapi import HTTPException

def processo_existe(numero):
    padrao = r'^\d{7}-\d{2}\.\d{4}\.\d{1}\.\d{2}\.\d{4}$'
    if re.match(padrao, numero):
        return True
    else:
        raise HTTPException(status_code=400, detail="Número do processo inválido")

def get_tribunal(url):
    return url[12:16]