import random
import tkinter as tk
import model
import controller


class PlayersDisplay(tk.Frame):
    def __init__(self, master: tk.Frame | tk.Tk, players: list[model.Player], *args, **kwargs):
        # Initialise our game as a tk.Frame

        super().__init__(master, *args, **kwargs)

        self.player_columns = {p: PlayerWidget(self, p) for p in players}

        for i, p in enumerate(players):
            self.player_columns[p].grid(row=0, column=i)

    def show_active(self, player):
        self.player_columns[player].show_active()

    def show_inactive(self, player):
        self.player_columns[player].show_inactive()


class PlayerWidget(tk.Frame):
    def __init__(self, master: tk.Frame | tk.Tk, player: model.Player, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.player = player
        self.master = master

        self.name_label = tk.Label(self, text=player.name)
        self.type_label = tk.Label(self)

        if isinstance(self.player, model.ComputerPlayer):
            self.type_label.config(text='Computer')
        elif isinstance(self.player, model.HumanPlayer):
            self.type_label.config(text='Human')

        self.choice = tk.IntVar()
        self.choice.set(-1)

        self.player_choices = {p: tk.Radiobutton(self, text=p.label, value=p.index, variable=self.choice) for i, p in enumerate(player.plays)}

        self.name_label.grid(row=0)
        self.type_label.grid(row=1)

        for i, p in enumerate(self.player_choices):
            self.player_choices[p].grid(row=i + 2)

    def show_active(self):
        self.name_label['bg'] = 'teal'

    def show_inactive(self):
        self.name_label['bg'] = 'SystemButtonFace'

class TkGame(tk.Frame):
    def __init__(self, master: tk.Frame | tk.Tk, rounds: int, *args, **kwargs):
        # Initialise our game as a tk.Frame

        super().__init__(master, *args, **kwargs)

        # Describe a standard two-player game of standard RPS

        self.plays = [model.Rock, model.Paper, model.Scissor]

        self.players = [
            model.ComputerPlayer('Player 1', self.plays),
            model.HumanPlayer('Player 2', self.plays)
        ]

        self.game = model.Game(self.players, rounds=rounds)

        self.controller = controller.GameController(self.game)

        # Now describe the widgets in our GUI

        # One row is our title row

        self.title = tk.Label(self, text="RPS")

        # One row is a frame that will contain each player's choices

        self.player_widgets = PlayersDisplay(self, self.players)

        # One row for a "play" button (which will force random choice for computer players)

        self.play_button = tk.Button(self, text='Play', command=self.game_play)

        # One row for result of round

        self.results_text = tk.StringVar()
        self.results_text.set('Results')

        self.results_label = tk.Label(self, textvariable=self.results_text)

        # One row for scores thus far

        self.scores_text = tk.StringVar()
        self.scores_text.set('Scores')

        self.score_label = tk.Label(self, textvariable=self.scores_text)

        # One row to declare "game on" or "game over"

        self.game_status_text = tk.StringVar()
        self.game_status_text.set('Press Play to Start')

        self.game_status_label = tk.Label(self, textvariable=self.game_status_text)

        # Now grid our widgets

        self.title.grid()
        self.player_widgets.grid()
        self.play_button.grid()
        self.results_label.grid()
        self.score_label.grid()
        self.game_status_label.grid()

    def game_play(self):
        # This needs to get the status of the game from the controller and trigger the next step on that basis

        # First, if the game hasn't started then we can start it

        self.controller.start_round()
        self.game_status_text.set('Round started')

        if not self.game.current_round.complete:
            if not self.game.current_round.awaiting_choice:
                self.controller.next_player()

        if self.game.current_round.complete:
            self.game_status_text.set('Round complete')

        else:
            player = self.game.current_round.current_player

            for p in self.players:
                if p != player:
                    self.player_widgets.show_inactive(p)

            self.player_widgets.show_active(player)

            self.game_status_text.set(f'{player} to make choice')

if __name__ == '__main__':
    root = tk.Tk()

    my_gui = TkGame(root, rounds=5)

    my_gui.grid()

    root.mainloop()
