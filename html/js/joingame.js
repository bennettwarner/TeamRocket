'use strict'

function join_game() {
    // $('#join_submit').on('click', function() {
        var attendee_location = $('#att_location').val();
        var type = $('#game_type').val();
        $.ajax({
            url: 'api/event/list',
            type: 'GET',
            data: {
                location: attendee_location,
                game_type: type
            },
            cache: false,
            timeout: 600000,
        }).done(function(data) {
            // take back to login screen?
            if (data['events'].length > 0) {
                data['events'].forEach((event) => {
                    $('#events').append(`<li>${event}<li>`)
                });
            }

        });
    // });
}

function init() {
    join_game();
}

init();