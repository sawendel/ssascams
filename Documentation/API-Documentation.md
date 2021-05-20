# SSCAMS API

This file was created with the objective of describing the Sscams API created to meet the project requirements regarding email, survey answers and user actions management.

Each endpoint will be explained in detail considering its url, kind of method, needed body and params to have a successful request and the expected result.

All the EPs check that the http request body follows the previously defined schema before executing its function.

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


