:vara = 10
:varb = 200
:vara = :varb
forward :varb
right 90
penup
forward :varb
right 90
pendown
forward :varb
right 90
penup
forward :varb
pendown
if :vara <= :varb [
   :vara = 0
   :varb = 0
]

if :vara < :varb [
   :vara = 0
   :varb = 0
   repeat 10 [
      :vara = :vara + 1
      repeat 10 [
         :vara = :vara + 1
      ]
   ]
]

goto(10,20)