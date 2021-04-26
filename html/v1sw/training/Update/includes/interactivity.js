function lessonOverlayOn() {
  document.getElementById("lessonOverlay").style.display = "block";
}

function lessonOverlayOff() {
  document.getElementById("lessonOverlay").style.display = "none";
}

function clickCaptureOverlayOn() {
  document.getElementById("clickCaptureOverlay").style.display = "block";
  return false; // Used to override the link
}

function clickCaptureOverlayOff() {
  document.getElementById("clickCaptureOverlay").style.display = "none";
  return false;  // Used to override the link
}

// Capture ALL Clicks
/*
var clickOverlayOff = true;
window.onclick = function(e) { 
	if (clickOverlayOff) {
		clickCaptureOverlayOn(); 
		clickOverlayOff = false;
	} else {
		clickCaptureOverlayOff(); 
		clickOverlayOff = true;
	}	
};
*/

function openEmailHeader() {
	var c=document.getElementById('toggled_panel-1');
	if(!c)
		return;
	c.setAttribute('style','max-height:'+c.scrollHeight+'px');
	c.setAttribute('aria-hidden',false);
	
}

function headerToggle(b) {
	var s=b.getAttribute('aria-expanded')==='true';
	var c=document.getElementById(b.getAttribute('aria-controls'));
	if(!c)
		return;
	c.setAttribute('style','max-height:'+c.scrollHeight+'px');
	b.setAttribute('aria-expanded',!s);
	c.setAttribute('aria-hidden',s);
}

// open the tooltips
function tooltipsOn() {
  openEmailHeader()

  let tooltips = document.getElementsByClassName('popuptext');  
  for (tooltip of tooltips) {
     tooltip.classList.toggle("show");
  };
  /*
  var tooltip = document.getElementById("tooltip1");
  if (tooltip) {
		tooltip.classList.toggle("show");
  }
  tooltip = document.getElementById("tooltip2");
  if (tooltip) {
	tooltip.classList.toggle("show");
  }
  tooltip = document.getElementById("tooltip3");
  if (tooltip) {
	tooltip.classList.toggle("show");
  }
  */
}

window.addEventListener("message", (event) => {
  // Do we trust the sender of this message?
  if (event.origin !== "https://uwmadison.co1.qualtrics.com")
    return;

  // event.source is window.opener
  // event.data is "hello there!"
	
  if (event.data == "lessonOverlay")
	lessonOverlayOn();
  if (event.data == "tooltips")
	tooltipsOn();	
}, false);
