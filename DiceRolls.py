import random


def roll(num):
    return random.randrange(int(num))+1


def sumroll(num, oftype):
    result = 0
    for i in range(num):
        result += roll(oftype)
    return result


def advantage(num=int, oftype=int):
    if num > 1:
        print('advantage applies to singular dice rolls')
        return 0
    sum1 = roll(oftype)
    sum2 = roll(oftype)
    list1 = sorted([sum1,sum2])
    #print(list1)
    result = list1[len(list1)-1]
    return result


def diceparser(ammount='1d20',type='none'):
    result = 0
    parsed = list(map(int, ammount.split('d')))
    if type == 'none':
        result = sumroll(parsed[0],parsed[1])
    if type == 'advantage':
        result = advantage(parsed[0],parsed[1])
    return result


