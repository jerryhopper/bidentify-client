import sys
import hashlib


def hashfile(theFile):
    # BUF_SIZE is totally arbitrary, change for your app!
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

    md5 = hashlib.md5()

    with open(theFile, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
    theHash = md5.hexdigest()

    #print("MD5: {0}".format(theHash))

    return theHash
