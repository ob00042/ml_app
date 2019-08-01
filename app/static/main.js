$(document).ready(function() {
    console.log("fully loaded");

    $('#upload-csv-form').on('submit', function() {

        let fd = new FormData($('#upload-csv-form')[0]);

        $.ajax({
            type: "POST",
            url: "/upload",
            data: fd,
            cache: false,
            dataType : 'json',
            contentType: false,
            processData: false,
            success: function(su) {
                console.log(su);
                fileUploaded();
            },
            error: function(err) {
                console.log(err);
            }
        });

    });

    $('#analyse').on('click', function() {
        $.ajax({
            type: 'POST',
            url: '/analyse',
            success: function(s) {
                console.log(s);
            },
            error: function(e) {
                console.log(e)
            }
        })
    });

    function fileUploaded() {
        $('.upload-area').hide();
        $('#csv-uploaded').show();
        $('.analyse-area').show();
    }

});
