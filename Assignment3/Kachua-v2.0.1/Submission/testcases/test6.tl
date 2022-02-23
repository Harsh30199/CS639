:vara = 0
:varb = 20 
forward 5 * :varb
repeat 4[
backward 50
left 45
if(:vara == 0)[
right -45
right 90
repeat 4[
forward 25
right 90
]
:vara = 1
]
else[
left -45
left 270
repeat 3[
forward 25
right 60
]
right 30
:vara = 0
]

forward 100
]


