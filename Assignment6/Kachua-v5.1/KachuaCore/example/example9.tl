:squareside = 5
repeat 6 [
	forward 100
	repeat 8 [
		right 45
			repeat 90 [
				forward 2
				right 2
			]
			repeat 4 [
				forward :squareside
				left 90
			]
	]
	left 60
]
right 90
penup
forward 100
pendown