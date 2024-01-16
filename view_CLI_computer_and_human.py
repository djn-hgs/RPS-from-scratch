import itertools
import random
from dataclasses import dataclass, field
from typing import Iterator

import model
import controller


class CLIGame:
    def __init__(self, rounds: int):

        self.plays = [model.Rock, model.Paper, model.Scissor]

        self.players = [
            model.ComputerPlayer('Player 1', self.plays),
            model.HumanPlayer('Player 2', self.plays)
        ]

        self.game = model.Game(self.players, rounds=rounds)

        self.controller = controller.GameController(self.game)

    def play(self):
        print('Game started')

        while not self.game.over:

            self.controller.start_round()
            print('Round started')

            while not self.game.current_round.complete:
                self.controller.next_player()

                if self.game.current_round.complete:
                    print('Round complete')
                else:
                    player = self.game.current_round.current_player

                    print(f'Current player is {player}')

                    if isinstance(player, model.ComputerPlayer):
                        self.controller.make_play_computer()
                        print(f'Play chosen was {self.game.current_round.plays[player]}')

                    if isinstance(player, model.HumanPlayer):
                        choice: model.Play = self.get_human_choice(player)
                        self.controller.make_play_human(choice)
                        print(f'Play chosen was {self.game.current_round.plays[player]}')

            self.controller.decide_winner()
            print(f'Round won by {self.game.current_round.winner}')

            self.controller.record_result()
            print(f'Result recorded {self.game.scores}')
            print(f'{len(self.game.history)} rounds of {self.game.rounds} complete')

            self.controller.check_game_over()
            if self.game.over:
                print(f'Game over (best of {self.game.rounds})')
                if self.game.winner:
                    print(f'Winner was {self.game.winner}')
                else:
                    print('No winner')

    def get_human_choice(self, player: model.Player):
        options = {}

        for p in player.plays:
            options[p.index] = p
            print(f'({p.index}) {p}')

        choice = int(input('Make a choice: '))

        return options[choice]()

if __name__ == "__main__":
    my_cli_game = CLIGame(rounds=5)

    my_cli_game.play()
