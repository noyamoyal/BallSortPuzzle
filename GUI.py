import tkinter as tk
from tkinter.constants import CENTER
from PIL import Image, ImageTk
import random

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 950


class BallSortGame:
    def __init__(self, root, n_colors):
        root.geometry("700x450")
        self.root = root
        self.root.title("Ball Sort Game")
        self.canvas = tk.Canvas(self.root, width=1158, height=720)
        self.canvas.pack()
        self.tubes = []
        self.image_refs = []  # Initialize list to keep track of image references

        self.n_colors = n_colors
        self.total_tubes = self.calculate_tubes(n_colors)
        self.balls = self.load_ball_images()
        self.create_game()

    def calculate_tubes(self, n_colors):
        if n_colors <= 3:
            return n_colors + 1
        elif n_colors <= 7:
            return n_colors + 2
        else:
            return n_colors + 3

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
            # tube_x = 100 + (WINDOW_WIDTH / self.total_tubes - 200) * i
            tube_y = 250
            tube_image = Image.open("utils/tube.png").resize((60, 200))
            tube_photo = ImageTk.PhotoImage(tube_image)
            self.image_refs.append(tube_photo)  # Keep a reference≠≠
            self.canvas.create_image(tube_x, tube_y, image=tube_photo)

            if i < self.n_colors:  # Fill first n tubes with balls
                tube_balls = [ball_list.pop() for _ in range(4)]
                self.tubes.append(tube_balls)
                self.draw_balls_in_tube(tube_balls, tube_x, tube_y)

    def draw_balls_in_tube(self, tube_balls, tube_x, tube_y):
        """Draw the balls inside a specific tube."""
        for idx, color in enumerate(tube_balls):
            ball_image = self.balls[color]
            self.canvas.create_image(tube_x, tube_y - 50 + (idx * 40), image=ball_image)

    def transfer_ball(self, src_idx, dst_idx):
        """Transfer the top ball from one tube to another with animation."""
        if not self.tubes[src_idx]:
            return

        # Pop the ball from the source tube
        ball_color = self.tubes[src_idx].pop()

        # Add the ball to the destination tube
        if len(self.tubes[dst_idx]) < 4:
            self.tubes[dst_idx].append(ball_color)
            self.animate_transfer(src_idx, dst_idx, ball_color)

    def animate_transfer(self, src_idx, dst_idx, ball_color):
        """Animate the ball transfer from one tube to another."""
        src_x = 100 + (src_idx * 80)
        dst_x = 100 + (dst_idx * 80)
        ball_image = self.balls[ball_color]

        # Starting position (top of source tube)
        ball = self.canvas.create_image(src_x, 150, image=ball_image)

        # Animate movement from src to dst
        for i in range(abs(dst_x - src_x) // 10):
            self.canvas.move(ball, (dst_x - src_x) / 10, 0)
            self.canvas.update()
            self.root.after(20)

        # Place the ball in the destination tube
        self.draw_balls_in_tube(self.tubes[dst_idx], dst_x, 300)

def start_game():
    root = tk.Tk()
    n_colors = 5  # You can modify this or set it via API
    game = BallSortGame(root, n_colors)
    root.mainloop()

if __name__ == "__main__":
    start_game()
