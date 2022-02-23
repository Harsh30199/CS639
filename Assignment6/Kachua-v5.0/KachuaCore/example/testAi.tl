:vara = 10
:varb = 200
:vara = :varb
:one = 1


if :vara < :varb [
   :vara = 0
   :varb = 0
   repeat 10 [
      :vara = :vara + :one
      repeat 10 [
         :vara = :vara + :one
      ]
   ]
]


