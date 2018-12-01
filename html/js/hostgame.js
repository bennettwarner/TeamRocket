'use strict'

function hostGame() {
    $('#host_submit').on('click', function() {
        var title = $('#title').val();
        var location = $('#location').val();
        var time = $('#event_date').val();
        var details = $('#event_details').val();
        var required = $('#items_required').val();
        var fee = $('#event_fee').val();
        var game = $('#game').val();
        if (title && location && time && details && game) {
            $.ajax({
                url: '/api/event/create',
                type: 'POST',
                data: {

                    title: title,
                    location: location,
                    time: time,
                    description: details,
                    required: required,
                    fee: fee,
                    game: game

                },
                beforeSend: function(xhr) { xhr.setRequestHeader('Authorization', localStorage.getItem('auth')); },
                cache: false,
                timeout: 600000,
            }).done(function(data) {
                console.log(data);
                console.log('Success! Event created');
            });
        }

    });
}

function init() {
    hostGame();
}

init();