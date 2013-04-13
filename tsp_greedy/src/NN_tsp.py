#!/usr/local/bin/python

#Traveling Salesman Solution using NearestNeighbor Algorithm
#Scott Stevenson, Jack Koppenaal, John Costantino

import time, itertools, math, exceptions

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

def num(s):
	try:
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
				city = [num(parts[0]), num(parts[1]), num(parts[2].strip('\n')), False]
				cities.append(city)
		except Exception as e:
			#The ident was not an int so we skip (pass) it and move on to the next
			pass

#A function to calculate the nearest neighbor of an abitrary node
def getNearestNeighbor(i):
	#Start at infinity
	nearest = [-1, float("inf")]

	#print '\n cities:' + str(cities)
	for index in range(len(cities)):
		#Skip if looking at itself or looking at a visited node
		if i == index or cities[index][3] == True:
			pass
		#Otherwise calculate distance and update nearest if necessary
		else:
			distance = getDistance(cities[i], cities[index])
			#print nearest
			if distance < nearest[1]:
				nearest = [index, distance]

	#Set nearest to visited and return
	cities[nearest[0]][3] = True
	return nearest

#A function to calculate the 'best' TSP tour on a given set of vertexes
def nearestNeighbor(cities):
	data = []
	tour = [[],0]
	first = getNearestNeighbor(0)
	data.append(first)
	next = first
	#Get the nearest neighbor and weight for every vertex and append to the list
	for index in range(1,len(cities)):
		cur = getNearestNeighbor(next[0])
		data.append(cur)
		next = cur

	#Once we have the path and weight, split into 2 arrays for ease of use
	for element in data:
		tour[1] += element[1]
		tour[0].append(element[0])
	#Account for weight of last node -> first node to complete the cycle
	tour[1] += getDistance(cities[tour[0][-1]],cities[tour[0][0]])
	#Return the tour
	return tour

#A function to write the output of a tour to a file in a specified format
def toFile(tour):
    loc = raw_input('Enter the location where you would like to save the tour:\n') 
    fname = cityFile.name
    #Index for the last file separator to get ONLY the file name not its path
    sep_index = 0
    #Linux/OSX files use /'s to separate dirs so get the position of the last one in the name
    if '/' in fname:
        sep_index = fname.rindex('/')+1
    #Windows files use \'s to separate dirs so get the position of the last one in the name
    if '\\' in fname:
        sep_index = fname.rindex('\\')+1
    #Create the header for the output file
    header = ('NAME : ' + str(fname[sep_index:-4]) + '.opt.tour\n'
          'COMMENT : Optimal tour for ' + str(fname[sep_index:]) + ' (' + str(tour[1]) + ')\n'
          'TYPE : Tour\n'
          'DIMENSON : ' + str(len(tour[0])) + '\n'
          'TOUR_SECTION\n')
    #Create the trailer for the output file
    trailer = "-1\nEOF\n"
    #Create the output file and write the results to it
    try:
        f = open(loc,'w')
        f.write(header)
        for city in tour[0]:
            f.write(str(city) + '\n')
        f.write(trailer)
        f.close()
        print 'Successfully saved tour data to: ' + loc
    except Exception as e:
        print loc + ' could not be written to: ' + str(e) 

#-------------------The actual script begins here-----------------------
cities = []
cityFile = getFile()
getCities(cityFile)
#Start the stopwatch
start = time.time()
opt_tour = nearestNeighbor(cities)
#Stop the stopwatch
finish = time.time()
print 'The optimum tour is: %s (%f)' % (opt_tour[0], opt_tour[1])
print 'There are %d cities in this tour.' % (len(opt_tour[0]))
print 'This solution took %0.3f seconds to calculate.' % (finish-start)
toFile(opt_tour)
