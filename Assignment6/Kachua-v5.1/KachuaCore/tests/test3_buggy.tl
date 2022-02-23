penup
:x = 50
:t = :y + :x
if :t <= 90[
	:z = :t + 10
	if :z < 90[
	forward 20
	]
]
else[
	:z = :t - 30
	if :z < 90 [
	forward 10
	]
]
forward 20
