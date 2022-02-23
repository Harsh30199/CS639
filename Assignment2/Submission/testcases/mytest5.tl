:m = 10
:suma = -50
:sumb = 50
repeat :m[
:a=5
:b=9
:c = -7
repeat :a[
if(:suma <=0)[
:suma = :suma + (:a - :c)
]
]
:c = :c + 1
repeat :b[
if(:sumb != 0)[
:sumb = :sumb - (:b + :c)
]
]
:c = :c - 1
]

if (:suma != :sumb)[
:a = :m * 5
:b = :m * 2
]
