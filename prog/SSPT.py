import math
from math import gcd
from random import randrange

# банально по делителям, для проверки свидетеля a
from Crypto.Util import number


def is_prime(a):
    """
    for i in range (2, a):
        print(i, a%i)
    """
    return all(a % i for i in range(2, a))

# решето Эратосфена
def primeSieve(sieveSize):
    # Returns a list of prime numbers calculated using
    # the Sieve of Eratosthenes algorithm.

    sieve = [True] * sieveSize
    sieve[0] = False
    sieve[1] = False

    # Формирование:
    for i in range(2, int(math.sqrt(sieveSize)) + 1):
        pointer = i * 2
        while pointer < sieveSize:
            sieve[pointer] = False
            pointer += i

    # Только простые:
    primes = []
    for i in range(sieveSize):
        if sieve[i] == True:
            primes.append(i)

    return primes

LOW_PRIMES = primeSieve(100)


def factorize(n):
    factors = []
    p = 2
    while True:
        while n % p == 0 and n > 0:
            factors.append(int(p))
            n = n / p
        p += 1
        if p > n / p:
            break
    if n > 1:
        factors.append(int(n))
    return factors


def legendre(a, p):
    if a >= p or a < 0:
        return legendre(a % p, p)
    elif a == 0 or a == 1:
        return a
    elif a == 2:
        if p % 8 == 1 or p % 8 == 7:
            return 1
        else:
            return -1
    elif a == p - 1:
        if p % 4 == 1:
            return 1
        else:
            return -1

    # jacobi -> factorize
    elif not is_prime(a):  #
        factors = factorize(a)
        product = 1
        for pi in factors:
            product *= legendre(pi, p)
        return product

    else:
        if ((p - 1) / 2) % 2 == 0 or ((a - 1) / 2) % 2 == 0:
            return legendre(p, a)
        else:
            return (-1) * legendre(p, a)


def solovayStrassen(n):
    if n % 2 == 0 or n < 2:
        return False

    for k in range(5):
        a = randrange(2, n - 1)
        if gcd(a, n) != 1:
            return False
        an = pow(a, (n - 1) // 2, n)
        if an == (n - 1):
            an = -1
        if not (an == legendre(a, n)):
            return False
    return True

# проверка по SS
def isPrimeSS(num):
    # Return True if num is a prime number. This function does a quicker
    # prime number check before calling solovayStrassen().
    if (num < 2):
        return False

    # Проверка через первые 100 простых числа:
    for prime in LOW_PRIMES:
        if (num % prime == 0):
            return False
    return solovayStrassen(num)


def generatePrime(keysize):
    while True:
        x = randrange(2 ** (keysize - 1), 2 ** (keysize))
        if isPrimeSS(x):  # is_prime(x):
            return x


if __name__ == '__main__':

    keysize = 128
    #x = generatePrime(keysize)
    x= number.getPrime(keysize)

    print(x)
    print(is_prime(x))

