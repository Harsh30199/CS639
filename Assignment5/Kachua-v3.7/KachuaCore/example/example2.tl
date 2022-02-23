pendown
:move = 10
:dir = 5
repeat 11 [
	repeat 4 [
		repeat 2 [
			repeat 4 [
				forward :move
				right :dir
			]
		]
		:move = :move + 5 	
	]
	left 20
	forward 150
	left 45
]
forward 20
penup