:squaresize1 = 50
:squaresize2 = 70
:squaresize3 = 90
repeat 2 [
	repeat 4 [
		repeat 4 [
			forward :squaresize1
			left 90
		]
		repeat 4 [
			forward :squaresize2
			left 90
		]
		repeat 4 [
			forward :squaresize3
			left 90
		]
		repeat 90 [
			forward 10
			backward 10
			left 4
		]
		penup
		forward :squaresize1 + :squaresize2
		right 45
		pendown
	]
]