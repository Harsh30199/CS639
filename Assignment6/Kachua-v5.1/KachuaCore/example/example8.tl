:squareside = 10
penup
goto (100,100)
pendown
repeat 8 [
	right 45
		repeat 90 [
			forward 4
			right 2
		]
		repeat 4 [
			forward :squareside
			left 90
		]
]
penup
forward 100
pendown