import pandas as pd
import numpy as np
from statsmodels.formula.api import ols
from swstats import *
from scipy.stats import ttest_ind
import xlsxwriter
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.proportion import proportions_ztest

debugging = False

def pToSign(pval):
    if pval < .001:
        return "***"
    elif pval < .01:
        return "**"
    elif pval < .05:
        return "*"
    elif pval < .1:
        return "+"
    else:
        return ""

def analyzeExperiment_ContinuousVar(dta, varName):

    order_value_control_group = dta.loc[dta.surveyArm == "arm1_control", varName]
    order_value_arm2_group = dta.loc[dta.surveyArm == "arm2_written_techniques", varName]
    order_value_arm3_group = dta.loc[dta.surveyArm == "arm3_existingssa", varName]
    order_value_arm4_group = dta.loc[dta.surveyArm == "arm4_interactive_training", varName]


    # Arm 1
    arm1mean = np.mean(order_value_control_group)
    arm1sd = np.std(order_value_control_group)
    arm1text = "" + "{:.2f}".format(arm1mean) + " (" + "{:.2f}".format(arm1sd) + ")"

    # Effect of Arm 2
    arm2mean = np.mean(order_value_arm2_group)
    arm2sd = np.std(order_value_arm2_group)
    tscore, pval2 = ttest_ind(order_value_control_group, order_value_arm2_group)
    arm2sign = pToSign(pval2)
    arm2text = "" + "{:.2f}".format(arm2mean) + " (" + "{:.2f}".format(arm2sd) + ")" + arm2sign + " p:"  + "{:.3f}".format(pval2)

    # Effect of Arm 3
    arm3mean = np.mean(order_value_arm3_group)
    arm3sd = np.std(order_value_arm3_group)
    tscore, pval3 = ttest_ind(order_value_control_group, order_value_arm3_group)
    arm3sign = pToSign(pval3)
    arm3text = "" + "{:.2f}".format(arm3mean) + " (" + "{:.2f}".format(arm3sd) + ")" + arm3sign + " p:"  + "{:.3f}".format(pval3)

    # Effect of Arm 4
    arm4mean = np.mean(order_value_arm4_group)
    arm4sd = np.std(order_value_arm4_group)
    tscore, pval4 = ttest_ind(order_value_control_group, order_value_arm4_group)
    arm4sign = pToSign(pval4)
    arm4text = "" + "{:.2f}".format(arm4mean) + " (" + "{:.2f}".format(arm4sd) + ")" + arm4sign + " p:"  + "{:.3f}".format(pval4)

    # Correct P-values
    y = multipletests(pvals=[pval2, pval3, pval4], alpha=0.05, method="holm")
    # print(len(y[1][np.where(y[1] < 0.05)]))  # y[1] returns corrected P-vals (array)
    sigWithCorrection = y[1] < 0.05
    if sigWithCorrection[0]:
        arm2text = arm2text + ",#"
    if sigWithCorrection[1]:
        arm3text = arm3text + ",#"
    if sigWithCorrection[2]:
        arm4text = arm4text + ",#"

    # Additional checks
    tscore, pval2to4 = ttest_ind(order_value_arm2_group, order_value_arm4_group)
    arm2to4sign = pToSign(pval2to4)
    arm2to4text = "" + "{:.2f}".format(arm4mean - arm2mean) + " " + arm2to4sign + " p:" + "{:.3f}".format(pval2to4)

    tscore, pval3to4 = ttest_ind(order_value_arm3_group, order_value_arm4_group)
    arm3to4sign = pToSign(pval3to4)
    arm3to4text = "" + "{:.2f}".format(arm4mean - arm3mean) + " " + arm3to4sign + " p:" + "{:.3f}".format(pval3to4)


    results = {"Outcome": varName,
         "Arm1": arm1text,
         "Arm2": arm2text,
         "Arm3": arm3text,
         "Arm4": arm4text,
         "Arm2To4": arm2to4text,
         "Arm3To4": arm3to4text,
        }

    return results

def analyzeExperiment_BinaryVar(dta, varName):

    order_value_control_group = dta.loc[dta.surveyArm == "arm1_control", varName]
    order_value_arm2_group = dta.loc[dta.surveyArm == "arm2_written_techniques", varName]
    order_value_arm3_group = dta.loc[dta.surveyArm == "arm3_existingssa", varName]
    order_value_arm4_group = dta.loc[dta.surveyArm == "arm4_interactive_training", varName]

    # Arm 1
    arm1Successes = sum(order_value_control_group.isin([True, 1]))
    arm1Count = sum(order_value_control_group.isin([True, False, 1, 0]))
    arm1PercentSuccess = arm1Successes/arm1Count
    arm1text = "" + "{:.2f}".format(arm1PercentSuccess) + " (" + "{:.0f}".format(arm1Successes) + ")"

    # Effect of Arm 2
    arm2Successes = sum(order_value_arm2_group.isin([True, 1]))
    arm2Count = sum(order_value_arm2_group.isin([True, False, 1, 0]))
    arm2PercentSuccess = arm2Successes/arm2Count
    zstat, pval2 = proportions_ztest(count=[arm1Successes,arm2Successes], nobs=[arm1Count,arm2Count], alternative='two-sided')
    arm2sign = pToSign(pval2)
    arm2text = "" + "{:.2f}".format(arm2PercentSuccess) + " (" + "{:.0f}".format(arm2Successes) + ")" + arm2sign + " p:"  + "{:.3f}".format(pval2)

    # Effect of Arm 3
    arm3Successes = sum(order_value_arm3_group.isin([True, 1]))
    arm3Count = sum(order_value_arm3_group.isin([True, False, 1, 0]))
    arm3PercentSuccess = arm3Successes/arm3Count
    zstat, pval3 = proportions_ztest(count=[arm1Successes,arm3Successes], nobs=[arm1Count,arm3Count], alternative='two-sided')
    arm3sign = pToSign(pval3)
    arm3text = "" + "{:.2f}".format(arm3PercentSuccess) + " (" + "{:.0f}".format(arm3Successes) + ")" + arm3sign + " p:"  + "{:.3f}".format(pval3)

    # Effect of Arm 4
    arm4Successes = sum(order_value_arm4_group.isin([True, 1]))
    arm4Count = sum(order_value_arm4_group.isin([True, False, 1, 0]))
    arm4PercentSuccess = arm4Successes/arm4Count
    zstat, pval4 = proportions_ztest(count=[arm1Successes,arm4Successes], nobs=[arm1Count,arm4Count], alternative='two-sided')
    arm4sign = pToSign(pval4)
    arm4text = "" + "{:.2f}".format(arm4PercentSuccess) + " (" + "{:.0f}".format(arm4Successes) + ")" + arm4sign + " p:"  + "{:.3f}".format(pval4)

    # Correct P-values
    y = multipletests(pvals=[pval2, pval3, pval4], alpha=0.05, method="holm")
    # print(len(y[1][np.where(y[1] < 0.05)]))  # y[1] returns corrected P-vals (array)
    sigWithCorrection = y[1] < 0.05
    if sigWithCorrection[0]:
        arm2text = arm2text + ",#"
    if sigWithCorrection[1]:
        arm3text = arm3text + ",#"
    if sigWithCorrection[2]:
        arm4text = arm4text + ",#"

    # Additional checks
    zstat, pval2to4 = proportions_ztest(count=[arm2Successes,arm4Successes], nobs=[arm2Count,arm4Count], alternative='two-sided')
    arm2to4sign = pToSign(pval2to4)
    arm2to4text = "" + "{:.2f}".format(arm4PercentSuccess - arm2PercentSuccess) + " " + arm2to4sign + " p:" + "{:.3f}".format(pval2to4)

    zstat, pval3to4 = proportions_ztest(count=[arm3Successes,arm4Successes], nobs=[arm3Count,arm4Count], alternative='two-sided')
    arm3to4sign = pToSign(pval3to4)
    arm3to4text = "" + "{:.2f}".format(arm4PercentSuccess - arm3PercentSuccess) + " " + arm3to4sign + " p:" + "{:.3f}".format(pval3to4)

    results = {"Outcome": varName,
         "Arm1": arm1text,
         "Arm2": arm2text,
         "Arm3": arm3text,
         "Arm4": arm4text,
         "Arm2To4": arm2to4text,
         "Arm3To4": arm3to4text,
        }

    return results

def analyzeResults(dta, outputFileName, scoringVars, surveyVersion, primaryOnly=True):

    if primaryOnly:
        dta = dta[dta.IsPrimaryWave].copy()

    dataDir  = "C:/Dev/src/ssascams/data/"

    ''' Analyze the answers'''
    writer = pd.ExcelWriter(dataDir + 'RESULTS_' + outputFileName + '.xlsx', engine='xlsxwriter')

    # ###############
    # Export summary stats
    # ###############

    demographicVars = ['trustScore', 'TotalIncome', 'incomeAmount', 'Race', 'race5', 'employment3', 'educYears', 'Married', 'marriedI', 'Age', 'ageYears', 'Gender', 'genderI']
    allSummaryVars = ["percentCorrect", "surveyArm", "Wave", "daysFromTrainingToTest"] + scoringVars + demographicVars

    summaryStats = dta[allSummaryVars].describe()

    summaryStats.to_excel(writer, sheet_name="summary_FullPop", startrow=0, header=True, index=True)


    grouped = dta[allSummaryVars].groupby(["surveyArm"])
    summaryStats = grouped.describe().unstack().transpose().reset_index()
    summaryStats.rename(columns={'level_0' :'VarName', 'level_1' :'Metric'}, inplace=True)
    summaryStats.sort_values(['VarName', 'Metric'], inplace=True)
    summaryStats.to_excel(writer, sheet_name="summary_ByArm", startrow=0, header=True, index=False)

    if ~primaryOnly:
        grouped = dta[allSummaryVars].groupby(["surveyArm", "Wave"])
        summaryStats = grouped.describe().unstack().transpose().reset_index()
        summaryStats.rename(columns={'level_0' :'VarName', 'level_1' :'Metric'}, inplace=True)
        summaryStats.sort_values(['Wave','VarName', 'Metric'], inplace=True)
        # grouped.describe().reset_index().pivot(index='name', values='score', columns='level_1')

        summaryStats.to_excel(writer, sheet_name="summary_ByArmAndWave", startrow=0, header=True, index=False)

    # summaryStats.to_csv(dataDir + "RESULTS_" + outputFileName + '.csv')

    # ###############
    # RQ1: What is the effect?
    # ###############
    row1 = analyzeExperiment_ContinuousVar(dta, "numCorrect")
    row2 = analyzeExperiment_ContinuousVar(dta, "numFakeLabeledReal")
    row3 = analyzeExperiment_ContinuousVar(dta, "numRealLabeledFake")
    row4 = analyzeExperiment_ContinuousVar(dta, "percentCorrect")
    pd.DataFrame([row1, row2, row3, row4]).to_excel(writer, sheet_name="r1", startrow=1, header=True, index=True)

    ##############
    # RQ1* Robustness check on result: is the experiment randomized correctly?
    ##############
    # NumCorrect Regression
    resultTables = ols('numCorrect ~ C(surveyArm) + daysFromTrainingToTest + trustScore + lIncomeAmount + '
                     'C(employment3) + educYears + marriedI + ageYears + ageYearsSq + genderI + lose_moneyYN + duration_p2_Quantile ', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="r1_reg", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="r1_reg", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    # ###############
    # RQ2: Communication Type
    # ###############
    row1 = analyzeExperiment_ContinuousVar(dta, "numEmailsCorrect")
    row2 = analyzeExperiment_ContinuousVar(dta, "numSMSesCorrect")
    row3 = analyzeExperiment_ContinuousVar(dta, "numLettersCorrect")
    pd.DataFrame([row1, row2, row3]).to_excel(writer, sheet_name="r2", startrow=1, header=True, index=True)

    ##############
    # RQ2* Robustness check on Emails result: is the experiment randomized correctly?
    ##############
    # NumEmailsCorrect Regression
    resultTables = ols('numEmailsCorrect ~ C(surveyArm) + daysFromTrainingToTest + trustScore + lIncomeAmount + '
                     'C(employment3) + educYears + marriedI + ageYears + ageYearsSq + genderI + lose_moneyYN + duration_p2_Quantile ', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="r2_reg", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="r2_reg", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    # ###############
    # RQ3: Time Delay
    # ###############
    resultTables = ols('numCorrect ~ C(surveyArm)*Wave + daysFromTrainingToTest', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="r3a_CorrectWaveAndDay_Simple", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="r3a_CorrectWaveAndDay_Simple", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    resultTables = ols('numEmailsCorrect ~ C(surveyArm)*Wave + daysFromTrainingToTest', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="r3b_EmailWaveAndDay_Simple", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="r3b_EmailWaveAndDay_Simple", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    # ###############
    # RQ4: Rainloop
    # ###############
    if surveyVersion == '6':
        resultTables = ols('NumHeadersOpened ~ C(surveyArm)', data=dta).fit().summary().tables
        pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="r4_HeadersOpened", startrow=1, header=False, index=False)
        pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="r4_HeadersOpened",startrow=1 + len(resultTables[0]) + 2, header=False, index=False)


    ########################
    # R5a: What determines fraud susceptibility (whether people get tricked or not)?
    # Ie, false negatives
    ########################

    # First Try on Regression
    # resultTables = ols('numFakeLabeledReal ~ C(surveyArm) + daysFromTrainingToTest + trustScore + lIncomeAmount + '
    #                   'C(race5) + C(employment3) + educYears + marriedI + ageYears + ageYearsSq + genderI + lose_moneyYN + duration_p2_Quantile ', data=dta).fit().summary().tables
    # pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="reg_numFakeLabeledReal_WRace", startrow=1, header=False, index=False)
    # pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="reg_numFakeLabeledReal_WRace", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    # Remove race - many variables, small counts - likely over specifying
    resultTables = ols('numFakeLabeledReal ~ C(surveyArm) + daysFromTrainingToTest + trustScore + lIncomeAmount + '
                       'C(employment3) + educYears + marriedI + ageYears + ageYearsSq + genderI + lose_moneyYN + duration_p2_Quantile ', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="r5a_numFakeLabeledReal", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="r5a_numFakeLabeledReal", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    resultTables = ols('numLabeledReal ~ C(surveyArm) + trustScore + lIncomeAmount + C(employment3) + educYears + marriedI + ageYears + ageYearsSq + genderI + lose_moneyYN + duration_p2_Quantile ', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="reg_numLabeledReal", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="reg_numLabeledReal", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)


    ########################
    # R5b: What determines lack of trust?
    ########################
    # Ie, false positive
    resultTables = ols('numRealLabeledFake ~ C(surveyArm) + daysFromTrainingToTest + trustScore + lIncomeAmount + '
                       'C(employment3) + educYears + marriedI + ageYears + ageYearsSq + genderI + lose_moneyYN + duration_p2_Quantile ', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="r5b_numRealLabeledFake", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="r5b_numRealLabeledFake", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    resultTables = ols('numLabeledFake ~ C(surveyArm) + daysFromTrainingToTest + trustScore + lIncomeAmount + '
                       'C(employment3) + educYears + marriedI + ageYears + ageYearsSq + genderI + lose_moneyYN + duration_p2_Quantile ', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="reg_numLabeledFake", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="reg_numLabeledFake", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    # ###############
    # RQ6: Impostor Type
    # ###############
    row1 = analyzeExperiment_ContinuousVar(dta, "numCorrect_SSA")
    row2 = analyzeExperiment_ContinuousVar(dta, "numCorrect_Other")
    row3 = analyzeExperiment_ContinuousVar(dta, "numEmailsCorrect_SSA")
    row4 = analyzeExperiment_ContinuousVar(dta, "numEmailsCorrect_Other")
    pd.DataFrame([row1, row2, row3, row4]).to_excel(writer, sheet_name="r6", startrow=1, header=True, index=True)

    # ###############
    # RQ7: Likelihood of being tricked
    # ###############
    dta['isTrickedByFraud'] = dta.numFakeLabeledReal > 0
    dta['isTrickedByAnySSAEmail'] = dta.numEmailsCorrect_SSA < max(dta.numEmailsCorrect_SSA)
    dta['isTrickedByAnyNonSSAEmail'] = dta.numEmailsCorrect_Other < max(dta.numEmailsCorrect_Other)

    row1 = analyzeExperiment_BinaryVar(dta, "isTrickedByFraud")
    row2 = analyzeExperiment_BinaryVar(dta, "isTrickedByAnySSAEmail")
    row3 = analyzeExperiment_BinaryVar(dta, "isTrickedByAnyNonSSAEmail")
    pd.DataFrame([row1, row2, row3]).to_excel(writer, sheet_name="r7", startrow=1, header=True, index=True)

    # ###############
    # RQ8: Every Email
    # ###############
    filter_cols = [col for col in dta.columns if col.startswith('Correct_')]
    theRows = []
    for filter_col in filter_cols:
        arow = analyzeExperiment_BinaryVar(dta, filter_col)
        theRows = theRows + [arow]

    pd.DataFrame(theRows).to_excel(writer, sheet_name="r8", startrow=1, header=True, index=True)


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

    # Full regression, within each specific wave, with controls
    startRow = 1
    for wave in dta.Wave.unique():
        # worksheet = writer.book.add_worksheet("numCorrect_ByArmAndWave")
        # worksheet.write(startRow, 1, 'Wave ' + str(wave))
        # startRow = startRow + 2
        resultTables = ols('numCorrect ~ C(surveyArm) + lIncomeAmount + ageYears + ageYearsSq + educYears + marriedI +  genderI', data=dta.loc[dta.Wave==wave]).fit().summary().tables
        pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="numCorrect_ByArmInWave", startrow=startRow, header=False, index=False)
        startRow = startRow + len(resultTables[0]) + 2
        pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="numCorrect_ByArmInWave", startrow=startRow, header=False, index=False)
        startRow = startRow + len(resultTables[1]) + 2

    startRow = 1
    for wave in dta.Wave.unique():
        # worksheet = writer.book.add_worksheet("numEmailsCorrect_ByArmAndWave")
        # worksheet.write(startRow, 1, 'Wave ' + str(wave))
        # startRow = startRow + 2
        resultTables = ols('numEmailsCorrect ~ C(surveyArm) + lIncomeAmount + ageYears + ageYearsSq + educYears + marriedI +  genderI', data=dta.loc[dta.Wave == wave]).fit().summary().tables
        pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="numEmailsCorrect_ByArmInWave", startrow=startRow, header=False, index=False)
        startRow = startRow + len(resultTables[0]) + 2
        pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="numEmailsCorrect_ByArmInWave", startrow=startRow, header=False, index=False)
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
    # Is there an effect of wave: Additional Exporation
    ##############
    # NumCorrect Regression
    resultTables = ols('numCorrect ~ C(surveyArm)*Wave + daysFromTrainingToTest + trustScore + lIncomeAmount + '
                     'C(employment3) + educYears + marriedI + ageYears + ageYearsSq + genderI + lose_moneyYN + duration_p2_Quantile ', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="reg_CorrectWithWaveAndDays", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="reg_CorrectWithWaveAndDays", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

    resultTables = ols('numCorrect ~ C(surveyArm)*Wave + trustScore + lIncomeAmount + '
                     'C(employment3) + educYears + marriedI + ageYears + ageYearsSq + genderI + lose_moneyYN + duration_p2_Quantile ', data=dta).fit().summary().tables
    pd.DataFrame(resultTables[0]).to_excel(writer, sheet_name="reg_CorrectWithWave", startrow=1, header=False, index=False)
    pd.DataFrame(resultTables[1]).to_excel(writer, sheet_name="reg_CorrectWithWave", startrow=1 + len(resultTables[0]) + 2, header=False, index=False)

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
