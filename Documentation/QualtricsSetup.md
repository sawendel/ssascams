## Javascript Extensions

The core survey works by extending Qualtrics with a set of Javascript and HTML commands.

## Marking the Study Arm 

QR~QID42

## Displaying the email

<div><p>Is the following letter real or fake?</p><p> </p></div>
<iframe src="https://behavioralsurvey.com/wp-content/uploads/2021/05/ssa_letter_medicareReview.html" style="height:500px;width:100%;">
</iframe>

## Opening the Email Client - Rainloop 

Standalone Script

<script> 
Qualtrics.SurveyEngine.addOnload(function()
{
/*Place your JavaScript here to run when the page loads*/
function NewTab() { 
		$myQ2Val = "${q://QID42/ChoiceTextEntryValue}";
		const encodedData = window.btoa($myQ2Val + "@behavioralsurvey.com");
		var fullUrl = "http://3.20.89.142:7000?email=" + encodedData + "&pass=UGFzc3dvcmQxMjM0Kg==";
		window.open(fullUrl , "_blank"); 
    }
NewTab();
});


Button to Opening

<div align="center">
<button style="background-color:slateblue;color:white;display:block;width=60%;border=none;text-align:center;" class="btn" onclick="
     $myQ2Val = '${q://QID42/ChoiceTextEntryValue}';
   const encodedData = window.btoa($myQ2Val + '@behavioralsurvey.com');
   var fullUrl = 'http://3.20.89.142:7000?email=' + encodedData + '&pass=UGFzc3dvcmQxMjM0Kg==';
   window.open(fullUrl , '_blank');">Click to Start Reviewing the Emails 
 </button></div>


</script>



http://3.20.89.142:7000?email=U3RldmVUZXN0OQ==QGJlaGF2aW9yYWxzdXJ2ZXkuY29t&pass=UGFzc3dvcmQxMjM0Kg==
http://3.20.89.142:7000?email=U3RldmVUZXN0OUBiZWhhdmlvcmFsc3VydmV5LmNvbQ==&pass=UGFzc3dvcmQxMjM0Kg==



Password1234*
UGFzc3dvcmQxMjM0Kg==

Prolific
QGJlaGF2aW9yYWxzdXJ2ZXkuY29t
atob("QGJlaGF2aW9yYWxzdXJ2ZXkuY29t")
@behavioralsurvey.com"


Dynata
BiZWhhdmlvcmFsc3VydmV5LmNvbQ==
atob("ZWhhdmlvcmFsc3VydmV5LmNvbQ==")
QGJlaGF2aW9yYWxzdXJ2ZXkuY29t
ZWhhdmlvcmFsc3VydmV5LmNvbQ==



      <button class="btn btn-success" onclick="
	  		$myQ2Val = '${q://QID42/ChoiceTextEntryValue}';
			const encodedData = window.btoa($myQ2Val);
			var fullUrl = 'http://3.20.89.142:7000?email=' + encodedData + 'QGJlaGF2aW9yYWxzdXJ2ZXkuY29t&pass=UGFzc3dvcmQxMjM0Kg==';
			window.open(fullUrl , '_blank');"> Google</button>

	  
	  location.href='http://google.com';"
	  
	  
	  <button class="btn btn-success" 
	  onclick=" window.open('http://google.com','_blank')"> Google</button>
	  
	  window.open(
  'https://google.com',
  '_blank' // <- This is what makes it open in a new window.
);
