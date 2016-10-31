from GA import GA

G = GA( 3 )

G.FitnessFunctionPopulation()

G.PrintBestPerson()

for _ in xrange( 1 ):
	G.EvolucaoHierarquicaRandomica()

G.PrintBestPerson()