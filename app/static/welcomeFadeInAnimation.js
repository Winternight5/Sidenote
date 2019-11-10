/*
  This script utilizes JavaScript and jQuery to fade in the Welcome Page's contents, including the header3 and
  the login/registration form.
*/

$(document).ready(function() {

  // retrieving the html elements
  var $header = $("h3");
  var $aboutSidenote = $("img");
  var $loginForm = $("form");
  var $learnMoreButton = $("button");

  // hiding the elements
  $header.hide();
  $aboutSidenote.hide();
  $loginForm.hide();
  $learnMoreButton.hide();

  // delaying and fading in the elements
  $header.delay(50 * 3).fadeIn(1450);
  $aboutSidenote.delay(50 * 10).fadeIn(1450);
  $learnMoreButton.delay(50 * 25).fadeIn(1450);
  $loginForm.delay(50 * 25).fadeIn(1450);


});



