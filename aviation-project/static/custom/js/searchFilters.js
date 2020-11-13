$(document).ready(function() {
	//variable for distance
	var distance = 0;
	//variable for date posted
	var dateRange = 0;
	//variables for salary range
	var salary = false;
	var salaryAmount = $('#amount').val();
	//variable for US Work Auth
	var usAuth = false;
	function filterJobs(){

	}
    $('#fullTimeChk').change(function() {
        //uncheck all jobs
    	if($('#allJobsChk').is(":checked")){
    		$('#allJobsChk').prop('checked', false);
    	}
        $.ajax({
	        url: '/ajax/filterJobtype/',
	        data: {
	            'url': window.location.search,
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
	            console.log(data.results)
	        }
	    })
      	console.log($(this).is(':checked'));
    });
});