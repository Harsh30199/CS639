
if (:y1 - :y2 > 42) [
  forward 10
  if (:y1 + :y2 < 60) [
    forward 10
    if :y1 < :y2 [ 
      forward 10
    ]
  ]
  else [
    forward 10
  ]
  
] else [
  forward 10
]


