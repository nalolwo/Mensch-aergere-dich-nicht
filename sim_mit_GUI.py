from Spielfeld import create_board
from Spielfiguren import create_pieces
import tkinter as tk
import random
import var

wuerfel_wuerfe = 0
#computer_piece = None
rect = None
SIZE = 55
OFFSET = 10
bewegung_möglich = False
zugzwang_kontrolle = False
COLORS = ["ROET", "BLAU", "GRÜN", "GELB"]

# ------------------------------------------------- Kontrolle, ob Spieler dran ist -------------------------------------------------------
def kontrolle_move(i):
    piece = var.pieces[i + 4 * var.spieler]
    move_piece(piece)

# ------------------------------------------------- Kontrolle, ob Spieler dran ist -------------------------------------------------------
def kontrolle_roll():
    roll_dice()

# ------------------------------------------------- Zugzwang oder Bewegung der Spielfigur ------------------------------------------------
def zugzwang_oder_move(piece, position):
    global bewegung_möglich, zugzwang_kontrolle
    if zugzwang_kontrolle:
        bewegung_möglich = True
    else:
        move_piece_to(piece, position)

# ------------------------------------------------- Spielfiguren bewegen -----------------------------------------------------------------
def move_piece(piece):
    from var import GOAL_POSITIONS, GO_POSITIONS

    if (var.wuerfel == 0) and not zugzwang_kontrolle:
        add_text("Bitte zuerst würfeln!")
        return

    if check_start(piece):
        if (var.wuerfel == 6 and check_free_position(GO_POSITIONS[var.spieler*10]) is None):
            zugzwang_oder_move(piece, GO_POSITIONS[var.spieler*10])
        
        elif var.wuerfel != 6:
            add_text("Sie haben keine 6 gewürfelt!")
            return
        
        else:
            occupying_piece = check_free_position(GO_POSITIONS[var.spieler*10])
            if occupying_piece is not None:
                if not piece_schlag(piece, occupying_piece):
                    return
    
    elif check_goal(piece):
        i = next((idx for idx, pos in enumerate(GOAL_POSITIONS[var.spieler]) if piece["position"] == pos), None)
        if i is None:
            add_text("Fehler: Position im Zielbereich nicht gefunden!")
            print("Fehler", var.spieler, piece)
            return
        ziel_index = i + var.wuerfel
        if ziel_index > 3:
            add_text("Bewegung nicht möglich!")
            return
        
        if check_free_position(GOAL_POSITIONS[var.spieler][i+var.wuerfel]) is not None:
            add_text("Zielposition ist besetzt!")
            return
        
        # Prüfen, ob alle Felder bis zum Ziel frei sind
        if var.wuerfel > 1:
            if all(check_free_position(GOAL_POSITIONS[var.spieler][k]) is None for k in range(i + 1, ziel_index)):
                zugzwang_oder_move(piece, GOAL_POSITIONS[var.spieler][ziel_index])
            
            else:
                add_text("Bewegung nicht möglich, weil eine Figur im Weg ist!")
        
        else:
            zugzwang_oder_move(piece, GOAL_POSITIONS[var.spieler][ziel_index])

    else:
        position_neu = neue_position(var.wuerfel, piece)
        if not zieleinlauf_möglich(piece, position_neu):
            occupying_piece = check_free_position(GO_POSITIONS[position_neu])
            if occupying_piece is None:
                zugzwang_oder_move(piece, GO_POSITIONS[position_neu])
            
            elif not piece_schlag(piece, occupying_piece):
                return

        else:
            if gewonnen(var.spieler):
                add_text(f"Spieler {COLORS[var.spieler]} hat gewonnen!")
                return # Damit der Gewinner angezeigt wird
    
    # if not zugzwang_kontrolle:                
    #     change_player()

# ------------------------------------------------- Bewegung der Spielfiguren ------------------------------------------------------------
def move_piece_to(piece, position):
    global SIZE, OFFSET
    x = position[0]
    y = position[1]
    x1, y1 = OFFSET + x * SIZE, OFFSET + y * SIZE
    x2, y2 = x1 + SIZE, y1 + SIZE
    canvas.coords(piece["rect"], (x1 + 13), (y1 + 13), (x2 - 13), (y2 - 13))
    canvas.coords(piece["text"], (x1 + x2) / 2, (y1 + y2) / 2)
    piece["position"] = [x, y]

# ------------------------------------------------- Figur schlagen -----------------------------------------------------------------------
def piece_schlag(piece, occupying_piece):
    from var import START_POSITIONS, GO_POSITIONS
    global zugzwang_kontrolle
    if occupying_piece["spieler"] == var.spieler:
        add_text("Sie können nicht ihre eigenen Figuren schlagen!")
        return False
    
    occupying_piece_spieler = occupying_piece["spieler"]
    if occupying_piece["position"] == GO_POSITIONS[occupying_piece_spieler*10]:
        add_text("Figur ist auf eigenem Startfeld sicher!")
        return False
    
    zugzwang_oder_move(piece, occupying_piece["position"])
    
    if not zugzwang_kontrolle:
        move_piece_to(occupying_piece, START_POSITIONS[occupying_piece["spieler"]][occupying_piece["piece_number"]-1])
    return True

# ------------------------------------------------- Überprüfen, ob Zieleinlauf möglich ist -----------------------------------------------
def zieleinlauf_möglich(piece, position_neu):
    from var import GO_POSITIONS, GOAL_POSITIONS, spieler

    # Prüfen, ob die Figur in Zielreichweite ist
    in_zielreichweite = any(
        piece["position"] == GO_POSITIONS[(spieler if spieler > 0 else 4) * 10 - (i + 1)]
        for i in range(6)
    )
    if not in_zielreichweite:
        return False

    # Prüfen, ob ein Zielfeld erreicht werden kann und alle Felder davor frei sind
    for j in range(4):
        if GO_POSITIONS[position_neu] == GO_POSITIONS[spieler * 10 + j] and check_free_position(GOAL_POSITIONS[spieler][j]) is None:
            if all(check_free_position(GOAL_POSITIONS[spieler][k]) is None for k in range(j)):
                zugzwang_oder_move(piece, GOAL_POSITIONS[spieler][j])
                return True
    return False

# ------------------------------------------------- Überprüfen, ob Spieler gewonnen hat --------------------------------------------------
def gewonnen(spieler):
    global COLORS, figuren_buttons
    # Prüfe, ob alle 4 Figuren des Spielers im Zielbereich stehen
    goals = set(tuple(pos) for pos in var.GOAL_POSITIONS[spieler])
    alle_im_ziel = all(tuple(var.pieces[4*spieler + i]["position"]) in goals for i in range(4))
    if not alle_im_ziel:
        return False
    var.gewonnen = True
    return True

# ------------------------------------------------- Spielerwechsel -----------------------------------------------------------------------
def change_player():
    global wuerfel_wuerfe, COLORS
    
    wuerfel_wuerfe = 0
    var.wuerfel = 0
    var.spieler = (var.spieler + 1) % (var.anzahl_mensch + var.anzahl_computer)
        
# ------------------------------------------------- Überprüfen von Positionen der Spielfiguren (Ziel/Start) ------------------------------
def check_position(player):
    from var import START_POSITIONS, GOAL_POSITIONS
    zaehler = 0
    for i in range(player*4, player*4+4):
        piece = var.pieces[i]
        for j in range(4):
            if (piece["position"] == START_POSITIONS[player][j-1] 
                or piece["position"] == GOAL_POSITIONS[player][j-1]):
                zaehler += 1
    if zaehler == 4:
        return True
    return False

# ------------------------------------------------- Überprüfen, ob Position frei ist------------------------------------------------------
def check_free_position(position):
    return next((piece for piece in var.pieces if tuple(piece["position"]) == tuple(position)), None)

# ------------------------------------------------- Berechnung der neuen Position --------------------------------------------------------
def neue_position(wuerfel, piece):
    for go in var.GO_POSITIONS:
        if go == piece["position"]:
            x = var.GO_POSITIONS.index(go) + wuerfel
            if x > 39:
                x = x - 40
            return x
    return -1  # Falls die Position nicht gefunden wird

# ------------------------------------------------- Überprüfen, ob Figur im Start ist ----------------------------------------------------
def check_start(piece):
    for start in var.START_POSITIONS[var.spieler]:
        if piece["position"] == start:
            return True
    return False

# ------------------------------------------------- Überprüfen, ob Figur im Ziel ist -----------------------------------------------------
def check_goal(piece):
    # Vergleicht die Position als Tupel, um Listen/Tupel-Mischung zu vermeiden
    return tuple(piece["position"]) in [tuple(goal) for goal in var.GOAL_POSITIONS[var.spieler]]

# ------------------------------------------------- Zugzwang -----------------------------------------------------------------------------
def zugzwang():
    global bewegung_möglich, zugzwang_kontrolle, figuren_buttons, computer_piece
    if var.wuerfel == 0:
        return False

    zugzwang_kontrolle = True
    muss_gehen = False

    for i in range(4):
        move_piece(var.pieces[i + 4 * var.spieler])
        if bewegung_möglich:
            muss_gehen = True
            computer_piece = i
            bewegung_möglich = False
        else:
            pass
    zugzwang_kontrolle = False

    return muss_gehen

# ------------------------------------------------- Würfeln ------------------------------------------------------------------------------
def roll_dice():
    global wuerfel_wuerfe
    var.wuerfel = random.randint(1, 6)
    zugzwang()
    wuerfel_wuerfe += 1

# ------------------------------------------------- Funktion zum Einfügen von Text -------------------------------------------------------
def add_text(text):
    global zugzwang_kontrolle
    if not zugzwang_kontrolle:
        output_label.config(text = text)

# ------------------------------------------------- Funktion zum Ändern des Spielerlabels ------------------------------------------------
def change_player_label(text):
    pass

# ------------------------------------------------- Klick auf Spielfigur -----------------------------------------------------------------
def on_piece_click(event):
    pass

# ------------------------------------------------- Neustart des Spiels ------------------------------------------------------------------
def restart():
    global wuerfel_wuerfe
    start_positions = var.START_POSITIONS
    var.spieler = 0
    var.wuerfel = 0
    wuerfel_wuerfe = 0
    var.gewonnen = False

    for piece in var.pieces:
        move_piece_to(piece, start_positions[piece["spieler"]][piece["piece_number"]-1])

# ------------------------------------------------- Kontroller ---------------------------------------------------------------------------
def controller():
    global wuerfel_wuerfe, computer_piece, COLORS
    
    while True:
        while wuerfel_wuerfe < 3:
            if zugzwang():
                kontrolle_move(computer_piece)
                break
            else:
                roll_dice()
        if not var.gewonnen:
            change_player()
        else:
            break
    
    root.after(var.computer_v.get(), restart) # type: ignore
    root.after(var.computer_v.get(), controller) # type: ignore

# ------------------------------------------------- Hauptprogramm ------------------------------------------------------------------------
def main_sim():
    global root, canvas, output_label, COLORS
    root = tk.Tk()
    root.title("Mensch ärgere dich nicht")
    # root.wm_state('zoomed')  # Vollbild-Modus
    root.overrideredirect(True) ###

    #### Transparente Farbe
    TRANSPARENT = "magenta"
    root.configure(bg=TRANSPARENT)
    root.attributes("-transparentcolor", TRANSPARENT)

    # Haupt-Container
    main_frame = tk.Frame(root, bg=TRANSPARENT, highlightthickness=0, bd=0)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Textfeld für Ausgaben
    output_label = tk.Label(
        root, text="", font=("Helvetica", 16), width=50, 
        height=1, anchor="w", justify="left"
    )
    output_label.config(bg="white", relief="sunken")
    output_label.pack(side=tk.LEFT, padx=10)

    # Canvas für das Spielfeld
    canvas = tk.Canvas(main_frame, width=650, height=630, bg=TRANSPARENT, highlightthickness=0, bd=0)
    canvas.pack(side=tk.LEFT, expand=False, fill=tk.BOTH)

    # ======================
    # Fenster verschiebbar
    # ======================
    def start_move(event):
        root.x_offset = event.x # type: ignore
        root.y_offset = event.y # type: ignore

    def do_move(event):
        x = event.x_root - root.x_offset # type: ignore
        y = event.y_root - root.y_offset # type: ignore
        root.geometry(f"+{x}+{y}")

    canvas.bind("<Button-1>", start_move)
    canvas.bind("<B1-Motion>", do_move)

    # Das Spielfeld und die Figuren erstellen
    create_board(canvas, SIZE, OFFSET)
    create_pieces(canvas, SIZE, OFFSET, on_piece_click)
    
    # Größe des Kreuzes
    CLOSE_SIZE = 18
    MARGIN = 8

    def draw_close_button():
        x1 = 640 - CLOSE_SIZE - MARGIN
        y1 = MARGIN
        x2 = x1 + CLOSE_SIZE
        y2 = y1 + CLOSE_SIZE

        # Hintergrund (optional)
        bg = canvas.create_rectangle(
            x1 - 4, y1 - 4, x2 + 4, y2 + 4,
            fill="white",
            outline="black",
            width=1
        )

        # Kreuz
        l1 = canvas.create_line(x1, y1, x2, y2, width=2)
        l2 = canvas.create_line(x1, y2, x2, y1, width=2)

        # Klickfläche
        for item in (bg, l1, l2):
            canvas.tag_bind(item, "<Button-1>", lambda e: root.destroy())
            canvas.tag_bind(item, "<Enter>", lambda e: canvas.config(cursor="hand2"))
            canvas.tag_bind(item, "<Leave>", lambda e: canvas.config(cursor=""))

    draw_close_button()

    root.after(100, controller)

    root.mainloop()
