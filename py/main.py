# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
import numpy as np
from DataProcessor import *
from ResultsAnalyzer import *
import random

surveyVersion = '5D'

debugging = False
trainingQuestions = {'CyberAttack':'Fake',
                     'ProtectYourself':'Real',
                     'AnnualReminder':'Real',
                     'CovidSSA':'Fake',
                     'GetProtected':'Fake',
                     'lt_favorable':'Real'}

def doIt(surveyVersion):

    testQuestions = getTestQuestions(surveyVersion)

    (dta,priorPids) = readData(surveyVersion)

    dta = cleanData(dta, priorPids, surveyVersion, testQuestions)

    dta = processDemographics(dta)

    dta = markCorrectAnswers(dta, testQuestions)

    scoringVars = ['numCorrect', 'numEmailsCorrect', 'numLettersCorrect', 'numSMSesCorrect', 'numFakeLabeledReal', 'numRealLabeledFake',
                           'numRealLabeledReal', 'numFakeLabeledFake', 'numLabeledReal', 'numLabeledFake', 'numNoAnswer']

    if (surveyVersion in ['5D', '5P']):
        scoringVars = scoringVars + ['NumHeadersOpened']

    analyzeResults(dta, outputFileName = surveyVersion, scoringVars = scoringVars, surveyVersion = surveyVersion)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    doIt("4")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
