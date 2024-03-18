RULES_TEXT:list = [
    ["Objective: Rearrange the photons in the grid",
     "to match the Goal grid before running out of energy.",
     "Sounds simple enough, right?"],
     ["You can move a photon between any two connected", 
      "crystals on the grid. Moving a photon of any color",
      "costs one energy. To move a photon, click on it,",
      "and then click on its destination. If you decide",
      "you don't want to move the photon after all, place", 
      "it back in its original crystal or right-click anywhere," ,
      "and no energy will be deducted."],
      ["These are the primary photons: red, green, and blue.",
       "If you move primary photons on top of each other, they",
       "will blend into a compound photon:"]
]

# estrutra de LEVEL
# [0] -> board inicial
# [1] -> energia do nivel
# [2] -> path para a imagem do objetivo
# [3] -> titulo do nivel
# [4] -> board objetivo

LEVEL1:list = [
    [
        [0, 1, 0],
        [1, 1, 0, 2],
        [0, 0, 0, 2, 0],
        [3, 3, 0, 2],
        [0, 3, 0]
    ],
    9,
    "./images/lvl1goal.png",
    "Level 1: Finger Painting",
    [
        [0, 0, 0],
        [0, 0, 5, 0],
        [0, 6, 4, 0, 0],
        [0, 0, 7, 0],
        [0, 0, 0]
    ]
]

LEVEL2:list = [
    [
        [0, 1, 0],
        [0, 0, 0, 2],
        [3, 0, 0, 2, 0]
    ],
    9,
    "./images/lvl2goal.png",
    "Level 1: Finger Painting",
    [
        [2, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 4, 0, 0]
    ]
]
