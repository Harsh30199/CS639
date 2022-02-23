repeat 6 [
	:y = 3
	:totalshape = 10
	repeat :totalshape [
		repeat :y [
			forward 50
			left 360 / :y
		]
		:x = :totalshape - :y + 5
		if ((:x / 2)  == (:x + :y)) [
			repeat :x [
			forward 50
			right 360 / :x
			]
		]
		:y = :y  + 1
	]
	right 60
]
penup
forward 500
pendown