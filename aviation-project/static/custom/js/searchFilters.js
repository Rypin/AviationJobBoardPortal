$(document).ready(function() {
	//variable for distance
	var distance = 25;
	//variable for date posted
	var dateRange = 0;
	//variables for salary range
	var salary = false;
	var salaryAmount = $('#amount').val();
	//variable for US Work Auth
	var usAuth = false;
	var oldJobs = $(".resultButton").map(function(){return $(this).val();}).get();
	console.log(oldJobs)
	function filterJobs(){
	    $(".result").hide();
        $(".post").hide();
        $.ajax({
	        url: '/ajax/filterJobtype/',
	        data: {
	            'url': window.location.search,
	            'oldJobs': oldJobs,
	            'Full-Time': $('#fullTimeChk').is(":checked"),
	            'Part-Time': $('#partTimeChk').is(":checked"),
	            'Internship': $('#internChk').is(":checked"),
	            'Temporary': $('#tempChk').is(":checked"),
	            'Contract': $('#contractChk').is(":checked"),
	            'distance': distance,
	            'dateRange': dateRange,
	            'salary': salary,
	            'salaryRange': salaryAmount,
	            'USAuth': usAuth
	        },
	        dataType:'json',
	        success: function(data){
	            if (data.results.length === 0){
	                $("#postCount").html("")
	                $("#noJob").show();
	            }
	            else{
	                jQuery.each(data.results, function(index, item) {
	                    if (index == 0){
	                        $("#post"+item).show();
	                    }
	                    $("#result"+item).show();
                    });
                    if((data.results.length) === 1){
                        $("#postCount").html("1 Job Found")
                    }
                    else{
                        $("#postCount").html((data.results.length)+" Job Found");
                    }
	            }
	            for(var key in data.newJobs){
	            	console.log(key);
	            	console.log(data.newJobs.key);
	            }
	        }
	    });
	}
	$('.resultButton').on("click",function(e){
	    var postId= $(this).val();
	    $(".post").hide();
	    $("#post"+postId).show();
	});
	$('#jobTypeFilter').change(function() {
	            var test = $("input[type='checkbox']:checked").attr('name');
        console.log(test);
	    filterJobs();
	});
    $('#distanceFilter').change(function(){
						selected_value = $("input[name='distance']:checked").val();
						distance = selected_value;
						filterJobs();
			        });
    $('#dateFilter').change(function(){
						selected_value = $("input[name='posted_dur']:checked").val();
						dateRange = selected_value;
						console.log(dateRange)
						filterJobs();
			        });
    $('#salaryFilter').change(function(){
						selected_value = $("input[name='amount']:checked").val();
                        salary= $("#salaryRangeChk").is(":checked");
						dateRange = selected_value;
						salaryAmount = $('#amount').val();
						filterJobs();
			        });
	$('#workAuthChk').change(function(){
                        filterJobs();
	});
});