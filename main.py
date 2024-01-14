import itertools
import random
from dataclasses import dataclass, field
from typing import Iterator


@dataclass
class Play:
    beats = []

    def __gt__(self, other):
        return type(other) in self.beats

    def __lt__(self, other):
        return type(self) in other.beats

    def beats_play(self, other):
        self.beats.append(other)


class Rock(Play):
    ...


class Paper(Play):
    ...


class Scissor(Play):
    ...


Rock.beats = [Scissor]
Paper.beats = [Rock]
Scissor.beats = [Paper]


class Player:
    plays = [Rock, Paper, Scissor]

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def make_choice(self):
        type_to_play = random.choice(self.plays)
        return type_to_play()


class GameError(Exception):
    ...


class PlayerError(Exception):
    ...


class RoundError(Exception):
    ...


class Round:
    def __init__(self, players: [Player]):
        self.players = players
        self.plays: dict[Player: Play] = {}
        self.cursor: Iterator[Player] = iter(players)
        self.current_player: Player | None = None
        self.complete: bool = False
        self.play_winners: list[Player] = []
        self.winner: Player | None = None

    def __repr__(self):
        return f'Round {str(self.plays)}'

    def next_player(self):
        self.current_player = next(self.cursor, None)

        if self.current_player is None:
            self.complete = True

    def get_play(self):
        if self.complete:
            raise RoundError("Round complete")

        self.plays[self.current_player] = self.current_player.make_choice()

    def decide_winner(self):
        if not self.complete:
            raise RoundError("Round underway")

        num_players = len(self.players)

        for i in range(num_players - 1):
            for j in range(i + 1, num_players):
                p1 = self.players[i]
                p2 = self.players[j]

                if self.plays[p1] > self.plays[p2]:
                    self.play_winners.append(p1)
                elif self.plays[p2] > self.plays[p1]:
                    self.play_winners.append(p2)

        if len(self.play_winners) == 1:
            [self.winner] = self.play_winners
        else:
            self.winner = None


class GameController:
    def __init__(self, players: list[Player] | None = None, rounds=3):
        self.winner: Player | None = None
        self.rounds: int = rounds
        self.over: bool = False

        if players:
            self.players = players
        else:
            self.players = []

        self.history: list[Round] = []
        self.current_round: Round | None = None
        self.scores = {p: 0 for p in self.players}

    def start_round(self) -> None:
        self.current_round = Round(self.players)

    def next_player(self):
        if not self.current_round:
            raise GameError("Game not started")

        if self.current_round.complete:
            raise GameError("Round complete")

        self.current_round.next_player()

    def play(self):
        if not self.current_round:
            raise GameError("Game not started")

        if self.current_round.complete:
            raise GameError("Round complete")

        self.current_round.get_play()

    def round_complete(self):
        return self.current_round.complete

    def decide_winner(self):
        self.current_round.decide_winner()

        winner = self.current_round.winner

        if winner:
            self.scores[winner] += 1

    def record_result(self):
        self.history.append(self.current_round)

    def check_game_over(self):
        leader = max(self.scores, key=lambda p: self.scores[p])

        self.over = True

        for p in self.players:
            if p != leader:
                if self.scores[leader] - self.scores[p] < self.rounds - len(self.history):
                    self.over = False

        if self.over:
            self.winner = leader


class CLIGame:
    def __init__(self, rounds):
        self.players = [Player('Player 1'), Player('Player 2')]

        self.game = GameController(self.players, rounds=rounds)

    def play(self):
        print('Game started')

        while not self.game.over:

            self.game.start_round()
            print('Round started')

            while not self.game.current_round.complete:
                self.game.next_player()

                if self.game.current_round.complete:
                    print('Round complete')
                else:
                    player = self.game.current_round.current_player

                    print(f'Current player is {player}')

                    self.game.play()
                    print(f'Play chosen was {self.game.current_round.plays[player]}')

            self.game.decide_winner()
            print(f'Round won by {self.game.current_round.winner}')

            self.game.record_result()
            print(f'Result recorded {self.game.scores}')

            self.game.check_game_over()
            if self.game.over:
                print(f'Game over (best of {self.game.rounds})')
            if self.game.winner:
                print(f'Winner was {self.game.winner}')
            else:
                print('No winner')


my_cli_game = CLIGame(rounds=5)

my_cli_game.play()
