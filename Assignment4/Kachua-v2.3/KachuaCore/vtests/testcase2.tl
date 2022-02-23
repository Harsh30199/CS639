pendown
if (:x + :y > 50) [
    forward :x
    backward :y
] else [
    if (:x + :y < 30) [
        backward 100
    ]
    forward 100
]
penup