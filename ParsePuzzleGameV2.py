#!/usr/bin/python2.7 -tt
#coding: ascii

import csv
import sys
import numpy

'''
import the .csv file containing the output of the entry associated with the swapGameMapList
the argument to this script is the name of the .csv file to be parsed
'''

gameListFile = open(sys.argv[1], 'rb')

'''
the first value in each line is game difficulty, the second value in each line is the 
numTurnsTaken (off by 1 as this is stored in the database as the number of board maps whilst
turns are transitions between board maps), the third value in each line is the swapGameMapList 
- this contains information mapping coordinates to speciesIDs.
'''

#create a list of all the game's played (unparsed within line)
gamePlayedDataList = list(csv.reader(gameListFile))

#iterate through each of the games played in the list
for gamePlayedData in gamePlayedDataList:
	print "==================================="
	print "========== GAME ANALYSIS =========="
	print "==================================="	
	#extract level difficulty
	data = [i.split(',')[0] for i in gamePlayedData]
	levelDiff = data[0]
	print "Difficulty Level Is: ", levelDiff 

	#and extract the number of turns taken
	numTurns = (data[1] - 1)
	print "Num Turns Taken: ", numTurns

	#calculate the minimum number of turns needed to solve the puzzle based on the starting map
	
	#start by cleaning the initBoardMap string
	initBoardMap = data[2]
	#print "Initial Board Map: ", initBoardMap, "| type(initBoardmap): ", type(initBoardMap)
	v2 = initBoardMap.lstrip("[")
	print "Clean Map: ", v2, "| type(initBoardmap): ", type(v2)

	
	#split the string to a list of coordinate/card mapped elements
	boardCoordList = v2.split(";")
	del boardCoordList[-1]
	#print "boardCoordList: ", boardCoordList, "| type(boardCoordList): ", type(boardCoordList)

	#create storage matrix for counting species in each row
	countMatrix = [[0] * (int(levelDiff) + 1) for _ in range(int(levelDiff) + 1)]
	#print "countMatrix: ", countMatrix
	
	speciesIDs = [0] * (int(levelDiff) + 1)		#This list holds the species associated with a game
	speciesInserted = 0				#This keeps track of the number of species found
	print "speciesIDs: ", speciesIDs, "| type(speciesIDs): " , type(speciesIDs), "speciesInserted: ", speciesInserted
	
	#iterate over cells in list and identify the target row and species for each cell - this
	#loop will also determine which speciesIDs are present for a given game map and update speciesIDs
	for cell in boardCoordList:
		
		#the species associated with the current cell may be a 1 or 2 character number 
		#NOTE: if subsequent datasets allow for more than 99 species this needs to be updated
		if (cell[6] == '.'):
			curSpecies = int(cell[5])
		elif (cell[7] == '.'):	
			curSpecies = 10*int(cell[5]) + int(cell[6])
		else:
			print "ERROR: No Target Species Identified"	
		
		#iterate over speciesIDs list (initialized to zeros) - once updated this list 
		#will contains the species associated with the tiles for a given board
		if not curSpecies in speciesIDs:
			speciesIDs[speciesInserted] = curSpecies
			speciesInserted = speciesInserted + 1
		#print "populated speciesIDs: ", speciesIDs
		
		countMatrixTargetCol = speciesIDs.index(curSpecies)
		countMatrixTargetRow = int(cell[1])
				
		#debug: print state of current cell being checked, uncomment as needed			
		#print "cell: ", cell, "countMatrixTargetCol: ", countMatrixTargetCol, "| countMatrixTargetRow: ", countMatrixTargetRow, "| curSpecies]: ", curSpecies
			
		#update state of countMatrix to reflect additional cell for a given species on the given row
		countMatrix[countMatrixTargetCol][countMatrixTargetRow] = (countMatrix[countMatrixTargetCol][countMatrixTargetRow] + 1) 
	
	print "countMatrix Final: ", countMatrix
	
	#a counter to keep track of sum (correctly placed tiles at start) in countMatrix rows
	sumCorrect = 0
	curRow = 0
	
	#iterate over rows of the count matrix to find the max value on a row
	for row in countMatrix:
		sumCorrect = sumCorrect + max(countMatrix[curRow])
		curRow = curRow + 1
	
	print "sum correctly placed tiles: ", sumCorrect
	
	#Calculate the Minimum Total Number of Turns required given the Starting Map
	numTiles = (int(levelDiff) + 1) * 4
	turnsMin = (numTiles - sumCorrect) / 2
	
	turnsTaken = float(numTurns)
	print "turnsMin: ", turnsMin, "type(turnsMin): ", type(turnsMin), " | turnsTaken: ", turnsTaken, " | type(turnsTaken): ", type(turnsTaken)
	
	#Calculate the play efficiency: turnsMin / numTurns taken
	gameEfficiency = (turnsMin / float(numTurns))
	print ">>> gameEfficiency: ", gameEfficiency

gameListFile.close()
