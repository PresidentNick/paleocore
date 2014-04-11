$(document).ready(function() {
    var search_data_table = $('#search_data_table');

    var input = $('#search_box');
    input.jqxInput({placeHolder: 'Enter Search', height: 25, width: 200, minLength: 1});

    var button = $('#search_box_button');
    button.jqxButton({width: 45});
    button.click(function() {
        var val = input.val();
        var csrftoken = $.cookie('csrftoken');

        var url = window.location.href;
        var beginning_project_name_index = url.indexOf('/data/search/')+13;
        var end_project_name_index = url.indexOf('/', beginning_project_name_index);
        var project_name = url.substring(beginning_project_name_index, end_project_name_index);
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                function getCookie(name) {
                    var cookieValue = null;
                    if (document.cookie && document.cookie != '') {
                        var cookies = document.cookie.split(';');
                        for (var i = 0; i < cookies.length; i++) {
                            var cookie = jQuery.trim(cookies[i]);
                            // Does this cookie string begin with the name we want?
                            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                break;
                            }
                        }
                    }
                    return cookieValue;
                }
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    // Only send the token to relative URLs i.e. locally.
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            }
        });
        $.ajax({
            type:'POST',
            url: '/data/search/' + project_name + '/',
            contentType: 'application/x-www-form-urlencoded',
            data: {
                'post_action': 'search_box_query',
                'query': val
            },
            success: function(data) {
                var data_inside = data.substring(data.indexOf('>') + 1, data.lastIndexOf('<'));
                search_data_table.html(data_inside);
            }
        });
    });
});