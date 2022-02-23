penup
forward 100
right 90
forward 100
left 90
pendown
:shape = 60
repeat 9 [
	:x = 1
	:y = 20
	repeat 10 [
		forward :shape
		if :x > :y [
			right :shape - :x
			:y = :y +1
		]
		else [
			left :shape - :y
			:x = :x + 1
		]
	]
	forward 100
]