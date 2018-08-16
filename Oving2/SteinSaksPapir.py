import random
import matplotlib.pyplot as plt

class Player:

    def __init__(self,name):
        self.name=name
        self.points=0.0

    def choose(self):
        pass

    def recieve_result(self,opponent,own,result):
        if result == 1:
            self.points += 1.0
        elif result == 2:
            self.points += 0.5


    def get_name(self):
        return self.name

    def get_points(self):
        return self.points


class RandomPlayer(Player):

    def __init__(self):
        name="Random"
        super().__init__(name)

    def choose(self):
        x = random.randint(0, 2)
        return x


class SequentialPlayer(Player):

    def __init__(self):
        name = "Sequential"
        self.ind = 0
        super().__init__(name)

    def choose(self):
        x=self.ind
        if self.ind < 2:
            self.ind += 1
        else:
            self.ind = 0
        return x


class MostCommonPlayer(Player):

    def __init__(self):
        name = "Most Common"
        self.r = 0
        self.p = 0
        self.s = 0
        super().__init__(name)

    def choose(self):
        if self.r-(self.s+self.p) > 0:
            return 1
        elif self.p-(self.s+self.r) > 0:
            return 2
        elif self.s-(self.r+self.p) > 0:
            return 0
        else:
            return random.randint(0,2)

    def recieve_result(self,opponent,own,result):
        if opponent == 0:
            self.r += 1
        elif opponent == 1:
            self.p += 1
        elif opponent == 2:
            self.s += 1
        super().recieve_result(opponent,own,result)


class Historian(Player):

    def __init__(self,husk):
        name = "Historian"
        self.husk = husk
        self.history = []
        super().__init__(name)

    def choose(self):
        if len(self.history) < self.husk+2:
            return random.randint(0,2)
        else:
            matches = []
            husk=self.history[-self.husk:]

            for i in range(len(self.history)-len(husk)):
                if self.history[i] == husk[0] and self.history[i:i+len(husk)] == husk:
                    matches.append(self.history[i+len(husk)])
            if len(matches)==0:
                return random.randint(0,2)
            expected = max(set(matches), key=matches.count)
            if expected == 0:
                return 1
            elif expected == 1:
                return 2
            else:
                return 0

    def recieve_result(self,opponent,own,result):
        self.history.append(opponent)
        super().recieve_result(opponent,own,result)


class SimpleGame:

    list = ["Rock", "Paper", "Scissor"]

    def __init__(self, spiller1, spiller2):
        self.p1 = spiller1
        self.p2 = spiller2
        self.choice1 = None
        self.choice2 = None
        self.result = None

    def play(self):
        self.choice1 = self.p1.choose()
        self.choice2 = self.p2.choose()

        if self.choice1 == self.choice2:
            self.p1.recieve_result(self.choice2,self.choice1,2)
            self.p2.recieve_result(self.choice1,self.choice2,2)
            self.result = "Draw"

        else:
            self.compare(self.choice1,self.choice2)
        print(self)

    def compare(self,s1,s2):
        if s1 == 0:
            if s2 == 1:
                self.p1.recieve_result(s2,s1,0)
                self.p2.recieve_result(s1,s2,1)
                self.result = self.p2.get_name() #p2 vant
            elif s2 == 2:
                self.p1.recieve_result(s2,s1,1)
                self.p2.recieve_result(s1,s2,0)
                self.result = self.p1.get_name() #p1 vant
        elif s1 == 1:
            if s2 == 0:
                self.p1.recieve_result(s2,s1,1)
                self.p2.recieve_result(s1,s2,0)
                self.result = self.p1.get_name() #p1 vant
            elif s2 == 2:
                self.p1.recieve_result(s2,s1,0)
                self.p2.recieve_result(s1,s2,1)
                self.result = self.p2.get_name() #p2 vant
        elif s1 == 2:
            if s2 == 0:
                self.p1.recieve_result(s2,s1,0)
                self.p2.recieve_result(s1,s2,1)
                self.result = self.p2.get_name() #p2 vant
            elif s2 == 1:
                self.p1.recieve_result(s2,s1,1)
                self.p2.recieve_result(s1,s2,0)
                self.result = self.p1.get_name() #p1 vant

    def __str__(self):
        return "P1 - "+self.p1.get_name()+": "+self.list[self.choice1]+",\t"+"P2 - "+self.p2.get_name()+": "+self.list[self.choice2]+"\t-> winner: "+self.result


class ManyGames(SimpleGame):

    def __init__(self,spiller1,spiller2,nr_games):
        super().__init__(spiller1,spiller2)
        self.games=nr_games
        self.p1_result=[]

    def single_game(self):
        self.play()

    def play_games(self):
        i=0
        while i<self.games:
            self.single_game()
            self.p1_result.append((self.p1.points)/(i+1))
            i += 1
        print("\n"+self.p1.get_name()+": "+str(self.p1.points)+",\t"+self.p2.get_name()+": "+str(self.p2.points))
        print("Player1 win rate = "+str(self.p1.points/(self.p1.points+self.p2.points)))
        plt.plot(self.p1_result)
        plt.ylabel("P1: win-rate")
        plt.xlabel("Games")
        plt.grid(True)
        plt.show()

def main():
    print("Velg type spiller. Ran=Tilfeldig, Seq=Sekvensiell, MC=Mest Vanlig, Hist1=Historiker(husker1), Hist2=Historiker(husker2)")
    p1 = input("P1: ")
    if p1 == "Ran":
        p1 = RandomPlayer()
    elif p1 == "Seq":
        p1 = SequentialPlayer()
    elif p1 == "MC":
        p1 = MostCommonPlayer()
    elif p1 == "Hist1":
        p1 = Historian(1)
    elif p1 == "Hist2":
        p1 = Historian(2)
    else:
        print("Ugyldig input for P1")

    p2 = input("P2: ")
    if p2 == "Ran":
        p2 = RandomPlayer()
    elif p2 == "Seq":
        p2 = SequentialPlayer()
    elif p2 == "MC":
        p2 = MostCommonPlayer()
    elif p2 == "Hist1":
        p2 = Historian(1)
    elif p2 == "Hist2":
        p2 = Historian(2)
    else:
        print("Ugyldig input for P2")
    turnering = ManyGames(p1,p2,100)
    turnering.play_games()

main()

#player1 = Historian(1)
#player2 = SequentialPlayer()
#turnering = ManyGames(player1,player2,100)
#turnering.play_games()

