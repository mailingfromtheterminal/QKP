from random import *
import os
import time
from Functions import *
class ij:
#Class that represents the data of every item's quadratic index
   j=0 #Index of item 'j', to which the current item points
   value=0 #the actual quadratic profit
class Item:
  c_i=0 #Linear coefficient
  c_ij=[] #Quadratic coefficients
  ev_func=0 #not included in the mathematical model
  weight=0
  packed=0 #packed=1 if the item will be inside the knapsack
  index=0 #Item's index
def calc_ev_func(List_of_Items, index): #TEST PENDING
    #Function to calculate the evaluation function of a given item in the list
    quadratic_index=0 #Variable that helps us make the code more readable, as you will see 5 statements below (not considering the comments)
    c_ijs_quantity=len(List_of_Items[index].c_ij)
    List_of_Items[index].ev_func=0 #Initialize the value of the item's evaluation function as 0, to avoid miscalculations

    if not c_ijs_quantity==0:
        for k in range(c_ijs_quantity): #For every quadratic profit the item has
            quadratic_index=List_of_Items[index].c_ij[k].j #Set the value of 'quadratic_index' to the 'j' coordinate of the current quadratic profit
            if List_of_Items[quadratic_index].packed==1: #If the j'th item is packed
                #do
                #Add to the index'th item's evaluation function, the individual profit of the j'th item
                List_of_Items[index].ev_func=List_of_Items[index].ev_func+List_of_Items[index].c_ij[k].value
                #end
        
        #Get the average of the current value of the index'th item's evaluation function, dividing that by c_ijs_quantity
        List_of_Items[index].ev_func=List_of_Items[index].ev_func/c_ijs_quantity #That'll be the average of the item's quadratic coefficients

    List_of_Items[index].ev_func=List_of_Items[index].ev_func+List_of_Items[index].c_i #Add to the item's evaluation function, it's individual profit
def heuristic(Items1, Knapsack_capacity):
    
    List_of_Items1=list(Items1) #Copy the main Items list, to modify just the copy
    Capacity_verif=Knapsack_capacity # Variable that will be used to control the consumption of the knapsack's capacity, it's maximum value will be the full
                                     # knapsack's capacity, and it's minimum value, 0

    greatest_ev_func=0 #Variable that will be used to register the current greatest evaluation function value found in the list of items 
    index_of_greatest_ev_func=0 # Variable that will be used to register the index of the item with the current greatest evaluation
                                # function value found in the list

    List_of_Items1_size=len(List_of_Items1) # Variable that will store the size of the item's list (as a number representing the amount of items in the list),
                                          # so that this quantity doesn't have to be calculated every time it is needed

    for O in range(List_of_Items1_size): #For every item in the list
            
        #For every UNPACKED item in the list: calculate it's evaluation function
        for i in range(List_of_Items1_size):
            if List_of_Items1[i].packed==0:
                calc_ev_func(List_of_Items1, i)
                
        i=0 #'i' is the iteration variable that will be used in the following while loop
        #The following while loop's purpose is to find the UNPACKED item with the greatest evaluation function value
        while i<List_of_Items1_size: #while the list is not items is still not entirely traversed
            if List_of_Items1[i].packed==0 and (Capacity_verif-List_of_Items1[i].weight)>=0: #IF the current item is unpacked AND fits in terms of weight
                if not greatest_ev_func==0:
                    if ((List_of_Items1[i].ev_func>greatest_ev_func\
                    or (List_of_Items1[i].ev_func==greatest_ev_func\
                        and List_of_Items1[i].weight<List_of_Items1[index_of_greatest_ev_func].weight))):
                    # IF a greatest_ev_func was found
                    #   AND (The current item's evaluation function is bigger than the current biggest evaluation function
                    #       OR (The current item's evaluation function is equal to the current biggest evaluation function
                    #           AND the current item's weight is smaller than the weight of the item with the current greatest evaluation function value))
                        index_of_greatest_ev_func=i
                        greatest_ev_func=List_of_Items1[i].ev_func
                else: #Execute the following 2 statements only if greatest_ev_func==0
                    index_of_greatest_ev_func=i
                    greatest_ev_func=List_of_Items1[i].ev_func
            i=i+1
        
        if not greatest_ev_func==0: #IF greatest_ev_func's value is not equal to 0 (which means that the item with the greatest evaluation function value was found)
            List_of_Items1[index_of_greatest_ev_func].packed=1 # Mark the found element as packed
            Capacity_verif=Capacity_verif-List_of_Items1[index_of_greatest_ev_func].weight #Update the Capacity_verif variable
        else: #IF no unpacked item with the greatest evaluation function was found
            break #THEN quit the 'for' loop, because we can't pack any more items in the knapsack
                
        # Update greatest_ev_func and index_of_greatest_ev_func to avoid miscalculations, etc.
        greatest_ev_func=0
        index_of_greatest_ev_func=0

    return List_of_Items1 # Return the list of items with the found solution
def local_search_first_improvement(S, Knapsack_capacity):
    # local_search_first_improvement does not modify the list given in the argument

    #S is the 'old' solution list of items, the packed ones are flagged, from that: Calculate the profil that it'll return and store it in f_S:
    f_S=calculate_profit_given_packed_items(S)
    # Knapsack_capacity is the variable that contains the number that represents the knapsack's total weight capacity
        # Because we will work with the 'S' solution, we must keep a register of the weight already used with that solution,
        # and with that quantity, calculate the knapsack's remaining capacity and store it in Capacity_verif:
    Capacity_verif=Knapsack_capacity-weight_consumed(S)
    #Initialize the new solution S_ap as an empty list:
    S_ap=[]
    #Then, to make the necessary movements to the original solution, it'll be copied to S_ap:
    S_ap=list(S)

    S_ap_size=len(S_ap) # Variable that will store the size of the item's list S_ap (as a number representing the amount of items in the list),
                        # so that this quantity doesn't have to be calculated every time it is needed

    #f_S_ap is the profit that S_ap would return
    f_S_ap=0

    # excluded_items is a list of indexes 'pointing' to those items that were removed from S (well, S_ap),
    # but that when where removed, the found solution was not better that the older one
    excluded_items=[]
    
    # greatest_weight is the variable that will help to store the current greatest_weight value found some statements later
    greatest_weight=0
    # index_of_greatest_weight is the variable that will help to store the item's index of the current greatest_weight value found
    index_of_greatest_weight=0

    # greatest_ev_func is the variable that will help to store the current greatest_ev_func value found some statements later
    greatest_ev_func=0
    # index_of_greatest_ev_func is the variable that will help to store the item's index of the current greatest_ev_func value found
    index_of_greatest_ev_func=0

    i=0 # 'i' is the iteration variable for the following 'while' loop
    while i<S_ap_size:
        # Find the heaviest PACKED item and remove it from the knapsack, when doing so, keep a record of the item's index and weight value, so that it can be accessed later if necessary
        j=0 #'j' is the iteration variable that will be used in the following while loop
        while j<S_ap_size: #While S_ap is not yet fully traversed
            greatest_weight=0
            if not A_belongs_to_B(j, excluded_items) and (S_ap[j].packed==1): #IF the current item is not an excluded one AND it is packed in S_ap
                if not greatest_weight==0:
                    if (S_ap[j].weight>greatest_weight\
                        or (S_ap[j].weight==greatest_weight\
                            and S_ap[j].ev_func<S_ap[index_of_greatest_weight].ev_func)):
                    # IF the current item's weight is greater than the current greatest weight found
                        # OR (The current item's weight is the same as the current greatest weight found
                        #     AND The current item's ev_func is smaller than the ev_func of the item with the current greatest weight found)
                        #       [because, if 2 or more items with the same weight are found, it is logical to unpack the one with the smallest
                        #        ev_func]
                        greatest_weight=S_ap[j].weight
                        index_of_greatest_weight=j
                else:
                    greatest_weight=S_ap[j].weight
                    index_of_greatest_weight=j
            j=j+1
        if not greatest_weight==0: #IF a greatest_weight value was found
            S_ap[index_of_greatest_weight].packed=0 # Flag the selected item as unpacked
            #Update Capacity_verif, adding to it the weight of the unpacked item, because it's weight is now 'available' to occupy in the knapsack
            Capacity_verif=Capacity_verif+S_ap[index_of_greatest_weight].weight
        
        items_fit=1 #Variable that indicates if more items fit into the knapsack
        while items_fit==1:
            # Calculate the ev_func of every unpacked item in S_ap
            for k in range(S_ap_size):
                if S_ap[k].packed==0:
                    calc_ev_func(S_ap, k)
            #Try to find the best (in terms of its ev_func) unpacked and fitting item
            m=0
            while m<S_ap_size: #While S_ap is not entirely traversed
                if S_ap[m].packed==0 and (Capacity_verif-S_ap[m].weight)>=0: #IF the current item is unpacked and fits:
                    if not greatest_ev_func==0: #IF a value of greatest_ev_func has been found previously:
                        if S_ap[m].ev_func>greatest_ev_func\
                            or (S_ap[m].ev_func==greatest_ev_func\
                                and S_ap[m].weight<S_ap[index_of_greatest_ev_func].weight):
                        #IF the current item's ev_func is greater than greatest_ev_func
                            #OR ((the current item's ev_func is equal to greatest_ev_func)
                                # AND (the current item is lighter than the one previously flagged with the same greatest_ev_func value)):
                            greatest_ev_func=S_ap[m].ev_func
                            index_of_greatest_ev_func=m
                    else: #Execute the following 2 statements only if greatest_ev_func==0
                        greatest_ev_func=S_ap[m].ev_func
                        index_of_greatest_ev_func=m
                m=m+1
            if not greatest_ev_func==0: #IF a valid item is found:
                S_ap[index_of_greatest_ev_func].packed=1 #Flag the item as packed
                Capacity_verif=Capacity_verif-S_ap[index_of_greatest_ev_func].weight #Update Capacity_verif
                #Update greatest_ev_func and index_of_greatest_ev_func
                greatest_ev_func=0
                index_of_greatest_ev_func=0
            else: #if no other item fits:
                items_fit=0 #exit the 'while True' loop
        
        f_S_ap=calculate_profit_given_packed_items(S_ap)

        if f_S_ap>=f_S: #IF S_ap is better than S:
            return S_ap
        else:
            #Add the index of the removed (from S_ap) item to the excluded_items list
            excluded_items.append(index_of_greatest_weight)
            #Set the value of S_ap to S (S_ap=S), because if the solution didn't get better with the movement applied, it won't get better later (as far as I know)
            S_ap=S
        i=i+1

    return S_ap
def A_belongs_to_B(Num, List_of_Num):
#Function to determine if a number belongs to a list of numbers
    for i in range(len(List_of_Num)):
        if Num==List_of_Num[i]:
            return True #Return True if the number was found in the list
    return False #Return False if the number was found in the list
def weight_consumed(List_of_Items):
#Function to know how much weight (of the knapsack's capacity) is consumed by a given solution
    weight_used=0
    for i in range(len(List_of_Items)):
        if List_of_Items[i].packed==1:
            weight_used=weight_used+List_of_Items[i].weight
    return weight_used
def calculate_profit_given_packed_items(List_of_Items):
#Function to calculate tha profit that a given solution (in form of a list of items) would return if chosen
    Profit=0 #Initialize the profit 'accumulator'
    for i in range(len(List_of_Items)): #for every item in the list
        if List_of_Items[i].packed==1: #IF the current item is packed
            Profit=Profit+List_of_Items[i].c_i #Add to 'Profit' the individual profit of the current item
            for j in range(len(List_of_Items[i].c_ij)): #for every current item's quadratic coefficient
                if List_of_Items[List_of_Items[i].c_ij[j].j].packed==1: #If the item of index [(...).c_ij.j]  is packed
                    Profit=Profit+List_of_Items[i].c_ij[j].value #Add it's quadratic profit to the Profit 'accumulator'
    return Profit
def Instance_reader(file_name):
    n=0 #Variable that will store the number of elements in the list of items, directly from the instance file
    Items = [] #List of type 'Item' items, each one of those representing an item from the instance
    Knapsack_capacity=0 #Knapsack's weight capacity
    weights=0 #A list of weights directly read from the instance's file
    
    f=open(file_name, "r") #Open the file that it's name (or path) is as the file_name string
    
    f.readline() #Skip the file name

    n=int(f.readline())

    #Assignment of the linear coefficients to a list:
    c_is=f.readline().split()

    for i in range(n): #For every item
        Items.append(Item()) #Add one more type 'Item' items to the 'Items' list

        #Assignment of the values of the list to each item's linear coefficient
        Items[len(Items)-1].index=i
        Items[len(Items)-1].c_i=int(c_is[i]) #The [len(Items)-1] index is equal to the index of the last element in the 'Items' list
                                             #For example: If the 'Items' list has 4 elements, the indexes would be:
                                             # { [0], [1], [2], [3] }; len(Items)=4, (len(Items)-1)=3
                                             #The values that (len(Items)-1) adopts throughout this loop's iterations are (in order):
                                             # 0, 1, 2, 3, 4, 5, 6, 7, 8 and 9
                                             #So, if the items were already in the 'Items' list, this could be done also, and the result would be the same:
                                             #for i in range(n):
                                             #  Items[i].c_i=int(c_is[i])
                                             #  Items[i].index=i

    for i in range(n-1): #For every item (except the last one, because it has no quadratic coefficients)
        #Assignment of the quadratic coefficients to a list, per iteration
        c_ijs=f.readline().split()

        Items[i].c_ij=[] #Initialize the current item's c_ij list as an empty list

        for j in range(len(c_ijs)): #For every quadratic coefficient in the current item
            Items[i].c_ij.append(ij())
        
        for j in range(len(Items[i].c_ij)):
            #Assignment of the values of the list to each item of the quadratic coefficients list in each item   
            Items[i].c_ij[j].value=int(c_ijs[j])
            #'Coordinates' of each quadratic coefficient in the list, this is for convenience at the time of evaluating the total profit
            #Items[i].c_ij[j].i=i #Coordinate 'i' is not useful now: DEPRECATED
            Items[i].c_ij[j].j=j+i+1

        #print(f"Items[{(n-1)-i}].c_ij: {Items[(n-1)-i].c_ij}")

    f.readline() #Skip the space

    f.readline() #Skip the number that represents the constraint type, because it'll not be used in this program
    Knapsack_capacity=int(f.readline())

    #Assignment of the weights of the items to a list
    weights=f.readline().split()
    for i in range(n):
        #Assignment of each item in the list to each item's weight
        Items[i].weight=int(weights[i])
   
    f.close()
    
    results= []
    results.append(n) #results[0]= n
    results.append(Items) #results[1]= Items
    results.append(Knapsack_capacity) #results[2]= Knapsack_capacity
    
    return results
def is_solution_feasible(List_of_Items, Knap_capacity):
    accumulated_weight=0
    
    accumulated_weight=weight_consumed(List_of_Items) #Get the weight that the solution consumed from the knapsack's capacity
    
    if accumulated_weight<=Knap_capacity: #SELF EXPLANATORY
        return 1
    
#IF the solution is not feasible:
    return 0
def quicksort_by_attribute(List_of_Items, attribute):
    if len(List_of_Items) <= 1:
        return List_of_Items

    pivot_idx = len(List_of_Items) // 2 # Choose pivot as the middle element
    pivot = getattr(List_of_Items[pivot_idx], attribute)
 
    # Partition the list into two sublists
    smaller = [obj for obj in List_of_Items if getattr(obj, attribute) < pivot]
    equal = [obj for obj in List_of_Items if getattr(obj, attribute) == pivot]
    greater = [obj for obj in List_of_Items if getattr(obj, attribute) > pivot]
    
    if attribute=="ev_func":
        return quicksort_by_attribute(greater, attribute) + equal + quicksort_by_attribute(smaller, attribute)
    if attribute=="weight":
        return quicksort_by_attribute(smaller, attribute) + equal + quicksort_by_attribute(greater, attribute)
    if attribute=="index":
        return quicksort_by_attribute(smaller, attribute) + equal + quicksort_by_attribute(greater, attribute)
def print_Items(List_of_Items):
    packed=[]
    print("List_of_Items, quad and linear coeffs.:\n")
    List_of_Items_size=len(List_of_Items) #Variable that will be used to not calculate the length of the list of items every time that data is necessary
    print(f"     ", end="")
    for i in range(List_of_Items_size): #For every item in the list
        if List_of_Items[i].packed==1:
            packed.append(i)
        print(f"{i:4d}", end="") #Print the item's index
    print()
    for i in range(List_of_Items_size): #For every item on the list
        print(f"{i:4d} ", end="") #Print the item's index, then
        for j in range(List_of_Items_size-len(List_of_Items[i].c_ij)-1): #For every quadratic coefficient that the item does not have
            print("----", end="")                                        #(because it is or they are already in other item's collection of quadratic coefficients)            
        print(f"{List_of_Items[i].c_i:4d}", end="") #Print the item's individual profit
        for j in range(len(List_of_Items[i].c_ij)): #For every quadratic coefficient the item has
            print(f"{List_of_Items[i].c_ij[j].value:4d}", end="") #Print the i'th item's j'th quadratic coefficient
        print()
    print(f"Packed items => {packed}")
def Randomized_Constructive_Heuristic(Items2, Knapsack_capacity):
    seed(time.time()) #Function to make sure that the random numbers generated are really random
    List_of_Items2=[]
    List_of_Items2=list(Items2) #List of Items that will be manipulated, not the original one
    List_of_Items2_size=len(List_of_Items2)
    Capacity_verif=Knapsack_capacity #Variable that helps to control the knapsack's weight occupied
    k=3 #Determine 'k', it is the number of 'k' best selected items from the List of items used in this function
    k_best=[]
    greatest_ev_func=0
    index_of_greatest_ev_func=0
    random_index=0
    while not greatest_ev_func==-1:
        k_best=[]
        i=0
        for i in range(k):
            j=0
            for j in range(List_of_Items2_size):
                if List_of_Items2[j].packed==0 and (not A_belongs_to_B(j, k_best)) and (Capacity_verif-List_of_Items2[j].weight)>=0: #If the current item in fitting and unpacked and it not belongs to k_best
                    calc_ev_func(List_of_Items2, j) #Calculate the ev_func of unpacked items
                    if not greatest_ev_func==0: #If a greatest_ev_func has been found previously
                        if List_of_Items2[j].ev_func>greatest_ev_func\
                            or (List_of_Items2[j].ev_func==greatest_ev_func\
                                and List_of_Items2[j].weight<List_of_Items2[index_of_greatest_ev_func].weight):
                        # IF the current item has the greatest ev_func yet
                            # OR (it has the same as greatest_ev_func
                                # AND is lighter than the item with index index_of_greatest_ev_func):
                            greatest_ev_func=List_of_Items2[j].ev_func
                            index_of_greatest_ev_func=j
                    else:
                        greatest_ev_func=List_of_Items2[j].ev_func
                        index_of_greatest_ev_func=j
                j=j+1            
            if not greatest_ev_func==0: #IF some unpacked and fitting item was found
                k_best.append(index_of_greatest_ev_func) #Append index_of_greatest_ev_func to 'k_best'
            else:
                break
            i=i+1
        if not greatest_ev_func==0:
            k=len(k_best)-1 #Do this for the case when 'k' items cannot be appended to k_best
            random_index=k_best[randint(0, k)]
            List_of_Items2[random_index].packed=1 #Flag the item with index rand(0,k) as packed
            Capacity_verif=Capacity_verif-List_of_Items2[random_index].weight #Update the Capacity verif variable with the packed item's weight
            
            greatest_ev_func=0
        else:
            greatest_ev_func=-1
    return List_of_Items2
def Calculate(Instance_Path, optimal):
#Function to implement the instance reader, heuristic application functions and returning the results to the main.py file's execution
#Instance_Path is a string containing what it's name describes: The path to the instance to work with
#optimal is a number, that represents the optimal solution to which the solution obtained will be compared

    #Variable that will store the number of elements in the instance that will be read
    n=0
    #List that will store a type Item object, per item in the knapsack
    Items = []
    #Variable that will store the Knapsack weight capacity
    Knapsack_capacity=0
    #List that will store the weight of each item, each element will be assigned to it's respective item, and the list will be not used then
    weights=[]
    #Variable that will store the time that it takes to compute the solution of the processed instance
    COMPUTING_TIME=0

    if os.path.exists(Instance_Path)==False:
    #if file does not exist or argument is not included
        #Let the user know that the file does not exist or argument is not included
        print(f"File does not exist")
    else:
    #else

        #Set Computing_Time=0
        COMPUTING_TIME=0
        
        #Set list of values to an empty list, this list will contain the read instance data
        values=[]
        
        #sys.argv[0] is the argument given when calling the program Solver.py from the console:
        #the name of the file is Instance_Path
        #python Solver.py [file_name]

        #Read the instance and save it in the 'values' list
        values = Instance_reader(Instance_Path)
        
        #Assignment of the different elements in the 'values' list in 'n', the 'items' list and 'Knapsack_capacity'
        #
        n=values[0]
        Items=values[1]
        Knapsack_capacity=values[2]
        
        #----------------------------------------------APPLYING A HEURISTIC------------------------------------------------------
            
        start_time = time.time() #TIME COUNT STARTS

        #S is the list with the solution obtained with the constructive heuristic
        S=heuristic(Items, Knapsack_capacity)
        #f_S is the profit obtained with the S solution
        f_S=calculate_profit_given_packed_items(S)

        i=0
        #while (fixed number of iterations is not reached)
        while i<10:
            S_ap=[] #S_ap = S'
            S_ast=[] #S_ast = S*

            #S_ap is the list containing the solution obtained with the randomized constructive heuristic
            S_ap=Randomized_Constructive_Heuristic(Items, Knapsack_capacity-weight_consumed(Items))
            #S_ast is the list containing the solution obtained after applying the local search to S_ap
            S_ast=local_search_first_improvement(S_ap, Knapsack_capacity-weight_consumed(Items))
            
            #f_S_ap is the profit obtained with the S_ap solution
            f_S_ap=calculate_profit_given_packed_items(S_ap)
            #f_S_ast is the profit obtained with the f_S_ast solution
            f_S_ast=calculate_profit_given_packed_items(S_ast)
            if not f_S==f_S_ap:
                print(f"f_S: {f_S}, f_S_ap: {f_S_ap}, item {Instance_Path.split("/")[2].split(".")[0]}")
            if not f_S_ap==f_S_ast:
                print(f"f_S_ap: {f_S_ap}, f_S_ast: {f_S_ast}, item {Instance_Path.split("/")[2].split(".")[0]}")
            if f_S_ast>f_S:
                S=S_ast
                f_S=f_S_ast
            i=i+1

        COMPUTING_TIME=time.time()-start_time
        #Stop time counting and store it in the COMPUTING_TIME variable

        if is_solution_feasible(S, Knapsack_capacity):
        #IF solution S is feasible
            Profit=f_S
            Optimal=int(optimal)          
            Instance_Name=""
            Instance_Name=Instance_Path.split("/")[2].split(".")[0]
            results=""
            results=f"{Instance_Name},{Profit},{COMPUTING_TIME},{Optimal},{100-(Profit*100)/Optimal:.4f}"
            return results