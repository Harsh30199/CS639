if(:a >= :b)
[
	if(:a >= :c)
	[
		if(:a >= :d)
		[
			forward 100
		]
		else
		[
			right 90
			forward 100
		]	
	]
	else
	[
		if(:c >= :d)
		[
			right 180
			forward 100
		]
		else
		[
			right 90
			forward 100
		]
	]
	
]
else
[
	if(:b >= :c)
	[
		if(:b >= :d)
		[
			left 90
			forward 100
		]
		else
		[
			right 90
			forward 100
		]	
	]
	else
	[
		if(:c >= :d)
		[
			right 180
			forward 100
		]
		else
		[
			right 90
			forward 100
		]
	]
]
