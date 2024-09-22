import random
import time
import heuristic_search
from functools import partial
from BallSortProblem import *
from Tubes import Tubes

COLORS = ['red', 'green', 'blue', 'purple', 'pink', 'yellow', 'orange', 'turquoise', 'grey']
HUMAN = "human"
AI = "AI"


class BallSortGame:

    def __init__(self, agent=HUMAN, n_colors=5):
        self.n_colors = n_colors
        self.n_tubes = 0
        self.steps = 0
        self.tubes = []
        self.init_tubes()
        self.tubes = Tubes(self.tubes)
        self.init_balls_in_tubes()
        self.gui = GUI.BallSortGui(n_colors, self.tubes)
        self.selected_ball = None
        self.selected_tube_idx = None
        self.agent = agent

    def game_runner(self, actions=None):
        """
        function who incharge to run the main loop of the game, using UI when human agent plays, and AI agent as well.
        :param self:
        :return:
        """
        if not actions:
            self.set_user_events()
            self.gui.root.mainloop()
            return 1, 1
        else:
            for action in actions:
                self.do_action(action)
                self.gui.root.update()  # Update the GUI to reflect the changes
                time.sleep(0.5)

            #  Properly close the GUI window.
            self.gui.root.destroy()


    def init_tubes(self):
        """
        Function which choose amount of tubes according to number of ball colors in game.
        :return:
        """
        if self.n_colors < 3:
            self.n_tubes = self.n_colors + 1
        elif self.n_colors <= 7:
            self.n_tubes = self.n_colors + 2
        else:
            self.n_tubes = self.n_colors + 3
        for i in range(self.n_tubes):
            self.tubes.append([])

    def init_balls_in_tubes(self):
        """
        Function choose randomly ball colors for num colors chosen and add it to our tubes data structure.
        :return:
        """
        # Randomly assign 4 balls of each color to tubes
        ball_list = [color for color in COLORS[:self.n_colors] for _ in range(4)]
        random.shuffle(ball_list)
        for i in range(self.n_colors):
            self.tubes[i] = [ball_list.pop() for _ in range(4)]

    def is_goal_state(self):
        """
        Function which check if we got to solution in the game according to the rules.
        :return:
        """

        for tube in self.tubes:
            if not (len(tube) == 0 or (len(tube) == 4 and len(set(tube)) == 1)):
                return False
        return True

    def get_colors(self):
        return COLORS[:self.n_colors]

    def set_user_events(self):
        """
        Function sets click listener events of user agent game using tk tag binding.
        :return:
        """
        tube_ids = self.gui.get_tubes_ids()
        for i, tube in enumerate(tube_ids):
            # Connect gui to user inputs
            self.gui.get_canvas().tag_bind(tube, '<Button-1>', partial(self.on_tube_click, i))

    def get_steps(self):
        return self.steps

    def do_action(self, action):
        """
        Function which gets valid action and operates the visual movement and structures changes.
        :param action:
        :return:
        """
        src_idx = int(action[0])
        dst_idx = int(action[-1])
        self.on_tube_click(src_idx - 1, None)
        self.on_tube_click(dst_idx - 1, None)

    def on_tube_click(self, tube_idx, event):
        # Case whe choose ball to move
        if self.selected_ball is None:
            # Select the top ball from the clicked tube
            if self.tubes[tube_idx]:
                self.selected_tube_idx = tube_idx
                self.selected_ball = (self.tubes[tube_idx][-1], self.gui.lift_ball(tube_idx))

        else:
            # Handle case when user try to put ball in its origin tube, so we return the ball and not increment steps.
            if tube_idx == self.selected_tube_idx:
                self.gui.move_ball(self.selected_tube_idx, tube_idx, len(self.tubes[tube_idx]), self.selected_ball[1])
                self.selected_ball = None
                self.selected_tube_idx = None

            # Move the selected ball to the new tube
            elif (len(self.tubes[tube_idx]) < 4 and
                  (len(self.tubes[tube_idx]) == 0 or self.tubes[tube_idx][-1] == self.selected_ball[0])):
                self.steps += 1

                # Change ball positions in our data structure
                self.gui.update_steps_display(self.steps)
                self.tubes[self.selected_tube_idx].pop()  # Remove from source tube
                self.tubes[tube_idx].append(self.selected_ball[0])  # Add to destination tube

                # GUI render the move, and init selected ball
                self.gui.move_ball(self.selected_tube_idx, tube_idx, len(self.tubes[tube_idx]), self.selected_ball[1])
                self.selected_ball = None
                self.selected_tube_idx = None
                # Render win windows in case we got to goal state.
                if self.is_goal_state():
                    self.gui.win()

    def get_tubes(self):
        return self.tubes
