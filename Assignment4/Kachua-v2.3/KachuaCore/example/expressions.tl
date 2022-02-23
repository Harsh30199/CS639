

:varc = 10
if (:varc == 0) && (:vara < :varb) [
   :vara = 0
   :varb = 0
   :varb = (:vara + :varb) * :varc
]

if :varc != 0 && (:vara < :varb) [
  :varb = 0
]

if :vara < :varb || :vara == :varb [
   :vara = 0
   :varb = -5 + 10
]

