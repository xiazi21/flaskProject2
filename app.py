from flask import Flask, render_template, url_for, redirect, request
import random

app = Flask(__name__)


def preferenceGen(n):
    result = [[None]] * n
    for i in range(n):
        i = i + 1
        flag = random.randint(0, n - 1)  # the random rank in the preference
        if result[flag] == [None]:
            result[flag] = [i]
        else:
            result[flag].append(i)
    for ele in result:
        if [None] in result:
            result.remove([None])
    return result


class people:
    # get the data to creat a class for a people include the man and woman
    def __init__(self, index, sex, num):
        # num is the number of male or female
        self.index = index  # index of male or female
        self.sex = sex  # male or female
        self.engaged = []  # engaged with who
        tmp = preferenceGen(num)
        print(tmp)
        self.preference = tmp
        self.originalPreference = 'is ' + str(tmp)

    def isFree(self):
        if self.engaged == [] and self.preference != []:
            return True
        return False


class mainHelper:
    def __init__(self, num):
        self.maleList = []
        self.femaleList = []
        for i in range(1, num + 1):
            self.maleList.append(people(i, "male", num))
            self.femaleList.append(people(i, "female", num))

    def someManEmpty(self):
        for male in self.maleList:
            if not male.preference:
                return True
        else:
            return False

    def propose(self, male, female):
        for man in self.maleList:
            if man == male:
                man.engaged.append(female.index)
        for woman in self.femaleList:
            if woman == female:
                woman.engaged.append(male.index)

    def findFemaleByIndex(self, femaleIndex):
        # find the object by index
        for ele in self.femaleList:
            if ele.index == femaleIndex:
                return ele

    def findMaleByIndex(self, maleIndex):
        # find the object by index
        for ele in self.maleList:
            if ele.index == maleIndex:
                return ele

    def breakEngaged(self, male, female):
        for man in self.maleList:
            if man == male:
                man.engaged.remove(female.index)
        for woman in self.femaleList:
            if woman == female:
                woman.engaged.remove(male.index)

    def deletePair(self, male, female):
        i = 0
        for man in self.maleList:
            if man == male:
                for ele in male.preference:
                    if female.index in ele:
                        man.preference[i].remove(female.index)
                    i += 1
                if [None] in man.preference:
                    man.preference.remove([None])
                if [] in man.preference:
                    man.preference.remove([])
        i = 0
        for woman in self.femaleList:
            if woman == female:
                for ele in female.preference:
                    if male.index in ele:
                        woman.preference[i].remove(male.index)
                    i += 1
            if [None] in woman.preference:
                woman.preference.remove([None])
            if [] in woman.preference:
                woman.preference.remove([])

    def isEveryoneEngaged(self):
        for man in self.maleList:
            if man.engaged == []:
                return False
        for woman in self.femaleList:
            if woman.engaged == []:
                return False
        return True

    def can_engage(self,man,woman):
        if man.index in woman.preference:
            if woman.index in man.preference:
                return True
        else:
            return False


def superMatchMain(num):
    """
    assign each person to be free
    while not some mans' list is empty or everyone is engaged
    for each woman w at the head of m’s list do
    begin
        m proposes, and becomes engaged, to w;
        for each strict successor m’ of m on w’s list do
        begin
            if m’ is engaged to w then
                break the engagement;
            delete the pair(m’.w)
            end
        end;
    for each woman w who is multiply engaged do
        begin
            break all engagements involving W;
            for each man m at the tail of w’s list do
                delete the pair (m. w)
            end
    if everyone is engaged then
        the engagement relation is a super-stable matching
    else
        no super-stable matching exists
    """
    object_local = mainHelper(num)  # this is target data that assign each person to be free
    while not object_local.someManEmpty() or object_local.isEveryoneEngaged():
        if object_local.someManEmpty():
            return None
        for man in object_local.maleList:
            if man.isFree():
                for girl in man.preference[0]:
                    # for the girls in mans' head
                    # m proposes, and becomes engaged, to w;
                    girl = object_local.findFemaleByIndex(girl)

                    bol = 1
                    for ele in girl.preference:
                        if man.index in ele:
                            for ele1 in man.preference:
                                if girl.index in ele1:
                                    bol = 0
                    if bol == 0:
                        object_local.propose(man, girl)



                    # for each strict successor m’ of m on w’s list do
                    i = 0  # counter
                    k = 0  # counter, get the rank in the girls preference
                    for j in girl.preference:  # find the boy in girls rank
                        if man.index in j:
                            k = i
                        else:
                            i += 1
                    mSuccessor = girl.preference[k + 1:len(girl.preference)]
                    # contain the man lower
                    for ele in mSuccessor:
                        for i in ele:
                            male = object_local.findMaleByIndex(i)
                            if i in girl.engaged:
                                # if the m’ is engaged to w then
                                #male = object_local.findMaleByIndex(i)
                                object_local.breakEngaged(male, girl)
                                # break the engagement;
                                # delete the pair(m',w)
                                #object_local.deletePair(male, girl)
                            male = object_local.findMaleByIndex(i)
                            object_local.deletePair(male, girl)
        if object_local.someManEmpty():
            return None
        multipleEngaged = []  # store the multiple engaged woman
        for female in object_local.femaleList:
            if len(female.engaged) > 1:
                multipleEngaged.append(female)
                # find who is multiple engaged
        for woman in multipleEngaged:
            for maleIndex in woman.engaged:
                male = object_local.findMaleByIndex(maleIndex)
                object_local.breakEngaged(male, woman)
                object_local.deletePair(male, woman)
            for maleIndex in woman.preference[-1]:
                male = object_local.findMaleByIndex(maleIndex)
                object_local.deletePair(male, woman)
        if object_local.someManEmpty():
            return None
        if object_local.isEveryoneEngaged():
            return object_local

    return object_local


@app.route('/')
def hello_world():  # put application's code here
    n = 1
    if request.method == 'GET':
        n = request.args.get('input1')
        if n != None and n != '':
            n = int(n)
            result = []
            data1 = superMatchMain(n)
            if data1 == None:
                return render_template("main.html", data=None, dataObj=data1)
            else:
                for male in data1.maleList:
                    for ele in male.engaged:
                        result.append([male.index, ele])
                return render_template("main.html", data=result, dataObj=data1)
        else:
            return render_template("main.html", dataObj=None, temp1=None)
    else:
        return render_template("main.html")


if __name__ == '__main__':
    app.run()
