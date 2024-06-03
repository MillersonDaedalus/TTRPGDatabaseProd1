import random

def diceroller(ammount):
    numtoroll = ammount.split('d')[0]
    typetoroll = ammount.split('d')[1]
    result = 0
    for i in range(int(numtoroll)):
        result += random.randrange(int(typetoroll))+1
    return result

def advantage(ammount):
    sum1 = diceroller(ammount)
    sum2 = diceroller(ammount)
    list1 = sorted([sum1,sum2])
    print(list1)
    result = list1[len(list1)-1]
    return result

for i in range(10):
    #print(diceroller('1d20'))
    print(advantage('1d20'))
