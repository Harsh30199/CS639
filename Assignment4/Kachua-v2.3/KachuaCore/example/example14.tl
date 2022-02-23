:x = 150
:y =150
:starlen = 100
repeat 12 [
forward :starlen
left 150
]
repeat 2 [
		penup
		goto(:x, :y)
		pendown
		repeat 12 [
			forward :starlen
			repeat 4 [
				forward 5
				left 90
			]
			left 150
		]

		penup
		goto(:x, 0)
		pendown
		repeat 12 [
			forward :starlen
			repeat 4 [
				forward 5
				left 90
			]
			left 150
		]
		
		penup
		goto(:x* -1, :y)
		pendown
		repeat 12 [
			forward :starlen
			repeat 4 [
				forward 5
				left 90
			]
			left 150
		]

		penup
		goto(:x * -1, 0)
		pendown
		repeat 12 [
			forward :starlen
			repeat 4 [
				forward 5
				left 90
			]
			left 150
		]
		
		penup
		goto(:x, :y * -1)
		pendown
		repeat 12 [
			forward :starlen
			repeat 4 [
				forward 5
				left 90
			]
			left 150
		]
		
		penup
		goto(0, :y*-1)
		pendown
		repeat 12 [
			forward :starlen
			repeat 4 [
				forward 5
				left 90
			]
			left 150
		]
		
		
		penup
		goto(:x * -1, :y * -1)
		pendown
		repeat 12 [
			forward :starlen
			repeat 4 [
				forward 5
				left 90
			]
			left 150
		]
		penup
		goto(0, :y)
		pendown
		repeat 12 [
			forward :starlen
			repeat 4 [
				forward 5
				left 90
			]
			left 150
		]
	:x = :x  + 100
	:y= :y + 100
]