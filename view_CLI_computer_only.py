import itertools
import random
from dataclasses import dataclass, field
from typing import Iterator

import model
import controller


class CLIGame:
    def __init__(self, rounds):
        self.players = [model.ComputerPlayer('Player 1'), model.ComputerPlayer('Player 2')]

        self.game = controller.GameController(self.players, rounds=rounds)

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


if __name__ == "__main__":
    my_cli_game = CLIGame(rounds=5)

    my_cli_game.play()
