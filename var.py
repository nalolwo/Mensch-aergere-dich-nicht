username = None
wuerfel = 0
anzahl_computer = None
computer_v = 1
anzahl_mensch = None
COLORS_1 = ["red", "blue", "green", "yellow"]
simulation = False
pieces = []
gewonnen = False
noch_ein_zug = False
auto_zuege = False
auto_wuerfeln = False
anzahl_zuege = 0
spieler = 0

START_POSITIONS = [
    [[0, 0], [0, 1], [1, 0], [1, 1]],
    [[9, 0], [9, 1], [10, 0], [10, 1]],
    [[9, 9], [9, 10], [10, 9], [10, 10]],
    [[0, 9], [0, 10], [1, 9], [1, 10]]
]
GOAL_POSITIONS = [
    [[1, 5], [2, 5], [3, 5], [4, 5]],
    [[5, 1], [5, 2], [5, 3], [5, 4]],
    [[9, 5], [8, 5], [7, 5], [6, 5]],
    [[5, 9], [5, 8], [5, 7], [5, 6]]
]
GO_POSITIONS = [
    [0,4], [1,4], [2,4], [3,4], [4,4], [4,3], [4,2], [4,1], [4,0], [5,0],
    [6,0], [6,1], [6,2], [6,3], [6,4], [7,4], [8,4], [9,4], [10,4], [10,5],
    [10,6], [9,6], [8,6], [7,6], [6,6], [6,7], [6,8], [6,9], [6,10], [5,10],
    [4,10], [4,9], [4,8], [4,7], [4,6], [3,6], [2,6], [1,6], [0,6], [0,5]
]
