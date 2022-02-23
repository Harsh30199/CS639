def armstrong(n):
    res=0
    while(n>0):
        r=n%10
        n=n//10
        res+=r**3
    return res

n=int(input())
res=armstrong(n)
if(n==res):
    print("Armstrong")
else:
    print("Not Armstrong")

n1=int(input("Enter 3 digit number: "))
if(99<n1<1000):
    x=n1%10
    y=(n1//10)%10
    z=(n1//100)
    if(x<y<=z):
        if(y!=z):
            print('Hundred Digits the Largest')
        else:
            print("Unit's Digit Smallest")
    else:
        print("Nothing")
    
