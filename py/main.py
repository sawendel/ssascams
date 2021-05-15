# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
import os
from scipy.stats import ttest_ind
import numpy as np

import numpy as np
from statsmodels.formula.api import ols

from swstats import *
import random

surveyVersion = 4

debugging = False
trainingQuestions = {'CyberAttack':'Fake',
                     'ProtectYourself':'Real',
                     'AnnualReminder':'Real',
                     'CovidSSA':'Fake',
                     'GetProtected':'Fake',
                     'lt_favorable':'Real'}

if (surveyVersion == 1 or surveyVersion == 2):
    testQuestions = {'ImportantInformation':'Real',
                     'AmazonPayment':'Fake',
                     'AmazonDelay':'Real',
                     'RedCross':'Fake',
                     'Disability':'Fake',
                     }
elif surveyVersion == 3:  # There was an unintentional mistake in the SSA_Optout and Replacement Card in v3
    testQuestions = {'ImportantInformation':'Real',
                     'AmazonPayment':'Fake',
                     'AmazonDelay':'Real',
                     'RedCross':'Fake',
                     'Disability':'Fake',
                     'ssa_optout':'Fake',
                     'replacementCard':'Fake',
                     'annualReminderKLEW':'Fake',
                     'lt_medicare':'Real',
                     'sms_disability':'Fake',
                     'lt_suspension':'Fake',
                     'sms_redcross':'Real'
                     }
elif surveyVersion >= 4:
    testQuestions = {'ImportantInformation':'Real',
                     'AmazonPayment':'Fake',
                     'AmazonDelay':'Real',
                     'RedCross':'Fake',
                     'Disability':'Fake',
                     'ssa_optout':'Fake',
                     'replacementCard':'Real',
                     'annualReminderKLEW':'Fake',
                     'lt_medicare':'Real',
                     'sms_disability':'Fake',
                     'lt_suspension':'Fake',
                     'sms_redcross':'Real'
                     }


def readdata():

    dataDir  = "C:/Dev/src/ssascams/data/"

    if surveyVersion == 1:
        dataFileName = "SSA_February 14_Test2_Clean.csv"
        dta = pd.read_csv(dataDir + dataFileName)
    elif surveyVersion == 3:
        # dataFileName = "SSA_v3_May 9, 2021_08.18_clean.csv"
        dataFileName = "SSA_v3_asFielded_May 10, 2021_07.41_clean.csv"
        dta = pd.read_csv(dataDir + dataFileName)
    elif surveyVersion == 4:
        dataFileName_p1 = "SSA_v4_Part1_May 13, 2021_20.02_clean.csv"
        dataFileName_prolific = "prolific_export_6099c49373d406738c79f948.csv"
        dataFileName_p2 = "SSA_v4_Part2_AllQualtrics_May 14, 2021_17.51_clean.csv"
        dataFileName =  "SSA_v4_May 13, 2021_20.02_clean.csv" # For Output Files

        dta_p1 = pd.read_csv(dataDir + dataFileName_p1)
        dta_profilic = pd.read_csv(dataDir + dataFileName_prolific)
        dta_p2 = pd.read_csv(dataDir + dataFileName_p2)
        dta_p2.drop(columns={'surveyArm'})

        dta = dta_p1.merge(dta_profilic, right_on="participant_id", left_on = "PID", how="left")
        dta = dta.merge(dta_p2, right_on="PID", left_on = "PID", how="left", suffixes=["", "_end"])

    # remove empty columns
    dta = dta.dropna(axis=1, how='all')

    # Some early data had this arm mislabeled
    dta.surveyArm.replace({"notSet": "arm4_training"}, inplace=True)
    dta.surveyArm.fillna(value="Unknown", inplace=True)

    # Mark the Various Waves of the Study
    dta['StartDate'] = pd.to_datetime(dta.StartDate)

    dta['Wave'] = None
    if surveyVersion == 3:
        # Small tests to see if it was working
        dta.loc[(dta.StartDate < '2021-05-08 10:00'), 'Wave'] = 1
        dta.loc[(dta.StartDate >= '2021-05-08 10:00') & (dta.StartDate < '2021-05-08 13:00'), 'Wave'] = 2
        # 3: Full test
        dta.loc[(dta.StartDate >= '2021-05-08 13:00') & (dta.StartDate < '2021-05-08 17:00'), 'Wave'] = 3
        # 4: Added Stronger Language to clarify purpose; REAL and FAKE
        dta.loc[(dta.StartDate >= '2021-05-08 17:00') & (dta.StartDate < '2021-05-08 23:59'), 'Wave'] = 4
        # 5: Mobile Only Version of 1; Has Updated Files meant for Study Version 4
        dta.loc[(dta.StartDate >= '2021-05-09 08:00') & (dta.StartDate < '2021-05-10 10:00'), 'Wave'] = 5
    elif surveyVersion == 4:
        dta.loc[(dta.StartDate < '5/9/2021 23:59'), 'Wave'] = 1
        dta.loc[(dta.StartDate >= '5/9/2021 23:59'), 'Wave'] = 2
    else:
        dta.Wave = 1

    print(dta.Wave.value_counts(dropna=False))


    ''' Data Cleaning '''
    dta['cleanStatus'] = "Keep"
    if surveyVersion == 3:
        dta.loc[(dta['cleanStatus'] == "Keep") & (dta['Duration (in seconds)'] < 60*3), 'cleanStatus'] = 'Too Fast'
    elif surveyVersion == 4:
        dta.loc[(dta['cleanStatus'] == "Keep") & (dta['status'] == 'RETURNED'), 'cleanStatus'] = 'Task Returned'
        dta.loc[(dta['cleanStatus'] == "Keep") & (dta['Progress_end'].isna()), 'cleanStatus'] = 'No Second Round'
        dta.loc[(dta['cleanStatus'] == "Keep") & (dta['Progress_end'] < 98), 'cleanStatus'] = 'Incomplete Round 2'

    # dta.loc[(dta['cleanStatus'] == "Keep") & (dta['statusCode'] != 200), 'cleanStatus'] = 'Email Error'
    dta.loc[(dta['cleanStatus'] == "Keep") & (dta['Progress'] < 98), 'cleanStatus'] = 'Incomplete'


    if (debugging):
        # dta.cleanStatus.value_counts(dropna=False)
        # Check for repeat Prolific users
        len(dta.PID.unique())/len(dta.PID)

    dta.sort_values('StartDate', inplace=True)  # This now sorts in date order
    dta['DuplicatedPID'] = dta.PID.duplicated(keep='first')
    dta.loc[(dta['cleanStatus'] == "Keep") & (dta['DuplicatedPID']), 'cleanStatus'] = 'Dup PID'

    # dta['DuplicatedIP'] = dta.IPAddress.duplicated(keep='first')
    # dta.loc[(dta['cleanStatus'] == "Keep") & (dta['DuplicatedIP']), 'cleanStatus'] = 'Dup IPAddress'

    dta['PID_Length'] = dta.PID.map(str).apply(len)
    dta.loc[(dta['cleanStatus'] == "Keep") & (dta.PID_Length < 10), 'cleanStatus'] = 'Invalid PID'

    if (debugging):
        dta.cleanStatus.value_counts(dropna=False)

        dta['Duration (in seconds)'].describe()
        dta.loc[dta.surveyArm == "arm1_control", 'Duration (in seconds)'].describe()
        dta.loc[dta.surveyArm == "arm2_generalinfo", 'Duration (in seconds)'].describe()
        dta.loc[dta.surveyArm == "arm3_tips", 'Duration (in seconds)'].describe()
        dta.loc[dta.surveyArm == "arm4_training", 'Duration (in seconds)'].describe()

        dta.numReal.value_counts(dropna=False)
        dta.loc[(dta['cleanStatus'] == "Keep") & (dta.numReal == len(testQuestions.keys())), 'cleanStatus'] = 'Straightline_Real'
        dta.loc[(dta['cleanStatus'] == "Keep") & (dta.numReal == 0), 'cleanStatus'] = 'Straightline_Fake'
        grouped = dta.groupby("surveyArm")
        grouped.agg(["count"])
        grouped.cleanStatus.value_counts(dropna=False, normalize=True)
        # Interesting -- this is STRONGLY by arm. The training arm isn't straightining, the others are.
        # So, not somethin we can clean on.


    # dta.cleanStatus.value_counts(dropna=False)
    dta = dta[dta.cleanStatus == "Keep"].copy()
    # dta = dta[dta.Wave==5].copy()

    createRandomization = False
    if (createRandomization):
        dta['RAND'] = [random.randint(1, 2) for k in dta.index]
        dta.groupby(["RAND", "Wave", 'Ethnicity (Simplified)']).count()
        dta.groupby(["RAND", "Wave", 'Sex']).count()
        grouped = dta.groupby(["RAND", "Wave"])
        grouped.agg(["count"])
        grouped['Ethnicity (Simplified)'].count()
        grouped['Sex'].mean()

    # Setup Vars for tracking data on the # correct, etc.
    dta['numCorrect'] = 0
    dta['numFakeLabeledReal'] = 0 # It is FAKE, and the person thought it was a REAL
    dta['numRealLabeledFake'] = 0 # It is REAL, and the person thought it was a FAKE
    dta['numRealLabeledReal'] = 0 # It is REAL, and the person recognized it
    dta['numFakeLabeledFake'] = 0  # It is a FAKE, and the person recognized it

    dta['numLabeledReal'] = 0
    dta['numLabeledFake'] = 0
    dta['numNoAnswer'] = 0

    varsToSummarize = ['numCorrect', 'numFakeLabeledReal', 'numRealLabeledFake',
                       'numRealLabeledReal', 'numFakeLabeledFake',
                       'numLabeledReal', 'numLabeledFake',
                       'numNoAnswer']

    ''' Analzyze the answers'''
    for testQuestion in testQuestions.keys():
        # Get the correct answer
        correctAnswer = testQuestions[testQuestion]

        # Increment each peron's correct count if they go it
        correctMask = dta[testQuestion] == correctAnswer
        dta.loc[correctMask, 'numCorrect'] = 1 + dta.loc[correctMask, 'numCorrect']

        # Create a new boolean var indicating, for each question, if they got it right
        dta['Correct_' + testQuestion] = (dta[testQuestion] == correctAnswer)
        varsToSummarize = varsToSummarize + ['Correct_' + testQuestion]

        # Dig into the response correct/incorrect to label as true possitive / false positive , etc.
        if (correctAnswer == "Fake"):
            dta.loc[(dta[testQuestion] == "Real"), 'numFakeLabeledReal'] = 1 + dta.loc[(dta[testQuestion] == "Real"), 'numFakeLabeledReal']
            dta.loc[(dta[testQuestion] == "Fake"), 'numFakeLabeledFake'] = 1 + dta.loc[(dta[testQuestion] == "Fake"), 'numFakeLabeledFake']
        elif (correctAnswer == "Real"):
            dta.loc[(dta[testQuestion] == "Real"), 'numRealLabeledReal'] = 1 + dta.loc[(dta[testQuestion] == "Real"), 'numRealLabeledReal']
            dta.loc[(dta[testQuestion] == "Fake"), 'numRealLabeledFake'] = 1 + dta.loc[(dta[testQuestion] == "Fake"), 'numRealLabeledFake']
        else:
            raise Exception("Invalid Question Data")

        # Count how many total they marked as 'real' or 'fake'
        dta.loc[dta[testQuestion] == 'Real', 'numLabeledReal'] = 1 + dta.loc[dta[testQuestion] == 'Real', 'numLabeledReal']
        dta.loc[dta[testQuestion] == 'Fake', 'numLabeledFake'] = 1 + dta.loc[dta[testQuestion] == 'Fake', 'numLabeledFake']
        dta.loc[~(dta[testQuestion].isin(['Fake','Real'])), 'numNoAnswer'] = 1 + dta.loc[~(dta[testQuestion].isin(['Fake','Real'])), 'numNoAnswer']

    dta['percentCorrect'] = dta.numCorrect/len(testQuestions) * 100


    order_value_control_group = dta.loc[dta.surveyArm == "arm1_control", "numCorrect"]
    order_value_arm2_group = dta.loc[dta.surveyArm == "arm2_generalinfo", "numCorrect"]
    order_value_arm3_group = dta.loc[dta.surveyArm == "arm3_tips", "numCorrect"]
    order_value_arm4_group = dta.loc[dta.surveyArm == "arm4_training", "numCorrect"]

    np.std(dta.percentCorrect)
    tscore, pval = ttest_ind(order_value_control_group, order_value_arm4_group)
    # print('t-score:', round(tscore, 3))
    print('p value, control to arm4:', round(pval, 3))

    tscore, pval = ttest_ind(order_value_control_group, order_value_arm2_group)
    # print('t-score:', round(tscore, 3))
    print('p value, control to arm2:', round(pval, 3))

    tscore, pval = ttest_ind(order_value_arm2_group, order_value_arm4_group )
    # print('t-score:', round(tscore, 3))
    print('p value, arm2 to arm4:', round(pval, 3))

    grouped = dta[varsToSummarize + ["percentCorrect", "surveyArm", "Wave"]].groupby(["surveyArm", "Wave"])
    # grouped = dta[varsToSummarize + ["percentCorrect","surveyArm", "Wave"]].groupby(["surveyArm"])

    summaryStats = grouped.agg(["mean", "median"])
    summaryStats.sort_values(['Wave', 'surveyArm'], inplace=True)
    summaryStats.to_csv(dataDir + "RESULTS_" + dataFileName)

    # ##############
    # Demographic processing, etc
    # ##############
    dta['trustScore'] = dta['GeneralTrust'].replace({"Most people can't be trusted":0, "Most people can be trusted":1}) + \
                        dta['TakeAdvantage'].replace({"Would try to take advantage of you if they got a chance": 0, "Would try to be fair no matter what": 1}) + \
                        dta['TryToHelp'].replace({"Just look out for themselves": 0, "Try to help others": 1})

    dta['incomeAmount'] = dta['TotalIncome'].replace({"$0 - $19,999":10, "$20,000 - $39,999":30,
                        "$40,000 - $59,999":60, "$60,000 - $79,999":70, "$80,000 - $99,999":90,
                        "$100,000 - $149,999":125, "$150,000 or more":175})

    dta['race5'] = dta['Race'].replace({"White or Caucasian (Non-Hispanic)":'W',
                                               "Hispanic":'H',
                        "African American or African (Non-Hispanic)":'B',
                                               "Asian American or Asian":'A',
                                               "Native American, Native Hawaiian or Pacific Islander":'O',

                                        "White or Caucasian (Non-Hispanic),Hispanic": 'H',
                                        "White or Caucasian (Non-Hispanic),Native American, Native Hawaiian or Pacific Islander": 'O',
                                        "White or Caucasian (Non-Hispanic),Asian American or Asian":'A',
                        "I prefer not to say":'O'})
    dta['employment3'] = dta['Employment'].replace({"Employed, working 1-29 hours per week": 'U',
                                           "Employed, working 30 or more hours per week": 'E',
                                           "Retired": 'R',
                                           "Not employed, looking for work": 'U',
                                           "Not employed, NOT looking for work": 'U',
                                           "Disabled, not able to work": 'R'})

    dta['educYears'] = dta['Education'].replace({"Some high school": 8,
                "High school degree or equivalent (e.g., GED)": 12,
                "Some college but no degree": 13, "Associate degree": 14,
                "Bachelor degree": 16,
                "Graduate or professional degree": 18})

    dta['marriedI'] = dta['Married'].replace({"Married": 1,
                                             "Divorced or Separated": 0,
                                             "Widowed": 0, "Single": 0,
                                             "I prefer not to say": None})

    dta['ageYears'] = dta['Age'].replace({"Under 18": 16,
                                             "18-24": 21.5,
                                             "25-34": 29.5, "35-44": 39.5,
                                             "45-54": 49.5,
                                             "55-64": 59.5,
                                             "65 or older": 69.5,
                                             "Prefer not to say": None})

    dta['genderI'] = dta['Gender'].replace({"Male": 0,
                                             "Female": 1,
                                             "Other": None})
    dta['ageYearsSq'] = dta.ageYears * dta.ageYears
    dta['lIncomeAmount'] = np.log(dta.incomeAmount)

    # ##############
    # Regressions
    # ##############

    indepVars = ['surveyArm', 'trustScore', 'incomeAmount', 'race5', 'employment3', 'educYears', 'married2', 'ageYears', 'Gender']
    # What determines whether people get tricked or not?
    # Ie, false negatives
    resultTables = ols('numFakeLabeledReal ~ C(surveyArm) + trustScore + lIncomeAmount + '
              'C(race5) + C(employment3) + educYears + marriedI + ageYears + ageYearsSq + genderI', data=dta).fit().summary().tables()

    # Remove race - many variables, small counts - likely over specifying
    resultTables = ols('numFakeLabeledReal ~ C(surveyArm) + trustScore + lIncomeAmount + '
              'C(employment3) + educYears + marriedI + ageYears + ageYearsSq + genderI', data=dta).fit().summary().tables()

    resultTables = ols('numLabeledReal ~ C(surveyArm) + trustScore + lIncomeAmount + '
              'C(employment3) + educYears + marriedI + ageYears + ageYearsSq + genderI', data=dta).fit().summary().tables()


    # What determines who doesn't trust?
    # Ie, false positive
    resultTables = ols('numRealLabeledFake ~ C(surveyArm) + trustScore + lIncomeAmount + '
              'C(employment3) + educYears + marriedI + ageYears + ageYearsSq + genderI', data=dta).fit().summary().tables()

    resultTables = ols('numLabeledFake ~ C(surveyArm) + trustScore + lIncomeAmount + '
              'C(employment3) + educYears + marriedI + ageYears + ageYearsSq + genderI', data=dta).fit().summary().tables()




    # ##############
    # Save it
    # ##############
    dta.to_csv(dataDir + "PROCESSED_" + dataFileName)

    if (debugging):
        grouped.agg(["count"])
        grouped.percentCorrect.mean()
        grouped.numCorrect.mean()
        grouped.numReal.mean()
        grouped['Correct_ImportantInformation'].value_counts(dropna=False, normalize=True)
        grouped['Correct_AmazonPayment'].value_counts(dropna=False, normalize=True)
        grouped['Correct_AmazonDelay'].value_counts(dropna=False, normalize=True)
        grouped['Correct_RedCross'].value_counts(dropna=False, normalize=True)
        grouped['Correct_Disability'].value_counts(dropna=False, normalize=True)
        grouped['Correct_ssa_optout'].value_counts(dropna=False, normalize=True)
        grouped['Correct_replacementCard'].value_counts(dropna=False, normalize=True)
        grouped['Correct_annualReminderKLEW'].value_counts(dropna=False, normalize=True)
        grouped['Correct_lt_medicare'].value_counts(dropna=False, normalize=True)
        grouped['Correct_sms_disability'].value_counts(dropna=False, normalize=True)
        grouped['Correct_lt_suspension'].value_counts(dropna=False, normalize=True)
        grouped['Correct_sms_redcross'].value_counts(dropna=False, normalize=True)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    readdata()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
