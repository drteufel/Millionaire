from millionaire import Player


class TestPlayer:
    def test_one(self):
        player: Player = Player(1, "test")
        assert hasattr(player, "name") and player.name == "test"
        assert hasattr(player, "player_id") and player.player_id == 1
        assert hasattr(player, "pos") and player.pos == 0
        assert hasattr(player, "money") and player.money == 150000
