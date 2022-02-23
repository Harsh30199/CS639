:x = 50
:y =50
:squareshape = 50
repeat 4 [
	forward :squareshape
	left 90
]
repeat 4 [
		penup
		goto(:x, :y)
		pendown
		repeat 4 [
			forward :squareshape
			left 90
			]
		penup
		goto(:x* -1, :y)
		pendown
		repeat 4 [
			forward :squareshape
			left 90
			]
		penup
		goto(:x, :y * -1)
		pendown
		repeat 4 [
			forward :squareshape
			left 90
			]
		penup
		goto(:x * -1, :y * -1)
		pendown
		repeat 4 [
			forward :squareshape
			left 90
		]
	:x = :x  + 20
	:y= :y + 20
]