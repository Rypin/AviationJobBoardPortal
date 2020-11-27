// $(window).on('load', function() {
//     if($("#favoriteJobs").length != 0){
//         var url_mask = "{% url 'search_page'%}?job=id";

//         $.ajax({
//             url: '/ajax/load_favoritejobs/',
//             dataType: 'json',
//             success: function (respData) {
//                 for(x of respData.jobs) {
//                     link = url_mask.replace("id", x[0])
//                     $("#favoriteJobs").append(`<button class=\"btn btn-secondary\" onclick=\"window.location.href=\'${link}\'\">${x[1]} (#${x[0]})</button>`);
//                 }
//             }
//         });

//         console.log("fav job loading function fired")
//     }
// });

$(window).on('load', function() {
    refreshSideBarFavJobListings();
    refreshFavJobListings();
});


$(".outer").click(function() {
    console.log("button clicked");
    toggleFavoriteForJob($(this));
    //refreshSideBarFavJobListings();
    //refreshFavJobListings();
});

function toggleFavoriteForJob(elemObject) {
    console.log("Job id clicked: " + Number(elemObject.attr('value')));

    $.ajax({
        url: '/ajax/add_favoritejobs/',
        data: {
            'JobID': Number(elemObject.attr('value'))
        },
        dataType: 'json',
        success: function (respData) {
            refreshSideBarFavJobListings();
            //refreshFavJobListings();
            $(elemObject).toggleClass("unfavoritedBody favoritedBody");
            $(elemObject).children(":first").toggleClass("fa-heart fa-heart-o");
            $(elemObject).children(":first").toggleClass("unfavoritedHeart favoritedHeart");
        }
    });
}


function refreshSideBarFavJobListings() {
    
    $("#favoriteJobs").empty();

    var url_mask = global_vars.searchPageURL + "?job=id";

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

    console.log("function 1 fired");
    
}

function refreshFavJobListings() {
    $.ajax({
        url: '/ajax/refresh_favoritejobbutton_styles/',
        dataType: 'json',
        success: function (respData) {
            var allFavButtons = $(".outer").toArray();
            //console.log(respData.jobIDs);
            for(x of allFavButtons) {
                if(respData.jobIDs.includes(Number(x.getAttribute('value')))){
                    $(x).toggleClass("unfavoritedBody favoritedBody");
                    $(x).children(":first").toggleClass("fa-heart fa-heart-o");
                    $(x).children(":first").toggleClass("unfavoritedHeart favoritedHeart");
                }
            }



            
            // for(x of respData.jobIDs) {
            //     for(y of allFavButtons) {
            //         if(x == y.getAttribute('value')) {
            //             $(y).toggleClass("unfavoritedBody favoritedBody");
            //             $(y).children(":first").toggleClass("fa-heart fa-heart-o");
            //             $(y).children(":first").toggleClass("unfavoritedHeart favoritedHeart");

            //             /*
            //             $(y).toggleClass("unselected selected");
            //             $(y).toggleClass("fa-heart fa-heart-o");
            //             $(y).toggleClass("unfavoritedHeart favoritedHeart");
            //             $(y).parent().toggleClass("unfavoritedBody favoritedBody"); */
            //         }
            //     }
            // }
        }
    });

    console.log("function 2 fired");
}