left 90
penup
right 90
forward 200
left 90
pendown

:move = 5
repeat :move [
	repeat 360 [
		forward :move
		left 1
	]
	repeat 4 [
	 forward 10 * :move
	 right 90
	]
	:move = :move -1
	penup
	left 90
	forward 60
	right 90
	pendown
]
right 90
forward 400