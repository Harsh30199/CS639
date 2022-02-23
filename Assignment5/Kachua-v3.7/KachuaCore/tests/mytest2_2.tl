:b = :a
if(:a>10)
[
	:b = :a + :c1
]
else
[
	if(:a>5)[
	:b = :a + :c3
	]
	
	:b = :b + :c2

]
