import hashlib

from Crypto.Util.number import getPrime

from prog.SSPT import generatePrime


def computeMD5hash(my_string):
    m = hashlib.md5()
    m.update(my_string.encode('utf-8'))
    return m.hexdigest()


if __name__ == "__main__":

    nn=computeMD5hash(23)
    print(nn, type(nn))
    x= getPrime(128)
    print(x)
    res=int(nn,16)+x
    print(res)



