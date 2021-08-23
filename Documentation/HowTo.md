# Social Security Scams

Here, you'll learn how to use the Social Security Scam package.  

The process of setting up a research study occurs in four parts:

1) Setup the opening survey in the package of your choice. We'll use Qualtrics for this example.  That survey should have 
a) any demographic information you need,
b) the training process you want participants to undertake
c) a call to the SSA API, https://k2gy69kvfc.execute-api.us-east-2.amazonaws.com/prod/email, to create a record for the individual in the backend system (GoPhish, database and email)

2) Setup the campaigns you want 
a) Log into GoPhish
b) Create a new Group under Users and Groups. You'll need to enter 1 test email address to start the group.
	Make note of the exact name of this Group -- you'll need to set it in Qualtrics later.
c) Under Email Templates, create the emails you want to send.
d) under Sending Profiles, create the sender information you want to use to send those emails
	Interace: SMTP
	Host: iredmail:465
	Username: performance1@behavioralsurvey.com
	password: 
	
	In particular, you'll want to set the Email Header: "Reply-To" to the appropriate value for your study 
e) Under Campaigns, create one campaign for each Email Template : Sending Profile pair and assign to your group.  
   The combination of all three (Template, Profile, and Group) defines a campaign, is needed for each outbound email in GoPhish. 
   If you have existing campaigns, you can skip steps c and d, and instead make a copy of the existing campaign (double checking the template and profile, and assigning it for your new group)
   
   URL: test.com
   Landing Page: test
f) Go back into your survey package from Step 1, and ensure the group name used in the API call is the one you've created for this research.

3) Test the system
a) Start with first wave of the survey - covering the training process.
b) Check that the data is properly stored in the survey package's database (Qualtrics, etc).   Especially, check that the ID for the person is stored -- that's required to connect results across systems.
c) Log into GoPhish, click on your group, and ensure that the sample users were created
d) Log into RainLoop 


4) Provide the survey to participants
a) Send them to first wave of the survey - covering the training process.
b) Check that the 

Key Addresses:
1) GoPhish: https://3.20.89.142:3333/login   Admin / Gophish1234
2) RainLoop: http://3.20.89.142:7000/  [ID]@behavioralsurvey.com / Password1234*
3) Dynamo DB: 

https://docs.aws.amazon.com/cli/latest/reference/dynamodb/scan.html
aws dynamodb scan --table-name YOURTABLE --output text > outputfile.txt

aws dynamodb scan --table-name Emails --output json > emails.json
aws dynamodb scan --table-name Survey_Answers --output text > Survey_Answers.txt
aws dynamodb scan --table-name User_Actions --output text > User_Actions.txt
aws dynamodb scan --table-name User_Events --output json > User_Events.json

aws dynamodb scan --table-name Emails --output json > emails.json
--filter-expression "RESEARCH_NAME = :a"
-- a:{"S": "SSA Fraud v5 Dynata"}
				
Tables:				
Emails
Survey_Answers
User_Actions
User_Events


Credentials

GoPhish https://3.20.89.142:3333/
admin
Gophish1234

iredmail
3.20.89.142
postmaster@behavior.com
pass1234

rainloop
3.20.89.142:7000?admin
admin
1234




