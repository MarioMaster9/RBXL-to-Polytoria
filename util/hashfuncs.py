import hashlib
from multimethod import multimethod

@multimethod
def md5(data: str):
    m = hashlib.md5()
    m.update(data.encode('utf-8'))
    return m.hexdigest()

@multimethod
def md5(data: bytes):
    m = hashlib.md5()
    m.update(data)
    return m.hexdigest()
