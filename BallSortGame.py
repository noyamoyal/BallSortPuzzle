import random
import GUI
from functools import partial

COLORS = ['red', 'green', 'blue', 'purple', 'pink', 'yellow', 'orange', 'turquoise', 'grey']
HUMAN = "human"

class BallSortGame:

    def __init__(self, agent=HUMAN, n_colors=5):
        self.n_colors = n_colors
        self.n_tubes = 0
        self.steps = 0
        self.tubes = []
        self.init_tubes()
        self.init_balls_in_tubes()
        self.gui = GUI.BallSortGui(n_colors, self.tubes)
        if agent == HUMAN:
            self.set_user_events()
        self.selected_ball = None
        self.selected_tube_idx = None
        self.gui.root.mainloop()

    def init_tubes(self):
        if self.n_colors <= 3:
            self.n_tubes = self.n_colors + 1
        elif self.n_colors <= 7:
            self.n_tubes = self.n_colors + 2
        else:
            self.n_tubes = self.n_colors + 3
        for i in range(self.n_tubes):
            self.tubes.append([])

    def init_balls_in_tubes(self):
        # Randomly assign 4 balls of each color to tubes
        ball_list = [color for color in COLORS[:self.n_colors] for _ in range(4)]
        random.shuffle(ball_list)
        for i in range(self.n_colors):
            self.tubes[i] = [ball_list.pop() for _ in range(4)]

    def is_goal_state(self):
        for tube in self.tubes:
            if not (len(tube) == 0 or (len(tube) == 4 and len(set(tube)) == 1)):
                return False
        return True

    def set_user_events(self):
        tube_ids = self.gui.get_tubes_ids()
        for i, tube in enumerate(tube_ids):
            self.gui.get_canvas().tag_bind(tube, '<Button-1>', partial(self.on_tube_click, i))

    def on_tube_click(self, tube_idx, event):
        if self.selected_ball is None:
            # Select the top ball from the clicked tube
            if self.tubes[tube_idx]:
                self.selected_tube_idx = tube_idx
                self.selected_ball = (self.tubes[tube_idx][-1], self.gui.lift_ball(tube_idx))

        else:
            if tube_idx == self.selected_tube_idx:
                self.gui.move_ball(self.selected_tube_idx, tube_idx, len(self.tubes[tube_idx]), self.selected_ball[1])
                self.selected_ball = None
                self.selected_tube_idx = None

            # Move the selected ball to the new tube
            elif (len(self.tubes[tube_idx]) < 4 and
                    (len(self.tubes[tube_idx]) == 0 or self.tubes[tube_idx][-1] == self.selected_ball[0])):
                self.steps += 1
                self.gui.update_steps_display(self.steps)
                self.tubes[self.selected_tube_idx].pop()  # Remove from source tube
                self.tubes[tube_idx].append(self.selected_ball[0])  # Add to destination tube

                self.gui.move_ball(self.selected_tube_idx, tube_idx, len(self.tubes[tube_idx]), self.selected_ball[1])
                self.selected_ball = None
                self.selected_tube_idx = None

    def main_loop(self):
        while not self.is_goal_state():
            continue
        self.gui.win()

if __name__ == '__main__':
    game = BallSortGame()


