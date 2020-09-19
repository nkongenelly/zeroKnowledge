import random

m = random.getrandbits(10)
# print(m)
choices = list(range(1024))
print(choices)
binaryList = [bin(choice) for choice in choices]
# for choice in choices:
#     binary = bin(choice)
#     binaryList.append(binary)

print(binaryList)
