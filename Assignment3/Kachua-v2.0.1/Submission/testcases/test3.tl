:vara = 15
:varb = 20
:varc = 10
:vard = 25
if(:vara < :varb)
[
	forward 10
	if(:vara < :varc)[
		forward 25
		right 30

		if(:varc < :vard)[
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
		if(:varb < :varc)[
		forward 55
		backward 60
		]
		else[
		right 45
		right 180
		backward 70
		]
	]
	
	backward 20
	backward 50
]
else[
	forward 50
	forward 20
	backward 50
]
