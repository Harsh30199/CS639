:a = 6
:b = 8

if :a > 0 && :a<= 10[
   if :a >= 5[
   :a = :a - 5
   ]
   :a = (:a * 2) - 1
 ]

if (:a <= 0 || :a != -50)[
   :m = :a + :b
   :n = :b - :a
   if :m == :n[
   :m = :m + :a
   :n = :n - :b
   ]
]
