#!/usr/local/bin/python

#Traveling Salesman Solution using NearestNeighbor Algorithm
#Scott Stevenson, Jack Koppenaal, John Costantino

import time, itertools, math, exceptions, random

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
		return int(s)
	except exceptions.ValueError:
		return float(s)

#Get the cities from a specified city file
#def getCities(cityFile):
#	for line in cityFile:
#		try:
#			#Lines split by a space char will look like:
#			#[ident, x-coord, y-coord]
#			ident = line.split(' ')[0]
#			x = line.split(' ')[1]
#			y = line.split(' ')[2].strip('\n')
#			#If the ident is not an int (not a city) skip it otherwise add it	
#			if ident.isdigit():
#				#Cities are just lists with values (almost a pseudo-class)
#				city = [num(ident), num(x), num(y)]
#				cities.append(city)
#		except:
#			#The ident was not an int so we skip (pass) it and move on to the next
#			print "exception adding city"

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

def two_opt(cities):
	curbest = [[], float("inf")]
	for city in cities:
		curbest[0].append(city[0])
	curbest[1] = getWeight(curbest[0])
	next = [curbest[0][:], None]

  	for x in range(0,1):
  		for x in range(0,(len(cities)**3)/16):
  			#next = curbest
  			num1 = random.randint(0, len(cities)-1)
  			num2 = (num1 + random.randint(0, len(cities)-2))%len(cities)
  			#Swap
  			next[0][num1], next[0][num2] = next[0][num2], next[0][num1]
  			next[1] = getWeight(next[0])
  			print "curbest:"
  			print curbest[1]
  			print "next after:"
  			print next[1]
  			if next[1] < curbest[1]:
  				curbest = next
  	return curbest



#-------------------The actual script begins here-----------------------
cities = []
cityFile = getFile()
getCities(cityFile)
#Start the stopwatch
start = time.time()
opt_tour = two_opt(cities)
#Stop the stopwatch
finish = time.time()
print 'The optimum tour is: %s (%f)' % (opt_tour[0], opt_tour[1])
print 'There are %d cities in this tour.' % (len(opt_tour[0]))
print 'This solution took %0.3f seconds to calculate.' % (finish-start)
