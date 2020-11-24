$(window).on('load', function(){
    if($("#favoriteJobs").length != 0){
        var url_mask = "{% url 'search_page'%}?job=id";

        $.ajax({
            url: '/ajax/load_favoritejobs/',
            dataType: 'json',
            success: function (respData) {
                for(x of respData.jobs) {
                    link = url_mask.replace("id", x[0])
                    $("#favoriteJobs").append(`<button class=\"btn btn-secondary\" onclick=\"window.location.href=\'${link}\'\">${x[1]} (#${x[0]})</button>`);
                }
            }
        });

        console.log("fav job loading function fired")
    }
});