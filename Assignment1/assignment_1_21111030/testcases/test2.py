def printer(a=5,b='*'):
    for i in range(a+1):
        for j in range(i):
            print(b,sep='',end='')
        print()
    for i in range(a-1,-1,-1):
        for j in range(i):
            print(b,sep='',end='')
        print()

flag1=flag2=0          
n=input("Enter single digit number: ")
if(len(n)==1):
    if(ord(n) in range(48,58)):
        n=int(n)
        flag1=1

m=input("Enter character for pattern between A-D ")
if(ord(m) in range(ord('A'),ord('E'))):
   flag2=1
   m.lower()

if (flag1 and not(flag2)):
   printer(n)
elif(not flag1 and flag2):
    printer(b=m)
elif(not(flag1) and not flag2):
    printer()
else:
    printer(n,m)


