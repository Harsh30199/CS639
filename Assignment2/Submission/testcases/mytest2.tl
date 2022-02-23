:vara = 10
:varb = 5
:varc = :vara * :varb
repeat :varc[
:vard = :vard + (:vara - :varb)
repeat :vard[
:vare = :vare + 5 * :vard
]
:varef = :vard - :vare
]
:vara = :vare
:varb = :varf
