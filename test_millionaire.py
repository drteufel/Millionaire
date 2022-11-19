from millionaire import Asset, Player, Street, locations


class TestPlayer:
    def test_one(self):
        player: Player = Player(1, "test")
        assert hasattr(player, "name") and player.name == "test"
        assert hasattr(player, "player_id") and player.player_id == 1
        assert hasattr(player, "pos") and player.pos == 0
        assert hasattr(player, "money") and player.money == 150000


class TestAsset:
    def test_can_buy_house(self):
        locations[1].owner_id = 1
        locations[3].owner_id = 1
        street: Street = locations[1]
        assert street.buy_house(Player(1, "test"))
        assert street.buy_house(Player(2, "test")) is False

    def test_should_not_buy_house_if_any_is_mortgaged(self, capfd):
        locations[1].is_mortgaged = True
        locations[1].owner_id = 1
        locations[3].owner_id = 1
        street: Street = locations[1]
        assert street.buy_house(Player(1, "test")) is False
        out, err = capfd.readouterr()
        assert "pantsatt" in out

    def test_should_not_buy_house_if_already_hotel(self, capfd):
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

    def test_mortgage(self):
        asset: Asset = locations[1]
        assert asset.mortgage_asset() == 3000
