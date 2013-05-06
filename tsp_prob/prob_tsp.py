#!/usr/local/bin/python

#Traveling Salesman Solution using 2-opt Algorithm
#Scott Stevenson, Jack Koppenaal, John Costantino

import time, itertools, math, exceptions, random
from optparse import OptionParser

#Get the city file
def getFile():
	cityFile = raw_input('Enter the location of your city file:\n')
	try:
		f = open(cityFile)
		return f
	except Exception as e:
		print cityFile + ' could not be opened: ' + str(e)

#Get distance between 2 cities
#Cities stored as [ident, x, y]
def getDistance(city1, city2):
	return 	math.sqrt((int(city2[1]) - int(city1[1]))**2 + (int(city2[2])-int(city1[2]))**2)

#A function to get the total weight of a path
#This function is messy because of an off-by-1 error introduced by the tour file starting at 1 instead of 0
def getWeight(perm):
	#Set the initial distance to 0
	dist = 0
	#We now need to calculate and add the distance between each city in the path from 0 to n
	for index in range(len(perm)):
		try:
			#Pass the 2 cities to the distance formula and add the value to dist
			dist += getDistance(cities[perm[index]-1], cities[perm[index+1]-1])
		except:
			#We don't need to check bounds because the final pass will throw an out-of-bounds
			#exception so we just catch it and skip that calculation
			pass
	#All TSP solutions are cycles so we now have to add the final city back to the initial city to the total dist
	#Python has a nifty convention where list[-1] will return the last element, list[-2] will return second to last, etc.
	dist += getDistance(cities[perm[-1]-1], cities[perm[0]-1])
	#We now have the total distance so return it
	return dist

#Function to work with both float and int inputs
def num(s):
	try:
		#If there is an error it is due to precision loss
		return int(s)
	except exceptions.ValueError:
		return float(s)

#Get the cities from a specified city file
def getCities(cityFile):
	for line in cityFile:
		try:
			#Lines split by white space will look like:
			#[ident, x-coord, y-coord]
			parts = line.split()
			if parts[0].isdigit():
				#Cities are just lists with values (almost a pseudo-class)
				#city = [num(ident), num(x), num(y), False]
				city = [num(parts[0]), num(parts[1]), num(parts[2].strip('\n'))]
				cities.append(city)
		except Exception as e:
			#The ident was not an int so we skip (pass) it and move on to the next
			print "exception adding city"

#Calculate the 'best' tour for a set of cities using 2-opt
def two_opt(cities, numrounds, numiters):
	#Initialize the total weight to be averaged to 0
	results = 0
	#Create the initial 1...N permutation and find its weight
	curbest = [[], None]
	for city in cities:
		curbest[0].append(city[0])
	curbest[1] = getWeight(curbest[0])
	#Create the 'next' tour
	#[:] makes a copy of the array in curbest[0]
	next = [curbest[0][:], curbest[1]]

  	for x in range(0, numrounds):
  		for x in range(0, numiters):
  			#Pick 2 random edges
  			num1 = random.randint(0, len(cities)-1)
  			num2 = (num1 + random.randint(0, len(cities)-2))%len(cities)
  			#Swap the edges and get the new weight
  			next[0][num1], next[0][num2] = next[0][num2], next[0][num1]
  			next[1] = getWeight(next[0])
  			#If the new tour is better than the old tour, set new tour as current best
  			if next[1] < curbest[1]:
  				curbest = next
  		#Add the current best weight to results after each round
  		results += curbest[1]
  	#Return an arbitrary path and the average of all of the results of the rounds
  	return [curbest[0], results/numrounds]

#-------------------The actual script begins here-----------------------
#Add command line option parsing
#Rounds and Iters are not required - defaults will be used if needed
parser = OptionParser()
parser.add_option("-r", "--rounds", dest = "rounds",
					help = "The desired number of rounds.")
parser.add_option("-i", "--iters", dest = "iters",
					help = "The desired number of iterations (per round).")
(options, args) = parser.parse_args()

cities = []
cityFile = getFile()
getCities(cityFile)

#Set the default values for rounds and iters
rounds = 2
iters = (len(cities)**3)/16
#If the user provides values, use them
if (options.rounds != None):
	rounds = num(options.rounds)
if (options.iters != None):
	iters = num(options.iters)

#Start the stopwatch
start = time.time()
opt_tour = two_opt(cities, rounds, iters)
#Stop the stopwatch
finish = time.time()
print 'The optimum tour is: %s (%f)' % (opt_tour[0], opt_tour[1])
print 'There are %d cities in this tour.' % (len(opt_tour[0]))
print 'This solution took %0.3f seconds to calculate.' % (finish-start)
