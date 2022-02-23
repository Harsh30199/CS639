:vara = 20
:varb = 10
:varc = 60
repeat 14 [
	penup
	goto (0, 0)
	pendown
	repeat 6 [
		if (:vara == :varb) [
			right :varb
			
		]
		else [
		 if ((:vara > :varc) && (:varb < :varc)) [
			:vara = :varc / :vara
			:varb = :varb / :varc
		 ]
		]
		forward :vara
		right :vara
		forward :varb
		backward :varb
		forward :varc
		left :varc
	]
	left 90
]
penup
forward 500
