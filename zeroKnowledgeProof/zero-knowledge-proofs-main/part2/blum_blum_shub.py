# from primality import probablyPrime
import random
import sympy


def goodPrime(p):
    # return p % 4 == 3 and probablyPrime(p, accuracy=100)
    return p % 4 == 3 and sympy.primerange(p,100)


def findGoodPrime(numBits=512):
    candidate = 1

    while not goodPrime(candidate):
        candidate = random.getrandbits(numBits)

    return candidate


# def makeModulus(numBits=512):
def makeModulus(numBits=10):
    # print("find good prime = ", findGoodPrime(numBits))
    # print("find good prime length = ", len(str(findGoodPrime(numBits))))
    # print("find good prime squared= ", findGoodPrime(numBits) * findGoodPrime(numBits))
    # print("find good prime squared length = ", len(str(findGoodPrime(numBits) * findGoodPrime(numBits))))
    prime = 281333
    # return findGoodPrime(numBits) * findGoodPrime(numBits)
    return prime


def parity(n):
    n = 8464
    # p = sum(int(x) for x in bin(n)[2:]) % 2
    # print("parity sum = ", p)
    # print("parity n = ", n)     #n = 10
    # print("bin(n) = ", bin(n))      # = 0b1010
    # print("bin(n)[2:] = ", bin(n)[2:])  # = 1010
    # z = bin(n)[2:]
    # p = sum(int(x) for x in z) % 2
    # for x in z:
    #     print("x in the loop", x)
    #     x += x
    #
    # # p1 = x % 2
    # x1 = int(x)
    # p1 = x1 % 2
    # print("x total binary = ", x)
    # print("x total int = ", int(x))
    # print("p final = ", p1)
    # print("parity sum p=p1 ==  ", p)
    # print("parity n = ", n)
    return sum(int(x) for x in bin(n)[2:]) % 2


# def blum_blum_shub(modulusLength=512):
def blum_blum_shub(modulusLength=10):
    modulus = makeModulus(numBits=modulusLength)
    print("blum blum shum fixed module", modulus)

    def f(inputInt):
        m = pow(inputInt, 2, modulus)
        #m = (inputInt squared) % (modulus = 587489)
        # print("blum_blum_shub power m is ", m)
        return pow(inputInt, 2, modulus)

    # print("blum_blum_shub function f = ", f)
    return f


if __name__ == "__main__":
    owp = blum_blum_shub()
    print(owp(70203203))
    print(owp(12389))
    print(owp(10))
    print("blum blum shum owp 92 = ", owp(92))
