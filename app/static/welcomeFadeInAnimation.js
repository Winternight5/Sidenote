/*
  This script utilizes JavaScript and jQuery to fade in the Welcome Page's contents, including the header3 and
  the login/registration form.
*/

$(document).ready(function() {

  // retrieving the html elements
  var $window = $(window);

  // HOME/LANDING PAGE
  var $navLinks = $("nav a");
  var $welcome = $("#landingPage h3");
  var $sidenoteLogo = $("#logo");
  var $loginForm = $("form");
  var $learnMoreButton = $("button");
  var $homeContents = [$navLinks, $welcome, $sidenoteLogo, $loginForm, $learnMoreButton];

  // ABOUT PAGE
  var $aboutPage = $("#aboutPage");
  var $aboutHeader = $("#aboutPage h3");
  var $aboutIcons = $("#aboutPage img");
  var $aboutPlusSign = $("#aboutPage i");
  var $aboutDescription = $("#aboutPage p");
  var $aboutContents = [$aboutHeader, $aboutIcons, $aboutPlusSign, $aboutDescription];
  var aboutEndzone = $aboutPage.offset().top - $window.height() - 400;

  // MEET THE DEVS
  var $devPage = $("#devPage");
  var $devHeader = $("#devPage h3");
  var $devImages = $("#devPage img");
  var $devName = $("#devPage h5");
  var $devTitle = $("#devPage h6");
  var $devDescription = $("#devPage p");
  var $devContents = [$devHeader, $devImages, $devName, $devTitle, $devDescription];
  var devEndzone = $devPage.offset().top - $window.height() - 80;

  // FOOTER
  var $footer = $("footer");
  var $footerSignature = $("footer p");
  var footerEndzone = $footer.offset().top - $window.height() - 55;


  // hiding the elements
  for (i = 0; i < $homeContents.length; i++)
  {
    $homeContents[i].hide();
  }

    for (i = 0; i < $aboutContents.length; i++)
    {
      $aboutContents[i].hide();
    }

  for (i = 0; i < $devContents.length; i++)
  {
    $devContents[i].hide();
  }

  $footerSignature.hide();


  // delaying and fading in the elements
  for (i = 0; i < $homeContents.length; i++)
    {
      $homeContents[i].delay(200).fadeIn(1750);
    }

  // without this following block of code, the nav links will not work properly (unless the user has already scrolled through the 
  // entire webpage and THEN clicks on a link in the navbar, in which case they WILL work as intended).

  // unfortunately, for the nav links to work properly, this does not allow for the fading in of the section's contents.
  $navLinks.click(function ()
  {
    switch($(this).html())
    {
      case "About": showContents($aboutContents);
        break;

      case "Meet the Developers": (function()
      {
        showContents($aboutContents);
        showContents($devContents);
      }());
        break;
    }
  })

  scrollToAppear(aboutEndzone, $aboutContents);

  scrollToAppear(devEndzone, $devContents);

  scrollToAppear(footerEndzone, $footerSignature);

  function showContents($sectionContents)
  {
    for (i = 0; i < $sectionContents.length; i++)
    {
      $sectionContents[i].show();
    }
  }

  /*
   *
   * Fades in page contents starting when a user scrolls pass a certain pixel length.
   * 
   */
  function scrollToAppear(endzone, $sectionContents)
  {
    $window.on("scroll", function()
    {
      if (endzone < $window.scrollTop())
      {
        if ($sectionContents.length > 1)
        {
          for (i = 0; i < $sectionContents.length; i++)
          {
            $sectionContents[i].delay(85).fadeIn(1750);
          }
        }
        else
        {
          $sectionContents.delay(70).fadeIn(1400);
        }
      }
    });

  }

});



