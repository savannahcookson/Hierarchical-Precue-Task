import subprocess
import os
import numpy
import sys

ITERATIONS = 100
RUNS = 1
SESSION = 's2'

def fileSummer():
	fhcurr = open('rm_Output.txt','r')

	loopIndex = 1
	nums = []
	for line in fhcurr:
	    if loopIndex == 3:
	        nums.append(float(line[28:-1]))
	        loopIndex = 1
	    else:
	        loopIndex += 1

	fhcurr.close()

	return sum(nums)/len(nums)

def seqGen(counter):
	runBash('sh afni_gen_prac_test.sh ' + str(counter) + ' >> output.txt')
	runBash('sh rm_design_test.sh > rm_Output.txt')
	return

def fileClear(badCounter):
	runBash('rm rm*')
	runBash('rm ' + str(badCounter) + '_prac*.1D')


def runBash(bashCommand):
	os.system(bashCommand)

if __name__ == '__main__':

	#runBash('sh clearFiles.sh')
	fh = open('loopLog.txt','a')

	counter = 0
	testCounter = []
	bestOutput = []
	while counter < 100:

		seqGen(counter)

		currOutput = fileSummer()
		fileText = str(counter) + ', ' + str(currOutput)
		fh.write(fileText)
		if counter == 0 or currOutput < bestOutput:
			bestOutput = currOutput
			badCounter = testCounter
			testCounter = counter
			fh.write(' better match!')
			print(counter)
		else:
			badCounter = counter
		fileClear(badCounter)
		fh.write('\n')
		runBash('rm output.txt')

		counter += 1

	fh.close()
	print('best option is round ' + str(testCounter) + ' with output ' + str(bestOutput))
