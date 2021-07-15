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
c) Under Email Templates, create the emails you want to send.
d) under Sending Profiles, create the sender information you want to use to send those emails
e) Under Campaigns, create one campaign for each Email Template : Sending Profile pair and assign to your group.  
   The combination of all three (Template, Profile, and Group) defines a campaign, is needed for each outbound email in GoPhish. 
   If you have existing campaigns, you can skip steps c and d, and instead make a copy of the existing campaign (double checking the template and profile, and assigning it for your new group)
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
				
https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_json.html
				
Emails
Survey_Answers
User_Actions
User_Events


https://uwmadison.co1.qualtrics.com/jfe/form/SV_8tVZyOYluXZGvCS?psid=vRW8bp6ZNeM7snM4FB-oyASW2**&pid=1111111111111&Preview=Survey
https://uwmadison.co1.qualtrics.com/jfe/form/SV_8tVZyOYluXZGvCS?psid=vRW8bp6ZNeM7snM4FB-oyASW3**&pid=sw3&Preview=Survey
https://uwmadison.co1.qualtrics.com/jfe/form/SV_8tVZyOYluXZGvCS?psid=vRW8bp6ZNeM7snM4FB-oyASW4**&pid=sw4&Preview=Survey

---


## Endpoints

<br>

**API URL for production:** https://k2gy69kvfc.execute-api.us-east-2.amazonaws.com/prod 

<br>

### <u>Add New Email to the list</u>

Given the user ID, gophish group, first name, last name, researcher name, research name and intervention id it stores it in the data base to be used then to sent the emails that correspond to the current research, it also add the user to the given gophish group.

**EP Path:** https://k2gy69kvfc.execute-api.us-east-2.amazonaws.com/prod/email 

**Method:** POST

#### *Request body elements*

<br>

| Item name   | Type   | Required    | Description|
| ----------- | ----------- | ----------- | ----------- | 
| userId | String| Required | ID of the user who completed the survey|
| gophishGroupName | String| Required | gophish group name to whose the user will be added|
| firstName| String | Optional | The user's first name|
| lastName | String | Optional | The user's last name|
| researcherName | String | Required | The researcher name|
| researchName | String | Required | The research name|
| interventionId | String | Required | The id of the intervention the user was trained with|

<br>

#### *Request body example*

``` json
    {
        "userId": "3c6b6a3c-0e2c-4384-ae2d-9ae2f19bd248",
        "gophishGroupName": "Email Research 1",
        "firstName": "Fernando",
        "lastName": "Rodriguez",
        "researcherName" : "Charles Xavier",
        "researchName": "Social Security",
        "interventionId": "2"
    }
```
<br>

#### *Responses*

<br>

If a the request has been made successfully

``` json
    {
        "statusCode": 200,
        "body": "Email created successfully"
    }
```

If a the request body does not match the schema

``` json
    {
        "statusCode": 400,
        "body": "The request body does not match the valid schema"
    }
```

If a the request has failed at saving the data

``` json
    {
        "statusCode": 500,
        "body": "Could not create mail"
    }
```

### <u>Add a user answer to the survey</u>

Given the user ID, session ID, question and answer information, it stores it in the data base.

**EP Path:** https://k2gy69kvfc.execute-api.us-east-2.amazonaws.com/prod/survey-answer 

**Method:** POST

<br>

#### *Request body elements*

<br>

| Item name   | Type   | Required    | Description|
| ----------- | ----------- | ----------- | ----------- | 
| userId | String| Required | ID of the user who is answering the survey|
| surveySessionId| String| Required | ID of the user's active session|
| questionNumber| String | Required | The number of the question|
| questionCaption | String | Required | The text of the question|
| answerValue | String | Required | The answer identifier if it is a multiple choice question (a, b, c, d...)|
| answer | String | Required | The answer's text |

<br>

#### *Request body example*


``` json
    {
        "userId": "3c6b6a3c-0c3c-4384-ae2d-9ae2f19bd248",
        "surveySessionId": "Session-02",
        "questionNumber": 2,
        "questionCaption": "Is this email fake or real?",
        "answerValue": "A",
        "answer": "Fake"
    }
```

<br>

#### *Responses*

<br>

If a the request has been made successfully

``` json
    {
        "statusCode": 200,
        "body": "Survey answer logged successfully"
    }
```

If a the request body does not match the schema

``` json
    {
        "statusCode": 400,
        "body": "The request body does not match the valid schema"
    }
```

If a the request has failed at saving the data

``` json
    {
        "statusCode": 500,
        "body": "Data could not be saved"
    }
```

<br>

### <u>Add new action performed in an email</u>

Given the user ID, email ID, intervention ID, research information, event and mode, it stores it in the data base.

**EP Path:** https://k2gy69kvfc.execute-api.us-east-2.amazonaws.com/prod/user-action 

**Method:** POST

<br>

#### *Request body elements*

<br>

| Item name   | Type   | Required    | Description |
| ----------- | ----------- | ----------- | ----------- |
| userId | String| Required | ID of the user who is answering the survey |
| emailId | String| Required | ID of the email in which the action was performed|
| interventionId | String | Required | From 1 to 4, the number of intervention the user received previously| 
| researchName| String | Required | The name of the research|
| researcherName | String | Required | The name of the researcher |
| event | String | Required | The event description (open the mail, click on links...)|
| Mode | String | Required | To distinguish if it is Testing or Training mode |

<br>

#### *Request body example*

``` json
    {
        "userId": "3c6b6a3c-0e2c-4384-ae2d-9ae2f19bd248",
        "emailId": "SOCIAL-1",
        "interventionId": 3,
        "researchName": "SSA Testing",
        "researcherName": "Carlos Jiménez",
        "event": "Click links",
        "Mode": "Test"
    }
```

<br>

#### *Responses*

<br>

If a the request has been made successfully

``` json
    {
        "statusCode": 200,
        "body": "User action logged successfully"
    }
```

If a the request body does not match the schema

``` json
    {
        "statusCode": 400,
        "body": "The request body does not match the valid schema"
    }
```

If a the request has failed at saving the data

``` json
    {
        "statusCode": 500,
        "body": "Data could not be saved"
    }
```

### <u>Get logged user actions on emails</u>

This End Point's parameters on the payload will act as a filter to retrieve the stored user actions on the emails

**EP Path:** https://k2gy69kvfc.execute-api.us-east-2.amazonaws.com/prod/user-action 

**Method:** GET

<br>

#### *Request body elements*
* The filter will be applied depending on which parameters the user sends in the payload. There can be no params, or use just some of them.
* The date parameters are both needed if the user wants to filter by date
<br>

| Item name   | Type   | Required    | Description |
| ----------- | ----------- | ----------- | ----------- |
| researchName | String| Optional | Name of the research of the event |
| EmailID | String| Optional | ID of the email in which the action was performed|
| DateFrom | String | Optional | The date from which the filter is going to start (IMPORTANT: It must follow the format "yyyy-mm-dd")| 
| DateTo| String | Optional | The date in which the filter is going to end (IMPORTANT: It must follow the format "yyyy-mm-dd")|

<br>

#### *Request body example*

``` json
    {
        "ResearchName": "SSA Testing",
        "EmailId": "ssaopOut-1",
        "DateFrom": "2021-05-14",
        "DateTo": "2021-05-18"
    }
```

<br>

#### *Responses*

<br>

If a the request has been made successfully, the link to download the csv with the filtered data

``` json
    {
        "statusCode": 200,
        "body": "https://sscams.s3.us-east-2.amazonaws.com/1621454897449-User-Events.csv"
    }
```

If a the request body does not match the schema, it should have the missmatch with the schema described in the response body

``` json
    {
        "statusCode": 400,
        "body": "The request body does not match the valid schema"
    }
```

If a the request has failed retrieving the data

``` json
    {
        "statusCode": 500,
        "body": "The data could not be retrieved"
    }
```


### <u>Get logged user actions on emails</u>

This End Point's parameters on the payload will act as a filter to retrieve the stored user actions on the emails

**EP Path:** https://k2gy69kvfc.execute-api.us-east-2.amazonaws.com/prod/email-info 

**Method:** GET

<br>

#### *Request body elements*
* The request does not need a payload, it just requires 1 param
<br>

|  Param Key   | Example Value   | Required    | Description |
| ----------- | ----------- | ----------- | ----------- |
| Email | testmail@behavioralsurvey.com| Required | Email account from which I want to retrieve the user's email information |


<br>



#### *Responses*

<br>

If a the request has been made successfully, the link to download the csv with the filtered data

``` json
    {
        "statusCode": 200,
        "body": {
            "userID": "test17",
            "email": "test17@behavioralsurvey.com",
            "interventionID": "Testing Intervention",
            "researcherName": "Nahomy",
            "researchName": "Performance test"
        }
    }
```

If a the request body does not match the schema, it should have the missmatch with the schema described in the response body

``` json
    {
        "statusCode": 400,
        "body": "The request body does not match the valid schema"
    }
```

If a the request has failed retrieving the data

``` json
    {
        "statusCode": 500,
        "body": "The data could not be retrieved"
    }
```


