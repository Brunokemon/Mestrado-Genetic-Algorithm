from __future__ import division
import numpy as np
import math
import copy

class GA(object):

	def __init__( self, tamanhoPopulacao ):

		#caracteristicas de cada elemento
		self.genes = []
		self.genes.append( { "caracteristicaA": 05, "caracteristicaB": 10 })
		self.genes.append( { "caracteristicaA": 15, "caracteristicaB": 30 })
		#genes A. Exemplo: diesel
#		self.genes.append({ "caracteristicaA": 10, "caracteristicaB": 20, "caracteristicaC": 30, "caracteristicaD": 40, "caracteristicaE": 50 })
		#genes B. Ex: biodiesel de mamona
#		self.genes.append( { "caracteristicaA": 05, "caracteristicaB": 30, "caracteristicaC": 35, "caracteristicaD": 45, "caracteristicaE": 10 })
		#genes C
#		self.genes.append( { "caracteristicaA": 15, "caracteristicaB": 10, "caracteristicaC": 20, "caracteristicaD": 10, "caracteristicaE": 20 })
		#genes D
#		self.genes.append( { "caracteristicaA": 20, "caracteristicaB": 25, "caracteristicaC": 10, "caracteristicaD": 30, "caracteristicaE": 60 })
		#genes E
#		self.genes.append( { "caracteristicaA": 25, "caracteristicaB": 15, "caracteristicaC": 40, "caracteristicaD": 20, "caracteristicaE": 15 })

		self.individuos = []
		self.notas = []

		self.GeraPrimeiraPopulacao( tamanhoPopulacao )

	#Gera populacao inicial randomicamente
	#Recebe int tamanhoPopulacao
	#Devolve array individuos
	def GeraPrimeiraPopulacao( self, tamanhoPopulacao ):
		
		#Para porcentagem
		DNATotal = 100
		#Alternativa para maior precisao
		#DNATotal = 1000

		for n in xrange( tamanhoPopulacao ):
			self.individuos.append([])
			DNAOcupado = 0

			for m in xrange(len(self.genes)):
				if m==(len(self.genes)-1):
					self.individuos[n].append(DNATotal-DNAOcupado)
				else:
					self.individuos[n].append(np.random.random_integers(0,DNATotal-DNAOcupado))
					DNAOcupado = DNAOcupado+self.individuos[n][m]

		self.FitnessFunctionPopulation()

	#Funcao para calculo de fitness com objetivo de minimizacao das caracteristicas
	#Devolve array de notas de cada individuo
	def FitnessFunctionPopulation( self ):
		
		novasNotas = []
		for individuo in self.individuos:
			notaLocal = 0	
			for gene in xrange( len(self.genes) ):
				#notaLocal = notaLocal + individuo[gene]*(self.genes[gene]["caracteristicaA"]+self.genes[gene]["caracteristicaB"]+self.genes[gene]["caracteristicaC"]+self.genes[gene]["caracteristicaD"]+self.genes[gene]["caracteristicaE"])
				notaLocal = notaLocal + individuo[gene]*(self.genes[gene]["caracteristicaA"]+self.genes[gene]["caracteristicaB"])
			#novasNotas.append( 15000 - notaLocal )
			novasNotas.append( notaLocal )

		self.notas = novasNotas

	#Funcao para calculo de fitness com objetivo de minimizacao das caracteristicas
	#Devolve nota do individuo
	def FitnessFunctionIndividual( self, individuo ):
		notaLocal = 0
		for gene in xrange( len(self.genes) ):
			notaLocal = notaLocal + individuo[gene]*(self.genes[gene]["caracteristicaA"]+self.genes[gene]["caracteristicaB"])
			#notaLocal = notaLocal + individuo[gene]*(self.genes[gene]["caracteristicaA"]+self.genes[gene]["caracteristicaB"]+self.genes[gene]["caracteristicaC"]+self.genes[gene]["caracteristicaD"]+self.genes[gene]["caracteristicaE"])

		return 15000 - notaLocal

	#Verifica se a soma dos genes do individuo resultam em 100%
	def VerificaSomaGenes( self, individuo ):
		somaTotal = 0
		for n in xrange( len(self.genes) ):
			somaTotal = somaTotal + individuo[n]
		return somaTotal

	#Retorna individuo com maior nota
	#Recebe array de individuos da populacao
	#Retorna o indice do individuo com maior nota
	def BestPerson( self ):
		bestPersonIndex = self.notas.index( max(self.notas) )		
		return bestPersonIndex

	def PrintBestPerson( self ):
		bestPersonIndex = self.BestPerson()
		print "Nota do melhor individuo: " + str(self.notas[bestPersonIndex])

	#Seleciona os melhores individuos baseado em probabilidade utilizando a formula de fitness e a reproducao se da por 50% pai e 50% mae
	#Recebe arrays de individuos e de notas
	#Devolve nova populacao (novos individuos)
	def EvolProbabilisticaMeioAMeio( self ):

		notaTotal = 0
		for nota in self.notas:
			notaTotal = notaTotal + nota

		novosIndividuos = copy.deepcopy( self.individuos )
		for number in xrange( len(self.individuos) ):

			#Sorteio do individuo 1
			probabilidade = np.random.uniform( 0 , notaTotal )
			notaLocal = 0
			individuoEscolhido1 = 0
			for i in xrange( len(self.notas) ):
				if notaLocal <= probabilidade and probabilidade <= (notaLocal + self.notas[i]):
					individuoEscolhido1 = i
					break
				notaLocal = notaLocal + self.notas[i]

			#Deixado explicito por simplicidade de leitura
			#Sorteio do individuo 2
			probabilidade = np.random.uniform( 0 , notaTotal )
			notaLocal = 0
			individuoEscolhido2 = 0
			for i in xrange( len(self.notas) ):
				if notaLocal <= probabilidade and probabilidade <= (notaLocal + self.notas[i]):
					individuoEscolhido2 = i
					break
				notaLocal = notaLocal + self.notas[i]

			novoIndividuo = copy.deepcopy( self.individuos )
			for gene in xrange( len(self.genes) ):
				novosIndividuos[number][gene] = ( self.individuos[individuoEscolhido1][gene] + self.individuos[individuoEscolhido2][gene] )/2

		self.individuos = novosIndividuos
		self.FitnessFunction()

	#Seleciona os melhores individuos baseado em probabilidade utilizando a formula de fitness e a reproducao se da por 100-x(gerado randomicamente)% pai e x% mae
	#Recebe arrays de individuos e de notas
	#Devolve nova populacao (novos individuos)
	def EvolProbabilisticaRandomica( self ):
		
		notaTotal = 0
		for nota in self.notas:
			notaTotal = notaTotal + nota

		novosIndividuos = copy.deepcopy( self.individuos )
		for number in xrange( len(self.individuos) ):

			#Sorteio do individuo 1
			probabilidade = np.random.uniform( 0 , notaTotal )
			notaLocal = 0
			individuoEscolhido1 = 0
			for i in xrange( len(self.notas) ):
				if notaLocal <= probabilidade and probabilidade <= (notaLocal + self.notas[i]):
					individuoEscolhido1 = i
					break
				notaLocal = notaLocal + self.notas[i]

			#Deixado explicito por simplicidade de leitura
			#Sorteio do individuo 2
			probabilidade = np.random.uniform( 0 , notaTotal )
			notaLocal = 0
			individuoEscolhido2 = 0
			for i in xrange( len(self.notas) ):
				if notaLocal <= probabilidade and probabilidade <= (notaLocal + self.notas[i]):
					individuoEscolhido2 = i
					break
				notaLocal = notaLocal + self.notas[i]

			novoIndividuo = copy.deepcopy( self.individuos )

			influenciaParental = np.random.uniform()
			for gene in xrange( len(self.genes) ):
				novosIndividuos[number][gene] = self.individuos[individuoEscolhido1][gene]*(influenciaParental) + self.individuos[individuoEscolhido2][gene]*(1-influenciaParental)

		self.individuos = novosIndividuos
		self.FitnessFunction()

	#Seleciona os 2 melhores individuos e a reproducao se da por 100-x(gerado randomicamente)% pai e x% mae
	#Recebe arrays de individuos e de notas
	#Devolve nova populacao (novos individuos)
	def EvolHierarquicaRandomica( self  ):

		notaTotal = 0
		for nota in self.notas:
			notaTotal = notaTotal + nota

		novosIndividuos = copy.deepcopy( self.individuos )

		individuoMaiorNota = self.BestPerson()
		segundaMaiorNota = 0
		individuoSegundaMaiorNota = 0

		for nota in self.notas:
			if nota is not self.notas[individuoMaiorNota] and nota > segundaMaiorNota :
				segundaMaiorNota = nota
				individuoSegundaMaiorNota = self.notas.index( segundaMaiorNota )

		for number in xrange( len(self.individuos) ):

			influenciaParental = np.random.uniform()
			for gene in xrange( len(self.genes) ):
				novosIndividuos[number][gene] = self.individuos[individuoMaiorNota][gene]*influenciaParental + self.individuos[individuoSegundaMaiorNota][gene]*(1-influenciaParental)

		self.individuos = novosIndividuos
		self.FitnessFunctionPopulation()

	#Seleciona os 2 melhores individuos e a reproducao se da por 100-x(gerado randomicamente)% pai e x% mae
	#Recebe arrays de individuos e de notas
	#Devolve nova populacao (novos individuos)
	def EvolHierarquicaRandomica2( self  ):
		notaTotal = 0
		for nota in self.notas:
			notaTotal = notaTotal + nota

		novosIndividuos = copy.copy( self.individuos )

		individuoMaiorNota = self.BestPerson()
		segundaMaiorNota = 0
		individuoSegundaMaiorNota = 0
		print self.notas[individuoMaiorNota]
		for nota in self.notas:
			if nota is not self.notas[individuoMaiorNota] and nota > segundaMaiorNota :
				segundaMaiorNota = nota
				individuoSegundaMaiorNota = self.notas.index( segundaMaiorNota )

		#PRECISA MEXER AQUI
		for number in xrange( len(self.individuos) ):
			
			while True is True :
				influenciaParental = np.random.random_sample()
				for gene in xrange( len(self.genes) ):
					novosIndividuos[number][gene] = self.individuos[individuoMaiorNota][gene]*(influenciaParental) + self.individuos[individuoSegundaMaiorNota][gene]*(1-influenciaParental)

				if (self.FitnessFunctionIndividual(novosIndividuos[number])>self.notas[individuoMaiorNota]):
					print "achou"
					break

		self.individuos = novosIndividuos
		self.FitnessFunctionPopulation()