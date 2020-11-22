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
	var currentJobs = '';
	$('.result').each(function(i,obj){
	   currentJobs = currentJobs + $(this).attr("value")+ " ";
	});
	console.log(currentJobs)
	function filterJobs(){
	    $(".result").hide();
        $(".post").hide();
        $.ajax({
	        url: '/ajax/filterJobtype/',
	        data: {
	            'url': window.location.search,
	            'currentJobs': currentJobs,
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
                    if((data.results.length) === 1){
                        $("#postCount").html("1 Job Found")
                    }
                    else{
                        $("#postCount").html((data.results.length)+" Job Found");
                    }
                    $("#noJob").hide();
                    jQuery.each(data.newPosts, function(index, item){ //iterate through newPosts
                        console.log(index);
                        if($('#result'+item.id).length == '0') {
                            console.log('cloning');
                            var $lastListing = $('div[id^="result"]:last');
                            var $lastPost = $('div[id^="post"]:last');
                            var $cloneListing = $lastListing.clone().prop('id', 'result'+item.id);
                            var $clonePost = $lastPost.clone().prop('id', 'post'+item.id);
                            $cloneListing.find(".resultButton").val(item.id);
                            $cloneListing.find(".age").html(item.age);
                            $cloneListing.find(".resultCompany").html(item.company);
                            $cloneListing.find(".resultAddress").html(item.address);
                            $cloneListing.find(".resultButton").on("click",function(e){
                                var postId= $(this).val();
                                $(".post").hide();
                                $("#post"+postId).show();
                            });
                            $clonePost.find(".jobTitle").html(item.title);
                            $clonePost.find(".companyName").html(item.company);
                            $clonePost.find(".bannerImg").attr('src', item.banner);
                            $clonePost.find(".salary").html(item.salary);
                            $clonePost.find(".resultDescription").html(item.description);
                            $clonePost.find(".favoriteButton");
                            $clonePost.find(".applyButton").attr('href', '/applyjob/'+item.id);
                            $clonePost.find(".companyButton").attr('href', '/userviewcompany/'+item.id);
                            $lastListing.after($cloneListing);
                            $lastPost.after($clonePost);
                        }
                    });
	                jQuery.each(data.results, function(index, item) {
	                    if (index == 0){
	                        $("#post"+item).show();
	                    }
	                    $("#result"+item).show();
                    });
                    currentJobs = '';
                 	$('.result').each(function(i,obj){
	                        currentJobs = currentJobs + $(this).attr("value")+ " ";
	                });
	            }
	        }
	    });
	}
	$('.resultButton').on("click",function(e){
	    var postId= $(this).val();
	    console.log(postId);
	    $(".post").hide();
	    $("#post"+postId).show();
	});
	$('#jobTypeFilter').change(function() {
	            var checked = $("input[type='checkbox']:checked").attr('name');
                console.log(checked);
                if ($("input[type='checkbox']").is(":checked")){
                      $(".menuHeader1").parent().addClass("headerActive");
                      $(".dot1").addClass("dotActive");
                }
                else{
						    if ($(".menuHeader1").parent(".headerActive").length > 0){
						        $(".menuHeader1").parent().removeClass("headerActive");
						        $(".dot1").removeClass("dotActive");
						    }
                }
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
						if (selected_value != 0){
                            $(".menuHeader3").parent().addClass("headerActive");
                            $(".dot3").addClass("dotActive");
						}
						else{
						    if ($(".menuHeader3").parent(".headerActive").length > 0){
                                $(".menuHeader3").parent().removeClass("headerActive");
                                $(".dot3").removeClass("dotActive");
                            }
						}
						console.log(dateRange)
						filterJobs();
			        });
    $('#salaryFilter').change(function(){
//						selected_value = $("input[name='amount']:checked").val();
						if ( $("#salaryRangeChk").is(":checked")){
						    $(".menuHeader4").parent().addClass("headerActive");
						    $(".dot4").addClass("dotActive");
						    salary = true;
						}
						else{
						    if ($(".menuHeader4").parent(".headerActive").length > 0){
						        $(".menuHeader4").parent().removeClass("headerActive");
						        $(".dot4").removeClass("dotActive");
						    }
						    salary = false;
						}
						salaryAmount = $('#amount').val();
						filterJobs();
			        });
	$('#otherFilters').change(function(){
	    if($("input[type='checkbox']").is(":checked")){
						    $(".menuHeader5").parent().addClass("headerActive");
						    $(".dot5").addClass("dotActive");
	    }
	    else{
			    $(".menuHeader5").parent().removeClass("headerActive");
				$(".dot5").removeClass("dotActive");
	    }
	    filterJobs();
	});
	$('#clearFilter').on("click",function(e){
	    $('.filter').removeAttr('checked');
	    $('.default').attr('checked', true);
	    //reset job type filter
	    $(".menuHeader1").parent().removeClass("headerActive");
		$(".dot1").removeClass("dotActive");
	    //reset salary filter
	    $(".menuHeader4").parent().removeClass("headerActive");
		$(".dot4").removeClass("dotActive");
        //reset date filter
        $(".menuHeader3").parent().removeClass("headerActive");
        $(".dot3").removeClass("dotActive");
	    //reset other filter
	    $(".menuHeader5").parent().removeClass("headerActive");
	    $(".dot5").removeClass("dotActive");
        filterJobs();
	});
});