import tkinter as tk
from tkinter.constants import CENTER
from PIL import Image, ImageTk
import random
from functools import partial

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 950
TUBE_HEIGHT = 250


class BallSortGui:
    def __init__(self, n_colors, tubes):
        root = tk.Tk()
        root.geometry("700x450")
        self.root = root
        self.root.title("Ball Sort Game")
        self.canvas = tk.Canvas(self.root, width=1158, height=720)
        self.canvas.pack()
        self.tube_ball_images = []
        self.tube_ids = []
        self.ball_images = {}
        self.n_colors = n_colors
        self.cur_ball_image_id = None
        self.image_refs = []  # Initialize list to keep track of image references
        self.load_ball_images()
        self.create_game(tubes)
        # self.total_tubes = 0
        # self.selected_ball = None  # To track selected ball and its tube
        # self.selected_tube_idx = None

    def load_ball_images(self):
        """Load all ball images from the 'balls' folder."""
        self.ball_images = {}
        ball_colors = ['red', 'green', 'blue', 'purple', 'pink', 'yellow', 'orange', 'turquoise', 'grey']
        for color in ball_colors:
            img_path = f"utils/balls/{color}.png"
            ball_image = Image.open(img_path).resize((45, 45))  # Resize if necessary
            ball_photo = ImageTk.PhotoImage(ball_image)
            self.ball_images[color] = ball_photo
            self.image_refs.append(ball_photo)  # Keep a reference
        return self.ball_images

    def create_game(self, tubes):
        """Create the game layout, placing tubes and balls on the canvas."""
        # Set background image
        bg_image = Image.open("utils/background.jpg").resize((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.bg_photo = ImageTk.PhotoImage(bg_image)
        self.image_refs.append(self.bg_photo)  # Keep a reference
        self.canvas.create_image(0, 0, anchor=CENTER, image=self.bg_photo)

        # Set score text
        self.step_label = self.canvas.create_text(290, 413, anchor="nw", font=("Courier bold", 25), fill="goldenrod")
        self.canvas.itemconfig(self.step_label, text=f"Steps:0")

        # Set title image
        title = Image.open("utils/title.png").resize((230, 100))
        self.title = ImageTk.PhotoImage(title)
        self.image_refs.append(self.title)  # Keep a reference
        self.canvas.create_image(340, 50, anchor=CENTER, image=self.title)

        # Create tubes and balls
        for i in range(len(tubes)):
            tube_x = 100 + 83 * i
            tube_image = Image.open("utils/tube.png").resize((60, 210))
            tube_photo = ImageTk.PhotoImage(tube_image)
            self.image_refs.append(tube_photo)  # Keep a reference
            self.tube_ids.append(self.canvas.create_image(tube_x, TUBE_HEIGHT, image=tube_photo))
            self.tube_ball_images.append([])

        for i in range(self.n_colors):
            tube_x = 100 + 83 * i
            self.draw_balls_in_tube(tubes[i], tube_x, TUBE_HEIGHT, i)

    def get_tubes_ids(self):
        return self.tube_ids

    def get_canvas(self):
        return self.canvas

    def draw_balls_in_tube(self, tube_balls, tube_x, tube_y, tube_idx):
        """Draw the balls inside a specific tube."""
        for idx, color in enumerate(tube_balls):
            ball_image = self.ball_images[color]
            ball_id = self.canvas.create_image(tube_x, tube_y - 105 + ((4 - idx) * 45), image=ball_image)
            self.tube_ball_images[tube_idx].append(ball_id)  # Store the ball image ID

    def lift_ball(self, src_idx):
        ball_image_id = self.tube_ball_images[src_idx][-1]
        self.canvas.coords(ball_image_id, 100 + (src_idx * 83), 120)
        return ball_image_id

    def move_ball(self, src_idx, dst_idx, dst_tube_size, ball_id):
        if src_idx != dst_idx:
            ball_image_id = self.tube_ball_images[src_idx].pop()
            self.tube_ball_images[dst_idx].append(ball_image_id)

        self.canvas.coords(ball_id, 100 + (dst_idx * 83), 170)
        self.canvas.after(200, lambda: self.canvas.coords(ball_id, 100 + (dst_idx * 83),
                                                          TUBE_HEIGHT - 105 + ((5 - dst_tube_size) * 45)))
    def update_steps_display(self, steps):
        self.canvas.itemconfig(self.step_label, text=f"Steps:{steps}")

    def win(self):
        win_image = Image.open("utils/win.webp").resize((700, 450))
        self.win_image = ImageTk.PhotoImage(win_image)
        self.image_refs.append(self.win_image)  # Keep a reference
        self.canvas.create_image(350, 200, anchor=CENTER, image=self.win_image)

