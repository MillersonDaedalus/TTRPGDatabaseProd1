import random

class Roller():
    def __init__(self):
        pass

    def roll(self, num):
        return random.randrange(int(num)) + 1

    def sumroll(self, num, oftype):
        result = 0
        for i in range(num):
            result += self.roll(oftype)
        return result

    def kh(self, amount=int, oftype=int):
        results = []
        for i in range(amount):
            results.append(self.roll(oftype))
        list1 = sorted(results)
        # print(list1)
        result = list1[len(list1) - 1]
        return result

    def kl(self, amount=int, oftype=int):
        results = []
        for i in range(amount):
            results.append(self.roll(oftype))
        list1 = sorted(results)
        # print(list1)
        result = list1[0]
        return result

    def diceparser(self, ammount='1d20'):
        result = 0
        parsed = list(map(int, ammount.split('d')))
        result = self.sumroll(parsed[0], parsed[1])
        return result




if __name__ == '__main__':
    roller = Roller()

    print(roller.roll(6))
    print(roller.sumroll(3,6))
    print(roller.kh(2,20))
    print(roller.kl(2,20))
    print(roller.diceparser('3d6'))