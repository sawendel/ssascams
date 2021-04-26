var letterBody = `<p class="body-title center-text">Notice of Decision - @@Titlle Overlay@@Fully Favorable</p>
<p class="body-paragraph">I carefully reviewed the facts of your case and made the enclosed fully favorable decision. Please read this notice and my decision.</p>
<p class="body-paragraph">Another office will process my decision. That office may ask you for more information. If you @@Extra overlay message@@do not hear anything within 60 days of the date of this notice, please contact your local office. The contac information for your local office is at the end of this notice.</p>
<p class="body-subtitle">If You Disagree With My Decision</p>
<p class="body-paragraph">If you disagree with my decision, you may file an appeal with the Appeals Council.</p>
<p class="body-subtitle">How To File An Appeal </p>
<p class="body-paragraph">To file an appeal you @@last Overlay to show@@or your representative must ask in writing that the Appeals Council review my decision. You may user our request for Review form (HA-520) or write a letter. Ther form is available at www.socialsecurity.gov. Please put the Social Security number shown above on any appeal you file. If you need help, you may file in person at any Social Security or hearing office.</p>
<p class="body-paragraph">Please send your request to:</p>
<div class="request-sender">
  <p class="body-paragraph">Appeals Council</p>
  <p class="body-paragraph">Office of Disability Adjudication and Review</p>
  <p class="body-paragraph">5107 Lessburg Pike</p>
  <p class="body-paragraph">Falls Clurch, VA 22041-315</p>
</div>
<p class="body-subtitle">Time Limit To File An Appeal</p>
<p class="body-paragraph">You must file your written appeal <span class="body-subtitle">within 60 days</span> of the date this notice. @@Another overlay message@@The Appeals Council assumes you got this notice 5 days after the date of the notice unless you show you did</p>
<p id="form-id" class="body-paragraph right-text">Form HA-L76 (03-2010)</p>`;

letterBody = JSON.stringify(letterBody);
const jsonData = `{
    "Recipient_Name" : "Recipient Name Here",
    "Recipient_Street_Address": "Street Address",
    "Recipient_City": "City Name",
    "Recipient_State": "State Initials",
    "Recipient_Zip_Code": "Zip code",
    "Office_Name": "The office name",
    "Specific_Office_Name": "The specific office name",
    "Office_Address_In_Building": "example: building B 7th floor",
    "Office_Street_Address": "The office street address",
    "Office_City": "The office ciy",
    "Office_State":"The office state",
    "Office_Zip_Code":"The office zip code ",
    "Month": "April",
    "Day": "22",
    "Year": "2021",
    "Form_ID": "HA-L76 (03-2010)",
    "Letter_Body": ${letterBody}    
}`;



const overlayMessages = `{
    "Sender" : "",
    "Recipient_Direction" : "Recipient direction",
    "Date" : "the date"
}`