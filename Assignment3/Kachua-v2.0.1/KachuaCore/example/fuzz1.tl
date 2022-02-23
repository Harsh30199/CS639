left 90
pendown
if (:move > 50) [
	:move = 100
    forward :move - 10
] else [
    backward :move
]
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