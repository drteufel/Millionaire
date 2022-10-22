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
        assert street.can_buy_house(1)
        assert street.can_buy_house(2) == False
    def test_mortgage(self):
        asset : Asset = locations[1]
        assert asset.mortgage_asset() == 3000
