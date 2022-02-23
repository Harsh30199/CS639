penup
right 96
:vara = 0
:varb = 0 
forward 10 + 20
right 90
left 90
pendown
forward 30
if(:vara==0)
[
forward 10
if(:varb == 0)[
forward 100
]
else[
forward 200
]
forward 50
backward 20
backward 50
]
else[
forward 50
forward 20
backward 50
]
backward 100
right 90
