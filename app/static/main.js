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
                fileUploaded();
            },
            error: function(err) {
                console.log(err);
            }
        });

    });

    $('#analyse').on('click', function() {

        $('#analyse').html('<span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>' + '  Loading...');

        $.ajax({
            type: 'POST',
            url: '/analyse',
            success: function(succ) {
                $('#analyse').html('Analyse');
                afterAnalysis(succ);
            },
            error: function(e) {
                $('#analyse').html('Analyse');
                console.log(e)
            }
        })
    });

    $('#upload-more-test').on('submit', function() {
        $('#test-btn').html('<span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>' + '  Loading...');
        let fd = new FormData($('#upload-more-test')[0]);

        $.ajax({
            type: 'POST',
            url: '/test',
            data: fd,
            cache: false,
            dataType : 'json',
            contentType: false,
            processData: false,
            success: function(succ) {
                afterTest(succ);
                $('#test-btn').html('test');
            },
            error: function(err) {
                $('#test-btn').html('test');
            }
        })
    });

    function fileUploaded() {
        $('.upload-area').hide();
        $('#csv-uploaded').show();
        $('.analyse-area').show();
    }

    function afterAnalysis(succ) {
        $('.after-area').show();
        $('.upload-area').hide();
        $('.analyse-area').hide();
        $('#csv-analysed').show();
        if (succ && succ.accuracy) {
            $('#test-accuracy').html((succ.accuracy*100).toFixed(2));
        }
    }

    function afterTest(results) {
        $('#upload-more-test input')[0].value = '';
        $('.test-results-area').show();
        if (results && results.accuracy) {
            $('.test-results-area').append('<h2>Test accuracy was: ' + (results.accuracy*100).toFixed(2) + '%</h2>');
        }
        if (results && results.predictions && results.predictions.length > 0) {
            let ls = '';
            for (let i = 0; i < results.predictions.length; i++) {
                let lab = results.predictions[i] ? 'yes' : 'no';
                ls += '<li class="list-group-item">' + lab + '</li>'
            }
            $('.test-results-area').append('<h3>The test results were:</h3><ul>' + ls + '</ul>');
        }
    }

});
