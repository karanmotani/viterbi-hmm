import sys

def createProbMatrix():
	hotProb = {(1, 'hot') : 0.2, (2, 'hot') : 0.4, (3, 'hot') : 0.4}
	coldProb = {(1, 'cold') : 0.5, (2, 'cold') : 0.4, (3, 'cold') : 0.1}
	transitionProb = {('hot', 'hot') : 0.7, ('hot', 'cold') : 0.3, ('cold', 'cold') : 0.6, ('cold', 'hot') : 0.4}
	hotInitialProb = 0.8
	coldInitialProb = 0.2

	return hotProb, coldProb, transitionProb, hotInitialProb, coldInitialProb



def viterbi(input, hotProb, coldProb, transitionProb, hotInitialProb, coldInitialProb):
	hotProbList = []
	coldProbList = []
	hotWeather = []
	coldWeather = []

	number = [int(d) for d in str(input)]
	lenNumber = len(number)

	# Initial Hot and Cold Probabilities
	initialHot = hotInitialProb * hotProb[(number[0], 'hot')]
	initialCold = coldInitialProb * coldProb[(number[0], 'cold')]


	hotWeather.append((number[0], initialHot, 'hot'))
	coldWeather.append((number[0], initialCold, 'cold'))


	# Add the hot and cold prob to the list
	hotProbList.append(initialHot)
	coldProbList.append(initialCold)


	for i in range(1, len(number)):

		hGh = hotProbList[i-1] * transitionProb[('hot', 'hot')] * hotProb[(number[i], 'hot')]
		cGh = coldProbList[i-1] * transitionProb[('cold', 'hot')] * hotProb[(number[i], 'hot')]
		hGc = hotProbList[i-1] * transitionProb[('hot', 'cold')] * coldProb[(number[i], 'cold')]
		cGc = coldProbList[i-1] * transitionProb[('cold', 'cold')] * coldProb[(number[i], 'cold')]

		hotTemp = max(hGh, cGh)
		coldTemp = max(hGc, cGc)

		if hotTemp == hGh:
			hotWeather.append((number[i], hGh, 'hot'))
		else:
			hotWeather.append((number[i], cGh, 'cold'))

		if coldTemp == hGc:
			coldWeather.append((number[i], hGc, 'hot'))
		else:
			coldWeather.append((number[i], cGc, 'cold'))


		hotProbList.append(hotTemp)
		coldProbList.append(coldTemp)


	return hotWeather, coldWeather


def backTracking(input, hotWeather, coldWeather):
	bT = []

	number = [int(d) for d in str(input)]
	lenNumber = len(number)

	if hotWeather[lenNumber-1][1] > coldWeather[lenNumber-1][1]:
		bT.append('hot')
		vtProb = hotWeather[lenNumber-1][1]

	else:
		bT.append('cold')
		vtProb = coldWeather[lenNumber-1][1]

	while(lenNumber-1 > 0):
		if hotWeather[lenNumber-1][1] > coldWeather[lenNumber-1][1]:
			bT.append(hotWeather[lenNumber-1][2])
		
		else:
			bT.append(coldWeather[lenNumber-1][2])

		lenNumber -= 1

	bT = bT[::-1]

	return bT, vtProb

	

if __name__ == '__main__':
	hotProb, coldProb, transitionProb, hotInitialProb, coldInitialProb = createProbMatrix()
	# print ('Hot prob: ', hotProb)
	# print ('Cold prob: ', coldProb)
	# print ('Transition prob: ', transitionProb)
	# print ('Hot initial prob: ', hotInitialProb)
	# print ('Cold initial prob: ', coldInitialProb)
	# print ('\n')

	input = sys.argv[1]
	# input = 331123312
	hotWeather, coldWeather = viterbi(input, hotProb, coldProb, transitionProb, hotInitialProb, coldInitialProb)
	weatherSequence, finalProb = backTracking(input, hotWeather, coldWeather)

	print ('Weather Sequence: ', *weatherSequence, sep=' -> ')
	print ('Probability: ', finalProb)