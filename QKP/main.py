from Functions import *

#Open the file with the instance´s name and optimal value, and assign ´the opened file´ to Instances_data
Instances_data=open("./Instances data.txt", "r")

#Open the file that will contain the results obtained, and assign that ´opened file´ to Results_file
Results_file=open("./Results.txt", "w")
#Erase the contents of Results_file, so we can overwrite its contents with the most recent results
Results_file.write("")
#Close the file
Results_file.close()

#Reopen the file, but now in ´append mode´, so we can just append each new result without overwriting any previous contents
Results_file=open("./Results.txt", "a")

i=0

#while (the next line read in the file with the instances´ data is not equal to "EOF", that stands for "End Of File")
while i<29:

    #IF ELSE that determines what line in the Instances_data file to assign to the Optimal and Instance_name variables,
    #in case that i (the iteration variable) is an even number, the first 
    Instance_name=Instances_data.readline().replace("\n", "")
    Optimal=Instances_data.readline().replace("\n", "")
    
    Path=""
    Path="./Instances/" + Instance_name + ".txt"
    
    #Append the results of the Instance processing in the Results_file file
    Results_file.write(f"{Calculate(Path,Optimal)} \n")
    i=i+1

Results_file=open("./Results.txt", "r")

i=0
lines=[]
numbers=[]
while i<29:
    lines.append(Results_file.readline().replace("\n", ""))
    i=i+1

def quicksort_percentages_sm_to_bggst(Linen):
    if len(Linen) <= 1:
        return Linen

    pivot_idx = len(Linen) // 2 # Choose pivot as the middle element
    pivot = float(Linen[pivot_idx].split(",")[4])

    smaller=[quantity for quantity in Linen if float(quantity.split(",")[4]) < pivot]
    equal=[quantity for quantity in Linen if float(quantity.split(",")[4]) == pivot]
    bigger=[quantity for quantity in Linen if float(quantity.split(",")[4]) > pivot]

    return quicksort_percentages_sm_to_bggst(smaller) + equal + quicksort_percentages_sm_to_bggst(bigger)

lines=list(quicksort_percentages_sm_to_bggst(lines))

for i in range(len(lines)):
    print(lines[i].split(",")[4])

Results_file.close()

Results_file=open("./Results.txt", "w")

for i in range(len(lines)):
    Results_file.write(f"{lines[i]}\n")

Results_file.close()