
$(document).ready(function() {
    function quickApply(){
    $.ajax({
	        url: '/ajax/quickApply/',
	        data: {
                'job': $('#quickApply').val()
	        },
	        dataType:'json',
	        success: function(data){
	            console.log('hi');
	        }
        });
    };
	$(".applyJob").on("click", function(e){
		$("#applyModal").show();
		$("#quickApply").val($(this).attr("name"));
		$("#applyManually").attr("href", $(this).val());
	});
	$("#quickApply").on("click", function(e){
		quickApply();
	});
});


