import queue
import time
import matplotlib.pyplot as plt
import numpy as np

start_node = [0,0]
goal_node = [0,0] 
cost = 0
visited_node = {}
Queue = queue.PriorityQueue()
x_node = []
y_node = []

x, y = np.ogrid[:401, :251]
        
###########################################################
#################### Define obstacle zone #################
###########################################################


## hexagon obstacle
a1 = 4*x + 7*y - 1780 <= 0
a2 = x + 0*y <= 235
A1 = np.logical_and(a1, a2)
a3 = 4*x - 7*y -380 <= 0
A1 = np.logical_and(A1, a3)
a4 = 4*x + 7*y -1220 >= 0
A1 = np.logical_and(A1, a4)
a5 = x + 0*y >= 165
A1 = np.logical_and(A1, a5)
a6 = 4*x - 7*y + 180 >= 0
A = np.logical_and(A1, a6)

##circle obstacle
a1 = ((x-300)**2 + (y-185)**2 <= 40*40)

## obstacle area (hexagon + circle)
obstacle_area = np.logical_or(A, a1)

##polygon obstacle
##upper triangle obstacle
a1 = 25*x - 79*y + 13715 >= 0
a2 = 6*x -7*y +780 <= 0
A1 = np.logical_and(a1, a2)
a3 = 5*x + 44*y - 8320 >= 0  
A1 = np.logical_and(A1, a3)
##lower triangle obstacle
b1 = 5*x + 44*y - 8320 <= 0 
b2 = 85*x + 69*y - 15825 >= 0
B1 = np.logical_and(b1,b2)
b3 = 16*x + 5*y -2180 <= 0
B1 = np.logical_and(B1,b3)
##combine polygon obstacle
A = np.logical_or(A1, B1)

##obstacle area (hexagone + circle + polygon)
obstacle_area = np.logical_or(obstacle_area, A)

X_obstacle = []
Y_obstacle = []

for i in range(obstacle_area.shape[0]):
    for j in range(obstacle_area.shape[1]):
        if obstacle_area[i][j]==True:
            X_obstacle.append(i)
            Y_obstacle.append(j)

###########################################################
#################### Define clearance zone ################
###########################################################

## Hexagone outside area
x, y = np.ogrid[:401, :251]
a1 = 4*x + 7*y - 1780 > 0
a2 = x + 0*y > 235
A1 = np.logical_or(a1, a2)
a3 = 4*x - 7*y -380 > 0
A1 = np.logical_or(A1, a3)
a4 = 4*x + 7*y -1220 < 0
A1 = np.logical_or(A1, a4)
a5 = x + 0*y < 165
A1 = np.logical_or(A1, a5)
a6 = 4*x - 7*y + 180 < 0
A = np.logical_or(A1, a6)
## hexagone + 5 mm clearace area
a1 = ( (x-200)*(123-146) - (y-146)*(240-200)  >= 0 )
a2 = ( x + 0*y <= 240 )
A1 = np.logical_and(a1, a2)
a3 = ( (x-240)*(54-77) - (y-77)*(200-240)  >= 0 )
A1 = np.logical_and(A1, a3)
a4 = ( (x-200)*(77-54) - (y-54)*(160-200)  >= 0 )
A1 = np.logical_and(A1, a4)
a5 = ( x +0*y >= 160 )
A1 = np.logical_and(A1, a5)
a6 = ( (x-200)*(123-146) - (y-146)*(160-200)  <= 0 )
A1 = np.logical_and(A1, a6)
## clearnace area hexagone
clearance_area = np.logical_and(A, A1)


###Boundary
a1 = x + 0*y < 6
a2 = x + 0*y > 394
A1 = np.logical_or(a1, a2)
a3 = y + 0*y < 6
A1 = np.logical_or(A1, a3)
a4 = y +0*y > 244
A1 = np.logical_or(A1, a4)
## clearance area (boundary + hexagone)
clearance_area = np.logical_or(clearance_area, A1)


###circle
a1 = ((x-300)**2 + (y-185)**2 <= 45*45)
a2 = ((x-300)**2 + (y-185)**2 > 40*40)
A1 = np.logical_and(a1,a2)
###clearance area (boundary + hexagone + circle)
clearance_area = np.logical_or(clearance_area, A1)


##polygon outside area
##upper triangle outside area
a1 = 25*x - 79*y + 13715 < 0
a2 = 6*x -7*y +780 > 0
A1 = np.logical_or(a1, a2)
a3 = 5*x + 44*y - 8320 < 0 
A1 = np.logical_or(A1, a3)
##lower triangle outside area
b1 = 5*x + 44*y - 8320 > 0 
b2 = 85*x + 69*y - 15825 < 0
B1 = np.logical_or(b1,b2)
b3 = 16*x + 5*y -2180 > 0
B1 = np.logical_or(B1,b3)
##combine polygon outside area
A = np.logical_and(A1, B1)
##polygon + 5 mm clearance area
##upper triangle
a1 = ( 7*x - 6*y + 450 <= 0)
a2 = ( 6*x - 19*y + 3365 >=0 )
A1 = np.logical_and(a1, a2)
a3 = ( x + 13*y -2430 >= 0  )
A1 = np.logical_and(A1, a3)
##lower triangle
b1 = ( 19*x + 18*y -3805 >= 0 )
b2 = ( x + 13*y -2430 <= 0  )
B1 = np.logical_and(b1, b2)
b3 = ( 18*x + 5*y -2520 <= 0  )
B1 = np.logical_and(B1, b3)
# print(A1[120][215])
C = np.logical_or(A1, B1)
#clearance area of polygon
D = np.logical_and(A,C)

###clearance area (boundary + hexagone + circle + polygon)
clearance_area = np.logical_or(clearance_area, D)

X_clearance = []
Y_clearance = []

for i in range(clearance_area.shape[0]):
    for j in range(clearance_area.shape[1]):
        if clearance_area[i][j]==True:
            X_clearance.append(i)
            Y_clearance.append(j)

## obstacle and clerance area combines
obstacle_area = np.logical_or(obstacle_area, clearance_area)


def takeStartInput():
    
    print("Enter x and y co-ordinate of start node. Please press 'Enter' key after adding each element: ")
    for i in range(2):
        start_node[i] = int(input())
    if not start_node[0] == int(start_node[0]):
        print("Only integer number is acceptable. Please enter start node again. ")
        takeGoalInput()
    isTrue = nodeOutOfBound(start_node)
    if isTrue:
        print("start node is out of bound, please enter start node again.")
        takeStartInput()
    isObstacle = obstacle_area[start_node[0],start_node[1]]
    if isObstacle:
        print("Start node is either in obstacle area or in clearnace area. Please enter start node again. ")
        takeStartInput()

def takeGoalInput():
    print("Enter x and y co-ordinate of goal node. Please press 'Enter' key after adding each element: ")
    for i in range(2):
        goal_node[i] = int(input())
        if int(goal_node[i]) != goal_node[i]:
            print("Only integer number is acceptable. Please enter goal node again. ")
            takeGoalInput()
    isTrue = nodeOutOfBound(goal_node)
    if isTrue:
        print("Goal node is out of bound, please enter goal node again.")
        takeGoalInput()
    isObstacle = obstacle_area[goal_node[0],goal_node[1]]
    if isObstacle:
        print("Goal node is either in obstacle area or in clearnace area. Please enter goal node again. ")
        takeGoalInput()

def nodeOutOfBound(current_node):
    if current_node[0] < 0 or current_node[0] > 400 or current_node[1] < 0 or current_node[1] > 250:
        return True
    else:
        return False

def exploreNode(current_node,cost):
    
    left_node = (current_node[0]-1, current_node[1])
    isobstacle = obstacle_area[left_node[0],left_node[1]]
    if not isobstacle:
        isTrue = nodeOutOfBound(left_node)
        if not isTrue:
            if left_node not in visited_node:
                new_cost = cost + 1
                Queue.put((new_cost,(left_node[0], left_node[1], current_node[0], current_node[1])))
        
    up_left_node = (current_node[0]-1, current_node[1]+1)
    isobstacle = obstacle_area[up_left_node[0],up_left_node[1]]
    if not isobstacle:
        isTrue = nodeOutOfBound(up_left_node)
        if not isTrue:
            if up_left_node not in visited_node:
                new_cost = cost + 1.4
                Queue.put((new_cost,(up_left_node[0], up_left_node[1], current_node[0], current_node[1])))
    
    up_node = (current_node[0], current_node[1]+1)
    isobstacle = obstacle_area[up_node[0],up_node[1]]
    if not isobstacle:
        isTrue = nodeOutOfBound(up_node)
        if not isTrue:
            if up_node not in visited_node:
                new_cost = cost + 1
                Queue.put((new_cost,(up_node[0], up_node[1], current_node[0], current_node[1])))
    
    up_right_node = (current_node[0]+1, current_node[1]+1)
    isobstacle = obstacle_area[up_right_node[0],up_right_node[1]]
    if not isobstacle:
        isTrue = nodeOutOfBound(up_right_node)
        if not isTrue:
            if up_right_node not in visited_node:
                new_cost = cost + 1.4
                Queue.put((new_cost,(up_right_node[0], up_right_node[1], current_node[0], current_node[1])))
            
    right_node = (current_node[0]+1, current_node[1])
    isobstacle = obstacle_area[right_node[0],right_node[1]]
    if not isobstacle:
        isTrue = nodeOutOfBound(right_node)
        if not isTrue:
            if right_node not in visited_node:
                new_cost = cost + 1
                Queue.put((new_cost,(right_node[0], right_node[1], current_node[0], current_node[1])))
    
    
    down_right_node = (current_node[0]+1, current_node[1]-1)
    isobstacle = obstacle_area[down_right_node[0],down_right_node[1]]
    if not isobstacle:
        isTrue = nodeOutOfBound(down_right_node)
        if not isTrue:
            if down_right_node not in visited_node:
                new_cost = cost + 1.4
                Queue.put((new_cost,(down_right_node[0], down_right_node[1], current_node[0], current_node[1])))
            
    down_node = (current_node[0], current_node[1]-1)
    isobstacle = obstacle_area[down_node[0],down_node[1]]
    if not isobstacle:
        isTrue = nodeOutOfBound(down_node)
        if not isTrue:
            if down_node not in visited_node:
                new_cost = cost + 1
                Queue.put((new_cost,(down_node[0], down_node[1], current_node[0], current_node[1])))
    
    down_left_node = (current_node[0]-1, current_node[1]-1)
    isobstacle = obstacle_area[down_left_node[0],down_left_node[1]]
    if not isobstacle:
        isTrue = nodeOutOfBound(down_left_node)
        if not isTrue:
            if down_left_node not in visited_node:
                new_cost = cost + 1.4
                Queue.put((new_cost,(down_left_node[0], down_left_node[1], current_node[0], current_node[1])))


def animate(current_node):
    x_node.append(current_node[0])
    y_node.append(current_node[1])
    plt.scatter(x_node, y_node)

takeStartInput()
start_node = tuple(start_node)
takeGoalInput()
goal_node = tuple(goal_node)

Queue.put((cost,([start_node[0],start_node[1],-1,-1])))

start = time.time()

while True:
    
    pop_node = Queue.get()
    current_node = (pop_node[1][0], pop_node[1][1])
    parent_node = (pop_node[1][2], pop_node[1][3])
    cost = pop_node[0]

    if current_node == goal_node:
        visited_node[current_node] = parent_node
        x_node.append(current_node[0])
        y_node.append(current_node[1])
        print('reached at goal node')
        break
    
    if (visited_node.get(current_node, False) == False):
        visited_node[current_node] = parent_node
        x_node.append(current_node[0])
        y_node.append(current_node[1])
        exploreNode(current_node,cost)
    i = i+1 


key_list = list(visited_node.keys())
value_list = list(visited_node.values())

optimal_path = []
x_path = []
y_path = []
while True:
    position = key_list.index(goal_node)
    value = value_list[position]
    if key_list[position]==start_node:
        optimal_path.append(key_list[position])
        x_path.append(key_list[position][0])
        y_path.append(key_list[position][1])
        break
    else:
        optimal_path.append(key_list[position])
        x_path.append(key_list[position][0])
        y_path.append(key_list[position][1])
        goal_node = value
    
x_plot = []
y_plot = []
i = 0

plt.axis([0,400, 0,250])
plt.scatter(X_obstacle,Y_obstacle, color='red', label='Obstacle', s=3)
plt.scatter(X_clearance,Y_clearance, color='yellow', label ='clearance',s=3)

while True:
    x_temp = x_node.pop(0)
    y_temp = y_node.pop(0)
    x_plot.append(x_temp)
    y_plot.append(y_temp)
    i = i+1
    if len(x_node) > 1000:
        if i > 1000:
            plt.scatter(x_plot, y_plot, color='black', s=3)
            plt.title("Exploring nodes for optimal path")
            plt.pause(0.005)
            i = 0
            x_plot *= 0
            y_plot *= 0
    elif len(x_node) > 100: 
        if i > 100:
            plt.scatter(x_plot, y_plot, color='black', s=3)
            plt.title("Exploring nodes for optimal path")
            plt.pause(0.005)
            i = 0
            x_plot *= 0
            y_plot *= 0
    elif len(x_node) > 10: 
        if i > 10:
            plt.scatter(x_plot, y_plot, color='black', s=3)
            plt.title("Exploring nodes for optimal path")
            plt.pause(0.005)
            i = 0
            x_plot *= 0
            y_plot *= 0
    else:
            plt.scatter(x_plot, y_plot, color='black', s=3)
            plt.title("Exploring nodes for optimal path")
            plt.pause(0.005)
            x_plot *= 0
            y_plot *= 0   
            
    if not x_node:
        break

plt.plot(x_path, y_path, c = 'green')
plt.title("Optimal path to travel form start node to goal node")
end = time.time()
print("time taken to run the code"+ " : " + str(end-start)+ " seconds ")       
plt.show()   




    
    


    

     












