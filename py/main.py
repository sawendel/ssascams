# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
import os
from scipy.stats import ttest_ind
import numpy as np

from swstats import *

trainingQuestions = {'CyberAttack':'Fake',
                    'ProtectYourself':'Real',
                     'AnnualReminder':'Real',
                     'CovidSSA':'Fake',
                     'GetProtected':'Fake'}
testQuestions = {'ImportantInformation': 'Real',
                 'AmazonPayment': 'Fake',
                 'AmazonDelay':'Real',
                 'RedCross':'Fake',
                 'Disability':'Fake'}


def readdata():
    # dta = pd.read_csv("C:/Dev/sensitive_data/CFS/SSA_February14_Clean.csv")
    dta = pd.read_csv("C:/Dev/sensitive_data/CFS/SSA_February 14_Test2_Clean.csv")

    dta['numCorrect'] = 0

    for testQuestion in testQuestions.keys():
        correctAnswer = testQuestions[testQuestion]
        dta.loc[dta[testQuestion] == correctAnswer, 'numCorrect'] = 1 + dta.loc[dta[testQuestion] == correctAnswer, 'numCorrect']

    dta.surveyArm.fillna(value="Unknown", inplace=True)

    order_value_control_group = dta.loc[dta.surveyArm == "arm1_control", "numCorrect"]
    order_value_arm2_group = dta.loc[dta.surveyArm == "arm2_generalinfo", "numCorrect"]
    order_value_arm3_group = dta.loc[dta.surveyArm == "arm3_control", "numCorrect"]
    order_value_arm4_group = dta.loc[dta.surveyArm == "arm4_training", "numCorrect"]
    tscore, pval = ttest_ind(order_value_control_group, order_value_arm4_group)
    print('t-score:', round(tscore, 3))
    print('p value:', round(pval, 3))

    tscore, pval = ttest_ind(order_value_control_group, order_value_arm2_group)
    print('t-score:', round(tscore, 3))
    print('p value:', round(pval, 3))

    tscore, pval = ttest_ind(order_value_arm2_group, order_value_arm4_group )
    print('t-score:', round(tscore, 3))
    print('p value:', round(pval, 3))

    grouped = dta.groupby("surveyArm")

    grouped.agg(["count"])
    grouped.numCorrect.mean()
    grouped['ImportantInformation'].value_counts(dropna=False, normalize=True)
    grouped['AmazonPayment'].value_counts(dropna=False, normalize=True)
    grouped['AmazonDelay'].value_counts(dropna=False, normalize=True)
    grouped['RedCross'].value_counts(dropna=False, normalize=True)
    grouped['Disability'].value_counts(dropna=False, normalize=True)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    readdata()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
