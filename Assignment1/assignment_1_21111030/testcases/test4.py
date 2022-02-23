x=int(input())

y=(x+4)*(x-5)
z= x+4*x-5

print("(x+4)*(x-5) = ",y)
print("x+4*x-5 = ",z)
print("As we can see putting brackets has effect on expression value \n\n\n")


y = x>>1
z=x//2
print("Result using Bitwise Shift: ",y)
print("Result using Floor Division: ",z)
print("As we can see that result is same, we can use less expensive operators like bitwise instead of expensive operators like multiplication and division\n\n\n\n")

print("Values from -x to x")
y=-x
if(~x<0):
    while(y<=x):
        print(y,end=' ')
        y+=1
    print()
else:
    while(y>=x):
        print(y,end=" ")
        y-=1
    print()
