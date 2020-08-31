$(function() {

    // For the Double Slider
    $("#slider-range").slider({
        range: true,
        min: 20000,
        max: 300000,
        step: 5000,
        values: [50000, 200000],
        slide: function(event, ui) {
            $("#amount").val("$" + formatNumber(ui.values[0]) + " - $" + formatNumber(ui.values[1]));
            salarySelectionEvent(formatNumber(ui.values[0]), formatNumber(ui.values[1]));
        }
    });
    $("#amount").val("$" + $("#slider-range").slider("values", 0) +
        " - $" + $("#slider-range").slider("values", 1));



    // Indicate selection for the "Distance" filter option
    $(".dropdown2 a").click(function() {
         $(".menuHeader2").text($(this).text());
         $(".menuHeader2").val($(this).text());
         $(".menuHeader2").parent().addClass("headerActive");
         $(".dot2").addClass("dotActive");
    });

    // $(".dropdown2 a").change(function() {
    //     $(".menuHeader2").text($(this).text());
    //     $(".menuHeader2").val($(this).text());
    //     $(".menuHeader2").parent().addClass("headerActive");
    //     $(".dot2").addClass("dotActive");
    // }); 

    // Indicate selection for the "Date Posted" filter option
    $(".dropdown3 a").click(function() {
        $(".menuHeader3").text($(this).text());
        $(".menuHeader3").val($(this).text());
        $(".menuHeader3").parent().addClass("headerActive");
        $(".dot3").addClass("dotActive");
    });

    // Indicate selection for the "Salary Range" filter option
    $(".dropdown4 a").click(function() {
        $(".menuHeader4").text($(this).text());
        $(".menuHeader4").val($(this).text());
        $(".menuHeader4").parent().addClass("headerActive");
        $(".dot4").addClass("dotActive");
    });

    // The change event function for the filter options in "Other Filters"
    $('#workAuthChk').change(function() {
        if ($(this).prop('checked')) {
            $(".menuHeader5").parent().addClass("headerActive");
            $(".dot5").addClass("dotActive");
        } else {
            $(".menuHeader5").parent().removeClass("headerActive");
            $(".dot5").removeClass("dotActive");
        }
    })

    // The change event function for the "Job Type" filter option
    $('.jobTypeChk').change(function() {
        if ($(this).prop('checked')) {
            $(".menuHeader1").parent().addClass("headerActive");
            $(".dot1").addClass("dotActive");
        } else {
            var anyChecked = false;
            $('.jobTypeChk').each(function() {
                if ($(this).prop('checked')) {
                    anyChecked = true;
                }
            });
            if (!anyChecked) {
                $(".menuHeader1").parent().removeClass("headerActive");
                $(".dot1").removeClass("dotActive");
            }
        }
    })

    // Indicate selection for the "Other Filters" filter option
    $(".dropdown5 a").click(function() {
        $(".menuHeader5").text($(this).text());
        $(".menuHeader5").val($(this).text());
        $(".menuHeader5").parent().addClass("headerActive");
        $(".dot5").addClass("dotActive");
    });
    
    $(".dropdown6 a").click(function() {
        $(".menuHeader6").text($(this).text());
        $(".menuHeader6").val($(this).text());
    });

    

    /* $('#partTimeChk').click(function(e){
        if (e.target.checked) {
          localStorage.checked = true;
      } else {
          localStorage.checked = false;
      }
    })
    $( document ).ready(function() {
        document.querySelector('#partTimeChk').checked = localStorage.checked
    });

    $('#internChk').click(function(e){
        if (e.target.checked) {
          localStorage.checked = true;
      } else {
          localStorage.checked = false;
      }
    })
    $( document ).ready(function() {
        document.querySelector('#internChk').checked = localStorage.checked
    });

    $('#contractChk').click(function(e){
        if (e.target.checked) {
          localStorage.checked = true;
      } else {
          localStorage.checked = false;
      }
    })
    $( document ).ready(function() {
        document.querySelector('#contractChk').checked = localStorage.checked
    });

    $('#tempChk').click(function(e){
        if (e.target.checked) {
          localStorage.checked = true;
      } else {
          localStorage.checked = false;
      }
    })
    $( document ).ready(function() {
        document.querySelector('#tempChk').checked = localStorage.checked
    }); */

});



/* $("input:checkbox:not(:checked)").each(function() {
    var column = "table ." + $(this).attr("name");
    $(column).show();
});
$("input:checkbox").click(function(){
    var column = "table ." + $(this).attr("name");
    $(column).toggle();
}); */

// An auxiliary function for the double bar slider's change event that both indicates selection and displays slected range
function salarySelectionEvent(min, max) {
    $(".menuHeader4").text("$" + min + " - " + "$" + max);
    $(".menuHeader4").val("$" + min + " - " + "$" + max);
    $(".menuHeader4").parent().addClass("headerActive");
    $(".dot4").addClass("dotActive");
}

// A function that removes the selection indication for all filter options (and sets some options to default values)
/* function clearFilters() {
    $(".headerActive").removeClass("headerActive");
    $(".dotActive").removeClass("dotActive");
    $(".menuHeader1").text("Job Type");
    $(".menuHeader1").val("Job Type");
    $(".menuHeader2").text("Distance");
    $(".menuHeader2").val("Distance");
    $(".menuHeader3").text("Date Posted");
    $(".menuHeader3").val("Date Posted");
    $(".menuHeader4").text("Salary Range");
    $(".menuHeader4").val("Salary Range");
    $("#workAuthChk").removeAttr("checked");
    $("#fullTimeChk").removeAttr("checked");
    $("#partTimeChk").removeAttr("checked");
    $("#internChk").removeAttr("checked");
    $("#contractChk").removeAttr("checked");
    $("#internChk").removeAttr("checked");
    $("#tempChk").removeAttr("checked");
} */

function saveFilters(){
        console.log(document.getElementById("fullTimeChk").setAttribute("checked", "true"));
}

// An auxiliary function for the double bar slider's change event that returns a number with comma seperation (in string form)
function formatNumber(num) {
    return num.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,')
}