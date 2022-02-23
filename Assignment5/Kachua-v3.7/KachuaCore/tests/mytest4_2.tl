:b = :a
if(:a > 8)[
repeat 2
[
	:b = :b + :c1
]
]
if(:a < 6)[
repeat 3
[
	:b = :b + :c2
]
]

if (:a == 6 || :a == 7 || :a == 8)[
repeat 5
[
	:b = :b + :c3
]
]
