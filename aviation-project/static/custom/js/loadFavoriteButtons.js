$(window).on('load', function() {
    refreshFavJobListings();
});

function refreshFavJobListings() {
    $.ajax({
        url: '/ajax/refresh_favoritejobbutton_styles/',
        dataType: 'json',
        success: function (respData) {
            var allFavButtons = $(".outer").toArray();
            for(x of allFavButtons) {
                if(respData.jobIDs.includes(Number(x.getAttribute('value')))){
                    $(x).toggleClass("unfavoritedBody favoritedBody");
                    $(x).children(":first").toggleClass("fa-heart fa-heart-o");
                    $(x).children(":first").toggleClass("unfavoritedHeart favoritedHeart");
                }
            }
        }
    });

    console.log("refreshFavJobListings() fired");
}

$(".outer").click(function() {
    console.log("favorite button clicked");
    toggleFavoriteForJob($(this));
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
            $(elemObject).toggleClass("unfavoritedBody favoritedBody");
            $(elemObject).children(":first").toggleClass("fa-heart fa-heart-o");
            $(elemObject).children(":first").toggleClass("unfavoritedHeart favoritedHeart");
        }
    });
}