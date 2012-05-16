jQuery(function($) {
    $('div.inline-group').sortable({
        items: 'tr.has_original',
        handle: 'td',
        update: function() {
            $(this).find('tr.has_original').each(function(i) {
                $(this).find('input[name$=order]').val(i+1);
                $(this).removeClass('row1').removeClass('row2');
                $(this).addClass('row'+((i%2)+1));
            });
        }
    });
    $('tr.has_original').css('cursor', 'move');
});
