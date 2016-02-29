import random

commonStr = 'abcdefghijklmnopqrstuvwxyz1234567890'

nameSize = 6

passwordSize = 6

month = 30

year = 12

fileName = 'ssUser'

class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            new = super(Singleton, cls)
            cls._instance = new.__new__(cls, *args, **kw)
        return cls._instance

class User(Singleton):
    userDict = {}

    def getUserDict(self):
        return self.userdict

    def addUser(self, fileName, test = False):
        (newName, newPassword) = self.generateNewUser()
        print ('newName,newPassword:' + newName + ',' + newPassword)

        time = 3
        if (test == False):
            time = month * year
        value = {newName, newPassword, time}

        with open(fileName, "a") as f:
            f.write(newName + ',' + newPassword + ',' + str(time) + '\n')

        self.userDict[newName] = value
        return (newName, newPassword)

    def generateNewUser(self):
        newName = ''
        newPassword = ''

        while(1):
            i = 1
            while(i <= nameSize):
                newName += random.choice(commonStr)
                i += 1
            print("newName = " + newName)

            if (self.userDict.has_key(newName)):
                continue

            i = 1
            while(i <= passwordSize):
                newPassword += random.choice(commonStr)
                i += 1
            print ("newPassword = " + newPassword)

            break

        return (newName, newPassword)