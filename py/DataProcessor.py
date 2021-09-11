import pandas as pd
import numpy as np
import random


debugging = False


def getPIDs(dataDir, fileNames):
    pids = set()
    for theFileName in fileNames:
        dta = pd.read_csv(dataDir + theFileName)
        pids.update(dta.PID)
    return pids

def processRainloopData(dataDir, dataFileName_p1, dataFileName_p2, surveyVersion, surveyOutputFilesByVersion, dynamoResearchNames):
    dta_p1 = pd.read_csv(dataDir + dataFileName_p1, dtype = {'pid': str})
    # Dynata has a lower case 'pid', Prolific has an uppercase.
    dta_p1.rename(columns={'pid':"PID"},inplace=True)
    # dta_profilic = pd.read_csv(dataDir + dataFileName_prolific)
    dta_p2 = pd.read_csv(dataDir + dataFileName_p2, dtype = {'pid': str})
    dta_p2.rename(columns={'pid':"PID"},inplace=True)
    # dta_p2.drop(columns={'surveyArm'})

    # dta = dta_p1.merge(dta_profilic, right_on="participant_id", left_on = "PID", how="left")
    dta = dta_p1.merge(dta_p2, right_on="PID", left_on="PID", how="left", suffixes=["", "_p2"])

    priorPids = getPIDs(dataDir, [surveyOutputFilesByVersion['1'], surveyOutputFilesByVersion['3'],
                                  surveyOutputFilesByVersion['4']])

    # import re
    # string = open(dataDir + "SSA_v5_emails.json").read()
    # new_str = re.sub('[^\x00-\x7F]+', ' ', string)
    # open(dataDir + "SSA_v5_emails_ascii.json", 'w').write(new_str)

    emails = pd.read_json(dataDir + "Shared/emails.json", orient='records')
    for field in ['USER_ID', 'EMAIL', 'GOPHISH_GROUP_NAME', 'RESEARCHER_NAME', 'INTERVENTION_ID', 'RESEARCH_NAME','LOGIN_LINK', 'FIRST_NAME']:
        emails[field + '_clean'] = emails[field].apply(
            lambda x: "" if ((x is np.NaN) or (x == "")) else (x.get('S') if isinstance(x, dict) else str(x)))
    # emails.to_csv(dataDir + "test_email_export.csv")
    # Subset emails to the ones for this study
    # emails = emails.loc[emails.RESEARCH_NAME_clean.isin(dynamoResearchNames)].copy()

    dta = dta.merge(emails, left_on="PID", right_on="USER_ID_clean", how="left", suffixes=["", "_emails"])
    dta['NoMatchingDynamoEmail'] = dta.USER_ID.isna()

    events = pd.read_json(dataDir + "Shared/User_Events.json", orient='records')
    for field in ['EVENT', 'MODE', 'USER_ID', 'EMAIL_ID', 'RESEARCH_NAME', 'POSTTIME', 'USERID_MAILID',
                  'RESEARCHER_NAME', 'INTERVENTION_ID']:
        events[field + '_clean'] = events[field].apply(
            lambda x: "" if ((x is np.NaN) or (x == "")) else (x.get('S') if isinstance(x, dict) else str(x)))
    events.to_csv(dataDir + "test_event_export_" + surveyVersion + ".csv")
    # Subset events to the ones for this purpose
    # events = events.loc[events.RESEARCH_NAME_clean.isin(dynamoResearchNames)].copy()

    ## TODO -- check that ALL messages have at least a few correct answers
    emailIdMapping = {"ssaInfo-1": 'ImportantInformation',
                      "AmazonPay-1": 'AmazonPayment',
                      "AmazonMask-1": 'AmazonDelay',
                      "Redcross-1": 'RedCross',
                      "Disabilty-1": 'Disability',
                      "ssaopOut-1": 'ssa_optout',
                      "SSA-ReplacementCard-1": 'replacementCard',
                      "SSA-AnnualReminder-KLEW-1": 'annualReminderKLEW'
                      }

    dta['NumEmailsActedUpon'] = 0
    dta['NumHeadersOpened'] = 0

    for emailId in emailIdMapping.keys():
        val = emailIdMapping[emailId]
        eventsForEmail = events.loc[events.EMAIL_ID_clean == emailId]
        idsWithOpen = eventsForEmail.loc[eventsForEmail.EVENT_clean == "Open", "USER_ID_clean"].tolist()
        idsWithOpenHeaders = eventsForEmail.loc[eventsForEmail.EVENT_clean == "Open Headers", "USER_ID_clean"].tolist()
        idsWithTrustAction = eventsForEmail.loc[eventsForEmail.EVENT_clean.isin(
            ["Reply", "Click on Reply All", "Click on Links", "Click on Forward"]), "USER_ID_clean"].tolist()
        idsWithDisTrustAction = eventsForEmail.loc[eventsForEmail.EVENT_clean.isin(
            ["Click on Spam", "Click on Archive", "Click on Delete"]), "USER_ID_clean"].tolist()

        dta['Opened_' + val] = dta.PID.isin(idsWithOpen)
        dta['OpenedHeaders_' + val] = dta.PID.isin(idsWithOpenHeaders)
        dta['TrustAction_' + val] = dta.PID.isin(idsWithTrustAction)
        dta['DistrustAction_' + val] = dta.PID.isin(idsWithDisTrustAction)

        dta[val] = 'Real'  # The default is to assume people thought it was real, unless they flagged it otherwise
        dta.loc[dta['DistrustAction_' + val], val] = 'Fake'

        dta['NoAction_' + val] = ((~dta['Opened_' + val]) & (~dta['OpenedHeaders_' + val]) & \
                                  (~dta['TrustAction_' + val]) & (~dta['DistrustAction_' + val]))

        dta['NumEmailsActedUpon'] = dta['NumEmailsActedUpon'] + (~dta['NoAction_' + val])
        dta['NumHeadersOpened'] = dta['NumHeadersOpened'] + (dta['OpenedHeaders_' + val])

    dta.to_csv(dataDir + "test_processed_data_" + surveyVersion + ".csv")
    dta = dta.loc[dta.NumEmailsActedUpon >= 4].copy()
    dta.to_csv(dataDir + "test_processed_data_subset_" + surveyVersion + ".csv")

    return (dta, priorPids)

def processTwoPartQualtricsTestResults(dataDir, dataFileName_p1, dataFileName_p2, dataFileName_prolific, surveyOutputFilesByVersion):
    dta_p1 = pd.read_csv(dataDir + dataFileName_p1)
    dta_profilic = pd.read_csv(dataDir + dataFileName_prolific)
    dta_p2 = pd.read_csv(dataDir + dataFileName_p2)
    dta_p2.drop(columns={'surveyArm'})

    dta = dta_p1.merge(dta_profilic, right_on="participant_id", left_on="PID", how="left")
    dta = dta.merge(dta_p2, right_on="PID", left_on="PID", how="left", suffixes=["", "_p2"])

    priorPids = getPIDs(dataDir, [surveyOutputFilesByVersion['1'], surveyOutputFilesByVersion['3']])

    return (dta, priorPids)


def getTestQuestions(surveyVersion):
    if (surveyVersion == '1' or surveyVersion == '2'):
        testQuestions = {'ImportantInformation': ('Real', 'Email', 'SSA'),
                         'AmazonPayment': ('Fake', 'Email', 'Amazon'),
                         'AmazonDelay': ('Real', 'Email', 'Amazon'),
                         'RedCross': ('Fake', 'Email', 'RedCross'),
                         'Disability': ('Fake', 'Email', 'Lawyer'),
                         }
    elif surveyVersion == '3':  # There was an unintentional mistake in the SSA_Optout and Replacement Card in v3
        testQuestions = {'ImportantInformation': ('Real', 'Email', 'Amazon'),
                         'AmazonPayment': ('Fake', 'Email', 'Amazon'),
                         'AmazonDelay': ('Real', 'Email', 'Amazon'),
                         'RedCross': ('Fake', 'Email', 'RedCross'),
                         'Disability': ('Fake', 'Email', 'Lawyer'),
                         'ssa_optout': ('Fake', 'Email', 'SSA'),
                         'replacementCard': ('Fake', 'Email', 'SSA'),
                         'annualReminderKLEW': ('Fake', 'Email', 'SSA'),
                         'lt_medicare': ('Real', 'Letter', 'SSA'),
                         'sms_disability': ('Fake', 'SMS', 'SSA'),
                         'lt_suspension': ('Fake', 'Letter', 'SSA'),
                         'sms_redcross': ('Real', 'SMS', 'RedCross')
                         }
    else:
        testQuestions = {'ImportantInformation': ('Real', 'Email', 'Amazon'),
                         'AmazonPayment': ('Fake', 'Email', 'Amazon'),
                         'AmazonDelay': ('Real', 'Email', 'Amazon'),
                         'RedCross': ('Fake', 'Email', 'RedCross'),
                         'Disability': ('Fake', 'Email', 'Lawyer'),
                         'ssa_optout': ('Fake', 'Email', 'SSA'),
                         'replacementCard': ('Real', 'Email', 'SSA'),
                         'annualReminderKLEW': ('Fake', 'Email', 'SSA'),
                         'lt_medicare': ('Real', 'Letter', 'SSA'),
                         'sms_disability': ('Fake', 'SMS', 'SSA'),
                         'lt_suspension': ('Fake', 'Letter', 'SSA'),
                         'sms_redcross': ('Real', 'SMS', 'RedCross')
                         }
    return testQuestions


def readData(surveyVersion):

    dataDir  = "C:/Dev/src/ssascams/data/"

    surveyOutputFilesByVersion = {'1': "V1_AllQualtrics_ProlificPopulation/SSA_v1_asFielded_ExtractedMay 15, 2021_clean.csv",
                   '3': "V3_ImmediateTest_AllQualtrics_ProlificPopulation/SSA_v3_asFielded_ExtractedMay 9, 2021_clean.csv",
                   '4': "V4_WithDelay_AllQualtrics_ProlificPopulation/SSA_v4_asFielded_Part1_ExtractedMay 13, 2021.csv",
                  '5P': "V5_1_WithDelay_Rainloop_ProlificPopulation/SSA_v5_Part1_Prolific_July 8, 2021_17.29_clean.csv",
                  '5D': "V5_2_WithDelay_Rainloop_DynataPopulation/SSA_v5_Part1_Dynata_June 28, 2021_18.36_clean.csv",
                  '6': "v6/SSA_v6_Part1_Prolific_August 16, 2021_20.15_clean.csv"}


    # ###############
    # Get the data
    # ###############

    priorPids = None
    if surveyVersion == '1':
        dataFileName = surveyOutputFilesByVersion['1']
        dta = pd.read_csv(dataDir + dataFileName)
    elif surveyVersion == '3':
        dataFileName = surveyOutputFilesByVersion['3']
        dta = pd.read_csv(dataDir + dataFileName)
        priorPids =  getPIDs(dataDir, [surveyOutputFilesByVersion[1]])

    elif surveyVersion == '4':
        dataFileName_p1 = surveyOutputFilesByVersion['4']
        dataFileName_prolific = "V4_WithDelay_AllQualtrics_ProlificPopulation/prolific_export_SSA_v4_Wave2NatRep_6099c49373d406738c79f948.csv"
        dataFileName_p2 = "V4_WithDelay_AllQualtrics_ProlificPopulation/SSA_v4_Part2_AllQualtrics_May 23, 2021_15.52_clean.csv"

        (dta, priorPids) = processTwoPartQualtricsTestResults(dataDir, dataFileName_p1, dataFileName_p2, dataFileName_prolific, surveyOutputFilesByVersion)


    elif surveyVersion == '5P': # Prolific
        dataFileName_p1 = surveyOutputFilesByVersion['5P']
        # dataFileName_prolific = "prolific_export_SSA_v4_Wave2NatRep_6099c49373d406738c79f948.csv"

        if True:
            dataFileName_p2 = "V5_1_WithDelay_Rainloop_ProlificPopulation/SSA_v5_Part2_Prolific_Rainloop_July 8, 2021_17.10_clean.csv"
            dataFileName_p2wave3 = "V5_1_WithDelay_Rainloop_ProlificPopulation/SSA_v5_Part2_Wave3_Rainloop_Prolific_July 17, 2021_14.03_clean.csv"

            dataFileName_p2_1 = pd.read_csv(dataDir + dataFileName_p2, dtype={'pid': str})
            dataFileName_p2_2 = pd.read_csv(dataDir + dataFileName_p2wave3, dtype={'pid': str})
            dataFileName_p2combined = pd.concat([dataFileName_p2_1,dataFileName_p2_2], ignore_index=True)
            dataFileName_p2combined.to_csv(dataDir + "V5_1_WithDelay_Rainloop_ProlificPopulation/SSA_v5_Part2_Combined.csv", index=False)

        dataFileName_p2 = "V5_1_WithDelay_Rainloop_ProlificPopulation/SSA_v5_Part2_Combined.csv"
        # dataFileName_p2 = "V5_1_WithDelay_Rainloop_ProlificPopulation/SSA_v5_Part2_Prolific_Rainloop_July 8, 2021_17.10_clean.csv"

        dynamoResearchNames = ["SSA Fraud v5 Prolific","SSA Fraud"]

        (dta, priorPids) = processRainloopData(dataDir, dataFileName_p1, dataFileName_p2, surveyVersion, surveyOutputFilesByVersion, dynamoResearchNames)

    elif surveyVersion == '5D': # Dynata
        dataFileName_p1 = surveyOutputFilesByVersion['5D']
        dataFileName_p2 = "V5_2_WithDelay_Rainloop_DynataPopulation/SSA_v5_Part2_Rainloop_Dynata_July 13, 2021_17.00_clean.csv"
        dynamoResearchNames = ["SSA Fraud v5 Dynamo","SSA Fraud"]

        (dta, priorPids) = processRainloopData(dataDir, dataFileName_p1, dataFileName_p2, surveyVersion,  surveyOutputFilesByVersion, dynamoResearchNames)

    elif surveyVersion == '6':
        dataFileName_p1 = surveyOutputFilesByVersion['6']
        dataFileName_p2 = "v6/SSA_v6_Part2_Rainloop_Prolific_September 8, 2021_19.12_clean.csv"
        dynamoResearchNames = ["SSA Fraud v6 Prolific"]

        (dta, priorPids) = processRainloopData(dataDir, dataFileName_p1, dataFileName_p2, surveyVersion,  surveyOutputFilesByVersion, dynamoResearchNames)

    outputFileName = "SSA_v" + str(surveyVersion)

    # remove empty columns
    dta = dta.dropna(axis=1, how='all')

    # Some early data had this arm mislabeled
    dta.surveyArm.replace({"notSet": "arm4_training"}, inplace=True)

    # I changed the names in v6, to be clearer. Update the rest to follow
    dta.surveyArm.replace({
        "arm2_generalinfo": "arm2_written_techniques",
        "arm3_tips": "arm3_existingssa",
        "arm4_training": "arm4_interactive_training",
    }, inplace=True)

    dta.surveyArm.fillna(value="Unknown", inplace=True)

    # Mark the Various Waves of the Study
    dta['StartDate'] = pd.to_datetime(dta.StartDate)

    # ###############
    # Tag Waves of Study over time
    # ###############

    dta['Wave'] = None
    dta['IsPrimaryWave'] = False

    if surveyVersion == '3':
        # Small tests to see if it was working
        dta.loc[(dta.StartDate < '2021-05-08 10:00'), 'Wave'] = 1
        dta.loc[(dta.StartDate >= '2021-05-08 10:00') & (dta.StartDate < '2021-05-08 13:00'), 'Wave'] = 2
        # 3: Full test
        dta.loc[(dta.StartDate >= '2021-05-08 13:00') & (dta.StartDate < '2021-05-08 17:00'), 'Wave'] = 3
        # 4: Added Stronger Language to clarify purpose; REAL and FAKE
        dta.loc[(dta.StartDate >= '2021-05-08 17:00') & (dta.StartDate < '2021-05-08 23:59'), 'Wave'] = 4
        # 5: Mobile Only Version of 1; Has Updated Files meant for Study Version 4
        dta.loc[(dta.StartDate >= '2021-05-09 08:00') & (dta.StartDate < '2021-05-10 10:00'), 'Wave'] = 5

        dta.loc[dta.Wave == 3, "IsPrimaryWave"] = True

    elif surveyVersion == '4':
        dta.loc[(dta.StartDate < '5/9/2021 23:59'), 'Wave'] = 1
        dta.loc[(dta.StartDate >= '5/9/2021 23:59'), 'Wave'] = 2
        dta.loc[(dta.StartDate_p2 >= '5/20/2021 01:01'), 'Wave'] = 3

        dta.loc[dta.Wave.isin([2, 3]), "IsPrimaryWave"] = True

    elif surveyVersion == '5P': # Prolific
        dta.loc[(dta.StartDate_p2 >= '7/14/2021 01:01'), 'Wave'] = 3
        dta.loc[(dta.StartDate_p2 <= '7/14/2021 01:01'), 'Wave'] = 2
        dta.loc[(dta.StartDate_p2 < '6/30/2021 01:01'), 'Wave'] = 1
        dta['IsPrimaryWave'] = True

    elif surveyVersion == '5D': # Dynata
        dta['Wave'] = 1
        dta['IsPrimaryWave'] = True

    elif surveyVersion == '6':  # Final Prolific
        dta['Wave'] = 1
        dta.loc[(dta.StartDate < '8/1/2021 23:59'), 'Wave'] = 1
        dta.loc[(dta.StartDate >= '8/1/2021 23:59'), 'Wave'] = 2
        dta.loc[(dta.StartDate_p2 >= '8/31/2021 10:00'), 'Wave'] = 3
        dta.loc[dta.Wave.isin([2]), "IsPrimaryWave"] = True

    else:
        dta.Wave = 1
        dta['IsPrimaryWave'] = True

    # print(dta.Wave.value_counts(dropna=False))

    dta.rename(columns={'Previous Fraud':'previousFraud',    # From V5
                        'Previously_Targeted':'previousFraud', 'Lost_Money':'lose_money', # From v4
                        'Duration (in seconds)':'duration_p1',
                        'Duration (in seconds)_p2':'duration_p2'}, inplace=True)

    dta['previousFraudYN'] = ~dta.previousFraud.isna()
    dta['lose_moneyYN'] = dta.lose_money == "Yes"
    dta['duration_p1_Quantile'] = pd.qcut(dta.duration_p1, q=5, labels=False)
    dta['duration_p2_Quantile'] = pd.qcut(dta.duration_p2, q=5, labels=False)

    dta['daysFromTrainingToTest'] = (dta['StartDate_p2'].astype('datetime64') - dta['StartDate'].astype('datetime64')).dt.days

    return (dta, priorPids)



def cleanData(dta, priorPids, surveyVersion, testQuestions):
    # ###############
    # Do core data cleaning / filtering
    # ###############

    dta['cleanStatus'] = "Keep"
    dta.loc[(dta['cleanStatus'] == "Keep") & (dta.PID.isin(priorPids)), 'cleanStatus'] = 'PID from prior version'

    if surveyVersion == '3':
        dta.loc[(dta['cleanStatus'] == "Keep") & (dta['Duration (in seconds)'] < 60*3), 'cleanStatus'] = 'Too Fast'
    elif surveyVersion == '4':
        dta.loc[(dta['cleanStatus'] == "Keep") & (dta['status'] == 'RETURNED'), 'cleanStatus'] = 'Task Returned'
        dta.loc[(dta['cleanStatus'] == "Keep") & (dta['Progress_p2'].isna()), 'cleanStatus'] = 'No Second Round'
        dta.loc[(dta['cleanStatus'] == "Keep") & (dta['Progress_p2'] <= 95), 'cleanStatus'] = 'Incomplete Round 2'
    elif surveyVersion == '5P' or surveyVersion == '5D':
        dta.loc[(dta['cleanStatus'] == "Keep") & (dta['duration_p1'] < 60*2), 'cleanStatus'] = 'Too Fast'
        dta.loc[(dta['cleanStatus'] == "Keep") & (dta['Progress_p2'].isna()), 'cleanStatus'] = 'No Second Round'
        dta.loc[(dta['cleanStatus'] == "Keep") & (dta['Progress_p2'] <= 95), 'cleanStatus'] = 'Incomplete Round 2'
        dta.loc[(dta['cleanStatus'] == "Keep") & (dta['Consent_p2'] == 'No'), 'cleanStatus'] = 'No Consent Round 2'


    # dta.loc[(dta['cleanStatus'] == "Keep") & (dta['statusCode'] != 200), 'cleanStatus'] = 'Email Error'
    dta.loc[(dta['cleanStatus'] == "Keep") & (dta['Consent'] == 'No'), 'cleanStatus'] = 'No Consent'
    dta.loc[(dta['cleanStatus'] == "Keep") & (dta['Progress'] <= 95), 'cleanStatus'] = 'Incomplete'


    if (debugging):
        # dta.cleanStatus.value_counts(dropna=False)
        # Check for repeat Prolific users
        len(dta.PID.unique())/len(dta.PID)

    dta.sort_values('StartDate', inplace=True)  # This now sorts in date order
    dta['DuplicatedPID'] = False
    dta.loc[(dta['cleanStatus'] == "Keep"), 'DuplicatedCleanPID'] = dta.loc[(dta['cleanStatus'] == "Keep"), 'PID'].duplicated(keep='first')
    dta.loc[(dta['cleanStatus'] == "Keep") & (dta['DuplicatedCleanPID']), 'cleanStatus'] = 'Dup PID within current Version'

    # dta['DuplicatedIP'] = dta.IPAddress.duplicated(keep='first')
    # dta.loc[(dta['cleanStatus'] == "Keep") & (dta['DuplicatedIP']), 'cleanStatus'] = 'Dup IPAddress'

    dta['PID_Length'] = dta.PID.map(str).apply(len)
    dta.loc[(dta['cleanStatus'] == "Keep") & (dta.PID_Length < 10), 'cleanStatus'] = 'Invalid PID'

    if (debugging):
        dta.cleanStatus.value_counts(dropna=False)

        dta['duration_p1'].describe()
        dta.loc[dta.surveyArm == "arm1_control", 'duration_p1'].describe()
        dta.loc[dta.surveyArm == "arm2_written_techniques", 'duration_p1'].describe()
        dta.loc[dta.surveyArm == "arm3_existingssa", 'duration_p1'].describe()
        dta.loc[dta.surveyArm == "arm4_interactive_training", 'duration_p1'].describe()

        dta.numReal.value_counts(dropna=False)
        dta.loc[(dta['cleanStatus'] == "Keep") & (dta.numReal == len(testQuestions.keys())), 'cleanStatus'] = 'Straightline_Real'
        dta.loc[(dta['cleanStatus'] == "Keep") & (dta.numReal == 0), 'cleanStatus'] = 'Straightline_Fake'
        grouped = dta.groupby("surveyArm")
        grouped.agg(["count"])
        grouped.cleanStatus.value_counts(dropna=False, normalize=True)
        # Interesting -- this is STRONGLY by arm. The training arm isn't straightining, the others are.
        # So, not something we can clean on.


    # dta.cleanStatus.value_counts(dropna=False)
    dta = dta[dta.cleanStatus == "Keep"].copy()
    # dta = dta[dta.Wave==5].copy()

    return dta


def processDemographics(dta):

    # ################
    # Randomization
    # ################

    createRandomization = False
    if (createRandomization):
        dta['RAND'] = [random.randint(1, 2) for k in dta.index]
        dta.groupby(["RAND", "Wave", 'Ethnicity (Simplified)']).count()
        dta.groupby(["RAND", "Wave", 'Sex']).count()
        grouped = dta.groupby(["RAND", "Wave"])
        grouped.agg(["count"])
        grouped['Ethnicity (Simplified)'].count()
        grouped['Sex'].mean()


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
                                        'White or Caucasian (Non-Hispanic),African American or African (Non-Hispanic)':'B',
                                        'White or Caucasian (Non-Hispanic),African American or African (Non-Hispanic),Native American, Native Hawaiian or Pacific Islander':'O',
                                        'Asian American or Asian,Hispanic':'O',
                                        'Asian American or Asian,African American or African (Non-Hispanic)':'O',
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

    return dta


def markCorrectAnswers(dta, testQuestions):
    # ##############
    # Count Correct Answers
    # ##############

    # Setup Vars for tracking data on the # correct, etc.
    dta['numCorrect'] = 0
    dta['numFakeLabeledReal'] = 0 # It is FAKE, and the person thought it was a REAL
    dta['numRealLabeledFake'] = 0 # It is REAL, and the person thought it was a FAKE
    dta['numRealLabeledReal'] = 0 # It is REAL, and the person recognized it
    dta['numFakeLabeledFake'] = 0  # It is a FAKE, and the person recognized it

    dta['numEmailsCorrect'] = 0
    dta['numLettersCorrect'] = 0
    dta['numSMSesCorrect'] = 0

    dta['numCorrect_SSA'] = 0
    dta['numCorrect_Other'] = 0
    dta['numEmailsCorrect_SSA'] = 0
    dta['numEmailsCorrect_Other'] = 0

    dta['numLabeledReal'] = 0
    dta['numLabeledFake'] = 0
    dta['numNoAnswer'] = 0

    scoringVars = ['numCorrect', 'numEmailsCorrect', 'numLettersCorrect', 'numSMSesCorrect', 'numFakeLabeledReal', 'numRealLabeledFake',
                       'numRealLabeledReal', 'numFakeLabeledFake',  'numLabeledReal', 'numLabeledFake', 'numNoAnswer']

    for testQuestion in testQuestions.keys():
        # Get the correct answer
        correctAnswer = testQuestions[testQuestion][0]
        messageType = testQuestions[testQuestion][1]
        messageSender = testQuestions[testQuestion][2]

        # Increment each peron's correct count if they go it
        correctMask = dta[testQuestion] == correctAnswer
        dta.loc[correctMask, 'numCorrect'] = 1 + dta.loc[correctMask, 'numCorrect']

        if messageType == "Email":
            dta.loc[correctMask, 'numEmailsCorrect'] = 1 + dta.loc[correctMask, 'numEmailsCorrect']
        elif messageType == "Letter":
            dta.loc[correctMask, 'numLettersCorrect'] = 1 + dta.loc[correctMask, 'numLettersCorrect']
        elif messageType == "SMS":
            dta.loc[correctMask, 'numSMSesCorrect'] = 1 + dta.loc[correctMask, 'numSMSesCorrect']

        if messageSender == "SSA":
            dta.loc[correctMask, 'numCorrect_SSA'] = 1 + dta.loc[correctMask, 'numCorrect_SSA']
            if messageType == "Email":
                dta.loc[correctMask, 'numEmailsCorrect_SSA'] = 1 + dta.loc[correctMask, 'numEmailsCorrect_SSA']
        else:
            dta.loc[correctMask, 'numCorrect_Other'] = 1 + dta.loc[correctMask, 'numCorrect_Other']
            if messageType == "Email":
                dta.loc[correctMask, 'numEmailsCorrect_Other'] = 1 + dta.loc[correctMask, 'numEmailsCorrect_Other']


        # Create a new boolean var indicating, for each question, if they got it right
        dta['Correct_' + testQuestion] = (dta[testQuestion] == correctAnswer)
        scoringVars = scoringVars + ['Correct_' + testQuestion]

        # Dig into the response correct/incorrect to label as true positive / false positive , etc.
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

    return dta