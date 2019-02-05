#!/usr/bin/python2.7 -tt
#coding: ascii

import csv 
import sys

#open the .csv file (argv[1]) output from sql query (UID, game1mode, difficulty)  
gamesListFile = open(sys.argv[1],'rb')

#define the difficulty as the second argument - this allows us to determine T_min
gameDiff = sys.argv[2]
gameDiff = int(gameDiff)

#create a list of all of the games' played cardSelectedOrders
gamesCardsSelectedList = list(csv.reader(gamesListFile))

#iterate through the list of games played 
for cardSelectedOrderList in gamesCardsSelectedList:
	print "==================================="
	print "========== GAME ANALYSIS =========="
	print "==================================="

	#print cardSelectedOrderList

	#for each game played we need a metric for W(inning), L(uck), and E(rrors) in order to computer S(uccess)

	#to compute W = T(urns)_min / T(urns)_taken, we parse T_min from filename switching on diff and T_taken as the number of elements in the list
	W = 0.0

	#get T_min from gameDiff (passed as argv[2]
	T_min = 0
	if gameDiff == 1:
		T_min = 6
	elif gameDiff == 2:
		T_min = 8
	elif gameDiff == 3:
		T_min = 10
	else:
		print "Difficulty argument is out of range [1 -3]"

	#print "T_min is: ", T_min
	
	#T_taken is found by converting the csv string to a list - cardSelectedOrder - cleaning it, and finding its length
	T_taken = 0
	#print "len(cardSelectedOrderList): ", len(cardSelectedOrderList), " type(cardSelectedOrderList: ", type(cardSelectedOrderList)
	for x in cardSelectedOrderList:
		#print x, "type(x): ", type(x)
		cardSelectedOrder = x.strip().split(',')
		cardSelectedOrder.remove('')
		#print cardSelectedOrder, "type(cardSelectedOrder): ", type(cardSelectedOrder), " len(cardSelectedOrder): ", len(cardSelectedOrder)
		#T_taken is the length of the list over 2 (i.e. pairs) 
		T_taken = len(cardSelectedOrder) / 2
	
	#print "T_taken is: ", T_taken

	#compute W 
	W = float(T_min) / float(T_taken)
	#print "W(inning)", W, "= T_min", T_min, "/T_taken", T_taken

	'''
	The number of pairs found by luck is the number of pairs that are found with having been previously seen. [TODO consider not counting final pair? as not always 'luck']
	If the list of cards selected is ordered, then a card that appears only 2 times then it will necessarily  have been found by luck.
	A card that appears 3 or 4  times will be assumed to have been found, and then matched on finding the second one.
	Any additional instances of a given card will occur only if the card has been forgotten and turned again - this is the error in memory that we will define as E.
	This isn't strictly accurate as there is a possibility that a card matched on the 4th instance could have been matched on the 3rd but an error occured
        '''

	#to compute L(uck): L  = P_luck / P_total; P(airs)_luck counts the pairs that are found without either having been previously seen (TODO SOLVE how to deal with final pair?); P_total = T_min / 2
	L = 0.0

	P_total = float(T_min)
	#print "P_total: ", P_total
	P_luck = 0

        #to compute (Learning) E(rrors): E = C(ount)_repeats of cards > 4) ...
	E = 1.0
	C_repeats = 0.0

	cardSelectedOrder = map (int, cardSelectedOrder)
	#print sorted(cardSelectedOrder)
	
	#iterate over possible card values
	for i in range (1, int(P_total)):
		j = sorted(cardSelectedOrder).count(i)
		#print i, j
		#print cardSelectedOrder, "type(cardSelectedOrder): ", type(cardSelectedOrder), " i = ", i, " type(i): ", type(i)
		if j == 2: P_luck += 1.
		elif j > 4: C_repeats += (j - 4)

	#print "P_luck=", P_luck
	#print "C_repeats: ", C_repeats

	L = P_luck / P_total
	#print "L", L, "=P_luck", P_luck, "/P_total", P_total

	#to avoid a later potential divide by zero error, E = 1.0
	if C_repeats == 0.0:
		E += C_repeats
	else:
		E = C_repeats	

	#print "Winning W = ", W
	#print "Luck L = ", L
	print ">> Learning E = ", E, "=C_repeats ", C_repeats	
	
	'''
	S(uccess) is a function of W, L, & E s.t. S = (W * (1 -L)) / E
	'''

	S = ((W *(1 - L))/E)
	print ">> Success S = ", S


gamesListFile.close()
