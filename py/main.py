# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
import os
from scipy.stats import ttest_ind
import numpy as np

from swstats import *

debugging = False
trainingQuestions = {'CyberAttack':'Fake',
                    'ProtectYourself':'Real',
                     'AnnualReminder':'Real',
                     'CovidSSA':'Fake',
                     'GetProtected':'Fake',
                     'lt_favorable':'Real'}

testQuestions = {'ImportantInformation':'Real',
                 'AmazonPayment':'Fake',
                 'AmazonDelay':'Real',
                 'RedCross':'Fake',
                 'Disability':'Fake',
                 'ssa_optout':'Real',
                 'replacementCard':'Real',
                 'annualReminderKLEW':'Fake',
                 'lt_medicare':'Real',
                 'sms_disability':'Fake',
                 'lt_suspension':'Fake',
                 'sms_redcross':'Real'
                 }


def readdata():
    # dta = pd.read_csv("C:/Dev/sensitive_data/CFS/SSA_February14_Clean.csv")
    # dta = pd.read_csv("C:/Dev/sensitive_data/CFS/SSA_February 14_Test2_Clean.csv")
    dta = pd.read_csv("C:/Dev/src/ssascams/data/SSA_v3_May 9, 2021_08.18_clean.csv")

    dta = dta[dta.Wave==4].copy()

    # Some early data had this arm mislabeled
    dta.surveyArm.replace({"notSet": "arm4_training"}, inplace=True)

    '''
    dta['Duration (in seconds)'].describe()
    dta.loc[dta.surveyArm == "arm1_control", 'Duration (in seconds)'].describe()
    dta.loc[dta.surveyArm == "arm2_generalinfo", 'Duration (in seconds)'].describe()
    dta.loc[dta.surveyArm == "arm3_tips", 'Duration (in seconds)'].describe()
    dta.loc[dta.surveyArm == "arm4_training", 'Duration (in seconds)'].describe()
    '''

    dta['cleanStatus'] = "Keep"
    dta.loc[(dta['cleanStatus'] == "Keep") & (dta['Duration (in seconds)'] < 60*3), 'cleanStatus'] = 'Too Fast'

    dta['numCorrect'] = 0
    dta['numReal'] = 0

    for testQuestion in testQuestions.keys():
        correctAnswer = testQuestions[testQuestion]
        dta.loc[dta[testQuestion] == correctAnswer, 'numCorrect'] = 1 + dta.loc[dta[testQuestion] == correctAnswer, 'numCorrect']
        dta.loc[dta[testQuestion] == 'Real', 'numReal'] = 1 + dta.loc[dta[testQuestion] == 'Real', 'numReal']
        dta['Correct_' + testQuestion] = (dta[testQuestion] == correctAnswer)

    dta.surveyArm.fillna(value="Unknown", inplace=True)

    # dta.cleanStatus.value_counts(dropna=False)
    # dta.numReal.value_counts(dropna=False)

    if (debugging):
        dta.loc[(dta['cleanStatus'] == "Keep") & (dta.numReal == len(testQuestions.keys())), 'cleanStatus'] = 'Straightline_Real'
        dta.loc[(dta['cleanStatus'] == "Keep") & (dta.numReal == 0), 'cleanStatus'] = 'Straightline_Fake'
        grouped = dta.groupby("surveyArm")
        grouped.agg(["count"])
        grouped.cleanStatus.value_counts(dropna=False, normalize=True)
        # Interesting -- this is STRONGLY by arm. The training arm isn't straightining, the others are.
        # So, not somethin we can clean on.

    dta.cleanStatus.value_counts(dropna=False)
    dta = dta[dta.cleanStatus == "Keep"].copy()

    order_value_control_group = dta.loc[dta.surveyArm == "arm1_control", "numCorrect"]
    order_value_arm2_group = dta.loc[dta.surveyArm == "arm2_generalinfo", "numCorrect"]
    order_value_arm3_group = dta.loc[dta.surveyArm == "arm3_tips", "numCorrect"]
    order_value_arm4_group = dta.loc[dta.surveyArm == "arm4_training", "numCorrect"]

    tscore, pval = ttest_ind(order_value_control_group, order_value_arm4_group)
    # print('t-score:', round(tscore, 3))
    print('p value:', round(pval, 3))

    tscore, pval = ttest_ind(order_value_control_group, order_value_arm2_group)
    # print('t-score:', round(tscore, 3))
    print('p value:', round(pval, 3))

    tscore, pval = ttest_ind(order_value_arm2_group, order_value_arm4_group )
    # print('t-score:', round(tscore, 3))
    print('p value:', round(pval, 3))

    grouped = dta.groupby("surveyArm")

    grouped.agg(["count"])
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
