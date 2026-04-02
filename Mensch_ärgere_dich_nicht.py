from Spielfeld import create_board
from Spielfiguren import create_pieces
import tkinter as tk
import random
import var

wuerfel_wuerfe = 0
computer_piece = 0
rect = None
SIZE = 55
OFFSET = 10
bewegung_möglich = False
zugzwang_kontrolle = False
COLORS = ["Rot", "Blau", "Grün", "Gelb"]

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
    global dice_label

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
                if var.simulation:
                    root.after(100, restart)
                return # Damit der Gewinner angezeigt wird
    
    if not zugzwang_kontrolle:                
        change_player()

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
    for button in figuren_buttons:
        button.config(state="disabled")
    roll_button.config(state="disabled")
    add_text(f"Spieler {COLORS[spieler]} hat gewonnen!")
    var.gewonnen = True
    return True

# ------------------------------------------------- Spielerwechsel -----------------------------------------------------------------------
def change_player():
    global wuerfel_wuerfe, COLORS, figuren_buttons, dice_label
    dice_label.config(text="Gewürfelt: -")
    
    wuerfel_wuerfe = 0
    var.wuerfel = 0
    if var.noch_ein_zug == False:
        var.spieler = (var.spieler + 1) % (var.anzahl_mensch + var.anzahl_computer)
    else:
        var.noch_ein_zug = False

    if var.auto_wuerfeln.get() == True and not var.spieler >= var.anzahl_mensch: # type: ignore
        auto_würfeln()
    
    if not var.simulation:
        add_text("")
        change_player_label(f"Spieler: {COLORS[var.spieler]}")
        create_rectangle(canvas)
        default_bg = tk.Button().cget("bg")
        for i in range(4):
            figuren_buttons[i].config(bg=default_bg)
    
    if (var.spieler >= var.anzahl_mensch):
        computer_player()
    return
        
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

# ------------------------------------------------- Rahmen für die Spielfiguren ----------------------------------------------------------
def create_rectangle(canvas):
    global rect, SIZE, OFFSET
    canvas.delete(rect)
    player_field_position = [[0, 0], [9, 0], [9, 9], [0, 9]]
    x1 = OFFSET + player_field_position[var.spieler][0] * SIZE
    y1 = OFFSET + player_field_position[var.spieler][1] * SIZE
    x2, y2 = x1 + 2*SIZE, y1 + 2*SIZE
    rect = canvas.create_rectangle(x1, y1, x2, y2, outline="black", width=2)

# ------------------------------------------------- Computergegner -----------------------------------------------------------------------
def computer_player():
    global computer_piece, figuren_buttons
    if not var.simulation:
        add_text(f"Computer {var.spieler+1} ist am Zug! Bitte keine Buttons betätigen!")
    if zugzwang():
        root.after(var.computer_v.get(), figuren_buttons[computer_piece].invoke) # type: ignore
    else:
        root.after(var.computer_v.get(), roll_button.invoke) # type: ignore

# -------------------------------------------------------------------------------------------------------
def auto_würfeln():
    root.after(var.computer_v.get(), roll_button.invoke) # type: ignore

# ------------------------------------------------- Zugzwang -----------------------------------------------------------------------------
def zugzwang():
    global bewegung_möglich, zugzwang_kontrolle, figuren_buttons, computer_piece
    if var.wuerfel == 0:
        return False

    zugzwang_kontrolle = True
    muss_gehen = False
    var.anzahl_zuege = 0

    for i in range(4):
        move_piece(var.pieces[i + 4 * var.spieler])
        if bewegung_möglich:
            var.anzahl_zuege += 1
            muss_gehen = True
            if not var.simulation:
                figuren_buttons[i].config(bg="green")
            computer_piece = i
            bewegung_möglich = False
        else:
            if not var.simulation:
                figuren_buttons[i].config(bg="red")
    zugzwang_kontrolle = False
    
    if (var.anzahl_zuege == 1 
        and var.auto_zuege.get() == True  # type: ignore
        and not var.spieler >= var.anzahl_mensch
        ):
        root.after(var.computer_v.get(), figuren_buttons[computer_piece].invoke) # type: ignore
    
    return muss_gehen

# ------------------------------------------------- Würfeln ------------------------------------------------------------------------------
def roll_dice():
    global wuerfel_wuerfe, dice_label
    if zugzwang():
        add_text(f"Spieler {var.spieler+1} hat Zugzwang!")
        return
    
    if wuerfel_wuerfe == 3:
        change_player()

    elif (wuerfel_wuerfe == 1 and not check_position(var.spieler)):
        change_player()

    else:
        var.wuerfel = random.randint(1, 6)
        if var.wuerfel == 6:
            var.noch_ein_zug = True
        if not var.simulation:
            dice_label.config(text=f"Gewürfelt: {var.wuerfel}")
        zugzwang()
        wuerfel_wuerfe += 1

        if (var.spieler >= var.anzahl_mensch):
            computer_player()
        elif var.auto_wuerfeln.get() == True and var.anzahl_zuege == 0: # type: ignore
            auto_würfeln()

# ------------------------------------------------- Funktion zum Einfügen von Text -------------------------------------------------------
def add_text(text):
    global zugzwang_kontrolle
    if not zugzwang_kontrolle:
        output_label.config(text = text)

# ------------------------------------------------- Funktion zum Ändern des Spielerlabels ------------------------------------------------
def change_player_label(text):
    player_label.config(text= text)

# ------------------------------------------------- Tasteneingaben für die Steuerung -----------------------------------------------------
def on_key_press(event):
    if not var.gewonnen:
        if event.char in ("1", "2", "3", "4"):
            index = int(event.char) - 1  # Umwandeln in 0–3
            kontrolle_move(index)
        
        elif event.char.lower() == "w":
            kontrolle_roll()

# ------------------------------------------------- Klick auf Spielfigur -----------------------------------------------------------------
def on_piece_click(event):
    if not var.gewonnen:
        clicked_id = event.widget.find_closest(event.x, event.y)[0]
        for piece in var.pieces:
            if piece["rect"] == clicked_id or piece["text"] == clicked_id:
                kontrolle_move(piece["piece_number"]-1)
                break

# ------------------------------------------------- Neustart des Spiels ------------------------------------------------------------------
def restart():
    global wuerfel_wuerfe, figuren_buttons, dice_label
    start_positions = var.START_POSITIONS
    var.wuerfel = 0
    wuerfel_wuerfe = 0
    var.gewonnen = False

    dice_label.config(text="Gewürfelt: -")
    
    change_player_label(f"Spieler: {COLORS[var.spieler]}")
    if not var.simulation:
        add_text("")
        create_rectangle(canvas)

        default_bg = tk.Button().cget("bg")
        for i in range(4):
            figuren_buttons[i].config(bg=default_bg)
    
    for button in figuren_buttons:
        button.config(state="normal")
    roll_button.config(state="normal")

    for piece in var.pieces:
        move_piece_to(piece, start_positions[piece["spieler"]][piece["piece_number"]-1])
    
    if var.anzahl_computer == 4:
        computer_player()
    else:
        if var.auto_wuerfeln.get() == True: # type: ignore
            auto_würfeln()
        else:
            add_text(f"Spieler {var.spieler+1} ist am Zug! Bitte würfeln!")

# ------------------------------------------------- Hauptprogramm ------------------------------------------------------------------------
def main():
    global root, canvas, output_label, figuren_buttons
    global roll_button, player_label, COLORS, dice_label
    root = tk.Tk()
    root.title("Mensch ärgere dich nicht")

    # Haupt-Container
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Linker Bereich für Buttons
    button_frame = tk.Frame(main_frame, width=500)
    button_frame.pack(side=tk.LEFT, padx=10, pady=20)

    restart_button = tk.Button(
        button_frame, text="Neustart", 
        command=lambda: restart(), 
        font=("Helvetica", 16), width=10
    )
    restart_button.pack(pady=20)

    # Spieler Label
    player_label = tk.Label(
        button_frame, text=f"Spieler: {COLORS[var.spieler]}", 
        font=("Helvetica", 16), width=10, height=1
    )
    player_label.pack(pady=10)

    # Würfel-Button
    roll_button = tk.Button(
        button_frame, text="Würfeln", 
        command=lambda: kontrolle_roll(), 
        font=("Helvetica", 16), width=10
    ) 
    roll_button.pack(pady=10)

    # Würfelergebnis Label
    dice_label = tk.Label(
        button_frame, text="Gewürfelt: -", 
        font=("Helvetica", 16), width=10, height=1
    )
    dice_label.config(bg="white", relief="sunken")
    dice_label.pack(pady=10)

    # Figur-Buttons
    figuren_buttons = []
    for i in range(4):
        figur_button = tk.Button(
            button_frame, text=f"Figur {i+1}",
            command=lambda i=i: kontrolle_move(i),
            font=("Helvetica", 16), width=10
        )
        figur_button.pack(pady=5)
        figuren_buttons.append(figur_button)
    
    root.bind("<Key>", on_key_press)

    # Textfeld für Ausgaben
    output_label = tk.Label(
        root, text="", font=("Helvetica", 16), width=62, 
        height=1, anchor="w", justify="left"
    )
    output_label.config(bg="white", relief="sunken")
    output_label.pack(side=tk.LEFT, padx=10)

    # Canvas für das Spielfeld
    canvas = tk.Canvas(main_frame, width=640, height=630)
    canvas.pack(side=tk.LEFT, expand=False, fill=tk.BOTH)

    # Das Spielfeld und die Figuren erstellen
    create_board(canvas, SIZE, OFFSET)
    create_pieces(canvas, SIZE, OFFSET, on_piece_click)
    if not var.simulation:
        create_rectangle(canvas)
    
    if var.anzahl_computer == 4:
        root.after(100, computer_player)
    else:
        if var.auto_wuerfeln.get() == True: # type: ignore
            auto_würfeln()
        else:
            add_text(f"Spieler {var.spieler+1} ist am Zug! Bitte würfeln!")
    
    root.mainloop()
