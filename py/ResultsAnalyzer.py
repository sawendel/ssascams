import pandas as pd
import numpy as np
from statsmodels.formula.api import ols
from swstats import *
from scipy.stats import ttest_ind
import xlsxwriter

debugging = False
def analyzeResults(dta, outputFileName, scoringVars, surveyVersion):
    dataDir  = "C:/Dev/src/ssascams/data/"
    ''' Analyze the answers'''
    writer = pd.ExcelWriter(dataDir + 'RESULTS_' + outputFileName + '.xlsx', engine='xlsxwriter')

    # ###############
    # Export summary stats
    # ###############

    demographicVars = ['trustScore', 'TotalIncome', 'incomeAmount', 'Race', 'race5', 'employment3', 'educYears', 'Married', 'marriedI', 'Age', 'ageYears', 'Gender', 'genderI']
    allSummaryVars = ["percentCorrect", "surveyArm", "Wave"] + scoringVars + demographicVars

    summaryStats = dta[allSummaryVars].describe()

    summaryStats.to_excel(writer, sheet_name="summary_FullPop", startrow=0, header=True, index=True)


    grouped = dta[allSummaryVars].groupby(["surveyArm", "Wave"])
    # grouped = dta[varsToSummarize + ["percentCorrect","surveyArm", "Wave"]].groupby(["surveyArm"])
    # summaryStats = grouped.agg(["mean", "median"])
    # summaryStats.sort_values(['Wave', 'surveyArm'], inplace=True)

    # descriptiveStats = pd.DataFrame(group.describe().rename(columns={'score': name}).squeeze()
    #                   for name, group in dta.groupby('surveyArm, Wave'))

    summaryStats = grouped.describe().unstack().transpose().reset_index()
    summaryStats.rename(columns={'level_0' :'VarName', 'level_1' :'Metric'}, inplace=True)
    summaryStats.sort_values(['Wave','VarName', 'Metric'], inplace=True)
    # grouped.describe().reset_index().pivot(index='name', values='score', columns='level_1')

    summaryStats.to_excel(writer, sheet_name="summary_ByArmAndWave", startrow=0, header=True, index=False)

    # summaryStats.to_csv(dataDir + "RESULTS_" + outputFileName + '.csv')


    # ##############
    # Between Arm T-Tests
    # ##############

    order_value_control_group = dta.loc[dta.surveyArm == "arm1_control", "numCorrect"]
    order_value_arm2_group = dta.loc[dta.surveyArm == "arm2_generalinfo", "numCorrect"]
    order_value_arm3_group = dta.loc[dta.surveyArm == "arm3_tips", "numCorrect"]
    order_value_arm4_group = dta.loc[dta.surveyArm == "arm4_training", "numCorrect"]

    np.std(dta.percentCorrect)
    tscore, pval = ttest_ind(order_value_control_group, order_value_arm4_group)
    # print('t-score:', round(tscore, 3))
    print('NumCorrect: p value, control to arm4 (Interactive):', round(pval, 3))

    tscore, pval = ttest_ind(order_value_control_group, order_value_arm2_group)
    # print('t-score:', round(tscore, 3))
    print('NumCorrect: p value, control to arm2 (Tips):', round(pval, 3))

    tscore, pval = ttest_ind(order_value_arm2_group, order_value_arm4_group )
    print('NumCorrect: p value, arm2 (Tips) to arm4 (Interactive):', round(pval, 3))

    tscore, pval = ttest_ind(order_value_arm3_group, order_value_arm4_group)
    print('NumCorrect: p value, arm3 (GeneralInfo) to arm4 (Interactive):', round(pval, 3))



    order_value_control_group = dta.loc[dta.surveyArm == "arm1_control", "numEmailsCorrect"]
    order_value_arm2_group = dta.loc[dta.surveyArm == "arm2_generalinfo", "numEmailsCorrect"]
    order_value_arm3_group = dta.loc[dta.surveyArm == "arm3_tips", "numEmailsCorrect"]
    order_value_arm4_group = dta.loc[dta.surveyArm == "arm4_training", "numEmailsCorrect"]

    np.std(dta.percentCorrect)
    tscore, pval = ttest_ind(order_value_control_group, order_value_arm4_group)
    # print('t-score:', round(tscore, 3))
    print('NumEmailsCorrect: p value, control to arm4 (Interactive):', round(pval, 3))

    tscore, pval = ttest_ind(order_value_control_group, order_value_arm2_group)
    # print('t-score:', round(tscore, 3))
    print('NumEmailsCorrect: p value, control to arm2 (Tips):', round(pval, 3))

    tscore, pval = ttest_ind(order_value_arm2_group, order_value_arm4_group )
    print('NumEmailsCorrect: p value, arm2 (Tips) to arm4 (Interactive):', round(pval, 3))

    tscore, pval = ttest_ind(order_value_arm3_group, order_value_arm4_group)
    print('NumEmailsCorrect: p value, arm3 (GeneralInfo) to arm4 (Interactive):', round(pval, 3))

    # ##############
    # Regressions
    # ##############

    indepVars = ['surveyArm', 'trustScore', 'incomeAmount', 'race5', 'employment3', 'educYears', 'married2', 'ageYears','Gender']


    # Simple Experiment-Only test
    resultTables = ols('numCorrect ~ C(surveyArm)', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="numCorrect_ByArm", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="numCorrect_ByArm", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    resultTables = ols('numEmailsCorrect ~ C(surveyArm)', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="numEmailsCorrect_ByArm", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="numEmailsCorrect_ByArm", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    resultTables = ols('numLettersCorrect ~ C(surveyArm)', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="numLettersCorrect_ByArm", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="numLettersCorrect_ByArm", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    resultTables = ols('numSMSesCorrect ~ C(surveyArm)', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="numSMSesCorrect_ByArm", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="numSMSesCorrect_ByArm", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    if (surveyVersion in ['5D', '5P']):
        resultTables = ols('NumHeadersOpened ~ C(surveyArm)', data=dta).fit().summary().tables
        pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="NumHeadersOpened_ByArm", startrow=1, header=False, index=False)
        pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="NumHeadersOpened_ByArm", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

        resultTables = ols('NumEmailsActedUpon ~ C(surveyArm)', data=dta).fit().summary().tables
        pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="NumEmailsActedUpon_ByArm", startrow=1, header=False, index=False)
        pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="NumEmailsActedUpon_ByArm", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

        resultTables = ols('numLabeledFake ~ C(surveyArm)', data=dta).fit().summary().tables
        pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="numLabeledFake_ByArm", startrow=1, header=False, index=False)
        pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="numLabeledFake_ByArm", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    resultTables = ols('numFakeLabeledFake ~ C(surveyArm)', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="numFakeLabeledFake_ByArm", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="numFakeLabeledFake_ByArm", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    resultTables = ols('numRealLabeledReal ~ C(surveyArm)', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="numRealLabeledReal_ByArm", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="numRealLabeledReal_ByArm", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)


    # What determines fraud susceptibility (whether people get tricked or not)?
    # Ie, false negatives


    # First Try
    resultTables = ols('numFakeLabeledReal ~ C(surveyArm) + trustScore + lIncomeAmount + '
                       'C(race5) + C(employment3) + educYears + marriedI + ageYears + ageYearsSq + genderI', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="numFakeLabeledReal_WRace", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="numFakeLabeledReal_WRace", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)


    # Remove race - many variables, small counts - likely over specifying
    resultTables = ols('numFakeLabeledReal ~ C(surveyArm) + trustScore + lIncomeAmount + '
                       'C(employment3) + educYears + marriedI + ageYears + ageYearsSq + genderI', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="numFakeLabeledReal", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="numFakeLabeledReal", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    resultTables = ols('numLabeledReal ~ C(surveyArm) + trustScore + lIncomeAmount + '
                       'C(employment3) + educYears + marriedI + ageYears + ageYearsSq + genderI', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="numLabeledReal", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="numLabeledReal", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)


    # What determines lack of trust?
    # Ie, false positive
    resultTables = ols('numRealLabeledFake ~ C(surveyArm) + trustScore + lIncomeAmount + '
                       'C(employment3) + educYears + marriedI + ageYears + ageYearsSq + genderI', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="numRealLabeledFake", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="numRealLabeledFake", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    resultTables = ols('numLabeledFake ~ C(surveyArm) + trustScore + lIncomeAmount + '
                       'C(employment3) + educYears + marriedI + ageYears + ageYearsSq + genderI', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="numLabeledFake", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="numLabeledFake", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    # ##############
    # Save the processed data
    # ##############
    pd.DataFrame(dta).to_excel(writer, sheet_name="theData", startrow=0, header=True, index=False)
    # dta.to_csv(dataDir + "PROCESSED_" + outputFileName + ".csv")
    writer.save()
    # workbook.close()

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
