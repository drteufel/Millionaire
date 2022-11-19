from operator import contains
import os
import random
from colorama import Fore
from colorama import Style


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
        self.owner_id = -1
        self.is_mortgaged = False

    def mortgage_asset(self):
        if self.is_mortgaged:
            return 0
        self.is_mortgaged = True
        return self.mortgage

    def un_mortgage_asset(self):
        if not self.is_mortgaged:
            return 0
        self.is_mortgaged = False
        return -self.mortgage


class Street(Asset):
    def __init__(self, location_id, name, price, rent, house_cost, street_type):
        super().__init__(location_id, name, price, rent)
        self.house_cost = house_cost
        self.street_type = street_type
        self.__houses = 0

    @property
    def properties_in_street(self):
        if self.street_type == 1 or self.street_type == 8:
            return 2
        else:
            return 3

    def owns_entire_street(self, player_id: int) -> bool:
        match = [i for i, x in enumerate(locations) if type(x) == Street
                 and player_id == x.owner_id and self.street_type == x.street_type]
        return len(match) == self.properties_in_street
    
    def are_other_properties_in_street_underdeveloped(self):
        match = [i for i, x in enumerate(locations) if type(x) == Street
                 and self.owner_id == x.owner_id and self.street_type == x.street_type]
        for m in match:
            street: Street = locations[m]
            if self.__houses > street.__houses:
                return True
        return False

    def calculate_rent(self) -> int:
        if self.__houses > 0:
            return asset.rent[self.__houses]
        elif self.owns_entire_street(self.owner_id):
            return asset.rent[0]*2
        return asset.rent[0]

    def buy_house(self, player: Player) -> bool:
        if not self.owns_entire_street(player.player_id):
            print("Du eier ikke alle eiendommene i denne gaten")
        elif self.is_any_property_in_street_mortgaged():
            print("En eller flere av eiendommene i denne gruppen er pantsatt")
        elif self.__houses == 5:
            print("Det er allerede et hotell her")
        elif self.house_cost > player.money:
            print("Du mangler %ikr for å kjøpe et hus" % (self.house_cost - player.money))
        elif self.are_other_properties_in_street_underdeveloped():
            print("Du må bygge flere hus på en av de andre einendommene i gaten først")
        else:
            player.money -= self.house_cost
            self.__houses += 1
            return True
        return False

    def is_any_property_in_street_mortgaged(self) -> bool:
        match = [i for i, x in enumerate(locations) if type(x) == Street
                 and self.street_type == x.street_type and self.is_mortgaged]
        return len(match) > 0

    def mortgage_house(self) -> int:
        if self.__houses == 0:
            return 0
        self.__houses -= 1
        return -self.house_cost/2

    def __str__(self):
        fore: Fore = Fore.WHITE
        if self.street_type == 1:
            fore = Fore.BLUE
        elif self.street_type == 2:
            fore = Fore.LIGHTMAGENTA_EX
        elif self.street_type == 3:
            fore = Fore.LIGHTGREEN_EX
        elif self.street_type == 4:
            fore = Fore.LIGHTBLACK_EX
        elif self.street_type == 5:
            fore = Fore.RED
        elif self.street_type == 6:
            fore = Fore.LIGHTRED_EX
        elif self.street_type == 7:
            fore = Fore.LIGHTYELLOW_EX
        elif self.street_type == 8:
            fore = Fore.YELLOW

        return "%s[(%i) %s]%s" % (fore, self.location_id, self.name, Style.RESET_ALL)


class Cinema(Asset):
    def __init__(self, location_id, name):
        super().__init__(location_id, name, price=20000, rent=[2500, 5000, 10000, 20000])

    @staticmethod
    def calculate_rent() -> int:
        matches = [i for i, x in enumerate(locations) if type(x) == Cinema and x.owner_id == asset.owner_id]
        return asset.rent[len(matches) - 1]


class Culture(Asset):
    def __init__(self, location_id, name):
        super().__init__(location_id, name, price=15000, rent=[400, 1000])

    @staticmethod
    def calculate_rent(dice) -> int:
        matches = [i for i, x in enumerate(locations) if type(x) == Culture and x.owner_id == asset.owner_id]
        return asset.rent[len(matches) - 1] * dice


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
    ChanceCard("I annledning av bankens 100-års-jubileum utbetales kr 5000 i ekstra bonus.", -1, 5000),
    ChanceCard("Du har kjøpt et maleri på loppemarked og selger det videre med kr 5000 i fortjenelse "
               "som utbetales av banken.", -1, 5000),
    ChanceCard("Du har fødselsdag. Motta kr 1000 av hver motspiller i gave.", -1, 1000),  # ???
    ChanceCard("Rykk fram til nermeste kino og betal eieren to ganger den leie han ellers er berettiget til. "
               "Hvis ingen eier kinoen, kan du kjøpe den av banken.", -1, 0),  # ???
    ChanceCard("Arrestanten løslates. Dette kortet kan oppbevares til du får bruk for det.", -1, 0),  # ???
    ChanceCard("Betal for snørYdding kr 1000 pr tomt du eier.", -1, 0),  # ???
    ChanceCard("Arrestanten løslates. Dette kortet kan oppbevares til du får bruk for det.", -1, 0),  # ???
    ChanceCard(
        "Betal kr 2500 i brannforsikringspremie. Dette kortet oppbevares. Ved brann betales bare 10% av bygningens verdi.",
        -1, 0),  # ???
    ChanceCard("Gaten asfalteres. Du må betale et tilskudd på kr 5000 pr hus og kr 12500 pr hotell/slott.", -1, 0),
    # ???
    ChanceCard("Arrestanten løslates. Dette kortet kan oppbevares til du får bruk for det.", -1, 0),  # ???
    ChanceCard("Du må reparere det elektriske anlegget. Betal kr 2500 pr hus og kr 12500 pr hotell/slott.", -1, 0),
    ChanceCard(
        "Dine hus og hoteller/slott brenner. Har du assurert (dvs tidligere trukket sjansekort ang brannforsikringspremie) "
        "betales bare 10% av bigningenes verdi. Bygningene kan da bli stående. Bygningene leveres til banken hvis du ikke har assurert.",
        -1, 0)  # ???
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
    print("Du fikk " + str(d1 + d2))

    return d1 + d2, d1 == d2


while answer == "":
    if playerIndex != -1 and extra:
        extra = False
    else:
        playerIndex += 1
        if len(players) == playerIndex:
            playerIndex = 0
    current_player: Player = players[playerIndex]

    answer = input("Spiller: " + str(current_player) + ". Trykk enter for å rulle terning")
    os.system('cls')
    if answer != "":
        print("Goodbye!")
        break

    if answer == " ":
        extra = True
    else:
        test = ran_dice()
        extra = test[1]
        if extra:
            print("Esktra kast!")
        current_player.pos += test[0]

        if current_player.pos > 39:
            current_player.money += passStart
            current_player.pos -= 39
        if current_player.money < 0:
            print("du tapte:(")
            break
        elif current_player.money > 999999:
            print("du vant")
            break

        loc = locations[current_player.pos]
        print(loc)
        if issubclass(type(loc), Asset):
            asset: Asset = loc
            if asset.owner_id == -1:
                if current_player.money >= asset.price:
                    if input("koster " + str(asset.price) + " Enter = kjøp ") == "":
                        asset.owner_id = current_player.player_id
                        current_player.money -= asset.price
            elif asset.owner_id != current_player.player_id:
                rent_to_pay = 0
                if type(loc) == Cinema:
                    cinema: Cinema = loc
                    rent_to_pay = cinema.calculate_rent()
                elif type(loc) == Culture:
                    culture: Culture = loc
                    rent_to_pay = culture.calculate_rent(test[0])
                else:
                    street: Street = loc
                    rent_to_pay = street.calculate_rent()

                print("%s eies av %s du må betale %i kr" % (asset, players[asset.owner_id - 1].name, rent_to_pay))
                current_player.money -= rent_to_pay

        if type(loc) == Chance:
            chance: Chance = loc
            card: ChanceCard = Chance.get_card()
            print(card.text)
            current_player.money += card.amount
            if card.move_to != -1:
                if card.collect and card.move_to < current_player.pos:
                    current_player.money += passStart
                current_player.pos = card.move_to
    print(str(current_player))
    if input("Vill du se eiendomer: J = Ja ").upper() == "J":
        indices = [i for i, x in enumerate(locations) if issubclass(type(x), Asset) and x.owner_id == current_player.player_id]
        if len(indices) == 0:
            print("Du har ingen eiendommer")
        else:
            print("{")
            for index in indices:
                print(locations[index])
            print("}")
            id = "0"
            while id.isdigit():
                print(str(current_player))
                id = input("Velg en eiendom for å redigere den. int: ")
                if id.isdigit():
                    index = int(id) - 1
                    if contains(indices, index):
                        asset: Asset = locations[index]
                        print(locations[index])
                        action = input(
                            "Hva vill du gjøre: P = pantsett, L = løse inn, H = kjøpe hus, S = selge hus ").upper()
                        if action == "P":
                            current_player.money += asset.mortgage_asset()
                        elif action == "L":
                            current_player.money += asset.un_mortgage_asset()
                        elif action == "H":
                            if type(asset) != Street:
                                print("Du kan bare kjøpe hus på gater")
                            else:
                                street: Street = asset
                                print(street)
                                street.buy_house(current_player)
                        elif action == "S":
                            print("ikke implomentert")

                    else:
                        print("du har ikke denne eiendommen")
