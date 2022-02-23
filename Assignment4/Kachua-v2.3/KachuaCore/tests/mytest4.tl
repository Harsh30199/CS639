
if(:a > :b)
[
	forward 10
	if(:a < :c)[
		forward 25
		right 30

		if(:c < :d)[
		left 30
		forward 30
		backward 85
		]
		else[
		right 330
		forward 5
		backward 20
		]
	]
	else[
		forward 20
		if(:b < :c)[
		left 80
		forward 55
		backward 60
		]
		else[
		
		right 225
		backward 70
		]
	]
	
	backward 70
]
else[
	forward 70
	backward 50
]
