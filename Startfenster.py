import tkinter as tk
from tkinter import ttk
from Mensch_ärgere_dich_nicht import main
from sim_mit_GUI import main_sim
import var

def starte_spiel():
    main()

def starte_konfiguration():

    def speichern_und_starten():
        nonlocal entry_mensch, entry_computer
        try:

            var.anzahl_mensch = int(entry_mensch.get())
            var.anzahl_computer = int(entry_computer.get())
            if (var.anzahl_mensch + var.anzahl_computer) > 4:
                fehler_label.config(text="Die Summe darf maximal 4 sein!") # Überprüfen, ob die Summe 4 ergibt
            elif var.computer_v.get() > 2000 or var.computer_v.get() < 0: # pyright: ignore[reportAttributeAccessIssue]
                fehler_label.config(text = "Bitte eine gültige Zahl für die Geschwindigkeit eingeben!")
            else:
                konfig_fenster.destroy()  # Konfigurationsfenster schließen
                starte_spiel()  # Spiel starten

        except ValueError:

            fehler_label.config(text="Bitte gültige Zahlen eingeben!")

    def starte_simulation():
        var.anzahl_mensch = 0
        var.anzahl_computer = 4
        if var.computer_v.get() > 2000 or var.computer_v.get() < 0: # pyright: ignore[reportAttributeAccessIssue]
            fehler_label.config(text = "Bitte eine gültige Zahl für die Geschwindigkeit eingeben!")
        else:
            konfig_fenster.destroy()
            main_sim()

    # Fenster für die Konfiguration
    konfig_fenster = tk.Tk()
    konfig_fenster.title("Spielkonfiguration")

    def update_mensch(*args):
        wert = default_wert_men.get() #if entry_mensch.get() != "" else 0
        default_wert_com.set(4 - wert)

    def update_computer(*args):
        wert = default_wert_com.get() #if entry_computer.get() != "" else 0
        default_wert_men.set(4 - wert)
    
    default_wert_men = tk.IntVar(value=2)
    default_wert_com = tk.IntVar(value=2)

    default_wert_men.trace_add("write", update_mensch)
    default_wert_com.trace_add("write", update_computer)

    tk.Label(konfig_fenster, text="Anzahl menschlicher Spieler:").grid(row=0, column=0, padx=10, pady=10)
    entry_mensch = tk.Spinbox(
        konfig_fenster, 
        from_= 0, to=4, 
        textvariable = default_wert_men,
        command= update_mensch)
    entry_mensch.grid(row=0, column=1)

    tk.Label(konfig_fenster, text="Anzahl Computergegner:").grid(row=1, column=0, padx=10, pady=10)
    entry_computer = tk.Spinbox(
        konfig_fenster, 
        from_= 0, to=4, 
        textvariable = default_wert_com,
        command=update_computer)
    entry_computer.grid(row=1, column=1)

    var.computer_v = tk.IntVar(value = 1)
    tk.Label(konfig_fenster, text="Computer Geschwindigkeit(0-2000):").grid(row=2, column=0, padx=10, pady=10)
    entry_computer_v = tk.Entry(konfig_fenster, textvariable = var.computer_v)
    entry_computer_v.grid(row=2, column=1)

    fehler_label = tk.Label(konfig_fenster, text="", fg="red")
    fehler_label.grid(row=3, columnspan=2)

    var.auto_zuege = tk.BooleanVar(value=True)
    check = ttk.Checkbutton(konfig_fenster, text="Auto-Zug bei nur einer Möglichkeit", variable=var.auto_zuege)
    check.grid(row=5, columnspan=1, sticky= "w", pady=10)

    var.auto_wuerfeln = tk.BooleanVar(value=True)
    check = ttk.Checkbutton(konfig_fenster, text="Auto-Würfeln", variable=var.auto_wuerfeln)
    check.grid(row=6, columnspan=1, sticky= "w", pady=10)

    start_button = tk.Button(konfig_fenster, text="Spiel starten", command=speichern_und_starten)
    start_button.grid(row=7, column=0)
    simulation_button = tk.Button(konfig_fenster, text="Simulation", command=starte_simulation)
    simulation_button.grid(row=7, column=1, pady = 10)

    konfig_fenster.mainloop()

# Hauptprogrammstart
if __name__ == "__main__":
    starte_konfiguration()