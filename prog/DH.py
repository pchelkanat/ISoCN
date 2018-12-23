import numpy as np

# DH
from Crypto.Util.number import getPrime, getRandomRange


def gen_KM(n, q):
    xy = getRandomRange(0, n)
    print(xy)
    KM = (q ** xy) % n
    return xy, KM


def receive_CxCy(KM, xy, n):
    CxCy = (KM ** xy) % n
    return CxCy


# RC4
def S_block(mykey, bits):  # KSA L=len(mykey)
    S = np.linspace(0, bits-1, bits, dtype=np.int32)
    mykeys = np.array(list(bin(mykey)[2:].zfill(16)), dtype=np.int8)
    j = 0
    for i in range(bits):
        j = (j + S[i] + mykeys[i % len(mykeys)]) % bits
        S[i], S[j] = S[j], S[i]
    return S


def gen_K(S, bits):  # PRGA
    i, j = 0, 0
    while True:
        i = (i + 1) % bits
        j = (j + S[i]) % bits
        S[i], S[j] = S[j], S[i]
        t = (S[i] + S[j]) % bits
        K = S[t]
        yield K  # return


def RC4_enc(mykey, plaintext, bits):
    S = S_block(mykey, bits)
    keystream=gen_K(S, mykey)

    temp = [ord(char) for char in plaintext]

    cryptotext = ""
    for t in temp:
        cryptotext += str(chr(t ^ keystream.__next__()))
    return cryptotext

def RC4_dec(mykey,cryptotext,bits):
    S = S_block(mykey, bits)
    keystream = gen_K(S, mykey)

    temp = [ord(char) for char in cryptotext]
    newtext = ""
    for t in temp:
        newtext += str(chr(t ^ keystream.__next__()))
    return newtext

if __name__ == '__main__':
    bits = 16
    n, q = getPrime(bits), getPrime(bits)
    print("nq", n, q)

    x, M = gen_KM(n, q)
    y, K = gen_KM(n, q)
    print("xy", x, y)
    print("KM", K, M)

    mykeyA = receive_CxCy(K, x, n)
    mykeyB = receive_CxCy(M, y, n)

    key = mykeyA
    plaintext = "natalya"
    print("key, text",key, plaintext)

    cryptotext = RC4_enc(mykeyA, plaintext,bits)
    print(cryptotext)
    newtext=RC4_dec(mykeyB,cryptotext,bits)
    print(newtext)