import model


class GameError(Exception):
    ...


class PlayerError(Exception):
    ...


class RoundError(Exception):
    ...


class GameController:
    def __init__(self, game):
        self.game = game

    def start_round(self) -> None:
        self.game.current_round = model.Round(self.game.players)

    def next_player(self):
        if not self.game.current_round:
            raise GameError("Game not started")

        if self.game.current_round.complete:
            raise GameError("Round complete")

        self.game.current_round.next_player()

    def make_play_human(self, choice: model.Play):
        if not self.game.current_round:
            raise GameError("Game not started")

        if self.game.current_round.complete:
            raise GameError("Round complete")

        self.game.current_round.set_play(choice)

    def make_play_computer(self):
        if self.game.current_round.complete:
            raise GameError("Round complete")

        if not isinstance(self.game.current_round.current_player, model.ComputerPlayer):
            raise GameError("Only computer players can choose their own play")

        self.game.current_round.get_computer_choice()

    def round_complete(self):
        return self.game.current_round.complete

    def decide_winner(self):
        if not self.game.current_round.complete:
            raise RoundError("Round underway")

        self.game.current_round.decide_winner()

        winner = self.game.current_round.winner

        if winner:
            self.game.add_point(winner)

    def record_result(self):
        self.game.history.append(self.game.current_round)

    def check_game_over(self):
        self.game.check_game_over()
