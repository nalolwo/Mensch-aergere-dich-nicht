from var import COLORS_1, GO_POSITIONS

def create_board(canvas, size, offset):
    canvas.delete("all")  # Löscht alles, um das Spielfeld neu zu zeichnen
    BOARD_WIDTH, BOARD_HEIGHT = 11, 11

    # Raster zeichnen
    for i in range(BOARD_WIDTH):
        for j in range(BOARD_HEIGHT):
            x1, y1 = offset + i * size, offset + j * size
            x2, y2 = x1 + size, y1 + size
            #canvas.create_rectangle(x1, y1, x2, y2, outline="black", width=2)
    
    # Startfelder
    start_positions = [(0, 0), (9, 0), (9, 9), (0, 9)]
    for idx, (x, y) in enumerate(start_positions):
        for i in range(2):
            for j in range(2):
                x1, y1 = offset + (x + i) * size, offset + (y + j) * size
                x2, y2 = x1 + size, y1 + size
                canvas.create_oval(
                    (x1 + 3.5), (y1 + 3.5), (x2 - 3.5), (y2 - 3.5), 
                    fill=COLORS_1[idx], outline="black"
                )
    
    # Zielfelder
    goal_positions = [(5, 1), (6, 5), (5, 6), (1, 5)]
    for idx, (x, y) in enumerate(goal_positions):
        for i in range(4):
            x1 = offset + (x + (0 if idx % 2 == 0 else i)) * size
            y1 = offset + (y + (i if idx % 2 == 0 else 0)) * size
            x2, y2 = x1 + size, y1 + size
            canvas.create_oval(
                (x1 + 3.5), (y1 + 3.5), (x2 - 3.5), (y2 - 3.5), 
                fill=COLORS_1[idx +((-3) if idx==3 else 1)], outline="black"
            )
    
    # Spielfelder
    for idx, (x, y) in enumerate(GO_POSITIONS):
        x1, y1 = offset + x * size, offset + y * size
        x2, y2 = x1 + size, y1 + size
        
        if idx % 10 == 0: # Farbige Felder
            canvas.create_oval(
                (x1 + 3.5), (y1 + 3.5), (x2 - 3.5), (y2 - 3.5), 
                fill=COLORS_1[idx // 10], outline="black"
            )
        else: # Weiße Felder
            canvas.create_oval((x1 + 3.5), (y1 + 3.5), (x2 - 3.5), (y2 - 3.5), 
                               fill="white", outline="black"
            )
