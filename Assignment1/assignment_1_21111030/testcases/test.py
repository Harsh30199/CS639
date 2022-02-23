squares={x:x**2 for x in range(0,19,3) if x%2==0} ##Dictionary Comprehension
for x,y in squares.items():
    print("Square of ",x," is ",y)
else:
    s="For loop finished"
    print(s)

cubes=[(y,y**3) for y in range(0,50,5)]
cubes_mul_10=cubes[2::2]
print(cubes,cubes_mul_10,sep='\n')
