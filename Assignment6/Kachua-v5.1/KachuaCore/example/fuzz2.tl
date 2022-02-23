pendown
:z=:y+2
:z=:z+1
if ( :z < 6) [
    :z=:z-1
    repeat :z[
      forward 10
      backward 10
    ]
]
:z = :x+20
if ( :x < 30) [
    backward 10
]
