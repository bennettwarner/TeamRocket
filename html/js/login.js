'use strict'

var authorized = false;

function userLogin() {
    $('#signin-button').on('click', function() {
        var email = $('#inputEmail').val();
        var pw = $("#inputPassword").val();
        $.ajax({
                url: '/api/auth',
                type: 'POST',
                data: {
                    username: email,
                    password: pw
                },
            }).done(function(data) {
                console.log(data.token);
                console.log(data.expires);
                localStorage.setItem('auth', data.token);
                // bring back to splash page
                window.location.href = "/";
                $('#join_group').prop('disabled', false);
                $('#host_group').prop('disabled', false);
                authorized = true;
            })
            .fail(function(data) {
                console.log(data.AuthError);
            });
    });

}


function init() {
    
    userLogin();
}

init();
