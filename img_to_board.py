from PIL import Image
import numpy as np

TILE_SIZE = 32

# reference colors (sample these once from your image)
COLORS = {
    '%': np.array([120, 120, 120]),   # wall
    'b': np.array([255, 200, 50]),    # box
    'B': np.array([200, 170, 80]),    # box on dot
    '.': np.array([230, 160, 160]),   # goal
    'p': np.array([60, 120, 200]),    # player
    ' ': np.array([235, 225, 200])    # floor
}

def closest_tile(rgb):
    rgb = np.array(rgb)
    best = None
    dist = float('inf')
    for k, v in COLORS.items():
        d = np.linalg.norm(rgb - v)
        if d < dist:
            dist = d
            best = k
    return best

file_name = "hard_2"
img = Image.open(f"boards/{file_name}.png").convert("RGB")
w, h = img.size

board = []

for y in range(0, h, TILE_SIZE):
    row = []
    for x in range(0, w, TILE_SIZE):
        cx = x + TILE_SIZE // 2
        cy = y + TILE_SIZE // 2
        rgb = img.getpixel((cx, cy))
        row.append(closest_tile(rgb))
    board.append(row)

# print board
str_board = ""
for r in board:
    output = "".join(r)
    str_board = str_board+output+"\n"
with open(f"boards/sokoban_{file_name}.txt","w") as f:
    f.write(str_board)

