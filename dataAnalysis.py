import pandas as pd


# calculate a region's total population of a year
def totalPopulation(region, year):
    # read the population data file
    df = pd.read_csv("PopulationInfomation.csv")
    region = df['Region'] == region
    # check if need to simulate the data
    if year not in ['2011', '2012', '2013', '2014', '2015']:
        # use 2011 data to simulate the missing data
        time = df['TIME'] == 2015
    else:
        time = df['TIME'] == int(year)
    # get the total population only
    num = df['Data Item'] == 'Estimated Resident Population - Persons - Total (no.)'
    total = df[region & time & num].Value.sum()
    # predict total population for future years
    if year not in ['2011', '2012', '2013', '2014', '2015']:
        # We have no real data for this year, but as the population is growing,
        # the total population would have an increase of roughly 1% each year.
        # So we have some predictions for the population!
        growthRate = 1.01
        # the population should have an increase of roughly 1% each year
        if year == '2016':
            total *= growthRate
        elif year == '2017':
            total *= growthRate**2
        elif year == '2018':
            total *= growthRate**3
        elif year == '2019':
            total *= growthRate**4
        elif year == '2020':
            total *= growthRate**5
    # round the population to a whole number
    score = round(total/1000000, 1)
    return round(total), score


# calculate a region's age score of a year
def ageScore(region, year):
    # read the population data file
    df = pd.read_csv("PopulationInfomation.csv")
    region = df['Region'] == region
    # check if need to simulate the data
    if year not in ['2011', '2012', '2013', '2014', '2015']:
        # use 2011 data to simulate the missing data
        time = df['TIME'] == 2015
    else:
        time = df['TIME'] == int(year)
    # store all year range totals
    age = []
    # get all year range total for a region's target year
    for i in range(2, 20):
        ageRange = df['MEASURE'] == 'ERP_P_' + str(i)
        age.append(df[region & time & ageRange].Value.sum())
    # store the age score
    ages = 0
    # store display value
    nonScore = 0
    counter = 1
    # total population
    total = 0
    # from (0~4) to (30~34): from -2 to 5
    for i in range(7):
        ages += age[i] * (i-2)
        nonScore += age[i] * counter
        counter += 1
        total += age[i]
    # from (30~39) to (50~54): all have 6(experienced and physically strong)
    for i in range(7, 11):
        ages += age[i] * 5
        nonScore += age[i] * counter
        counter += 1
        total += age[i]
    minus = 12
    # from (55~59) to (85+): from -1 to -7(the older the more assistance required)
    for i in range(11, 18):
        ages += age[i] * (i-minus)
        total += age[i]
        nonScore += age[i] * counter
        counter += 1
        minus += 2

    # divide the score by the total population
    ages = ages / total
    # calculate average age range
    average = nonScore / total
    index = df['Data Item'].unique()
    average = index[round(average)]
    average = average[41:]
    average = average[:-5]

    # predict the age score for future years
    if year not in ['2011', '2012', '2013', '2014', '2015']:
        # We have no real data for this year, but as the population is aging,
        # the age score would have a decrease of roughly 1% each year.'
        # So we have some predictions for this score!
        growthRate = 0.91
        # the population is aging, and old people has a more negative effect,
        # so the age score should have an decrease of roughly 1% each year
        if year == '2016':
            ages *= growthRate
        elif year == '2017':
            ages *= growthRate**2
        elif year == '2018':
            ages *= growthRate**3
        elif year == '2019':
            ages *= growthRate**4
        elif year == '2020':
            ages *= growthRate**5
    return average, round(ages, 1)


# calculate a region's personal weekly income score of a year
def personalIncomeScore(region, year):
    # get the average household income based on given region & year
    df = pd.read_csv("Income.csv")
    region = df['State'] == region
    # a list to store all target income
    incomeList = []
    # get total of all income range
    for i in range(3, 10):
        incomeRange = df['INCP'] == int(i)
        incomeList.append(df[region & incomeRange].Value.sum())
    # add the rest of income range 9 values
    incomeRange = df['INCP'] == str('%02d' % 9)
    tmp = df[region & incomeRange].Value.sum()
    incomeList[-1] += tmp
    for i in range(10, 13):
        incomeRange = df['INCP'] == str(i)
        incomeList.append(df[region & incomeRange].Value.sum())
    # get the personal income not stated number
    incomeRange = df['INCP'] == 'Z'
    incomeList.append(df[region & incomeRange].Value.sum())
    # get the nil/negative income number
    incomeRange = df['INCP'] == '01_02'
    incomeList.append(df[region & incomeRange].Value.sum())
    # calculate the average income
    scaledIncome = 0
    # calculate population
    total = 0
    # sum the population for all the income ranges(0~199 to 2000+)
    for i in range(len(incomeList) - 2):
        # range starts with 1 and every next range worth 1 more
        scaledIncome += incomeList[i] * i
        total += incomeList[i]
    # negative income group would has negative of 1
    scaledIncome -= incomeList[-1]
    total += incomeList[-1]
    # calculate the average
    scaledIncome /= total
    # round the score to whole
    scaledIncome = round(scaledIncome)

    # calculate the average income
    incomeRanges = df['Total Personal Income (weekly)'].unique()
    average = incomeRanges[scaledIncome]

    # We have no real data for this year, but as the personal income is increasing,'
    # the income score would have an increase of roughly 3% each year.
    # So we have some predictions for this score!
    # the personal weekly income should have an increase of roughly 3% each year
    growthRate = 1.03
    if int(year) == 2012:
        scaledIncome *= growthRate
    elif int(year) == 2013:
        scaledIncome *= growthRate**2
    elif int(year) == 2014:
        scaledIncome *= growthRate**3
    elif int(year) == 2015:
        scaledIncome *= growthRate**4
    elif int(year) == 2016:
        scaledIncome *= growthRate**5
    elif int(year) == 2017:
        scaledIncome *= growthRate**6
    elif int(year) == 2018:
        scaledIncome *= growthRate**7
    elif int(year) == 2019:
        scaledIncome *= growthRate**8
    elif int(year) == 2020:
        scaledIncome *= growthRate**9

    return average, round(scaledIncome)


# get the population density of this region
def pDensity(region, year):
    # read the population data file
    df = pd.read_csv("PopulationInfomation.csv")
    region = df['Region'] == region
    # check if need to simulate the data
    if year not in ['2011', '2012', '2013', '2014', '2015']:
        # use 2011 data to simulate the missing data
        time = df['TIME'] == 2015
    else:
        time = df['TIME'] == int(year)
    measure = df['MEASURE'] == 'ERP_21'
    density = df[region & time & measure].Value.sum()
    # predict total population for future years
    if year not in ['2011', '2012', '2013', '2014', '2015']:
        # We have no real data for this year, but as the population density is increasing,
        # the population density would have an increase of roughly 1% each year.
        # So we have some predictions for the population!
        growthRate = 1.01
        # the population should have an increase of roughly 1% each year
        if year == '2016':
            density *= growthRate
        elif year == '2017':
            density *= growthRate ** 2
        elif year == '2018':
            density *= growthRate ** 3
        elif year == '2019':
            density *= growthRate ** 4
        elif year == '2020':
            density *= growthRate ** 5
    return round(density, 1)


# function used for running the data analysis system when given inputs
def start(region=None, year=None):
    df = pd.read_csv("PopulationInfomation.csv")
    regions = df.Region.unique()
    # can be used for unit testing, asks user input in console
    if not region or not year:
        # get user's target region & year
        while True:
            # get user's target region
            region = input("Enter the region name: ")
            # valid user input
            if region not in regions:
                print("Sorry, that is not a valid state.")
                continue
            else:
                break

        while True:
            # get user's target year
            year = input("Enter the year between 2011 and 2020: ")
            # valid user input
            if year not in ['2011', '2012', '2013', '2014', '2015',
                            '2016', '2017', '2018', '2019', '2020']:
                print("Sorry, that is not in the range.")
                continue
            else:
                break
        else:
            region = region
            year = year

    population = totalPopulation(region, year)
    age = ageScore(region, year)
    income = personalIncomeScore(region, year)
    density = pDensity(region, year)
    results = [population, age, income, density]
    return results
