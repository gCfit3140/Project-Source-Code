import dataAnalysis as dA
import pickle


# generate training data set using previous bushfire data
def generate():
    # get all the input
    trainInput = []
    # the first section are 17 real bushfire data
    # for 2011
    for i in range(3):
        aInput = []
        aInput.append(dA.totalPopulation('Western Australia', '2011'))
        aInput.append(dA.ageScore('Western Australia', '2011'))
        aInput.append(dA.personalIncomeScore('Western Australia', '2011'))
        aInput.append(dA.pDensity('Western Australia', '2011'))
        trainInput.append(aInput)
    # for 2012
    aInput = []
    aInput.append(dA.totalPopulation('Western Australia', '2012'))
    aInput.append(dA.ageScore('Western Australia', '2012'))
    aInput.append(dA.personalIncomeScore('Western Australia', '2012'))
    aInput.append(dA.pDensity('Western Australia', '2012'))
    trainInput.append(aInput)
    # for 2013
    aInput = []
    aInput.append(dA.totalPopulation('Tasmania', '2013'))
    aInput.append(dA.ageScore('Tasmania', '2013'))
    aInput.append(dA.personalIncomeScore('Tasmania', '2013'))
    aInput.append(dA.pDensity('Tasmania', '2013'))
    trainInput.append(aInput)
    for i in range(2):
        aInput = []
        aInput.append(dA.totalPopulation('New South Wales', '2013'))
        aInput.append(dA.ageScore('New South Wales', '2013'))
        aInput.append(dA.personalIncomeScore('New South Wales', '2013'))
        aInput.append(dA.pDensity('New South Wales', '2013'))
        trainInput.append(aInput)
    # for 2014
    aInput = []
    aInput.append(dA.totalPopulation('Western Australia', '2014'))
    aInput.append(dA.ageScore('Western Australia', '2014'))
    aInput.append(dA.personalIncomeScore('Western Australia', '2014'))
    aInput.append(dA.pDensity('Western Australia', '2014'))
    trainInput.append(aInput)
    # for 2015
    for i in range(2):
        aInput = []
        aInput.append(dA.totalPopulation('South Australia', '2015'))
        aInput.append(dA.ageScore('South Australia', '2015'))
        aInput.append(dA.personalIncomeScore('South Australia', '2015'))
        aInput.append(dA.pDensity('Sout Australia', '2015'))
        trainInput.append(aInput)
    for i in range(4):
        aInput = []
        aInput.append(dA.totalPopulation('Western Australia', '2015'))
        aInput.append(dA.ageScore('Western Australia', '2015'))
        aInput.append(dA.personalIncomeScore('Western Australia', '2015'))
        aInput.append(dA.pDensity('Western Australia', '2015'))
        trainInput.append(aInput)
    # for 2016
    aInput = []
    aInput.append(dA.totalPopulation('Western Australia', '2016'))
    aInput.append(dA.ageScore('Western Australia', '2016'))
    aInput.append(dA.personalIncomeScore('Western Australia', '2016'))
    aInput.append(dA.pDensity('Western Australia', '2016'))
    trainInput.append(aInput)
    # for 2017
    for i in range(2):
        aInput = []
        aInput.append(dA.totalPopulation('New South Wales', '2017'))
        aInput.append(dA.ageScore('New South Wales', '2017'))
        aInput.append(dA.personalIncomeScore('New South Wales', '2017'))
        aInput.append(dA.pDensity('New South Wales', '2017'))
        trainInput.append(aInput)

    # 30- property & 10- deaths: slight damage
    # 30~100 property & 10-30 deaths: medium damage
    # 100+ property & 30+ deaths: sever damage
    trainOutput = [[1, 0, 0],
                  [0, 0, 1],
                  [0, 1, 0],
                  [0, 1, 0],
                  [0, 0, 1],
                  [0, 0, 1],
                  [0, 0, 1],
                  [0, 1, 0],
                  [0, 0, 1],
                  [0, 0, 1],
                  [0, 1, 0],
                  [0, 1, 0],
                  [0, 0, 1],
                  [0, 0, 1],
                  [0, 0, 1],
                  [0, 1, 0],
                  [0, 1, 0]]
    # Above are some real bushfire data, but 17 cases are not sufficient
    # Therefore we randomly generate some bushfire data for training purpose

    # all available past years
    years = ['2011', '2012', '2013', '2014', '2015', '2016', '2017']
    # all available states
    states = ['Victoria', 'New South Wales', 'Queensland', 'South Australia',
              'Western Australia', 'Tasmania', 'Northern Territory',
              'Australian Capital Territory', 'Other Territories']

    # the second section are simulated bushfire cases for each year for each state
    for i in range(len(years)):
        for _ in range(10):
            for j in range(len(states)):
                aInput = []
                aInput.append(dA.totalPopulation(states[j], years[i]))
                aInput.append(dA.ageScore(states[j], years[i]))
                aInput.append(dA.personalIncomeScore(states[j], years[i]))
                aInput.append(dA.pDensity(states[j], years[i]))
                # assign same impact level for same state,
                # so there is a pattern for the NN to learn
                if states[j] == 'Victoria':
                    trainOutput.append([0, 0, 1])
                elif states[j] == 'New South Wales':
                    trainOutput.append([0, 0, 1])
                elif states[j] == 'Queensland':
                    trainOutput.append([0, 1, 0])
                elif states[j] == 'Western Australia':
                    trainOutput.append([0, 1, 0])
                elif states[j] == 'South Australia':
                    trainOutput.append([1, 0, 0])
                elif states[j] == 'Tasmania':
                    trainOutput.append([0, 1, 0])
                elif states[j] == 'Northern Territory':
                    trainOutput.append([1, 0, 0])
                elif states[j] == 'Australian Capital Territory':
                    trainOutput.append([0, 0, 1])
                elif states[j] == 'Other Territories':
                    trainOutput.append([1, 0, 0])
                trainInput.append(aInput)

    # save the input & output data
    with open('trainInput', 'wb') as f1:
        required = []
        for i in range(len(trainInput)):
            required.append([trainInput[i][0][1], trainInput[i][1][1], trainInput[i][2][1], trainInput[i][3]])
        pickle.dump(required, f1)
    with open('trainOutput', 'wb') as f2:
        pickle.dump(trainOutput, f2)

    # simulate test data
    testInput = []
    testOutput = []
    for i in ['2018', '2019', '2020']:
        for j in range(len(states)):
            aInput = []
            aInput.append(dA.totalPopulation(states[j], i))
            aInput.append(dA.ageScore(states[j], i))
            aInput.append(dA.personalIncomeScore(states[j], i))
            aInput.append(dA.pDensity(states[j], i))
            # assign same impact level for same state,
            # so there is a pattern for the NN to learn
            if states[j] == 'Victoria':
                testOutput.append([0, 0, 1])
            elif states[j] == 'New South Wales':
                testOutput.append([0, 0, 1])
            elif states[j] == 'Queensland':
                testOutput.append([0, 1, 0])
            elif states[j] == 'Western Australia':
                testOutput.append([0, 1, 0])
            elif states[j] == 'South Australia':
                testOutput.append([1, 0, 0])
            elif states[j] == 'Tasmania':
                testOutput.append([0, 1, 0])
            elif states[j] == 'Northern Territory':
                testOutput.append([1, 0, 0])
            elif states[j] == 'Australian Capital Territory':
                testOutput.append([0, 0, 1])
            elif states[j] == 'Other Territories':
                testOutput.append([1, 0, 0])
            testInput.append(aInput)

    # save the input & output data
    with open('testInput', 'wb') as f3:
        required = []
        for i in range(len(testInput)):
            required.append([testInput[i][0][1], testInput[i][1][1], testInput[i][2][1], testInput[i][3]])
        pickle.dump(required, f3)
    with open('testOutput', 'wb') as f4:
        pickle.dump(testOutput, f4)

    # load the input & output data for checking
    with open('trainInput', 'rb') as f1:
        trInput = pickle.load(f1)
    with open('trainOutput', 'rb') as f2:
        trOutput = pickle.load(f2)
    with open('testInput', 'rb') as f3:
        teInput = pickle.load(f3)
    with open('testOutput', 'rb') as f4:
        teOutput = pickle.load(f4)

    # print the stored data sets for validating data
    print(trInput)
    print(len(trInput))
    print(trOutput)
    print(len(trOutput))
    print(teInput)
    print(len(testInput))
    print(teOutput)
    print(len(testInput))
    print("Data simulated, saved to four data files!")
generate()
