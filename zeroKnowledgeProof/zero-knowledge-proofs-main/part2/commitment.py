import random


class CommitmentScheme(object):
    def __init__(self, oneWayPermutation, hardcorePredicate, securityParameter):
        '''
            oneWayPermutation: int -> int
            hardcorePredicate: int -> {0, 1}
        '''
        self.oneWayPermutation = oneWayPermutation
        self.hardcorePredicate = hardcorePredicate
        self.securityParameter = securityParameter

        # a random string of length `self.securityParameter` used only once per commitment
        self.secret = self.generateSecret()

    def generateSecret(self):
        raise NotImplemented

    def commit(self, x):
        raise NotImplemented

    def reveal(self):
        return self.secret


class BBSBitCommitmentScheme(CommitmentScheme):
    def generateSecret(self):
        # the secret is a random quadratic residue
        # securityParameter = 10
        # print(" oneWayPerm = ", oneWayPerm) ...f = (inputInt squared) % (modulus = 281333)
        # print("hardcorePred = ", hardcorePred) #.. function = sum(int(x) for x in bin(n)[2:]) % 2
        m = random.getrandbits(self.securityParameter)
        m = 92
        # self.secret = self.oneWayPermutation(random.getrandbits(self.securityParameter))
        self.secret = self.oneWayPermutation(m)
        # m = random.getrandbits(self.securityParameter)
        # print("BBSBitCommitmentScheme", m)
        # print("BBSBitCommitmentScheme oneWayPermutation from scratch = ", pow(m, 2, 281333) )
        # # print("BBSBitCommitmentScheme oneWayPermutation", self.oneWayPermutation(random.getrandbits(self.securityParameter))) #8464
        # print("BBSBitCommitmentScheme oneWayPermutation", self.oneWayPermutation(m)) #8464
        # print("BBSBitCommitmentScheme secret", self.secret) #8464
        return self.secret

    def commit(self, bit):
        # self.secret = 8464
        # print(" BBSBitCommitmentScheme commit bit = ", bit)
        unguessableBit = self.hardcorePredicate(self.secret)  # sum(int(x) for x in bin(n)[2:]) % 2 where n = 10
        # print("BBSBitCommitmentScheme unguessableBit = ", unguessableBit)  # = 0
        # print("BBSBitCommitmentScheme oneWayPermutation from scratch= ", pow(8464, 2, 281333))  # =180714
        # print("BBSBitCommitmentScheme oneWayPermutation = ", self.oneWayPermutation(self.secret))  # =180714
        # print("BBSBitCommitmentScheme commit return = ", self.oneWayPermutation(self.secret),  # 180714, 1
        #       unguessableBit ^ bit, )
        return (
            self.oneWayPermutation(self.secret),
            unguessableBit ^ bit,  # python xor
        )


class BBSBitCommitmentVerifier(object):
    def __init__(self, oneWayPermutation, hardcorePredicate):
        self.oneWayPermutation = oneWayPermutation
        self.hardcorePredicate = hardcorePredicate
        # print(" oneWayPerm = ", oneWayPerm) ...f = (inputInt squared) % (modulus = 281333)
        # print("hardcorePred = ", hardcorePred) #.. function = sum(int(x) for x in bin(n)[2:]) % 2

    def verify(self, securityString, claimedCommitment):
        # print("committment = ", commitment) # = (180714 1)
        # print("secret = ", secret)  # = 8464
        # print("hardcorePred = ", hardcorePred) #.. function = sum(int(x) for x in bin(n)[2:]) % 2
        trueBit = self.decode(securityString, claimedCommitment)
        # print("BBSBitCommitmentVerifier trueBit = ", self.decode(8464, claimedCommitment))  # = 1
        # print("BBSBitCommitmentVerifier trueBit = ", self.decode(securityString, (180714 1))
        unguessableBit = self.hardcorePredicate(securityString)  # wasteful, whatever
        # print("BBSBitCommitmentVerifier unguessableBit = ", self.hardcorePredicate(securityString))  # = 1
        # print("BBSBitCommitmentVerifier unguessableBit = ", self.hardcorePredicate(securityString))  # = 1
        # print("BBSBitCommitmentVerifier oneWayPermutation = ", self.oneWayPermutation(securityString))  # = 180714
        # print("BBSBitCommitmentVerifier oneWayPermutation = ", pow(8464, 2, 281333))  # = 180714
        # print("BBSBitCommitmentVerifier return = ", self.oneWayPermutation(securityString),
        #       unguessableBit ^ trueBit, )  # = 180714, 0
        return claimedCommitment == (
            self.oneWayPermutation(securityString),
            unguessableBit ^ trueBit,  # python xor
        )

    def decode(self, securityString, claimedCommitment):
        unguessableBit = self.hardcorePredicate(securityString)
        return claimedCommitment[1] ^ unguessableBit


class BBSIntCommitmentScheme(CommitmentScheme):
    def __init__(self, numBits, oneWayPermutation, hardcorePredicate, securityParameter=512):
        '''
            A commitment scheme for integers of a prespecified length `numBits`. Applies the
            bit commitment scheme to each bit independently.
        '''
        self.schemes = [BBSBitCommitmentScheme(oneWayPermutation, hardcorePredicate, securityParameter)
                        for _ in range(numBits)]
        # print("BBSIntCommitmentScheme schemes = ", self.schemes)
        # print("BBSIntCommitmentScheme schemes length= ", len(self.schemes))  # = 10
        super().__init__(oneWayPermutation, hardcorePredicate, securityParameter)
        # numBits = 10
        # securityParameter=512
        # print(" oneWayPerm = ", oneWayPerm) ...f = (inputInt squared) % (modulus = 281333)
        # print(" oneWayPerm1 = ", oneWayPermutation) #...f = (inputInt squared) % (modulus = 281333)
        # print("hardcorePred = ", hardcorePred) #.. function = sum(int(x) for x in bin(n)[2:]) % 2

    def generateSecret(self):
        # self.secret = 8464
        self.secret = [x.secret for x in self.schemes]
        # self.m = []
        # for x in self.schemes:
        #     print("BBSIntCommitmentScheme generateSecret x = ", x)
            # self.m.append(x)

        # print("BBSIntCommitmentScheme generateSecret self.m = ", self.m)
        # print("BBSIntCommitmentScheme generateSecret self.secret = ", self.secret)  # = [8464, 8464, 8464, 8464, 8464, 8464, 8464, 8464, 8464, 8464]
        return self.secret

    def commit(self, integer):
        integer = 750
        # first pad bits to desired length
        # print("BBSIntCommitmentScheme commit = ", bin(int(integer))[2:].zfill(len(self.schemes)))   # = 1011101110
        integer = bin(integer)[2:].zfill(len(self.schemes))
        # print("BBSIntCommitmentScheme commit again = ", integer)    # = 1011101110
        # print("BBSIntCommitmentScheme self.schemes length = ", len(self.schemes))
        # print("BBSIntCommitmentScheme commit = ", bin(750)[2:].zfill(10))   # = 1011101110
        bits = [int(bit) for bit in integer]
        # print("BBSIntCommitmentScheme commit bits = ", bits)    # = [1, 0, 1, 1, 1, 0, 1, 1, 1, 0]
        # b = []
        # for bit in integer:
        #     b.append(int(bit))
        # print("BBSIntCommitmentScheme commit b = ", b)
        # print("BBSIntCommitmentScheme commit b again = ", int(b)) # = [1, 0, 1, 1, 1, 0, 1, 1, 1, 0]
        r = [scheme.commit(bit) for scheme, bit in zip(self.schemes, bits)]
        # self.schemes = [BBSBitCommitmentScheme(oneWayPermutation, hardcorePredicate, securityParameter)
        #                 for _ in range(numBits)]
        # print("BBSIntCommitmentScheme self.schemes = ", self.schemes)
        # b  = zip(self.schemes, bits)
        # print("BBSIntCommitmentScheme self.schemes zip = ", tuple(b))
        # print("BBSIntCommitmentScheme return r = ", r)
        # r1 = []
        # for scheme, bit in zip(self.schemes, bits):
        #     r1.append(scheme.commit(bit))

        # print("BBSIntCommitmentScheme return r = ", r)  # =  [(180714, 0), (180714, 1), (180714, 0), (180714, 0), (180714, 0), (180714, 1), (180714, 0), (180714, 0), (180714, 0), (180714, 1)]
        # print("BBSIntCommitmentScheme return r1 = ", r1)    # r = r1 above
        # print("BBSIntCommitmentScheme return length = ", len(r))    # = 10
        # print("BBSIntCommitmentScheme return length r1= ", len(r1))    # = 10
        return [scheme.commit(bit) for scheme, bit in zip(self.schemes, bits)]


class BBSIntCommitmentVerifier(object):
    def __init__(self, numBits, oneWayPermutation, hardcorePredicate):
        self.verifiers = [BBSBitCommitmentVerifier(oneWayPermutation, hardcorePredicate)
                          for _ in range(numBits)]

    def decodeBits(self, secrets, bitCommitments):
        return [v.decode(secret, commitment) for (v, secret, commitment) in
                zip(self.verifiers, secrets, bitCommitments)]

    def verify(self, secrets, bitCommitments):
        return all(
            bitVerifier.verify(secret, commitment)
            for (bitVerifier, secret, commitment) in
            zip(self.verifiers, secrets, bitCommitments)
        )

    def decode(self, secrets, bitCommitments):
        decodedBits = self.decodeBits(secrets, bitCommitments)
        return int(''.join(str(bit) for bit in decodedBits), 2)


if __name__ == "__main__":
    import blum_blum_shub

    securityParameter = 10
    oneWayPerm = blum_blum_shub.blum_blum_shub(securityParameter)
    # print(" oneWayPerm initially= ", oneWayPerm)  # ...f = (inputInt squared) % (modulus = 587489)
    hardcorePred = blum_blum_shub.parity
    # print("hardcorePred = ", hardcorePred) #.. function = sum(int(x) for x in bin(n)[2:]) % 2

    print('Bit commitment')
    scheme = BBSBitCommitmentScheme(oneWayPerm, hardcorePred, securityParameter)  # 8464
    verifier = BBSBitCommitmentVerifier(oneWayPerm, hardcorePred)

    for _ in range(10):
        bit = random.choice([0, 1])
        print("random choice = ", bit)
        bit = 1
        commitment = scheme.commit(bit)  # BBSBitCommitmentScheme.commit(1)
        # print("committment = ", commitment) # = (180714, 1)
        secret = scheme.reveal()
        # print("secret = ", secret)  # = 8464
        trueBit = verifier.decode(secret, commitment)
        # print("trueBit = ", trueBit) # = 1
        valid = verifier.verify(secret, commitment)
        # print("valid = ", valid)    # = 180714, 0

        print("bit = ", bit)  # = 1
        print("trueBit = ", trueBit)  # = 1
        print("valid = ", valid)  # = True
        print("secret = ", secret)  # = 8464
        print("commitment = ", commitment)  # = 180714, 0

        print('{} == {}? {}; {} {}'.format(bit, trueBit, valid, secret, commitment))  # 1 == 1? True; 8464 (180714, 0)

    print('Int commitment')
    scheme = BBSIntCommitmentScheme(10, oneWayPerm, hardcorePred)
    verifier = BBSIntCommitmentVerifier(10, oneWayPerm, hardcorePred)
    choices = list(range(1024))
    # print("list in the range 1024 = ", list(range(1024)))   # = [0,1,2,3....,1022,1023]
    # print("list in the range 1024 length = ", len(choices))     # = 1024
    for _ in range(10):
        theInt = random.choice(choices)
        theInt = 750
        print("theInt random choice = ", theInt)    # = 750
        commitments = scheme.commit(theInt)
        # print("committments = ", commitments)   # =   [(180714, 0), (180714, 1), (180714, 0), (180714, 0), (180714, 0), (180714, 1), (180714, 0), (180714, 0), (180714, 0), (180714, 1)]
        secrets = scheme.reveal()
        # print("secrets reveal = ", secrets) # = [8464, 8464, 8464, 8464, 8464, 8464, 8464, 8464, 8464, 8464]
        trueInt = verifier.decode(secrets, commitments)
        # print("trueInt = ", trueInt)    # = 750
        valid = verifier.verify(secrets, commitments)
        # print("valid = ", valid)    # = True

        print('{} == {}? {}; {} {}'.format(theInt, trueInt, valid, secrets, commitments))       # = 750 == 750? True; [8464, 8464, 8464, 8464, 8464, 8464, 8464, 8464, 8464, 8464] [(180714, 0), (180714, 1), (180714, 0), (180714, 0), (180714, 0), (180714, 1), (180714, 0), (180714, 0), (180714, 0), (180714, 1)]
