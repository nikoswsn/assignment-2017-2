import sys
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-n", "--groups", help="number of groups to stop", type=int, default=2)
parser.add_argument("input_file", help="name of input file which describes the graph")
args = parser.parse_args()

table = {} #I use a dict as a 2D table each key ("row") has as value a list that has 4 values team of i, team of y, y, z (where y,z the pair)
teams = {} #I use a dict to store all the teams as lists
counter = 1; #This counter is used in order to store it's pair into a new key on dict "Table"
#Function to calculate a.
#Param: w is the team we want to calcA
#Param: table is the table that stores the pairs and their teams
def calcA(w, table):
	counter =0;
	for i in table:
		if (table.get(i)[0] == w and table.get(i)[1] == w):
			counter += 2
		elif (table.get(i)[0] == w or table.get(i)[1] == w):
			counter +=1
	A = counter / deliminator
	return A

#Function to update the table each time 2 teams are joined together
#Param: t is the team that got joined
#Param: nt is the new team 
#Param: table is the table that stores the pairs and their teams
def updTab(t,nt,table):
	for row in table:
		if table.get(row)[0] == t:
			table[row][0] = nt
		if table.get(row)[1] == t:
			table[row][1] = nt
	return None

#Let's parse the input file to get the pairs
with open(args.input_file) as f:
	for line in f:
		a,b= line.split()
		c,d = int(a),int(b)
		
		#Fill dictionary with the teams
		if c not in teams:
			teams[c]= [c]
		if d not in teams:
			teams[d]= [d]
			
		#Fill dictionary(table) which stores each pair including the team information
		table[counter] = [c , d , c, d]
		
		counter +=1
nteams = len(teams); #number of teams
deliminator = len(table) * 2; #number of links
#Let's count initial Q
Q = 0.0;
for n in teams:
	A = calcA(teams.get(n)[0], table)
	Q = Q + (0 - A * A)



while nteams > args.groups: #those steps repeat until we get to the needed amount of teams
	#Step 1: Calculate ΔQ of each pair
	DQmax = -1000000;
	imax,jmax, ymax, zmax,rowmax =0,0,0,0,0;
	for pair in table:
		if table.get(pair)[0] != table.get(pair)[1]:
			counter = 0;
			i,j,y,z = table.get(pair)[0],table.get(pair)[1], table.get(pair)[2],table.get(pair)[3]
			
			for row in table:
				if ((table.get(row)[0] == i and table.get(row)[1] == j) or (table.get(row)[0] == j and table.get(row)[1] == i)):
					counter += 1
			Eij = counter / deliminator
			Ai = calcA(i, table)
			Aj = calcA(j, table)
			DQ = 2*(Eij - (Ai *Aj))
			if DQmax < DQ: #We are interested for the DQ which is max
				DQmax = DQ
				imax, jmax,ymax, zmax, rowmax = i, j, y, z,pair
	Q +=DQmax #We add DQ which is max to the ld Q
	#We join the teams of the pairs with the max DQ
	updTab(imax,jmax,table) 
	teams[jmax] = teams[jmax] + teams.pop(imax)
	nteams -= 1 #One team less

#Requested Output
for keys in teams:
	print(sorted(teams.get(keys)))
print("Q= %.4f" % Q)