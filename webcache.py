import requests
from PIL import Image
from StringIO import StringIO


def get(url, cacheid, ctype='text'):
    content = None
    try:
        if 'image' == ctype:
            content = Image.open(cacheid)
        else:
            f = open(cacheid, 'r')
            content = f.read()
            f.close()
    except:
        r = requests.get(url)
        if 200 == r.status_code and r.content:
            content = r.content
            if 'image' == ctype:
                img = Image.open(StringIO(content))
                img.save(cacheid)
            else:
                if r.encoding:
                    content = content.encode(r.encoding)
                f = open(cacheid, 'w')
                f.write(content)
                f.close()
    return content