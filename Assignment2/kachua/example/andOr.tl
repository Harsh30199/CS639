:vara = 10
:varb = 20
:vara = :varb

if (:vara < :varb || :vara == :varb) && :vara != :varb [
   :vara = 0
   :varb = 0
]

if :vara < :varb && :vara >= 22 [
   :vara = 0
   :varb = 0	
   repeat 10 [  
      :vara = 0
      :varb = 0
      repeat 10 [
         :vara = 0
         :varb = 0
      ]
   ]
]


