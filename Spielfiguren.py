from var import COLORS_1, START_POSITIONS, pieces

def create_pieces(canvas, size, offset, click_handler):

    for spieler_idx, startfelder in enumerate(START_POSITIONS):
        for figuren_idx, (x, y) in enumerate(startfelder, start=1):

            x1, y1 = offset + x * size, offset + y * size
            x2, y2 = x1 + size, y1 + size
            rect = canvas.create_rectangle(
                x1 + 13, y1 + 13, x2 - 13, y2 - 13,
                fill=COLORS_1[spieler_idx], outline="black"
            )
            text = canvas.create_text(
                (x1 + x2) / 2, (y1 + y2) / 2, text=str(figuren_idx),
                font=("Helvetica", 16), fill="black"
            )
            canvas.tag_bind(rect, "<Button-1>", click_handler)
            canvas.tag_bind(text, "<Button-1>", click_handler)
            pieces.append({
                "rect": rect, "text": text, "position": [x, y],
                "spieler": spieler_idx, "piece_number": figuren_idx
            })
