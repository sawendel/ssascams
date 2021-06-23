
(function ($, window) {
	$(function () {
		function sleep(ms) {
			return new Promise(resolve => setTimeout(resolve, ms));
			}
			
		function registerEvent(event, mode){
		emailID = $('.bodyText>div:not([style*="display: none;"]) div[templateid]').attr("templateid");
		console.log(typeof(emailID));
		emailAccount = window.document.querySelector(`.accountPlace`).innerHTML;
		$.get( `https://k2gy69kvfc.execute-api.us-east-2.amazonaws.com/prod/email-info?Email=${emailAccount}`, function(data, status) {
				 json = {
					"userId": data.body.userID,
					"emailId": emailID,
					"interventionId":data.body.interventionID,
					"researchName":data.body.researchName,
					"researcherName": data.body.researcherName,
					"event": event,
					"Mode":mode
				};
				
				console.log(json);
				$.post('https://k2gy69kvfc.execute-api.us-east-2.amazonaws.com/prod/user-action', JSON.stringify(json), function(data, status){console.log(data)});
		});
	}
	function registerEventSpamDelete(event, mode, emailID){
		emailAccount = window.document.querySelector(`.accountPlace`).innerHTML;
		$.get( `https://k2gy69kvfc.execute-api.us-east-2.amazonaws.com/prod/email-info?Email=${emailAccount}`, function(data, status) {
				json = {
					"userId": data.body.userID,
					"emailId": emailID,
					"interventionId":data.body.interventionID,
					"researchName":data.body.researchName,
					"researcherName": data.body.researcherName,
					"event": event,
					"Mode":mode
				};	
				console.log(json);
				$.post('https://k2gy69kvfc.execute-api.us-east-2.amazonaws.com/prod/user-action', JSON.stringify(json), function(data, status){console.log(data)});
		});
	}
	
		function elementReady(selector) {
			return new Promise((resolve, reject) => {
			let el = document.querySelector(selector);
			if (el) {resolve(el);}
			new MutationObserver((mutationRecords, observer) => {
				// Query for elements matching the specified selector
				Array.from(document.querySelectorAll(selector)).forEach((element) => {
				resolve(element);
				//Once we have resolved we don't need the observer anymore.
				observer.disconnect();
				});
			})
				.observe(document.documentElement, {
				childList: true,
				subtree: true
				});
			});
		}
		 async function addCredentials(){
			var queryString = window.location.search;
			var params = new URLSearchParams(queryString);
			var email = params.get("email");
			var pass = params.get("pass");

			if(!!email & !!pass){
				var decodedEmail = window.atob(email);
				var decodedPass = window.atob(pass);
				console.log(decodedEmail);
				console.log(decodedPass);
				await elementReady("#RainLoopEmail");
				window.document.getElementById('RainLoopEmail').setAttribute('value', decodedEmail);
			    window.document.getElementById('RainLoopPassword').setAttribute('value', decodedPass);
				
			}
		}

	// 	//window.document.ready =  () => { addCredentials()};
		window.onload =  addCredentials();
	
	// 	//CAPTURE THE REPLY ACTIONS
		$('body').on('click', '.icon-reply',function () {
			console.log('le di al reply');
			registerEvent("Click on Reply", "Training");
			})
		$('body').on('click', '#menu-new-actions>div:nth-child(1)>li:nth-child(1) a',function () {
			console.log('le di al reply');
			registerEvent("Click on Reply", "Training");
			})
			

	// 	//CAPTURE THE OPEN MAIL ACTIONS
		$('body').on('click', '.messageListItem',async function () {
			console.log('abrí el correo');
			await sleep(1000);
			var emailID = window.document.getElementById('Email-ID');
			var emailIDToChange = $('.bodyText>div:not([style*="display: none;"]) div[templateid]').attr("templateid");
			emailID.innerHTML = emailIDToChange
			registerEvent("Open", "Training");
			})

	// 	//CAPTURE THE CLICK ON THE REPLY ALL ACTIONS
		$('body').on('click', '#menu-new-actions>div:nth-child(1)>li:nth-child(2) a',function () {
			console.log('click en reply all');
			registerEvent("Click on Reply All", "Training");
		})
		$('body').on('click', '.icon-reply-all',function () {
			console.log('click en reply all');
			registerEvent("Click on Reply All", "Training");
		})
		


		//CAPTURE CLICK ON FORWARD ACTIONS
		$('body').on('click', '#menu-new-actions>div:nth-child(1)>li:nth-child(3) a',function () {
			console.log('click en forward');
			registerEvent("Click on Forward", "Training");
			})

		$('body').on('click', '.icon-forward',function () {
			console.log('click en forward');
			registerEvent("Click on Forward", "Training");
			})


		//CAPTURE CLICK ON ARCHIVE
		$('body').on('click', '#menu-new-actions>div:nth-child(2)>li:nth-child(2) a',async function () {
			var emailID = window.document.getElementById('Email-ID').innerHTML;

			window.document.querySelector(".informationFull").style.display = "none";
			var headerHeight = $(".messageItemHeader").outerHeight(true);
			window.document.querySelector(".messageItem").style.top = headerHeight.toString() + "px";

			registerEventSpamDelete("Click on Archive", "Training", emailID);

			await sleep(1500);
			
			var emailID = window.document.getElementById('Email-ID');
			var emailIDToChange = $('.bodyText>div:not([style*="display: none;"]) div[templateid]').attr("templateid");
			emailID.innerHTML = emailIDToChange;
			})

	$('body').on('click', '.button-archive',async function () {
		var emailID = window.document.getElementById('Email-ID').innerHTML;

		window.document.querySelector(".informationFull").style.display = "none";
		var headerHeight = $(".messageItemHeader").outerHeight(true);
		window.document.querySelector(".messageItem").style.top = headerHeight.toString() + "px";

		registerEventSpamDelete("Click on Archive", "Training", emailID);

		await sleep(1500);

		var emailID = window.document.getElementById('Email-ID');
		var emailIDToChange = $('.bodyText>div:not([style*="display: none;"]) div[templateid]').attr("templateid");
		emailID.innerHTML = emailIDToChange;
		})


 		//CLICK EN SPAM
	$('body').on('click', '#menu-new-actions>div:nth-child(2)>li:nth-child(3) a', async function () {
		console.log('click en spam');
		var emailID = window.document.getElementById('Email-ID').innerHTML;

		window.document.querySelector(".informationFull").style.display = "none";
		var headerHeight = $(".messageItemHeader").outerHeight(true);
		window.document.querySelector(".messageItem").style.top = headerHeight.toString() + "px";

		registerEventSpamDelete("Click on Spam", "Training", emailID);

		await sleep(1500);

		var emailID = window.document.getElementById('Email-ID');
		var emailIDToChange = $('.bodyText>div:not([style*="display: none;"]) div[templateid]').attr("templateid");
		emailID.innerHTML = emailIDToChange
		})

	$('body').on('click', '.button-spam',async function () {
		console.log('click en spam');
		var emailID = window.document.getElementById('Email-ID').innerHTML;

		window.document.querySelector(".informationFull").style.display = "none";
		var headerHeight = $(".messageItemHeader").outerHeight(true);
		window.document.querySelector(".messageItem").style.top = headerHeight.toString() + "px";

		registerEventSpamDelete("Click on Spam", "Training", emailID);

		await sleep(1500);

		var emailID = window.document.getElementById('Email-ID');
		var emailIDToChange = $('.bodyText>div:not([style*="display: none;"]) div[templateid]').attr("templateid");
		emailID.innerHTML = emailIDToChange
		})

			//CLICK EN DELETE
		$('body').on('click', '#menu-new-actions>div:nth-child(2)>li:nth-child(5) a',async function () {
			var emailID = window.document.getElementById('Email-ID').innerHTML;

			window.document.querySelector(".informationFull").style.display = "none";
			var headerHeight = $(".messageItemHeader").outerHeight(true);
			window.document.querySelector(".messageItem").style.top = headerHeight.toString() + "px";

			registerEventSpamDelete("Click on Delete", "Training", emailID);

			await sleep(1500);

			var emailID = window.document.getElementById('Email-ID');
			var emailIDToChange = $('.bodyText>div:not([style*="display: none;"]) div[templateid]').attr("templateid");
			emailID.innerHTML = emailIDToChange;
			})

	$('body').on('click', '.button-delete', async function () {
		var emailID = window.document.getElementById('Email-ID').innerHTML;

		window.document.querySelector(".informationFull").style.display = "none";
		var headerHeight = $(".messageItemHeader").outerHeight(true);
		window.document.querySelector(".messageItem").style.top = headerHeight.toString() + "px";

		registerEventSpamDelete("Click on Delete", "Training", emailID);

		await sleep(1500);

		var emailID = window.document.getElementById('Email-ID');
		var emailIDToChange = $('.bodyText>div:not([style*="display: none;"]) div[templateid]').attr("templateid");
		emailID.innerHTML = emailIDToChange
		})


			//CLICK EN LINKS
		$('body').on('click', '.bodyText a:not(.btn):not(.e-link)',function () {
			console.log('click en link');
			registerEvent("Click on Links", "Training");
			alert("Links have been disabled in this email for testing purposes.");
			})
			//THIS PREVENTS THE OPENING OF THE CLICK EVENT ON LINKS
			$('body').on('click', '.bodyText a',function (event) {
				event.preventDefault();
				})
			


$('body').on('click', '.messageListItem',function () {
		var element = window.document.querySelector(".informationFull");
		var messageItem = window.document.querySelector(".messageItem");
		//if(element.style.visibility == "none")
		if($(".informationFull").css("display")!='none')
		{
			element.style.display = "none";
			var headerHeight = $(".messageItemHeader").outerHeight(true);
			messageItem.style.top = headerHeight.toString() + "px";
		}
		
})


$('body').on('click', '.infoParent.g-ui-user-select-none',function () {
	var element = window.document.querySelector(".informationFull");	
	var messageItem = window.document.querySelector(".messageItem");
	//if(element.style.visibility == "none")
	if($(".informationFull").css("display")!='none')
	{
		element.style.display = "none";
		var headerHeight = $(".messageItemHeader").outerHeight(true);
		messageItem.style.top = headerHeight.toString() + "px";
	}
	else{
		element.style.display = null;
		var headerHeight = $(".messageItemHeader").outerHeight(true);
		messageItem.style.top = headerHeight.toString() + "px";
		registerEvent("Open Headers", "Training");
	}
	
})
// $('body').on('click', '.e-quota',function () {
// 	var headerHeight = $(".messageItemHeader").outerHeight(true);

// 	console.log("hola")
// 	console.log(headerHeight);
// 	//if(element.style.visibility == "none")
// 	// if($(".informationFull").css("display")!='none')
// 	// {
// 	// 	element.style.display = "none";
// 	// }
// 	// else{
// 	// 	element.style.display = null;
// 	// }
	
// })



		

		
		
		

		
		
	 $('body').on('mouseover', '.bodyText a',function () {
		var href = $(this).attr('href');
		var thePopUp = window.document.getElementById('URL-view');
		thePopUp.innerHTML = href;
		thePopUp.style.visibility= "visible";
		})
		
	$('body').on('mouseleave', '.bodyText a',function () {
		var thePopUp = window.document.getElementById('URL-view');
		thePopUp.style.visibility= "hidden";
		})
	
		
	});
}($, window));