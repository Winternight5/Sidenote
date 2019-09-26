/*
  This script utilizes JavaScript and jQuery to fade in the Welcome Page's contents, including the header1 and
  the login/registration form.
*/

$(document).ready(function()
{

const delayTimer = 1;

var $header = $("h1");
var $loginForm = $("form");

$header.hide();
$loginForm.hide();

$header.delay(50 * delayTimer).fadeIn(1450);
$loginForm.delay(50 * delayTimer * 10).fadeIn(1450);

});



