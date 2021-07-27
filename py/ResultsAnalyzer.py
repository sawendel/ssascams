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


    grouped = dta[allSummaryVars].groupby(["surveyArm"])
    summaryStats = grouped.describe().unstack().transpose().reset_index()
    summaryStats.rename(columns={'level_0' :'VarName', 'level_1' :'Metric'}, inplace=True)
    summaryStats.sort_values(['VarName', 'Metric'], inplace=True)
    summaryStats.to_excel(writer, sheet_name="summary_ByArm", startrow=0, header=True, index=False)

    grouped = dta[allSummaryVars].groupby(["surveyArm", "Wave"])
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
    # Correlations
    ################

    indepVars = ['surveyArm', 'daysFromTrainingToTest', 'Wave', 'trustScore', 'incomeAmount', 'race5', 'employment3', 'educYears', 'marriedI', 'ageYears','Gender',
                 'previousFraudYN', 'lose_moneyYN', 'duration_p1', 'duration_p1_Quantile', 'duration_p2', 'duration_p2_Quantile', 'Employment']

    depVars = ['numCorrect', 'numFakeLabeledReal', 'numRealLabeledFake']

    dta.Wave = dta.Wave.astype('float64')
    # Look at  Correlations among variables
    allVarsToCorr = depVars + indepVars
    corrMatrix = dta[allVarsToCorr].corr()
    pd.DataFrame(corrMatrix).to_excel(writer, sheet_name="corrMatrix", startrow=1, header=True, index=True)
    # duration_p1 is a proxy for arm, so strange results there.
    # we'd need a fine-tuned var. Let's use p2 instead.  Also, the Quantile shows a much stronger relationship than the raw values (likely since it is not linear in the depvars)
    # Losing money and income and age show a moderate relationship


    # ##############
    # Scatter Plots
    ################

    import seaborn as sns
    sns.set_theme(style="ticks")

    toPlot = dta[['numCorrect', 'surveyArm', 'daysFromTrainingToTest', 'Wave', 'trustScore', 'lose_moneyYN', 'duration_p2_Quantile']]
    sns.pairplot(toPlot, hue="surveyArm")

    # ##############
    # Regressions
    # ##############

    # Sanity Check regression
    resultTables = ols('lIncomeAmount ~ageYears + ageYearsSq + educYears + marriedI +  genderI', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="reg_Sanity", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="reg_Sanity", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    # Simple Experiment-Only test
    resultTables = ols('numCorrect ~ C(surveyArm)', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="numCorrect_ByArm", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="numCorrect_ByArm", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    resultTables = ols('numEmailsCorrect ~ C(surveyArm)', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="numEmailsCorrect_ByArm", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="numEmailsCorrect_ByArm", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    startRow = 1
    for wave in dta.Wave.unique():
        # worksheet = writer.book.add_worksheet("numCorrect_ByArmAndWave")
        # worksheet.write(startRow, 1, 'Wave ' + str(wave))
        # startRow = startRow + 2
        resultTables = ols('numCorrect ~ C(surveyArm)', data=dta.loc[dta.Wave==wave]).fit().summary().tables
        pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="numCorrect_ByArmAndWave", startrow=startRow, header=False, index=False)
        startRow = startRow + len(resultTables[0]) + 2
        pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="numCorrect_ByArmAndWave", startrow=startRow, header=False, index=False)
        startRow = startRow + len(resultTables[1]) + 2

    startRow = 1
    for wave in dta.Wave.unique():
        # worksheet = writer.book.add_worksheet("numEmailsCorrect_ByArmAndWave")
        # worksheet.write(startRow, 1, 'Wave ' + str(wave))
        # startRow = startRow + 2
        resultTables = ols('numEmailsCorrect ~ C(surveyArm)', data=dta).fit().summary().tables
        pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="numEmailsCorrect_ByArmAndWave", startrow=startRow, header=False, index=False)
        startRow = startRow + len(resultTables[0]) + 2
        pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="numEmailsCorrect_ByArmAndWave", startrow=startRow, header=False, index=False)
        startRow = startRow + len(resultTables[1]) + 2


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


    ## ###########
    # Is there an effect of wave?
    ##############
    # NumCorrect Regression
    resultTables = ols('numEmailsCorrect ~ C(surveyArm)*Wave + daysFromTrainingToTest + trustScore + lIncomeAmount + '
                     'C(employment3) + educYears + marriedI + ageYears + ageYearsSq + genderI + lose_moneyYN + duration_p2_Quantile ', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="reg_CorrectWithWaveAndDays", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="reg_CorrectWithWaveAndDays", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    resultTables = ols('numEmailsCorrect ~ C(surveyArm)*Wave + daysFromTrainingToTest', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="reg_CorrectWaveAndDay_Simple", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="reg_CorrectWaveAndDay_Simple", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    resultTables = ols('numEmailsCorrect ~ C(surveyArm)*Wave + trustScore + lIncomeAmount + '
                     'C(employment3) + educYears + marriedI + ageYears + ageYearsSq + genderI + lose_moneyYN + duration_p2_Quantile ', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="reg_CorrectWithWave", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="reg_CorrectWithWave", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    ##############
    # Robustness check on Emails result: is the experiment randomized correctly?
    ##############
    # NumEmailsCorrect Regression
    resultTables = ols('numEmailsCorrect ~ C(surveyArm) + daysFromTrainingToTest + trustScore + lIncomeAmount + '
                     'C(employment3) + educYears + marriedI + ageYears + ageYearsSq + genderI + lose_moneyYN + duration_p2_Quantile ', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="reg_EmailsCorrect", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="reg_EmailsCorrect", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)


    ########################
    # What determines fraud susceptibility (whether people get tricked or not)?
    ########################
    # Ie, false negatives

    # First Try on Regression
    resultTables = ols('numFakeLabeledReal ~ C(surveyArm) + daysFromTrainingToTest + trustScore + lIncomeAmount + '
                       'C(race5) + C(employment3) + educYears + marriedI + ageYears + ageYearsSq + genderI + lose_moneyYN + duration_p2_Quantile ', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="reg_numFakeLabeledReal_WRace", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="reg_numFakeLabeledReal_WRace", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    # Remove race - many variables, small counts - likely over specifying
    resultTables = ols('numFakeLabeledReal ~ C(surveyArm) + daysFromTrainingToTest + trustScore + lIncomeAmount + '
                       'C(employment3) + educYears + marriedI + ageYears + ageYearsSq + genderI + lose_moneyYN + duration_p2_Quantile ', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="reg_numFakeLabeledReal", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="reg_numFakeLabeledReal", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    resultTables = ols('numLabeledReal ~ C(surveyArm) + trustScore + lIncomeAmount + '
                       'C(employment3) + educYears + marriedI + ageYears + ageYearsSq + genderI + lose_moneyYN + duration_p2_Quantile ', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="reg_numLabeledReal", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="reg_numLabeledReal", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)


    # What determines lack of trust?
    # Ie, false positive
    resultTables = ols('numRealLabeledFake ~ C(surveyArm) + daysFromTrainingToTest + trustScore + lIncomeAmount + '
                       'C(employment3) + educYears + marriedI + ageYears + ageYearsSq + genderI + lose_moneyYN + duration_p2_Quantile ', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="reg_numRealLabeledFake", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="reg_numRealLabeledFake", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    resultTables = ols('numLabeledFake ~ C(surveyArm) + daysFromTrainingToTest + trustScore + lIncomeAmount + '
                       'C(employment3) + educYears + marriedI + ageYears + ageYearsSq + genderI + lose_moneyYN + duration_p2_Quantile ', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="reg_numLabeledFake", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="reg_numLabeledFake", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

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
