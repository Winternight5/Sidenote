/*
  This script utilizes JavaScript and jQuery to fade in the Welcome Page's contents, including the header3 and
  the login/registration form.
*/

$(document).ready(function() {

  var navLinkCount = 4;
  // retrieving the html elements
  var $navLinks = $("nav a");
  var $welcome = $("h3");
  var $aboutSidenote = $("img");
  var $loginForm = $("form");
  var $learnMoreButton = $("button");

  // hiding the elements
  $navLinks.hide();
  $welcome.hide();
  $aboutSidenote.hide();
  $loginForm.hide();
  $learnMoreButton.hide();

  // delaying and fading in the elements
  fadeLinks($navLinks);
  $welcome.delay(50 * 3).fadeIn(1450);
  $aboutSidenote.delay(50 * 10).fadeIn(1450);
  $learnMoreButton.delay(50 * 25).fadeIn(1450);
  $loginForm.delay(50 * 25).fadeIn(1450);

  function fadeLinks($navLinks)
  {
    $navLinks.each(function(index)
    {
      $(this).delay(50 * index).fadeIn(1000);
    });
  }

});



