import itertools
import random
from dataclasses import dataclass, field
from typing import Iterator, Type


@dataclass
class Play:
    index = None
    beats = []
    label = ''

    def __gt__(self, other):
        return type(other) in self.beats

    def __lt__(self, other):
        return type(self) in other.beats

    def beats_play(self, other):
        self.beats.append(other)


class Rock(Play):
    index = 0
    label = 'Rock'


class Paper(Play):
    index = 1
    label = 'Paper'


class Scissor(Play):
    index = 2
    label = 'Scissor'


Rock.beats = [Scissor]
Paper.beats = [Rock]
Scissor.beats = [Paper]


class Player:
    def __init__(self, name: str, plays: list[Type[Play]]):
        self.plays = plays
        self.name = name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def make_random_choice(self):
        type_to_play = random.choice(self.plays)
        return type_to_play()


class ComputerPlayer(Player):
    ...


class HumanPlayer(Player):
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

    def get_computer_choice(self):
        self.plays[self.current_player] = self.current_player.make_random_choice()

    def set_play(self, choice: Play):
        self.plays[self.current_player] = choice

    def decide_winner(self):
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


class Game:
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

    def add_point(self, winner: Player):
        self.scores[winner] += 1

    def check_game_over(self):
        rounds_left = self.rounds - len(self.history)

        lead_score = max(self.scores.values())

        leaders = [
            p for p in self.scores
            if self.scores[p] == lead_score
        ]

        hopefuls = [
            p for p in self.scores
            if self.scores[p] < lead_score <= self.scores[p] + rounds_left
        ]

        self.over = (rounds_left == 0
                     or (len(leaders) == 1 and not hopefuls))

        if self.over and len(leaders) == 1:
            [self.winner] = leaders
        else:
            self.winner = None
