#!/usr/local/bin/python

#Traveling Salesman Solution
#Scott Stevenson, Jack Koppenaal, John Costantino

import time, itertools, math

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

#Get the cities from a specified city file
def getCities(cityFile):
	for line in cityFile:
		try:
			#Lines split by a space char will look like:
			#[ident, x-coord, y-coord]
			ident = line.split(' ')[0]
			x = line.split(' ')[1]
			y = line.split(' ')[2].strip('\n')
			#If the ident is not an int (not a city) skip it otherwise add it	
			if ident.isdigit():
				#Cities are just lists with values (almost a pseudo-class)
				city = [int(ident), int(x), int(y)]
				cities.append(city)
		except:
			#The ident was not an int so we skip (pass) it and move on to the next
			pass

#A function for bruteforcing the TSP problem based on a list of cities
def bruteForce(cities):
	#Tours are also stored as pseudo-class lists
	#tour[0] is the path and tour[1] is the weight

	#Make a start tour with a weight of infinity so all other tours will be smaller
	tour = [[], float("inf")]
	permparm = []
	#In order to get all permutations we need an array containing the values 1 through n
	#These values are the idents of the cities (their 0th element) so we get and add them
	for city in cities:
		permparm.append(city[0])

	#We now generate all permutations of n length from the array containing 1 - n idents
	#and loop through them looking for the smallest distance
	for perm in list(itertools.permutations(permparm, len(permparm))):
		#Get the total weight of the permutation
		dist = getWeight(perm)
		#Make a new tour to represent the current permutation
		thisTour = [perm, dist]
		#If the current tour is shorter than the old tour, point the old tour to the new one
		if thisTour[1] < tour[1]:
			tour = thisTour
	#Once we have gone through every permutation we have the shortest tour so return it
	return tour

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
#Start the stopwatch
start = time.time()
getCities(cityFile)
opt_tour = bruteForce(cities)
#Stop the stopwatch
finish = time.time()
print 'The optimum tour is: %s (%f)' % (opt_tour[0], opt_tour[1])
print 'This solution took %0.3f seconds to calculate.' % (finish-start)
toFile(opt_tour)
