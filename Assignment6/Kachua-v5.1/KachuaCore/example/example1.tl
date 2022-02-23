left 90
pendown
:move = 20
repeat 5 [
	repeat 2 [
		repeat 4 [
			forward :move
			right 45
		]
	]
	repeat 2 [
		repeat 4 [
			forward :move
			left 45
		]
	]
	:move = :move +5
]