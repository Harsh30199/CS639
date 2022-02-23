left 90
pendown
if (:move - :move1 > 50) [
	forward 10
]
if :move + :move1 < 100[
	if :move - :move1 + :z >20[
		forward 30
		if :move + :move1 + :z >39[
		forward 20
	]
	]
	
	if :move*:move1 +:z >90 [
		forward 20
	]
	if :move - :move1 < 1 [
		forward 20
	]
] 