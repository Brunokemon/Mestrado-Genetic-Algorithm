from GA import GA

G = GA( 4 )

G.FitnessFunction()

G.PrintBestPerson()

print ""

for _ in xrange( 100 ):
	G.EvolucaoProbabilisticaRandomica()

G.PrintBestPerson()