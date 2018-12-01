'use strict'


function userLogin() {
    var email = $('#inputEmail').val();
    var pw = $("#inputPassword").val();

    $('#signin-button').on('click', function() => {
        $.ajax({
                url: 'auth',
                type: 'POST',
                data: {
                    email: email,
                    pw: pw
                },
            }).done(function(data) {

                console.log(data.token);
                console.log(data.expires);
                localStorage.setItem('auth', data.token);
                // bring back to splash page

            })
            .fail(function(data) {
                console.log(data.AuthError);
            });
    });

}



function createAccount() {
    var email = $("email").val();
    var new_pass = $('#new_password').val();

    $.ajax({
        url: '',
        type: 'POST',
        data: {
            email: email,
            password: new_pass
        },
        cache: false,
        timeout: 600000,
    }).done(function(data) {
        // take back to login screen?

    }).fail(function(data){

    });
}



function init() {
    userLogin();
}

init();