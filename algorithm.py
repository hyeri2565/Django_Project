#진수변환
'''
def transfor(n,n2,n3):
    s=''
    c=-1
    answer=''
    while n>0:
        s=s+str(n%n2)
        n=n//n2
    print(s)
        
    for i in range(n3):
        answer=answer+s[c]
        c-=1
    return(answer)
    
print(transfor(100,6,3))
'''
import pyautogui as gui
gui.moveto(50,50)

    
