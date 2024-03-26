# Regras do jogo
RULES_TEXT:list = [
    ["Objective: Rearrange the photons in the grid",
     "to match the Goal grid before running out of energy.",
     "Sounds simple enough, right?"],
     ["You can move a photon between any two connected", 
      "crystals on the grid. Moving a photon of any color",
      "costs one energy. To move a photon, click on it,",
      "and then click on its destination. If you decide",
      "you don't want to move the photon after all, click" ,
      "the button 'undo' and no energy will be deducted."],
      ["These are the primary photons: red, green, and blue.",
       "If you move primary photons on top of each other, they",
       "will blend into a compound photon:"]
]

# Todas as jogadas possíveis que se podem efetuar.
POSSIBLE_MOVES: dict[tuple[int, int], list[tuple[int, int]]] = {
    (0,0): [(0,1), (1,0), (1,1)],
    (0,1): [(0,0), (0,2), (1,1), (1,2)],
    (0,2): [(0,1), (1,2), (1,3)],
    (1,0): [(0,0), (1,1), (2,0), (2,1)],
    (1,1): [(0,0), (0,1), (1,0), (2,2)],
    (1,2): [(0,1), (0,2), (1,3), (2,2)],
    (1,3): [(0,2), (1,2), (2,3), (2,4)],
    (2,0): [(1,0), (2,1), (3,0)],
    (2,1): [(1,0), (2,0), (2,2), (3,0)],
    (2,2): [(1,1), (1,2), (2,1), (2,3), (3,1), (3,2)],
    (2,3): [(1,3), (2,2), (2,4), (3,3)],
    (2,4): [(1,3), (2,3), (3,3)],
    (3,0): [(2,0), (2,1), (3,1), (4,0)],
    (3,1): [(2,2), (3,0), (4,0), (4,1)],
    (3,2): [(2,2), (3,3), (4,1), (4,2)],
    (3,3): [(2,3), (2,4), (3,2), (4,2)],
    (4,0): [(3,0), (3,1), (4,1)],
    (4,1): [(3,1), (3,2), (4,0), (4,2)],
    (4,2): [(3,2), (3,3), (4,1)]
}

# Representação de todas as cores que são utilizadas na representação do jogo.
BLACK: tuple[int, int, int] = (0, 0, 0)               
DARKGREY: tuple[int, int, int] = (169, 169, 169)      # para as linhas
LIGHTGREY: tuple[int, int, int] = (211, 211, 211)     # para exemplos das regras
GREY: tuple[int, int, int] = (128, 128, 128)          #0
RED: tuple[int, int, int] = (255, 0, 0)               #1
GREEN: tuple[int, int, int] = (0, 255, 0)             #2
BLUE: tuple[int, int, int] = (0, 0, 255)              #3
WHITE: tuple[int, int, int] = (255, 255, 255)         #4    
YELLOW: tuple[int, int, int] = (255, 255, 0)          #5
PINK: tuple[int, int, int] = (255, 0, 255)            #6
AQUA: tuple[int, int, int] = (0, 255, 255)            #7
ORANGE: tuple[int, int, int] = (255, 165, 0)          # highlight selected circle
PURPLE: tuple[int, int, int] = (160, 32, 240)         # highlight hint

# Como obter as cores compound com as cores primárias.
COMPUND_COLORS: dict[tuple[tuple[int, int, int], tuple[int, int, int]], tuple[int, int, int]] = {
    (RED, GREEN): YELLOW,
    (GREEN, RED): YELLOW,
    (RED, BLUE): PINK,
    (BLUE, RED): PINK,
    (GREEN, BLUE): AQUA,
    (BLUE, GREEN): AQUA,
    (RED, AQUA): WHITE,
    (AQUA, RED): WHITE,
    (GREEN, PINK): WHITE,
    (PINK, GREEN): WHITE,
    (BLUE, YELLOW): WHITE,
    (YELLOW, BLUE): WHITE
}

# estrutra de LEVELX
# [0] -> board inicial
# [1] -> energia do nivel
# [2] -> path para a imagem do objetivo
# [3] -> titulo do nivel
# [4] -> board objetivo
# [5] -> altura da board
LEVEL1:list = [
    [
        [0, 1, 0],
        [0, 0, 0, 2],
        [3, 0, 0, 2, 0]
    ],
    8,
    "./images/lvl1goal.png",
    "Level 1",
    [
        [2, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 4, 0, 0]
    ],
    3
]

LEVEL2:list = [
    [
        [0, 1, 0],
        [1, 1, 0, 2],
        [0, 0, 0, 2, 0],
        [3, 3, 0, 2],
        [0, 3, 0]
    ],
    9,
    "./images/lvl2goal.png",
    "Level 2",
    [
        [0, 0, 0],
        [0, 0, 5, 0],
        [0, 6, 4, 0, 0],
        [0, 0, 7, 0],
        [0, 0, 0]
    ],
    5
]

LEVEL3:list = [
    [
        [2, 2, 0],
        [0, 0, 0, 0],
        [2, 0, 3, 0, 1],
        [1, 0, 1, 0],
        [3, 0, 0]
    ],
    21,
    "./images/lvl3goal.png",
    "Level 3",
    [
        [1, 3, 1],
        [0, 0, 0, 0],
        [1, 0, 2, 0, 3],
        [0, 0, 0, 2],
        [2, 0, 0]
    ],
    5
]

LEVEL4: list = [
    [
        [1, 3, 2],
        [1, 0, 0, 0],
        [3, 2, 1, 0, 2],
        [3, 3, 2, 1],
        [1, 0, 3]
    ],
    17,
    "./images/lvl4goal.png",
    "Level 4",
    [
        [5, 0, 3],
        [0, 6, 0, 4],
        [7, 0, 0, 1, 0],
        [0, 2, 0, 0],
        [0, 0, 6]
    ],
    5
]
