import tkinter as tk
from tkinter import messagebox
import random
import math

class LudoGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ludo Game")
        self.root.geometry("800x900")
        self.root.resizable(False, False)
        
        # Game state
        self.current_player = 0
        self.players = ['Red', 'Blue', 'Yellow', 'Green']
        self.colors = ['#FF4444', '#4444FF', '#FFFF44', '#44FF44']
        self.dice_value = 0
        self.game_over = False
        
        # Initialize piece positions (all pieces start at home)
        self.piece_positions = {
            'Red': [-1, -1, -1, -1],
            'Blue': [-1, -1, -1, -1],
            'Yellow': [-1, -1, -1, -1],
            'Green': [-1, -1, -1, -1]
        }
        
        # Track which pieces are in safe zones
        self.safe_pieces = {
            'Red': [False, False, False, False],
            'Blue': [False, False, False, False],
            'Yellow': [False, False, False, False],
            'Green': [False, False, False, False]
        }
        
        # Define the board path (52 squares total)
        self.board_path = self.create_board_path()
        
        # Starting positions for each player
        self.start_positions = {'Red': 0, 'Blue': 13, 'Yellow': 26, 'Green': 39}
        
        # Safe squares (star positions)
        self.safe_squares = [8, 13, 21, 26, 34, 39, 47, 0]
        
        self.setup_ui()
        self.draw_board()
        self.update_display()
        
    def create_board_path(self):
        # Create the path coordinates for the board
        path = []
        size = 600
        center = size // 2
        
        # Bottom row (left to right)
        for i in range(6):
            path.append((100 + i * 40, 520))
        
        # Right column (bottom to top)
        for i in range(6):
            path.append((340, 520 - i * 40))
        
        # Top-right to top-left
        for i in range(6):
            path.append((340 + i * 40, 280))
        
        # Top column (right to left)
        for i in range(6):
            path.append((580 - i * 40, 240))
        
        # Right side going up
        for i in range(6):
            path.append((340, 240 - i * 40))
        
        # Top row (right to left)
        for i in range(6):
            path.append((340 - i * 40, 100))
        
        # Left column (top to bottom)
        for i in range(6):
            path.append((100, 100 + i * 40))
        
        # Bottom-left going right
        for i in range(6):
            path.append((100 + i * 40, 380))
        
        # Left side going down
        for i in range(4):
            path.append((260, 380 + i * 40))
        
        return path
    
    def setup_ui(self):
        # Create main frame
        main_frame = tk.Frame(self.root, bg='white')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Game info frame
        info_frame = tk.Frame(main_frame, bg='lightgray', height=60)
        info_frame.pack(fill='x', pady=(0, 10))
        info_frame.pack_propagate(False)
        
        # Current player label
        self.current_player_label = tk.Label(info_frame, text="Current Player: Red", 
                                           font=('Arial', 14, 'bold'), bg='lightgray')
        self.current_player_label.pack(side='left', padx=10, pady=10)
        
        # Dice frame
        dice_frame = tk.Frame(info_frame, bg='lightgray')
        dice_frame.pack(side='right', padx=10, pady=10)
        
        self.dice_label = tk.Label(dice_frame, text="Dice: -", font=('Arial', 12), bg='lightgray')
        self.dice_label.pack(side='left', padx=5)
        
        self.roll_button = tk.Button(dice_frame, text="Roll Dice", command=self.roll_dice,
                                   font=('Arial', 12), bg='lightblue')
        self.roll_button.pack(side='left', padx=5)
        
        # Game board canvas
        self.canvas = tk.Canvas(main_frame, width=600, height=600, bg='white', bd=2, relief='solid')
        self.canvas.pack(pady=10)
        
        # Bind click events
        self.canvas.bind('<Button-1>', self.on_canvas_click)
        
        # Status label
        self.status_label = tk.Label(main_frame, text="Roll the dice to start!", 
                                   font=('Arial', 12), bg='white')
        self.status_label.pack(pady=5)
    
    def draw_board(self):
        self.canvas.delete("all")
        
        # Draw board background
        self.canvas.create_rectangle(50, 50, 550, 550, fill='#F0F0F0', outline='black', width=2)
        
        # Draw the four home areas
        home_areas = [
            (70, 70, 220, 220),    # Red home
            (330, 70, 480, 220),   # Blue home
            (330, 330, 480, 480),  # Yellow home
            (70, 330, 220, 480)    # Green home
        ]
        
        home_colors = ['#FFCCCC', '#CCCCFF', '#FFFFCC', '#CCFFCC']
        
        for i, (x1, y1, x2, y2) in enumerate(home_areas):
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=home_colors[i], outline='black', width=2)
            
            # Draw home circles for pieces
            for row in range(2):
                for col in range(2):
                    cx = x1 + 40 + col * 70
                    cy = y1 + 40 + row * 70
                    self.canvas.create_oval(cx-15, cy-15, cx+15, cy+15, 
                                          fill='white', outline='black', width=2)
        
        # Draw the path squares
        for i, (x, y) in enumerate(self.board_path):
            color = 'white'
            if i in self.safe_squares:
                color = 'lightgreen'
            elif i in [1, 14, 27, 40]:  # Starting squares
                color = 'lightblue'
            
            self.canvas.create_rectangle(x-15, y-15, x+15, y+15, 
                                       fill=color, outline='black', width=1)
        
        # Draw center area
        self.canvas.create_rectangle(250, 250, 350, 350, fill='gold', outline='black', width=3)
        self.canvas.create_text(300, 300, text="HOME", font=('Arial', 16, 'bold'))
        
        # Draw pieces
        self.draw_pieces()
    
    def draw_pieces(self):
        # Clear existing pieces
        self.canvas.delete("piece")
        
        # Draw pieces in home areas
        home_positions = [
            [(110, 110), (180, 110), (110, 180), (180, 180)],  # Red
            [(370, 110), (440, 110), (370, 180), (440, 180)],  # Blue
            [(370, 370), (440, 370), (370, 440), (440, 440)],  # Yellow
            [(110, 370), (180, 370), (110, 440), (180, 440)]   # Green
        ]
        
        for player_idx, player in enumerate(self.players):
            for piece_idx in range(4):
                pos = self.piece_positions[player][piece_idx]
                
                if pos == -1:  # Piece is at home
                    x, y = home_positions[player_idx][piece_idx]
                    self.canvas.create_oval(x-12, y-12, x+12, y+12, 
                                          fill=self.colors[player_idx], outline='black', width=2, 
                                          tags=f"piece_{player}_{piece_idx}")
                elif pos < 52:  # Piece is on the board
                    x, y = self.board_path[pos]
                    self.canvas.create_oval(x-10, y-10, x+10, y+10, 
                                          fill=self.colors[player_idx], outline='black', width=2, 
                                          tags=f"piece_{player}_{piece_idx}")
                else:  # Piece has reached home (center)
                    # Draw in center area
                    center_positions = [(280, 280), (320, 280), (280, 320), (320, 320)]
                    finished_pieces = sum(1 for p in self.piece_positions[player] if p >= 52)
                    if finished_pieces <= 4:
                        x, y = center_positions[finished_pieces - 1]
                        self.canvas.create_oval(x-8, y-8, x+8, y+8, 
                                              fill=self.colors[player_idx], outline='black', width=2, 
                                              tags=f"piece_{player}_{piece_idx}")
    
    def roll_dice(self):
        if self.game_over:
            return
            
        self.dice_value = random.randint(1, 6)
        self.dice_label.config(text=f"Dice: {self.dice_value}")
        
        # Check if current player can move any piece
        can_move = self.can_player_move()
        
        if can_move:
            self.status_label.config(text=f"{self.players[self.current_player]} rolled {self.dice_value}. Click a piece to move!")
            self.roll_button.config(state='disabled')
        else:
            self.status_label.config(text=f"{self.players[self.current_player]} rolled {self.dice_value}. No valid moves. Next player's turn!")
            self.next_player()
    
    def can_player_move(self):
        player = self.players[self.current_player]
        
        for i, pos in enumerate(self.piece_positions[player]):
            if pos == -1:  # Piece at home
                if self.dice_value == 6:
                    return True
            elif pos < 52:  # Piece on board
                new_pos = pos + self.dice_value
                if new_pos <= 52:  # Can move without going beyond finish
                    return True
        
        return False
    
    def on_canvas_click(self, event):
        if self.game_over or self.dice_value == 0:
            return
        
        # Find clicked piece
        clicked_item = self.canvas.find_closest(event.x, event.y)[0]
        tags = self.canvas.gettags(clicked_item)
        
        for tag in tags:
            if tag.startswith(f"piece_{self.players[self.current_player]}_"):
                piece_idx = int(tag.split('_')[2])
                self.move_piece(piece_idx)
                break
    
    def move_piece(self, piece_idx):
        player = self.players[self.current_player]
        current_pos = self.piece_positions[player][piece_idx]
        
        # Check if move is valid
        if current_pos == -1:  # Piece at home
            if self.dice_value == 6:
                # Move to starting position
                start_pos = self.start_positions[player]
                self.piece_positions[player][piece_idx] = start_pos
                self.check_capture(start_pos, player, piece_idx)
            else:
                self.status_label.config(text="Need a 6 to move piece out of home!")
                return
        elif current_pos < 52:  # Piece on board
            new_pos = current_pos + self.dice_value
            if new_pos <= 52:
                self.piece_positions[player][piece_idx] = new_pos
                if new_pos < 52:
                    self.check_capture(new_pos, player, piece_idx)
            else:
                self.status_label.config(text="Cannot move beyond finish line!")
                return
        else:
            self.status_label.config(text="Piece already finished!")
            return
        
        # Redraw board
        self.draw_pieces()
        
        # Check for win
        if self.check_win():
            self.game_over = True
            messagebox.showinfo("Game Over!", f"{player} wins!")
            return
        
        # Check if player gets another turn (rolled 6)
        if self.dice_value == 6:
            self.status_label.config(text=f"{player} rolled 6! Roll again!")
            self.roll_button.config(state='normal')
            self.dice_value = 0
        else:
            self.next_player()
    
    def check_capture(self, pos, moving_player, moving_piece_idx):
        # Check if any opponent piece is on the same square
        for player in self.players:
            if player == moving_player:
                continue
            
            for i, piece_pos in enumerate(self.piece_positions[player]):
                if piece_pos == pos and pos not in self.safe_squares:
                    # Capture the piece
                    self.piece_positions[player][i] = -1
                    self.status_label.config(text=f"{moving_player} captured {player}'s piece!")
                    break
    
    def check_win(self):
        player = self.players[self.current_player]
        return all(pos >= 52 for pos in self.piece_positions[player])
    
    def next_player(self):
        self.current_player = (self.current_player + 1) % 4
        self.dice_value = 0
        self.roll_button.config(state='normal')
        self.update_display()
    
    def update_display(self):
        player = self.players[self.current_player]
        self.current_player_label.config(text=f"Current Player: {player}",
                                       fg=self.colors[self.current_player])
        self.dice_label.config(text="Dice: -")
        self.status_label.config(text=f"{player}'s turn. Roll the dice!")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = LudoGame()
    game.run()