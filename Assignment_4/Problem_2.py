## Question 2

# Global Variable i
i=0
def Monkey_go_box(x,y):
    global i
    i=i+1
    print('step',i,': Monkey goes from',x,'to',y)

def Monkey_move_box(x,y):
    global i
    i = i + 1
    print('step',i,': Monkey takes the box from',x,'and deliver it to',y)

def Monkey_on_box():
    global i
    i = i + 1
    print('step',i,': Monkey climbs up the box')

def Monkey_get_banana():
    global i
    i = i + 1
    print('step',i,': Monkey picks the banana')


import sys

print("Enter the position of monkey")
monkey=int(input())
print("Enter the position of banana")
banana=int(input())
print("Enter the position of box")
box=int(input())
print('The steps are as follows:')

Monkey_go_box(monkey, box)
Monkey_move_box(box, banana)
Monkey_on_box()
Monkey_get_banana()