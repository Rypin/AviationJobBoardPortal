// Search Filter Bar
$(document).ready(function(){
    $("#myInput").on("keyup", function() {
      var value = $(this).val().toLowerCase();
      $("#myTable tr").filter(function() {
        $(this).toggle($(this).find("td:first").text().toLowerCase().indexOf(value) > -1)
      });
    });
  });