# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your agent class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================

from Agent import Agent

class MyAI ( Agent ):

    def __init__ ( self ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================

        self.count = 0
        self.backlist = []
        self.moved = [[0,0]]
        self.gold = False #After grabbed gold this becomes true
        self.back = False #After encountered breeze, stench or bump, this becomes true
        self.next = [0,0]  #The current coordinate the agent is on
        self.direction = 0  # right = 0; up = 90; down = 270; left = 180;
        self.goup = False
        self.safelist = [[0,0]]
        self.row2 = False
        self.arrow = True
        self.wumpus = True
        self.test = False
        self.count1 = 0
        self.h = 1
        self.w = 1
        self.height = 7
        self.width = 7
        self.hitwall = False
        self.bcount = 0
        self.goingback = False
        self.news = [[False for i in range(8)] for j in range(8)]
        self.templ = []
        self.move = self.getsafeneighbor(self.safelist)
        self.stench = []
        self.wumpusposition = None
        self.stenchroute = []
        self.movelist = []
        self.goingto = []
        self.nextmove = []
        self.tcount = 0
    # ======================================================================


    def gotgold(self):
        """

        :return: movement grab triggers gold generates a list move movements to move in the future
        """
        self.gold = True
       # temp = self.goback1(self.moved)
        #self.backlist = temp
        return Agent.Action.GRAB
    def aftergold(self,dire):
        move = ''
        if self.backlist!= []:
            move = self.backlist.pop()
        if self.direction == dire and self.next == [0, 0]:
            return Agent.Action.CLIMB
        if move[1] == 1:
            return self.turnleft()
        elif move[1] == 2:
            return self.turnright()
        elif move[1] == 3:
            return self.moveforaward(self.next)

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        from random import shuffle
        self.generatenextmove()
        for i in self.nextmove:
            if i in self.moved:
                self.nextmove.remove(i)
        #print(self.next)
       # for i in self.news:
            #print(i)
        #print(self.nextmove)
        for i in self.nextmove:
            if i[1] >= self.width:
                self.nextmove.remove(i)
            if i[0] >= self.height:
                self.nextmove.remove(i)
        #print(self.gold,'sg1')
        #print(self.moved,'moved')
        #print(self.safelist)
        #print(self.next)
        #print(self.goingto)
        # print(self.safelist,'befroe')
        #print(self.getsafeneighbor(self.safelist))
        #print(self.moved,'moved')
       # if self.moved>70:
        if len(self.safelist) > 178:
            self.back = True
        if self.next[0]>=self.height:
            self.next[0] -= 1
        if self.next[1] >=self.width:
            self.next[1] -= 1
        for i in self.moved:
            if i[1] >= self.width:
                self.moved.remove(i)
            if i[0] >= self.height:
                self.moved.remove(i)
        for i in self.safelist:
            if i[1] >= self.width:
                self.safelist.remove(i)
            if i[0] >= self.height:
                self.safelist.remove(i)
        # print(self.safelist,'after')
        #print(self.moved)
        if len(self.moved) > 5:
            if  self.moved[-1] == self.moved[-3] and self.moved[-2] == self.moved[-4]:
                self.back = True
            elif self.moved[-1] == self.moved[-2] and self.moved[-1] ==self.moved[-3]and  self.moved[-1] == self.moved[-4]:
                self.back = True

        if self.moved != [[0, 0]] and self.safelist == [[0, 0], [0, 1]] and self.next == [0,0]:
            return Agent.Action.CLIMB
        if self.test:

            if self.nextmove == []:
                return Agent.Action.CLIMB
            if self.tcount == 2 and self.next == [0,0]:
                return Agent.Action.CLIMB
            if self.tcount == 0:
                temps = set()
                for i in self.nextmove:
                    temps.add(tuple(i))
                move = temps.pop()

                #print(move,'move')
                #print(self.shortestpath(move),'sp')
                self.templ = self.shortestpath(move)
                self.move = self.getsafeneighbor(self.templ)
                self.safelist = self.templ
                self.tcount += 1
            elif self.tcount == 1:
                self.move = self.getsafeneighbor(self.templ)
                self.tcount += 1
            self.movelist = self.toneighbor(self.move)
            # print(self.movelist)

            move1 = self.movelist.pop(0)

            if move1 == 1:
                return self.turnleft()
            elif move1 == 2:
                return self.turnright()
            elif move1 == 3:
                # print(self.moved,'before')
                # print(1)
                self.moved.append(self.move)
                # print(self.moved,'after')
                self.templ.pop(0)
                return self.moveforaward(self.next)
        if self.back:
            #print("gold")
            if self.next == [0,0] and self.gold:
                return Agent.Action.CLIMB
            elif self.next == [0,0]:
                #print('gn')

                self.test = True
                self.back = False
                return self.turnright()
            if self.bcount == 0:
                #print(self.next)
                #print(self.shortestpath(),'sp')
                #print(self.safelist, 'safel')
                self.templ = self.shortestpath([0,0])
                #print(self.templ,'temp')
                #print(self.safelist,'safel')
                self.move = self.getsafeneighbor(self.templ)
                # print(self.safelist, 'not b saf',type(self.safelist))
                self.safelist = self.templ
                # print(self.safelist, 'not b saf',type(self.safelist))
                #self.moved = []
                # print('bcont',self.bcount)
                self.goingback = True
                self.bcount += 1
            elif self.bcount > 0:
                self.move = self.getsafeneighbor(self.templ)
                #print(self.move,'move')
                self.bcount += 1
            #print(self.templ, 'temp1')
            #print(self.move,'move')
            self.movelist = self.toneighbor(self.move)
            #print(self.movelist)

            move1 = self.movelist.pop(0)

            if move1 == 1:
                return self.turnleft()
            elif move1 == 2:
                return self.turnright()
            elif move1 == 3:
                # print(self.moved,'before')
                #print(1)
                self.moved.append(self.move)
                # print(self.moved,'after')
                self.templ.pop(0)
                return self.moveforaward(self.next)




        if self.goingback and self.next == [0,0]:
            return Agent.Action.CLIMB
        if glitter:
            self.goingback = True
            self.gold = True
            self.back = True
            return self.gotgold()

        if scream:
            #print(self.next,'next')
            #print(self.safelist,'safe')
            #print(self.moved,'moved')
            self.wumpus = False
            #这里加if direction
            if self.direction == 0:
                self.move = [self.next[0], self.next[1] + 1]
            if self.direction == 90:
                self.move = [self.next[0] + 1, self.next[1]]
            if self.direction == 180:
                self.move = [self.next[0], self.next[1] - 1]
            if self.direction == 270:
                self.move = [self.next[0] - 1, self.next[1]]
            #print(self.move,'self.mve')
            #print(2)
            self.moved.append(self.move)
            return self.moveforaward(self.next)
        if self.wumpus and self.arrow:
            #print('w and a')
            if breeze and self.next == [0,0]:
                return Agent.Action.CLIMB
            if stench and self.next == [0,0]:
                self.arrow = False
                if self.direction == 0:

                    #self.safelist.append([2, 0])
                    #self.safelist.append([1, 1])
                    self.safelist.append([0, 1])
                elif self.direction == 90:
                    self.safelist.append([1,0])
                return Agent.Action.SHOOT

            if bump:
                #print("bumphere")
                temp = self.moved.pop()
                for i in self.safelist:
                    if i == temp:
                        self.safelist.remove(i)
                #print(self.safelist,'bump')
                self.next = self.moved[-1]
                self.hitwall = True
                if self.direction == 90:
                    self.height = self.h - 1
                    #self.deleteexceed()
                    return self.turnright()
                if self.direction == 0:
                    self.width = self.w - 1
                    #print(self.safelist)
                    #self.deleteexceed()
                    return self.turnleft()
            if not bump and not breeze and not stench:
                # print("here3")
                #print(self.next)

                #if not self.goingback:
                self.generatesafeneighbour(self.next)

                if self.goingto != self.next:
                    shuffle(self.safelist)
                self.goingto = self.next
                self.move = self.getsafeneighbor(self.safelist)
                #print(move)
                #print(self.toneighbor(self.next))
                if self.move != None:
                    #self.gold = True
                    self.movelist = self.toneighbor(self.move)
                #print(self.moved, 'afteml')

                    move1 = self.movelist.pop(0)
                    if move1 == 1:
                        return self.turnleft()
                    elif move1 == 2:
                        return self.turnright()
                    elif move1 == 3:
                        #print(self.moved,'before')
                        #print(3)
                        self.moved.append(self.move)
                       # print(self.moved,'after')

                        return self.moveforaward(self.next)
                else:
                    #print('here1')
                    self.back = True
                    return self.turnleft()
            elif breeze:

                #self.generatesafeneighbour(self.next)
                if self.getsafeneighbor(self.safelist) == None:
                    shuffle(self.safelist)
                    move = self.meetdanger(self.safelist)
                else:
                    if self.goingto != self.next:
                        shuffle(self.safelist)
                    move = self.getsafeneighbor(self.safelist)
                    self.goingto = self.next
                self.movelist = self.toneighbor(move)
                move1 = self.movelist.pop(0)
                if move1 == 1:
                    return self.turnleft()
                elif move1 == 2:
                    return self.turnright()
                elif move1 == 3:
                    #print(4)
                    self.moved.append(move)
                    return self.moveforaward(self.next)
            # haven't shot, wumpus alive

            elif stench:
                if self.arrow == True:
                    #print(self.next[1],'adn',self.width-1)
                    if self.direction == 0 and self.next[1] < self.width - 1:
                        self.safelist.append([self.next[0], self.next[1] + 1])
                    elif self.direction == 90 and self.next[0] < self.height - 1:
                        self.safelist.append([self.next[0] + 1,self.next[1]])
                    elif self.direction == 180 and self.next[1] > 0:
                        self.safelist.append([self.next[0], self.next[1] - 1])
                    elif self.direction == 270 and self.next[0] > 0:
                        self.safelist.append([self.next[0] - 1, self.next[1]])
                    self.arrow = False
                    return Agent.Action.SHOOT
        if self.wumpus:

            #print('wimpus')

            # self.safelist.append([self.next])
            #
            #
            # return Agent.Action.CLIMB
            # if self.wc ==0:
            #     self.safelist.insert(0,[1,0])
            #     self.moved.append(self.move)
            #     self.wc += 1
            #     return self.moveforaward()
            if bump:
                #print(self.moved)
                #print(self.safelist)
                #print('bumphere')
                temp = self.moved.pop()
                #print(temp)
                for i in self.safelist:
                    if i == temp:
                        self.safelist.remove(i)
                #print(self.safelist,'modified safe')
                self.next = self.moved[-1]
                self.hitwall = True
                if self.direction == 90:
                    self.height = self.h - 1
                    # self.deleteexceed()
                    return self.turnright()
                if self.direction == 0:
                    self.width = self.w - 1
                    # print(self.safelist)
                    # self.deleteexceed()
                    #print('turnedleft',self.width)
                    #print(self.safelist,'slis')
                    return self.turnleft()
            if not breeze and not stench:
                #print('next',self.safelist)
                #self.safelist.append(self.next)
                self.generatesafeneighbour(self.next)
                if self.goingto != self.next:
                    shuffle(self.safelist)
                self.goingto = self.next
                self.move = self.getsafeneighbor(self.safelist)
                # print(move)
                # print(self.toneighbor(self.next))
                if self.move != None:
                    # self.gold = True
                    self.movelist = self.toneighbor(self.move)
                    # print(self.moved, 'afteml')
                    #print(self.safelist,'sl')
                    move1 = self.movelist.pop(0)
                    if move1 == 1:
                        return self.turnleft()
                    elif move1 == 2:
                        return self.turnright()
                    elif move1 == 3:
                        # print(self.moved,'before')
                 #       print(5)
                        self.moved.append(self.move)
                        # print(self.moved,'after')
                        #print(self.safelist,'sl1')
                        return self.moveforaward(self.next)
                else:
                    #print('here')
                    self.back = True
                    return self.turnleft()
            elif breeze or stench:
                #print(self.safelist)
               # setl = set()
                #print(self.getsafeneighbor(self.safelist),'getsafe')
                if self.getsafeneighbor(self.safelist) == None:
                    # for i in self.safelist:
                    #     setl.add(tuple(i))
                    # setl = list(setl)
                    shuffle(self.safelist)

                    move = self.meetdanger(self.safelist)
                    #print('md')
                else:
                    if self.goingto != self.next:
                        shuffle(self.safelist)
                    move = self.getsafeneighbor(self.safelist)
                    self.goingto = self.next
                #print(self.safelist,'mds')
                self.movelist = self.toneighbor(move)
                #print(self.movelist,'movelist')
                #print(self.safelist,'safelist')
                move1 = self.movelist.pop(0)
                if move1 == 1:
                    return self.turnleft()
                elif move1 == 2:
                    return self.turnright()
                elif move1 == 3:
                    #print(6)
                    self.moved.append(move)
                    return self.moveforaward(self.next)

        if not self.wumpus:
            #print(self.next, 'next')
            #print(self.safelist, 'safe')
            #print(self.moved, 'moved')
            #print('not wumpus')
            #print(self.safelist)

            if bump:
                #print('bump here')
                #print(self.safelist,'bump')
                #print(self.moved,'moved atb')
                temp = self.moved.pop()
                for i in self.safelist:
                    if i == temp:
                        self.safelist.remove(i)
                self.next = self.moved[-1]
                self.hitwall = True
                if self.direction == 90:
                    self.height = self.h - 1
                    # self.deleteexceed()
                    return self.turnright()
                if self.direction == 0:
                    self.width = self.w - 1
                    # print(self.safelist)
                    # self.deleteexceed()
                    return self.turnleft()
            if breeze :
                #print(self.safelist)
                # self.generatesafeneighbour(self.next)
                if self.getsafeneighbor(self.safelist) == None:
                    move = self.meetdanger(self.safelist)
                else:
                    move = self.getsafeneighbor(self.safelist)
                self.movelist = self.toneighbor(move)
                move1 = self.movelist.pop(0)
                if move1 == 1:
                    return self.turnleft()
                elif move1 == 2:
                    return self.turnright()
                elif move1 == 3:
                    #print(7)
                    self.moved.append(move)
                    return self.moveforaward(self.next)
            if not breeze and not bump:
                # print(self.next)

                # if not self.goingback:
                #self.safelist.append(self.next)
                self.generatesafeneighbour(self.next)
                if self.goingto != self.next:
                    shuffle(self.safelist)
                self.goingto = self.next
                self.move = self.getsafeneighbor(self.safelist)
                # print(move)
                # print(self.toneighbor(self.next))
                if self.move != None:
                    # self.gold = True
                    self.movelist = self.toneighbor(self.move)
                    #print(self.moved, 'afteml')
                    #print(self.move)

                    move1 = self.movelist.pop(0)
                    if move1 == 1:
                        return self.turnleft()
                    elif move1 == 2:
                        return self.turnright()
                    elif move1 == 3:
                        # print(self.moved,'before')
#                        print(8)
                        self.moved.append(self.move)
                        # print(self.moved,'after')

                        return self.moveforaward(self.next)
                else:

                    self.back = True
                    return self.turnleft()
        else:
            print('here')
            #To catch the states that we missed
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
    def turnright(self):
        self.direction -= 90
        self.direction = self.changedirection(self.direction)
        return Agent.Action.TURN_RIGHT

    def generatesafeneighbour(self, coordinate):
        upn = [coordinate[0] + 1, coordinate[1]]
        downn = [coordinate[0] - 1, coordinate[1]]
        leftn = [coordinate[0], coordinate[1] - 1]
        rightn = [coordinate[0], coordinate[1] + 1]
        # print(coordinate, self.height, self.width)
        #print(coordinate[0])
        if coordinate[1] - 1 < 0 and coordinate[0] - 1 < 0:
            #print(0)
            self.safelist.insert(0, upn)
            self.safelist.insert(0, rightn)
        elif coordinate[0] + 1 >= self.height and coordinate[1] + 1 >= self.width:
            #print(1)
            self.safelist.insert(0, leftn)
            self.safelist.insert(0, downn)

        elif coordinate[0] - 1 < 0 and coordinate[1] + 1 >= self.width:
            #print(2)
            self.safelist.insert(0, leftn)
            self.safelist.insert(0, upn)
        elif coordinate[0] + 1 >= self.height and coordinate[1] - 1 < 0:
            #print(3)
            self.safelist.insert(0, rightn)
            self.safelist.insert(0, downn)
        elif coordinate[0] + 1 >= self.height:
            #print(4)
            self.safelist.insert(0, rightn)
            self.safelist.insert(0, downn)
            self.safelist.insert(0, leftn)

        elif coordinate[1] + 1 >= self.width:
            #print(5)
            self.safelist.insert(0, upn)
            self.safelist.insert(0, downn)
            self.safelist.insert(0, leftn)


        elif coordinate[0] - 1 < 0 and not coordinate[1] + 1 > self.width:
            #print(6)
            self.safelist.insert(0, upn)
            self.safelist.insert(0, leftn)
            self.safelist.insert(0, rightn)

        elif coordinate[1] - 1 < 0:
            #print(7)
            self.safelist.insert(0, upn)
            self.safelist.insert(0, downn)
            self.safelist.insert(0, rightn)

        else:
            #print('else')
            self.safelist.insert(0, upn)
            self.safelist.insert(0, downn)
            self.safelist.insert(0, leftn)
            self.safelist.insert(0, rightn)

    def turnleft(self):
        self.direction += 90
        self.direction = self.changedirection(self.direction)
        return Agent.Action.TURN_LEFT
    def moveforaward(self,coordinate):
        rightn = [coordinate[0], coordinate[1] + 1]
        leftn = [coordinate[0], coordinate[1] - 1]
        downn = [coordinate[0] - 1, coordinate[1]]
        upn = [coordinate[0] + 1, coordinate[1]]
        #print(self.moved, 'inmoveforward')
        if self.direction == 90:
            self.h += 1
            self.next = upn
        elif self.direction == 270:
            self.h -= 1
            self.next = downn
        elif self.direction == 180:
            self.w -= 1
            self.next = leftn
        elif self.direction == 0:
            self.w += 1
            self.next = rightn
        #print(self.moved,'inmoveforward')
        return Agent.Action.FORWARD
    def getallneighbors(self,coordinate):
        safeneigh = []
        rightn = [coordinate[0],coordinate[1] + 1]
        leftn = [coordinate[0],coordinate[1] -1]
        downn = [coordinate[0] -1,coordinate[1]]
        upn = [coordinate[0] + 1,coordinate[1]]
        if upn in self.safelist:
            safeneigh.append(upn)
        if downn in self.safelist:
            safeneigh.append(downn)
        if leftn in self.safelist:
            safeneigh.append(leftn)
        if rightn in self.safelist:
            safeneigh.append(rightn)
        return safeneigh
    def getsafeneighbor(self,safelist):  # Call this function when the agent is on nothing
        # print(self.moved,'movedget')
        # print(self.safelist,'getsaf')
        # print(self.next,'getsn')
        #print(safelist,self.next,'gets')
        for i in safelist:
            if (i or tuple(i)) not in self.moved:
                if (i[0] - 1 == self.next[0] or i[0] + 1 == self.next[0]) and i[1] == self.next[1]:
                    return i
                elif (i[1] - 1 == self.next[1] or i[1] + 1 == self.next[1]) and i[0] == self.next[0]:
                    return i

    def meetdanger(self,safelist):  # Call this function when the agent is on nothing
        # print(self.moved,'movedget')
        # print(self.safelist,'getsaf')
        #print(self.next,'getsn')
       # print(safelist,self.next,'md')
        for i in safelist:


            if (i[0] - 1 == self.next[0] or i[0] + 1 == self.next[0]) and i[1] == self.next[1]:
                return i
            elif (i[1] - 1 == self.next[1] or i[1] + 1 == self.next[1]) and i[0] == self.next[0]:
                return i
    def toneighbor(self,n):  # steps to move to safe neighbor
        """
        @param n generate a random move by safeneighbor function
        @return a list of actions 1 forward 2right 3 left
        """
        movelist = []
        #print(self.next,n,'here')
        if n == None:
            self.back = True
            return [1]
        if self.next[0] == n[0]:
            if self.next[1] == n[1] - 1:
                if self.direction == 0:
                    movelist.append(3)
                elif self.direction == 90:
                    movelist.append(2)
                    movelist.append(3)
                elif self.direction == 270:
                    movelist.append(1)
                    movelist.append(3)
                elif self.direction == 180:
                    movelist.append(1)
                    movelist.append(1)
                    movelist.append(3)
            if self.next[1] == n[1] + 1:
                if self.direction == 0:
                    movelist.append(1)
                    movelist.append(1)
                    movelist.append(3)
                elif self.direction == 90:
                    movelist.append(1)
                    movelist.append(3)
                elif self.direction == 270:
                    movelist.append(2)
                    movelist.append(3)
                elif self.direction == 180:
                    movelist.append(3)
        elif self.next[1] == n[1]:
            #print('here')
            if self.next[0] == n[0] - 1:
                if self.direction == 90:
                    movelist.append(3)
                elif self.direction == 0:
                    movelist.append(1)
                    movelist.append(3)
                elif self.direction == 180:
                    movelist.append(2)
                    movelist.append(3)
                elif self.direction == 270:
                    movelist.append(1)
                    movelist.append(1)
                    movelist.append(3)
            elif self.next[0] == n[0] + 1:
                if self.direction == 270:
                    movelist.append(3)
                elif self.direction == 180:
                    movelist.append(1)
                    movelist.append(3)
                elif self.direction == 0:
                    movelist.append(2)
                    movelist.append(3)
                elif self.direction == 90:
                    movelist.append(1)
                    movelist.append(1)
                    movelist.append(3)
        return movelist

    def changedirection(self,direction):
        return (direction ) % 360
    def isneighbor(self,current:list):
        if self.next[0] == current[0]:
            if self.next[1] == (current[1] + 1) or self.next[1] == current[1] - 1:
                return True
        elif self.next[1] == current[1]:
            if self.next[0] == current[0] + 1 or self.next[0] == current[0] - 1:
                return True
        else:
            return False
    def shortestpath(self,dest):
        move = ''
        temp = [tuple(self.next)]
        visited = {tuple(self.next): 0}
        end = False
        while len(temp) != 0 and not end:
            move = temp.pop(0)
            moves = self.getallneighbors(move)
            for i in moves:
                if tuple(i) not in visited:
                    visited[tuple(i)] = move
                    temp.append(tuple(i))
                if i == dest:
                    end = True
                    break
        if not end:
            return ""
        else:
            origin = tuple([0, 0])
            result = []
            while origin != tuple(self.next):
                result.insert(0, tuple(origin))
                origin = visited[tuple(origin)]
            result.insert(0, tuple(self.next))
            return result
    def generatenextmove(self):
        for x,y in self.safelist:
            self.news[x][y] = True
        for x in range(8):
            for y in range(8):
                if self.news[x][y] and [x,y] not in self.moved:
                    self.nextmove.append([x,y])


        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
