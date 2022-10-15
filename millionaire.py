import os
import random

os.system('cls')

opencards = 0
POS = 0
D1 = 0
D2 = 0
answear = ""
p1Money = 150000
ransjanse = 0
string = "1?1!;2?22#3§33;4?44¤5?55;66§6#77?7;?8!8"

class Location:
    def __init__(self, id : int, name : string):        
        self.id = id
        self.name = name
    def __str__(self):
        return self.name

class Chance(Location):
    def __init__(self, id):
        super().__init__(id, name = "Prøv lykken")   
        self.id = id
        def GetCard():
            return chanceCards[random.randint(0, 17)]

class ChanceCard:
  def __init__(self, text, moveTo, amount, collect=True):
    self.text = text
    self.moveTo = moveTo
    self.amount = amount
    self.collect = collect

class Asset(Location):
    def __init__(self, id, name, price):
        super().__init__(id, name)   
        self.id = id
        self.name = name
        self.price = price
        self.mortgage = price/2
        self.ownerId = -1

class Street(Asset):
    def __init__(self, id, name, price, rent, houseCost, streettype):
        super().__init__(id, name, price)        
        self.rent = rent
        self.houseCost = houseCost       
        self.streettype = streettype

class Cinema(Asset):
     def __init__(self, id, name):
        super().__init__(self, id, price = 20000)        
        self.rent = [2500, 5000, 10000, 20000]

class Culture(Asset):
     def __init__(self, id, name):
        super().__init__(id, name, price = 15000)        
        self.rent = [400, 1000]



locations = [
    Location(1, "Start"),
    Street(2, "Frognerveien", 6000, [200, 1000, 3000, 9000, 16000, 25000], 5000, 1),
    Chance(3), 
    Street(4, "Kirkeveien", 6000, [400, 2000, 6000, 18000, 32000, 45000], 5000, 1),
    Location(5, "Betal 10% 1 skatt eller 20000"),
    Cinema(6, "Eldorado kino"),
    Street(7, "Kronprinsensgate", 10000, [600, 3000, 9000, 27000, 40000, 55000], 5000, 2),
    Chance(8),
    Street(9, "Dronningens gate", 10000, [600, 3000, 9000, 27000, 40000, 55000], 5000, 2),
    Street(10, "Kongens gate", 12000, [800, 4000, 10000, 30000, 45000, 60000], 5000, 2),
    Location(11, "Fengsel"),
    Street(12, "Nedre slottsgate", 14000, [1000, 5000, 15000, 45000, 62000, 75000], 5000, 3),
    Culture(13, "Nationaltheatret"),
    Street(14, "Grensen", 14000, [1000, 5000, 15000, 45000, 62000, 75000], 5000, 3),
    Street(15, "Tordenskjolds gate", 16000, [1200, 6000, 18000, 50000, 70000, 90000], 10000, 3),
    Cinema(16, "Saga kino"),
    Street(17, "Trondheimsveien", 18000, [1400, 7000, 20000, 55000, 75000, 95000], 10000, 4),
    Chance(18),
    Street(19, "Mosseveien", 18000, [1400, 7000, 20000, 55000, 75000, 95000], 10000, 4),
    Street(20, "Drammensveien", 20000, [1600, 8000, 22000, 60000, 80000, 100000], 10000, 4),
    Location(21, "Trafiklys"),
    Street(22, "Bygdøy", 22000, [1800, 9000, 25000, 70000, 87000, 105000], 15000, 5),
    Chance(23),
    Street(24, "Holmenkollen", 22000, [1800, 9000, 25000, 70000, 87000, 105000], 15000, 5),
    Street(25, "Slemdal", 24000, [2000, 10000, 30000, 75000, 92000, 110000], 15000, 5),
    Cinema(26, "Klingenberg kino"),
    Street(27, "Karl johansgate", 26000, [2200, 11000, 33000, 80000, 97500, 115000], 15000, 6),
    Street(28, "Studenterlunden", 26000, [2200, 11000, 33000, 80000, 97500, 115000], 15000, 6),
    Culture(29, "operaen"),
    Street(30, "Stortingsgaten", 28000, [2400, 12000, 36000, 85000, 102000, 120000], 15000, 6),
    Location(31, "Du settes i fengsel"),
    Street(32, "Lambertseter", 30000, [2600, 13000, 39000, 90000, 110000, 127000], 20000, 7),
    Street(33, "Vålerenga", 30000, [2600, 13000, 39000, 90000, 110000, 127000], 20000, 7),
    Chance(34),
    Street(35, "Sinsen", 32000, [2800, 15000, 45000, 100000, 120000, 140000], 20000, 7),
    Cinema(36, "Colosseum kino"),
    Chance(37),
    Street(38, "Aker brygge", 35000, [3500, 17000, 50000, 110000, 130000, 150000], 20000, 8),
    Location(39, "Betal formueskatt 10000"),
    Street(40, "Slottsplassen", 40000, [5000, 20000, 60000, 140000, 170000, 200000], 20000, 8)
]


chanceCards = [
    ChanceCard("Du har kolidert med bilen! Betal kr 5000 for ny støt fanger.", -1, -5000), 
    ChanceCard("Flytt direkte til fengsel. Selv om du passerer START får du ikke kr 20000.", 10, 0, False),
    ChanceCard("Motta kr 30000 fra en onkel i amerika.", -1, 30000),
    ChanceCard("Du har vunnet kr 5000 på trav banen.", -1, 5000),
    ChanceCard("Du har vunnet i Lotto. Motta kr 20000", -1, 20000),
    ChanceCard("du har vunnet i Lotto. Motta kr 30000", -1, 30000),
    ChanceCard("Ligningen er utlagt. Betal restskatt på kr 7500", -1, -7500), 
    ChanceCard("Betal eiendomsskatt og avgifter med kr 2000", -1, -2000),
    ChanceCard("Du har mistet en plombe i en tann. Betal kr 1000 i tannlegeregning.", -1, -1000),
    ChanceCard("Flytt direkte til fengsel. Selv om du passerer START får du ikke kr 20000.", 10, 0, False),
    ChanceCard("Du blir utnevnt til landest mest lovende millionær-aspirant. Motta kr 30000", -1, 30000),
    ChanceCard("Du får julegratiale på kr 2000", -1, 2000),
    ChanceCard("Hev renter på sparekontoen din. Motta kr 5000", -1, 5000), 
    ChanceCard("Du selger aksjer og mottar kr 15000 fra banken.", -1, 15000),
    ChanceCard("Du er tatt i fartskontroll og må betale kr 1000 i bot.", -1, -1000),
    ChanceCard("Ligningen er utlagt og du får kr 5000 igjen på skatten.", -1, 5000),
    ChanceCard("Rykk fram til START.", 0, 0),
    ChanceCard("Etter tante Olga på Toten har du arvet 4 katter, en grønn papegøye, 16 juletrær på rot og kr 10000 som utpetales av banken.", -1, 10000), 
    ChanceCard("Du har vunnet i Tipping. Motta kr 10000", -1, 10000),
    ChanceCard("Rykk fram til gensen. Hvis tu passerer START, får du kr 20000", 13, 0, True), 
    ChanceCard("Rykk fram til stortingsgaten. Hvis du passerer START, får du kr 20000", 29, 0, True), 
    ChanceCard("Rykk fram til kongens gate. Hvis du passerer START, får du kr 20000", 9, 0, True),
    ChanceCard("Rykk fram til studenterlunden. Hvis du passerer START, får du kr 20000", 27, 0, True),
    ChanceCard("Flytt til Colosseum kino. Motta kr 20000 hvis du passerer START", 35, 0, True),
    ChanceCard("Rykk fram til Lambertseter. Hvis du passerer START, får du kr 20000", 31, 0, True),
]

print(" __       __   _   _       _       _      _      __    _   __________   ____")
print("|  \     /  | | | | |     | |     | |  _ |_| _  |  \  | | |   \______| |  __|_")
print("|   \   /   | | | | |     | |     | | | |   | | |   \ | | | |\ \_____  | |__|_|")
print("| |\ \_/ /| | | | | |     | |     | | | |   | | | |\ \| | | |_\ \____| | |\ \ ")
print("| | \   / | | | | | |___  | |___  | | |_|   |_| | | \   | | |__\ \___  | | \ \ ")
print("|_|  \_/  |_| |_| |_____| |_____| |_|    |_|    |_|  \ _| |_|   \_\__| |_|  \_\ ")

#print(str(POS + 1) + "-" + locations[POS])
#print("kr: " + str(p1Money))

def RanDice(currentPos):
   
    ekstra = False
    T_F = True
    os.system('cls')
    
    D1 = random.randint(1, 6)
    D2 = random.randint(1, 6)
    D3 = D1 + D2
    print("Terning 1 er " + str(D1))
    print("Terning 2 er " + str(D2))
    print("Du fikk " + str(D3))
    if D1 == D2:
        print("Ekstra kast")
        ekstra = True
    print("")
    return currentPos + D3, ekstra

while answear == "":
    answear = input("enter = rull terning: ")
    POS = RanDice(POS)[0]
    if POS > 39:
        p1Money += 20000
        POS -= 39
    elif POS == 38:
        p1Money -= 10000
    if p1Money < 0 and opencards == 0:
        print("du tapte:(")
        break
    elif p1Money > 999999:
        print("du vant")
        break

    
    loc = locations[POS]
    print(str(POS + 1) + "-" + str(loc) )
   
    
    print(string)
    print(" " * (POS - 1) + "^")
    print("du har: " + str(p1Money) + " kr")

    # if locations[POS] == "prøv lykken":
    #     ransjanse = random.randint(0, 17)
    #     chance = chanceCards[ransjanse]
    #     print(chance.text)
    #     if chance.moveTo!=-1:
    #         if(chance.collect and chance.moveTo < POS):
    #             p1Money += 20000
    #         POS = chance.moveTo
    #     p1Money += chance.amount
os.system('cls')