import builtins
from unittest import mock

import pytest

import millionaire
from millionaire import Asset, Player, Street, locations, Chance, chanceCards, players


class TestPlayer:
    def test_one(self):
        player: Player = Player(1, "test")
        assert hasattr(player, "name") and player.name == "test"
        assert hasattr(player, "player_id") and player.player_id == 1
        assert hasattr(player, "pos") and player.pos == 0
        assert hasattr(player, "money") and player.money == 150000


class TestChanceCards:
    def test_one(self):
        player: Player = players[0]
        money_before = player.money
        chance: Chance = locations[2]
        chance.draw(player, 27)
        assert player.money == money_before+1000*(len(players)-1)


class TestAsset:

    @pytest.fixture(autouse=True)
    def setup(self):
        millionaire.init()
  
    def test_can_sell_house(self, capfd):
        millionaire.init()
        player: Player = Player(1, "test")
        locations[1].owner_id = 1
        locations[3].owner_id = 1
        street: Street = locations[1]
        street2: Street = locations[3]
        assert street.sell_house(player) is False
        out, err = capfd.readouterr()
        assert "Du eier ingen hus på denne gata" in out
        street.buy_house(player)
        street2.buy_house(player)
        street.buy_house(player)
        assert street2.sell_house(player) is False
        out, err = capfd.readouterr()
        assert "Du må selge hus på en av de andre einendommene i gaten først" in out
        assert street.sell_house(player)

    def test_can_buy_house(self):
        millionaire.init()
        locations[1].owner_id = 1
        locations[3].owner_id = 1
        street: Street = locations[1]
        assert street.buy_house(Player(1, "test"))
        assert street.buy_house(Player(2, "test")) is False

    def test_should_not_buy_house_if_any_is_mortgaged(self, capfd):
        millionaire.init()
        locations[1].is_mortgaged = True
        locations[1].owner_id = 1
        locations[3].owner_id = 1
        street: Street = locations[1]
        assert street.buy_house(Player(1, "test")) is False
        out, err = capfd.readouterr()
        assert "pantsatt" in out

    def test_should_not_buy_house_if_not_own_entire_street(self, capfd):
        millionaire.init()
        locations[1].owner_id = 1
        locations[3].owner_id = 2
        street: Street = locations[1]
        assert street.buy_house(Player(1, "test")) is False
        out, err = capfd.readouterr()
        assert "Du eier ikke alle eiendommene i denne gaten" in out

    def test_should_not_buy_house_if_already_hotel(self, capfd):
        millionaire.init()
        locations[1].owner_id = 1
        locations[3].owner_id = 1
        street: Street = locations[1]
        street2: Street = locations[3]
        for i in range(5):
            street.buy_house(Player(1, "test"))
            street2.buy_house(Player(1, "test"))
        assert street.buy_house(Player(1, "test")) is False
        out, err = capfd.readouterr()
        assert "hotell" in out

    def test_should_not_buy_house_if_not_enough_money(self, capfd):
        millionaire.init()
        locations[1].owner_id = 1
        locations[3].owner_id = 1
        street: Street = locations[1]
        player: Player = Player(1, "test")
        player.money = 200
        assert street.buy_house(player) is False
        out, err = capfd.readouterr()
        assert "Du mangler 4800kr for å kjøpe et hus" in out
    # 
    # def test_should_not_buy_house_if_it_results_in_more_than_one_house_more_than_on_other_properties_in_street(self, capfd):
    #     locations[1].owner_id = 1
    #     locations[3].owner_id = 1
    #     street: Street = locations[1]
    #     street.buy_house(Player(1, "test"))
    #     assert street.buy_house(Player(1, "test")) is False
    #     out, err = capfd.readouterr()
    #     assert "flere hus" in out
    # 
    # def test_mortgage(self):
    #     asset: Asset = locations[1]
    #     assert asset.mortgage_asset() == 3000
