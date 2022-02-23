

repeat 5
[
	if(:b - :a > 40)
	[
		forward 50
		right 72
	]
	
	if(:b - :a > 30 && :b - :a <=40)
	[
		forward 50
		right 45
	]
	
	if(:b - :a > 20 && :b - :a <=30)
	[
		forward 50
		right 205
	]
	
	if(:b - :a > 10 && :b - :a <=20)
	[
		forward 50
		right 97
	]
	
	if(:b - :a > 0 && :b - :a <=10)
	[
		forward 50
		right 152
	]
	
	:b = :b - 10
	:a = :a + 10
	
]
