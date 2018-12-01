'use strict'

function join_game() {
    // $('#join_submit').on('click', function() {
        $.ajax({
            url: '/api/event/list',
            type: 'GET',
            cache: false,
            timeout: 600000,
        }).done(function(data) {
          console.log(data[0]);
            //for (event in data) {
            //    console.log(event);
            //    };

        });
    // });
}

function init() {
    join_game();
}

init();
