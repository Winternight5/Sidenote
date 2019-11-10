/*
  This script utilizes JavaScript and jQuery to fade in the Welcome Page's contents, including the header3 and
  the login/registration form.
*/

$(document).ready(function() {

  const delayTimer = 1;

  // this was updated
  var $header = $("h3");
  var $aboutSidenote = $("img");
  var $loginForm = $("form");
  var $learnMoreButton = $("button");

  $header.hide();
  $aboutSidenote.hide();
  $loginForm.hide();
  $learnMoreButton.hide();

  $header.delay(50 * delayTimer * 3).fadeIn(1450);
  $aboutSidenote.delay(50 * delayTimer * 10).fadeIn(1450);
  $learnMoreButton.delay(50 * delayTimer * 25).fadeIn(1450);
  $loginForm.delay(50 * delayTimer * 25).fadeIn(1450);


});



