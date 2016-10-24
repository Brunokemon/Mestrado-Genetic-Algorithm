from GA import GA

firstGA = GA( 4 )

for _ in xrange( 3 ):
	firstGA.EvolucaoProbabilisticaMeioAMeio()
	#firstGA.PrintBestPerson()
