import tkinter as tk
import random

class BrickBreakerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Brick Breaker Game")
        
        # Canvas setup
        self.canvas = tk.Canvas(root, width=800, height=800, bg='navy')
        self.canvas.pack()

        # Game variables
        self.paddle = None
        self.ball = None
        self.bricks = []
        self.ball_speed_x = 3
        self.ball_speed_y = -3
        self.paddle_speed = 20
        self.score = 0
        self.level = 1
        self.running = True

        # Initialize game objects
        self.create_paddle()
        self.create_ball()
        self.create_bricks()

        # Display score and level
        self.score_text = self.canvas.create_text(90, 10, anchor='nw', fill='black',
                                                  font=('Arial', 14), text=f"Score: {self.score}")
        self.level_text = self.canvas.create_text(700, 10, anchor='ne', fill='black',
                                                  font=('Arial', 14), text=f"Level: {self.level}")

        # Key bindings
        self.root.bind('<Left>', self.move_paddle_left)
        self.root.bind('<Right>', self.move_paddle_right)

        # Start game loop
        self.update_game()

    def create_paddle(self):
        self.paddle = self.canvas.create_rectangle(350, 560, 450, 580, fill='white')

    def create_ball(self):
        self.ball = self.canvas.create_oval(390, 540, 410, 560, fill='red')

    def create_bricks(self):
        self.bricks.clear()
        colors = ['red', 'orange', 'yellow', 'green', 'blue']
        for i in range(self.level + 2):
            for j in range(8):
                x1 = j * 100 + 10
                y1 = i * 30 + 10
                x2 = x1 + 80
                y2 = y1 + 20
                color = random.choice(colors)
                brick = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                self.bricks.append(brick)

    def move_paddle_left(self, event):
        if self.running:
            self.canvas.move(self.paddle, -self.paddle_speed, 0)

    def move_paddle_right(self, event):
        if self.running:
            self.canvas.move(self.paddle, self.paddle_speed, 0)

    def update_game(self):
        if not self.running:
            return

        # Move the ball
        self.canvas.move(self.ball, self.ball_speed_x, self.ball_speed_y)
        ball_coords = self.canvas.coords(self.ball)

        # Ball collision with walls
        if ball_coords[0] <= 0 or ball_coords[2] >= 800:
            self.ball_speed_x = -self.ball_speed_x

        if ball_coords[1] <= 0:
            self.ball_speed_y = -self.ball_speed_y

        # Ball collision with paddle
        paddle_coords = self.canvas.coords(self.paddle)
        if (paddle_coords[0] < ball_coords[2] and paddle_coords[2] > ball_coords[0] and
                paddle_coords[3] >= ball_coords[3] and paddle_coords[1] <= ball_coords[3]):
            self.ball_speed_y = -self.ball_speed_y

        # Ball collision with bricks
        for brick in self.bricks:
            brick_coords = self.canvas.coords(brick)
            if (brick_coords[0] < ball_coords[2] and brick_coords[2] > ball_coords[0] and
                    brick_coords[3] >= ball_coords[1] and brick_coords[1] <= ball_coords[3]):
                self.canvas.delete(brick)
                self.bricks.remove(brick)
                self.ball_speed_y = -self.ball_speed_y
                self.score += 10
                self.update_score()

        # Check if ball falls out of bounds
        if ball_coords[3] >= 600:
            self.running = False
            self.game_over()

        # Check if all bricks are destroyed
        if not self.bricks:
            self.level_up()

        # Continue the game loop
        if self.running:
            self.root.after(16, self.update_game)

    def update_score(self):
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")

    def level_up(self):
        self.level += 1
        self.ball_speed_x *= 1.1
        self.ball_speed_y *= 1.1
        self.create_bricks()
        self.canvas.itemconfig(self.level_text, text=f"Level: {self.level}")

    def game_over(self):
        self.canvas.create_text(400, 300, text="GAME OVER", fill='red', font=('Arial', 36))

if __name__ == '__main__':
    root = tk.Tk()
    game = BrickBreakerGame(root)
    root.mainloop()