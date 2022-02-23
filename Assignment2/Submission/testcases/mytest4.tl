:x = 5
:y = 10
:z = 25
if (:x > :y || :y == :x) && (:x >= :z)[
:max = :x
]
if (:y > :x && :x > :z) || (:y > :x && :y >= :z) [
:max = :y
]
if (:z > :x || :z > :y || (:z == :x && :z == :y)) [
if(:z > :max)[
:max = :z
]
]
