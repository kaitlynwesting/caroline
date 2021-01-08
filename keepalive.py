""" death = False        
def f():
    death = True      # Here python doesn't now death, so it creates a new, different variable
f()
print(death)    """       # False

death = False       
def f():
    global death
    num = input()
    
    if num == "no":
        death = True
f()
print(death)      # True