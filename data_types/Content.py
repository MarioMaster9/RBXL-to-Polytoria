import base64
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

class Content:
    def __init__(self, url):
        self.url = url
    def __str__(self):
        return self.url
    @staticmethod
    def FromXML(elem):
        if len(elem) == 0:
            print("MALFORMED CONTENT TAG!")
            return Content("")
        childElem = elem[0]
        match childElem.tag:
            case "url":
                return Content(childElem.text)
            case "null":
                return Content("")
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
