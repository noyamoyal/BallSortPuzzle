import tkinter as tk
from tkinter.constants import CENTER
from PIL import Image, ImageTk
import random
from functools import partial

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 950
TUBE_HEIGHT = 250


class BallSortGame:
    def __init__(self, n_colors):
        root = tk.Tk()
        root.geometry("700x450")
        self.root = root
        self.root.title("Ball Sort Game")
        self.canvas = tk.Canvas(self.root, width=1158, height=720)
        self.canvas.pack()

        self.steps = 0  # Initialize step counter
        self.tubes = []
        self.tube_ball_images = []  # List to store ball image IDs for each tube
        self.image_refs = []  # Initialize list to keep track of image references
        self.n_colors = n_colors
        self.total_tubes = 0
        self.selected_ball = None  # To track selected ball and its tube
        self.selected_tube_idx = None
        self.calculate_tubes()
        self.balls = self.load_ball_images()
        self.create_game()
        self.cur_ball_image_id = None
        root.mainloop()

    def calculate_tubes(self):
        if self.n_colors <= 3:
            self.total_tubes = self.n_colors + 1
        elif self.n_colors <= 7:
            self.total_tubes = self.n_colors + 2
        else:
            self.total_tubes = self.n_colors + 3
        for i in range(self.total_tubes):
            self.tubes.append([])
            self.tube_ball_images.append([])  # Initialize ball image list for each tube

    def load_ball_images(self):
        """Load all ball images from the 'balls' folder."""
        ball_images = {}
        ball_colors = ['red', 'green', 'blue', 'purple', 'pink', 'yellow', 'orange', 'turquoise', 'grey']
        for color in ball_colors[:self.n_colors]:
            img_path = f"utils/balls/{color}.png"
            ball_image = Image.open(img_path).resize((40, 40))  # Resize if necessary
            ball_photo = ImageTk.PhotoImage(ball_image)
            ball_images[color] = ball_photo
            self.image_refs.append(ball_photo)  # Keep a reference
        return ball_images

    def create_game(self):
        """Create the game layout, placing tubes and balls on the canvas."""
        # Set background image
        bg_image = Image.open("utils/background.jpg").resize((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.bg_photo = ImageTk.PhotoImage(bg_image)
        self.image_refs.append(self.bg_photo)  # Keep a reference
        self.canvas.create_image(0, 0, anchor=CENTER, image=self.bg_photo)

        self.step_label = self.canvas.create_text(290, 413, anchor="nw", font=("Courier bold", 25), fill="goldenrod")
        self.canvas.itemconfig(self.step_label, text=f"Steps:{self.steps}")

        # self.steps_label = tk.Label(self.root, text=, font=("Helvetica", 16), bg=self.root["bg"])
        # self.steps_label.place(x=315, y=410)

        title = Image.open("utils/title.png").resize((230, 100))
        self.title = ImageTk.PhotoImage(title)
        self.image_refs.append(self.title)  # Keep a reference
        self.canvas.create_image(340, 50, anchor=CENTER, image=self.title)

        # Randomly assign 4 balls of each color to tubes
        colors = list(self.balls.keys())
        ball_list = [color for color in colors for _ in range(4)]
        random.shuffle(ball_list)

        # Create tubes and balls
        for i in range(self.total_tubes):
            tube_x = 100 + 83 * i
            tube_image = Image.open("utils/tube.png").resize((60, 200))
            tube_photo = ImageTk.PhotoImage(tube_image)
            self.image_refs.append(tube_photo)  # Keep a reference
            tube_id = self.canvas.create_image(tube_x, TUBE_HEIGHT, image=tube_photo)

            # Bind tube clicks correctly using functools.partial to pass tube index
            self.canvas.tag_bind(tube_id, '<Button-1>', partial(self.on_tube_click, i))

        for i in range(self.n_colors):
            tube_x = 100 + 83 * i
            self.tubes[i] = [ball_list.pop() for _ in range(4)]
            self.draw_balls_in_tube(self.tubes[i], tube_x, TUBE_HEIGHT, i)

    def draw_balls_in_tube(self, tube_balls, tube_x, tube_y, tube_idx):
        """Draw the balls inside a specific tube."""
        for idx, color in enumerate(tube_balls):
            ball_image = self.balls[color]
            ball_id = self.canvas.create_image(tube_x, tube_y - 90 + ((4 - idx) * 40), image=ball_image)
            self.tube_ball_images[tube_idx].append(ball_id)  # Store the ball image ID

    def is_goal_state(self):
        for tube in self.tubes:
            if not (len(tube) == 0 or (len(tube) == 4 and len(set(tube)) == 1)):
                return False
        return True

    def on_tube_click(self, tube_idx, event):
        """Handle tube click events."""
        if self.selected_ball is None:
            # Select the top ball from the clicked tube
            if self.tubes[tube_idx]:
                self.selected_ball = self.tubes[tube_idx][-1]
                self.selected_tube_idx = tube_idx
                # Move the ball outside the tube (y index to 200)
                ball_image_id = self.tube_ball_images[tube_idx][-1]
                self.canvas.coords(ball_image_id, 100 + (tube_idx * 83), 120)

        else:
            if tube_idx == self.selected_tube_idx:
                ball_image_id = self.tube_ball_images[tube_idx][-1]
                self.canvas.coords(ball_image_id, 100 + (tube_idx * 83), 200)
                self.canvas.after(200, lambda: self.canvas.coords(ball_image_id, 100 + (tube_idx * 83),
                                                                  TUBE_HEIGHT - 90 + ((5 - len(self.tubes[tube_idx])) * 40)))
                self.selected_ball = None
                self.selected_tube_idx = None

            # Move the selected ball to the new tube
            elif (len(self.tubes[tube_idx]) < 4 and
                    (len(self.tubes[tube_idx]) == 0 or self.tubes[tube_idx][-1] == self.selected_ball)):
                # Ensure source and destination are not the same
                self.steps += 1  # Increment steps only if src != dst
                self.canvas.itemconfig(self.step_label, text=f"Steps:{self.steps}")  # Update label
                self.tubes[self.selected_tube_idx].pop()  # Remove from source tube
                ball_image_id = self.tube_ball_images[self.selected_tube_idx].pop()
                self.tubes[tube_idx].append(self.selected_ball)  # Add to destination tube
                self.tube_ball_images[tube_idx].append(ball_image_id)
                # Animate the ball to its new position
                self.canvas.coords(ball_image_id, 100 + (tube_idx * 83), 200)
                self.canvas.after(200, lambda: self.canvas.coords(ball_image_id, 100 + (tube_idx * 83),
                                                                  TUBE_HEIGHT - 90 + ((5 - len(self.tubes[tube_idx])) * 40)))
                self.selected_ball = None
                self.selected_tube_idx = None

            if self.is_goal_state():
                win_image = Image.open("utils/win.webp").resize((700, 450))
                self.win_image = ImageTk.PhotoImage(win_image)
                self.image_refs.append(self.win_image)  # Keep a reference
                self.canvas.create_image(350, 200, anchor=CENTER, image=self.win_image)


if __name__ == "__main__":
    BallSortGame(5)
