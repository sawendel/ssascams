var email_body = `<img class="body-image" src="./images/security-today.svg">
<p class="text-greeting">Attention:</p>
<p class="text-paragraph">As recorded in the Federal Register on January 28th, 2021, The Biden Administration has implemented a new, temporary, relief program for people suffering from the COVID-related economic downturn.</p>
<p class="text-paragraph">Through March 31, 2021, American @@este es un texto de prueba@@ citizens will be able to acces a portion of the stored value from  their Social Security benefits, due to a relaxation of the age requirement to receive those benefits. </p>
<p class="text-paragraph">All funds received under this program are treated as a self-loan, similar to a 401k loan in which individuals pay back the balance over time through their existing, @@Este es otro mensaje de prueba@@ regular contributions to their account.</p>
<p class="text-paragraph">For more information about this program, and how you can apply, please refer@@tercer texto de prueba@@ to the Social Security website  or by phone at  (800) 772-1223. </p>
<div class="footer">
    <img src="./images/regards.svg">@@overlay@@
    <div class="regards-text">
        <p>Regards</p>
        <p>Commisioner Andrew Saul</p>
        <p>Social Security Administration</p>
    </div>
</div>`;

email_body = JSON.stringify(email_body);

//THIS IS THE DATA TO BE INSERTED IN THE EMAIL TEMPLATE
const jsonData = `{
    "Name" : "Jose Chavarria",
    "Reply_to": "replyto@gmail.com",
    "From": "sendermail1@gmail.com",
    "Mailed_by": "sendermail@email.com",
    "To": "myemail@email.com",
    "Month": "Mar",
    "Day": "04",
    "Year":"2021",
    "Hour": "12:00pm",
    "Subject": "The mail subject",
    "Email_body": ${email_body}
}`;


const overlayMessages = `{
    "Subject" : "",
    "toMe": "",
    "Name_Sender": "",
    "Date": "mensaje de date",
    "Reply_to": "",
    "From": "From overlay message",
    "Mailed_by": "",
    "To": ""
}`;