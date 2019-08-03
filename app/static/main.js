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

        let model = $('.model-choice:checked').val();

        $('#analyse').html('<span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>' + '  Loading...');

        $.ajax({
            type: 'POST',
            url: '/analyse',
            data: {'model': model},
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
                $('#test-btn').html('Test');
            },
            error: function(err) {
                $('#test-btn').html('Test');
            }
        })
    });

    $('#enter-data-form').on('submit', function() {
        $('#test-directly').html('<span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>' + '  Loading...');
        let data = {'data': {}};

        $('#enter-data-form select, #enter-data-form input').each((i, el) => {
           let n = $(el).attr('name');
           let v = $(el).val();
           if (['day', 'balance', 'age'].includes(n)) {
               v = parseInt(v);
           }
           data['data'][n] = v;
        });

        $.ajax({
            type: 'POST',
            url: '/direct',
            contentType: "application/json",
            data: JSON.stringify(data),
            dataType: "json",
            success: function(succ) {
                afterTest(succ);
                $('#test-directly').html('Test directly');
            },
            error: function(err) {
                $('#test-directly').html('Test directly');
            }
        });
    });

    function fileUploaded() {
        $('.upload-area').hide();
        $('#csv-uploaded').show();
        $('.analyse-area').show();
    }

    function afterAnalysis(succ) {
        if (succ && succ.options) {
            showOptions(succ.options);
        }
        $('.after-area').show();
        $('.upload-area').hide();
        $('.analyse-area').hide();
        $('#csv-analysed').show();
        if (succ && succ.accuracy && typeof succ.accuracy === 'number') {
            $('#test-accuracy').html((succ.accuracy*100).toFixed(2));
        }
    }

    function showOptions(opts) {
        Object.keys(opts).forEach(function(key) {
            if (opts[key]) {
                let selectOpts = '';
                opts[key].forEach((v) => {selectOpts += '<option value="' + v + '">' + v + '</option>'});
                $('#enter-data-form').prepend('<div class="form-group row"><label for="enter-' + key + '" class="col-sm-2 col-form-label">' + key + '</label>' +
                    '<div class="col-sm-10"><select class="form-control custom-select" name="' + key + '" id="enter-' + key + '">' + selectOpts + '</select></div></div>');
            }
            else {
                $('#enter-data-form').prepend('<div class="form-group row"><label for="enter-' + key + '" class="col-sm-2 col-form-label">' + key + '</label>' +
                    '<div class="col-sm-10"><input name="' + key + '" id="enter-' + key + '" class="form-control"></div></div>');
            }
        });

    }

    function afterTest(results) {
        $('#upload-more-test input')[0].value = '';
        $('.test-results-area').show();
        if (results && results.accuracy !== null && typeof results.accuracy === 'number') {
            $('.test-results-area').append('<h2>Test accuracy was: ' + (results.accuracy*100).toFixed(2) + '%</h2>');
        }
        if (results && results.predictions && results.predictions.length > 0) {
            let ls = '';
            for (let i = 0; i < results.predictions.length; i++) {
                ls += '<li class="list-group-item">' + results.predictions[i] + '</li>'
            }
            $('.test-results-area').append('<h3>The test results were:</h3><ul>' + ls + '</ul>');
        }
    }

});
