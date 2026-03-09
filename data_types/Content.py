import base64
import re
import util.hashfuncs as hashfuncs
import hashlib
import io
from PIL import Image

def getExt(data):
    imageFile = io.BytesIO(data)
    fmt = ''
    with Image.open(imageFile) as i:
        fmt = i.format.lower()
        if fmt == 'jpeg':
            fmt = 'jpg'
    return fmt

magic = {
    b'version 1.00': "mesh"
}

idMatcher = re.compile(r'id=([0-9]+)')

class Content:
    def __init__(self, url):
        self.url = url
        self.identifier
    def __str__(self):
        return self.url
    def isPrefix(self, prefix):
        return self.url.startswith(prefix)
    @property
    def identifier(self):
        if self.isPrefix('rbxassetid://'):
            return self.url[13:]
        if self.isPrefix('http://') or self.isPrefix('https://'):
            result = idMatcher.search(self.url)
            if result is None:
                return self.url
            else:
                return result.group(1)
        if self.isPrefix('hash://'):
            return self.url[7:]
        return self.url
    @staticmethod
    def FromXML(elem):
        if len(elem) == 0:
            print("MALFORMED CONTENT TAG!")
            return Content.EMPTY
        childElem = elem[0]
        match childElem.tag:
            case "url":
                return Content(childElem.text)
            case "null":
                return Content.EMPTY
            case "binary":
                data = base64.b64decode(childElem.text)
                ext = ''
                for prefix, exten in magic.items():
                    if data.startswith(prefix):
                        ext = exten
                        break
                if ext == '':
                    # extension not found in magic dictionary
                    ext = getExt(data)
                if ext != '':
                    # extension found anywhere, prepend period
                    ext = '.' + ext
                dataHash = hashfuncs.md5(data)
                with open(f'embedded/{dataHash}{ext}', "wb+") as f:
                    f.write(data)
                return Content("hash://" + dataHash)
            case "hash":
                return Content("hash://" + childElem.text)
            case _:
                return Content("MALFORMED" + childElem.tag)
Content.EMPTY = Content("")