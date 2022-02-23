left 30
:shapes = 11
:space = 50
:move = 5
:dir = 15
repeat 5  [
	repeat :shapes [
		right 30
		repeat 15 [
			forward :move
			right 15
		]
		penup 
		forward :space
		left 360 / :dir
		pendown
	]
	penup
	left 90
	forward 150
	pendown
]