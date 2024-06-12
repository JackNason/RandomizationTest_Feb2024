
# RANDOMIZATION TEST
# Jack Nason, February 2024.

# ~~~~~~~~~~~~~~~~~~~~

# Feel free to use this.
# A lot of this uses column/header names that are specific to the dataset that I used,
# so those will have to be changed to reflect the data you are using.

import pandas as pd
import matplotlib.pyplot as plt


def mean(to_mean: list):
    """

    :param to_mean: list with len > 0
    :return: average value of list
    """

    return sum(to_mean) / len(to_mean)


def subset(df: pd.DataFrame, column_name: str, desired_value):

    """

    :param df: The dataframe you wish to have a subset of
    :param column_name: The name of the column which will be scanned for a value
    :param desired_value: The value that will be selected for
    :return: A subset of the original df. Having only rows with the desired value in the chosen column
    """

    sub = df[df[column_name] == desired_value]

    return sub


def randomize(data: pd.DataFrame):

    """

    :param data: The dataframe you wish to scramble, must have a column named NumOffspring
    :return: The original df, but shuffled NumOffspring column, so that this value is randomly assigned to each row
    """

    randomize_rows = data.sample(frac=1)  # This shuffles the rows around, so they are in a new order

    values = list(randomize_rows["NumOffspring"])

    for i in range(len(values)):

        data.loc[i, 'NumOffspring'] = values[i]

    return data


def measureDifferences(data: pd.DataFrame, isInitial: bool, diffs_df: pd.DataFrame, its: int):

    """

    :param data: the dataframe to work within
    :param isInitial: This is referring to whether this is the original difference (before randomization)
    :param diffs_df: dataframe to contain all differences
    :param its: number of iterations
    :return: dataframe containing all diffs
    """

    hand = subset(data, "Adult.Rearing", "SeaCage")
    heli = subset(data, "Adult.Rearing", "Hatchery")

    if isInitial:

        hand_avg = mean(hand["NumOffspring"])
        heli_avg = mean(heli["NumOffspring"])
    else:
        hand_avg = mean(hand["NumOffspring"])
        heli_avg = mean(heli["NumOffspring"])

    diffs_df.loc[len(diffs_df.index)] = hand_avg - heli_avg

    print(round(len(diffs_df.index) * 100 / its, 2))

    return diffs_df


def find_p(differences: pd.DataFrame, target, column: str, its):

    """

    :param differences: dataframe containing all calculated differences
    :param target: initial (observed) difference
    :param column: the column name (in the dataframe)
    :param its: the number of iterations used in the analysis
    :return: the probability of finding a difference that (or more) extreme in the randomized dataset
    """

    more_crazy_counter = 0  # tallies the

    if target < 0:

        for g in range(len(differences.index)):

            if differences.loc[g, column] < target:

                more_crazy_counter += 1

    else:

        for g in range(len(differences.index)):

            if differences.loc[g, column] > target:

                more_crazy_counter += 1

    return more_crazy_counter / its


def runAnalysis(dataToAnalyze: pd.DataFrame):

    """

    :param dataToAnalyze: The dataframe that you will be pulling all of your data from
    :return: This will randomize the response variable (NumOffspring), simulating the null hyp. that there is no
    difference caused by group. Then it will calculate the probability of finding results equal to, or more extreme
    than the observed.
    """

    #  This will be used to store all of the differences
    diffs_dict = {'SeaCage-Hatchery': [],
                  '1 year-recond': [],
                  '2 year-recond': []}

    diffs_df = pd.DataFrame(diffs_dict)  # converted into a pd dataframe

    iterations = 3000  # number of iterations to run in randomization

    initialDiffs = measureDifferences(dataToAnalyze, True, diffs_df, iterations)  # Measures the initial differences

    for i in range(iterations):

        use_data = randomize(dataToAnalyze)
        diffs_df = measureDifferences(use_data, False, diffs_df, iterations)

    print(mean(diffs_df["SeaCage-Hatchery"]))

    fig, axs = plt.subplots(2)
    fig.suptitle('Difference Histograms')
    axs[0].hist(diffs_df["SeaCage-Hatchery"], bins=100)

    plt.show()

    p1 = find_p(diffs_df, initialDiffs["SeaCage-Hatchery"][0], "SeaCage-Hatchery", iterations)

    print("initial:")
    print(initialDiffs)
    print("-----------")
    print(f"SeaCage-Hatchery: {p1}")


with open('Data/PWR-AdultResults-Updated.csv') as data_file:
    pwr_spawn_data = pd.read_csv(data_file)

runAnalysis(pwr_spawn_data)
