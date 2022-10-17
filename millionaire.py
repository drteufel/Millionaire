import os
import random


class Player:
    def __init__(self, player_id: int, name: str):
        self.player_id = player_id
        self.name = name
        self.money = 150000
        self.pos = 0

    def __str__(self):
        return "[Player %i - %s (%i kr)]" % (self.player_id, self.name, self.money)


class Location:
    def __init__(self, location_id: int, name: str):
        self.location_id = location_id
        self.name = name

    def __str__(self):
        return "[(%i) %s]" % (self.location_id, self.name)


class ChanceCard:
    def __init__(self, text, move_to: int, amount: int, collect: bool = True):
        self.text = text
        self.move_to = move_to
        self.amount = amount
        self.collect = collect


class Chance(Location):
    def __init__(self, location_id):
        super().__init__(location_id, name="Prøv lykken!")
        self.id = location_id

    @staticmethod
    def get_card() -> ChanceCard:
        return chanceCards[random.randint(0, 17)]


class Asset(Location):
    def __init__(self, location_id, name, price, rent):
        super().__init__(location_id, name)
        self.id = location_id
        self.name = name
        self.price = price
        self.rent = rent
        self.mortgage = price / 2
        self.ownerId = -1


class Street(Asset):
    def __init__(self, location_id, name, price, rent, house_cost, street_type):
        super().__init__(location_id, name, price, rent)
        self.house_cost = house_cost
        self.street_type = street_type


class Cinema(Asset):
    def __init__(self, location_id, name):
        super().__init__(location_id, name, price=20000, rent=[2500, 5000, 10000, 20000])


class Culture(Asset):
    def __init__(self, location_id, name):
        super().__init__(location_id, name, price=15000, rent=[400, 1000])


os.system('cls')

answer = ""
playerIndex = -1
extra = True
passStart = 20000
randomChance = 0
string = "1?1!;2?22#3§33;4?44¤5?55;66§6#77?7;?8!8"

players = [
    Player(1, "LOLeo"),
    Player(2, "pappaREal")
]

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
    ChanceCard("Etter tante Olga på Toten har du arvet 4 katter, en grønn papegøye, 16 juletrær på rot og kr 10000 "
               "som utpetales av banken.", -1, 10000),
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


def ran_dice():
    d1 = random.randint(1, 6)
    d2 = random.randint(1, 6)
    print("Terning 1 er " + str(d1))
    print("Terning 2 er " + str(d2))
    print("Du fikk " + str(d1+d2))

    return d1+d2, d1 == d2


while answer == "":
    if playerIndex != -1 and extra:
        extra = False
    else:
        playerIndex += 1
        if len(players) == playerIndex:
            playerIndex = 0
    player: Player = players[playerIndex]

    answer = input("Spiller: " + player.name)
    os.system("cls")
    if answer != "":
        print("Goodbye!")
        break

    if answer == " ":
        extra = True
    else:
        test = ran_dice()
        extra = test[1]
        player.pos += test[0]

        if player.pos > 39:
            player.money += passStart
            player.pos -= 39
        if player.money < 0:
            print("du tapte:(")
            break
        elif player.money > 999999:
            print("du vant")
            break

        loc = locations[player.pos]
        print(loc)
        if issubclass(type(loc), Asset):
            asset: Asset = loc
            if asset.ownerId == -1:
                if player.money >= asset.price:
                    if input("Enter = kjøp ") == "":
                        asset.ownerId = player.player_id
                        player.money -= asset.price
            elif asset.ownerId != player.player_id:
                print("%s eies av %s du må betale %i kr" % (asset, player.name, asset.rent[0]))
                player.money -= asset.rent[0]

        if type(loc) == Chance:
            chance: Chance = loc
            card: ChanceCard = Chance.get_card()
            print(card.text)
            player.money += card.amount
            if card.move_to != -1:
                if card.collect and card.move_to < player.pos:
                    player.money += passStart
                player.pos = card.move_to

    print(player)
    indices = [i for i, x in enumerate(locations) if issubclass(type(x), Asset) and x.ownerId == player.player_id]
    for index in indices:
        print(locations[index])
