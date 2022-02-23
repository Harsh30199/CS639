pendown
if (:move - :move1 > 50) [
	forward 10
]
if :move + :move1 < 100 [
	if :move - :move1 + :z >20[
		forward 30
		if :move + :move1 + :z >39[
		forward 20
]
]
]
if :move + :z < 100 [
	forward 10	
]
else [
	forward 10
]

if :move + :z > 400 && :move1 + :z < 450 [
	forward 10
]
else [
	forward 10
]