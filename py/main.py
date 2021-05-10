# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
import os
from scipy.stats import ttest_ind
import numpy as np

from swstats import *

surveyVersion = 3

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
    elif surveyVersion == 3:
        # dataFileName = "SSA_v3_May 9, 2021_08.18_clean.csv"
        dataFileName = "SSA_v3_asFielded_May 10, 2021_07.41_clean.csv"
    elif surveyVersion == 4:
        dataFileName = "SSA_v3_May 9, 2021_08.18_clean.csv"


    # dta = pd.read_csv("C:/Dev/sensitive_data/CFS/SSA_February 14_Test2_Clean.csv")
    dta = pd.read_csv(dataDir + dataFileName)

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
    else:
        dta.Wave = 1

    print(dta.Wave.value_counts(dropna=False))


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

    ''' Data Cleaning '''
    dta['cleanStatus'] = "Keep"
    dta.loc[(dta['cleanStatus'] == "Keep") & (dta['Duration (in seconds)'] < 60*3), 'cleanStatus'] = 'Too Fast'
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

    order_value_control_group = dta.loc[dta.surveyArm == "arm1_control", "numCorrect"]
    order_value_arm2_group = dta.loc[dta.surveyArm == "arm2_generalinfo", "numCorrect"]
    order_value_arm3_group = dta.loc[dta.surveyArm == "arm3_tips", "numCorrect"]
    order_value_arm4_group = dta.loc[dta.surveyArm == "arm4_training", "numCorrect"]

    dta['percentCorrect'] = dta.numCorrect/12 * 100
    np.std(dta.percentCorrect)
    tscore, pval = ttest_ind(order_value_control_group, order_value_arm4_group)
    # print('t-score:', round(tscore, 3))
    print('p value:', round(pval, 3))

    tscore, pval = ttest_ind(order_value_control_group, order_value_arm2_group)
    # print('t-score:', round(tscore, 3))
    print('p value:', round(pval, 3))

    tscore, pval = ttest_ind(order_value_arm2_group, order_value_arm4_group )
    # print('t-score:', round(tscore, 3))
    print('p value:', round(pval, 3))

    grouped = dta[varsToSummarize + ["percentCorrect", "surveyArm", "Wave"]].groupby(["surveyArm", "Wave"])
    # grouped = dta[varsToSummarize + ["percentCorrect","surveyArm", "Wave"]].groupby(["surveyArm"])

    summaryStats = grouped.agg(["mean", "median"])
    summaryStats.sort_values(['Wave', 'surveyArm'], inplace=True)
    summaryStats.to_csv(dataDir + "RESULTS_" + dataFileName)
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
