class Numbers:
    def func(self):
        l=set()
        for _ in range(3):
            l.add(int(input()))
            max1=0
            flag1=0
        x,y,z=tuple(l)
        if(x>z and x>y):
            if(x>0):
                max1=x
                flag1=1
        elif(y>z and y>x):
            if(y>0):
                max1=y
                flag1=1
        elif(z>x and z>y):
            if(z>0):
                max1=z
                flag1=1
        if(max1<=0 or not(flag1)):
            print("No greatest positive no")
        else:
            print("Greatest positive no is ",max1)

n=Numbers()
n.func()
            
            
