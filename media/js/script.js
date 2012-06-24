/* Author:

*/

// Listeners
$('#menu').hover(function() {
  var self = $(this);
  self.children('.dropdown-menu').show();
}, function() {
  var self = $(this);
  self.children('.dropdown-menu').hide();
});
