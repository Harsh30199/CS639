left 90
left 90
penup
forward 100
pendown
right 90

:dir1 = 15
:dir2 = 30
:dir3 = 45
:dir4 = 60

:mov1 = 20
:mov2 = 50
:mov3 = 100
:mov4 = 200

:x = 10
:y = 20
:z = 30

:loop1 = 8
:loop2 = 19
repeat :loop1 [
	repeat :loop2 [
		if ( :x >= :y ) [
			if (:x >= :z) [
				forward :mov1
				:y = :x + :z
				left :dir1 + :y
			]
			else [
				forward :mov3
				:y = :z + :x
				left :dir3 + :y
			]
		]
		else [
			if (:y >= :z) [
				forward :mov2
				:x = :y + :z
				left :dir2 + :x
			]
			else [
				penup
				forward :mov3
				:x = :z + :y 
				left :dir3 + :x
				pendown
			]
		]
	]
]