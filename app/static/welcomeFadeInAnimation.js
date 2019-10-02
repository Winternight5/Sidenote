/*
  This script utilizes JavaScript and jQuery to fade in the Welcome Page's contents, including the header1 and
  the login/registration form.
*/

$(document).ready(function()
{

const delayTimer = 1;

var $header = $("h1");
var $aboutSidenote = $(".introduction p");
var $loginForm = $("form");
var $learnMoreButton = $(".ghost-button button");

$header.hide();
$aboutSidenote.hide();
$loginForm.hide();
$learnMoreButton.hide();

$header.delay(50 * delayTimer * 3).fadeIn(1450);
$aboutSidenote.delay(50 * delayTimer * 10).fadeIn(1450);
$learnMoreButton.delay(50 * delayTimer * 25).fadeIn(1450);
$loginForm.delay(50 * delayTimer * 25).fadeIn(1450);


});



