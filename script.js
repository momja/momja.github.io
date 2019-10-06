// Navbar Toggle
window.addEventListener('load', function () {
    // Get all "navbar-burger" elements
    console.log("FUUCK");
    var $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);
    // Check if there are any navbar burgers
    if ($navbarBurgers.length > 0) {
  
      // Add a click event on each of them
      $navbarBurgers.forEach(function ($el) {
        $el.addEventListener('click', function () {
          var $target = document.getElementById("main-nav");
          $target.classList.toggle("hidden");
        });
      });
    }
  
  });