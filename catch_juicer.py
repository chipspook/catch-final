
import tkinter as tk
import random

# Game settings
GAME_WIDTH = 500
GAME_HEIGHT = 500
TARGET_SIZE = 20
GAME_SPEED = 50
TARGET_COLOR = "red"
PLAYER_COLOR = "blue"
BACKGROUND_COLOR = "black"

class CatchGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Catch Game")

        # Game stats
        self.score = 0
        self.high_score = 0

        # Start screen
        self.start_screen()

        self.window.mainloop()

    def start_screen(self):
        self.clear_window()

        title = tk.Label(self.window, text="Catch JUICER", font=("Arial", 24), fg="white", bg=BACKGROUND_COLOR)
        title.pack(pady=20)

        instructions = tk.Label(
            self.window,
            text="Use arrow keys to move the player. Catch the falling targets to score points!",
            font=("Arial", 12),
            fg="white",
            bg=BACKGROUND_COLOR,
            wraplength=400
        )
        instructions.pack(pady=20)

        start_button = tk.Button(self.window, text="START GAME", font=("Arial", 14), command=self.start_game)
        start_button.pack(pady=20)

    def start_game(self):
        self.clear_window()

        # Canvas setup
        self.canvas = tk.Canvas(self.window, width=GAME_WIDTH, height=GAME_HEIGHT, bg=BACKGROUND_COLOR)
        self.canvas.pack()

        # Game stats display
        self.score_label = tk.Label(
            self.window, text=f"Score: {self.score} High Score: {self.high_score}", font=("Arial", 14), fg="white", bg=BACKGROUND_COLOR
        )
        self.score_label.pack()

        # Initialize game state
        self.player = [GAME_WIDTH // 2, GAME_HEIGHT - 50]
        self.target = None
        self.running = True

        self.spawn_target()
        self.update_game()

        self.window.bind("<Left>", lambda e: self.move_player("left"))
        self.window.bind("<Right>", lambda e: self.move_player("right"))

    def move_player(self, direction):
        if direction == "left" and self.player[0] > 0:
            self.player[0] -= TARGET_SIZE
        elif direction == "right" and self.player[0] < GAME_WIDTH - TARGET_SIZE:
            self.player[0] += TARGET_SIZE

    def update_game(self):
        if not self.running:
            return

        # Move target downward
        target_x, target_y = self.target
        target_y += TARGET_SIZE // 2

        # Check if target is caught
        if (
            target_y + TARGET_SIZE >= self.player[1]
            and target_x < self.player[0] + TARGET_SIZE
            and target_x + TARGET_SIZE > self.player[0]
        ):
            self.score += 1
            self.spawn_target()
        elif target_y > GAME_HEIGHT:
            self.game_over()
            return

        else:
            self.target = (target_x, target_y)

        self.update_canvas()
        self.window.after(GAME_SPEED, self.update_game)

    def spawn_target(self):
        x = random.randint(0, (GAME_WIDTH // TARGET_SIZE) - 1) * TARGET_SIZE
        self.target = (x, 0)

    def update_canvas(self):
        self.canvas.delete("all")

        # Draw player
        player_x, player_y = self.player
        self.canvas.create_rectangle(
            player_x, player_y, player_x + TARGET_SIZE, player_y + TARGET_SIZE, fill=PLAYER_COLOR
        )

        # Draw target
        target_x, target_y = self.target
        self.canvas.create_oval(
            target_x, target_y, target_x + TARGET_SIZE, target_y + TARGET_SIZE, fill=TARGET_COLOR
        )

        # Update score
        self.score_label.config(text=f"Score: {self.score} High Score: {self.high_score}")

    def game_over(self):
        self.running = False
        self.high_score = max(self.high_score, self.score)
        self.clear_window()

        game_over_label = tk.Label(self.window, text="GAME OVER", font=("Arial", 24), fg="red", bg=BACKGROUND_COLOR)
        game_over_label.pack(pady=20)

        stats_label = tk.Label(
            self.window, text=f"Final Score: {self.score}\nHigh Score: {self.high_score}", font=("Arial", 14), fg="white", bg=BACKGROUND_COLOR
        )
        stats_label.pack(pady=20)

        home_button = tk.Button(self.window, text="HOME", font=("Arial", 14), command=self.start_screen)
        home_button.pack(pady=20)

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    CatchGame()
