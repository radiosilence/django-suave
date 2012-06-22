/* --------------------------------
 * GENERIC TING
 * ------------------------------ */

function init_special_select(element, type) {
    old = element.parent().parent().find('div.' + type);
    old.remove();
    var controls = jQuery('<div/>', {
        class: type,
    });
    jQuery('<ul/>').appendTo(controls);
    hide = jQuery('<div/>').appendTo(controls).hide();
    controls.prependTo(element.parent());
    element.addClass('orig');
    element.appendTo(hide);
    return controls;
}


/* --------------------------------
 * MULTIFILTER
 * ------------------------------ */
function killa(li) {
    var a = jQuery('<a/>', {
        href: 'javascript:void(0)',
        html: 'x',
        class: 'kill',
    });
    a.appendTo(li);
}


function create_dropdown(options, selected) {
    if (selected == undefined) {
        selected = { value: -1 }
    }
    var li = jQuery('<li/>');
    var select = jQuery('<select/>');
    var option = jQuery('<option/>', {
        value: -1,
        text: '- Select One -'
    });
    option.appendTo(select);
    $.each(options, function(k, v) {
        v = $(v);
        var option = jQuery('<option/>', {
            value: v.val(),
            text: v.text(),
        });
        if (v.val() == selected.value) {
            option.attr('selected', true);
        }
        option.appendTo(select);
    })
    select.appendTo(li);
    if (selected.value > 0) {
        killa(li);
    }
    return li;
}


function multifilter_update(controls) {
    var orig = $('select.orig', controls);
    var ul = $('ul', controls);

    $('ul li', controls).each(function(k, v) {
        var select = $('select', $(v));
        if (select.val() > 0) {
        } else {
            select.closest('li').remove();
            select.remove();
        }
    })


    var o = [];
    $('ul li', controls).each(function(k, v) {
        var li = $(v);
        var select = li.find('select');
        if (select.val() != -1) {
            o.push(select.val());
            if ($('a', li).length == 0) {
                killa(li);
            }
        }
    });
    orig.val(o);
    var li = create_dropdown($('option', orig));
    li.appendTo(ul);
}


function multifilter_change(event) {
    event.preventDefault();
    var select = $(event.currentTarget);
    var controls = $(event.delegateTarget);

    multifilter_update(controls);
}

var multifilter_change_debounced = _.debounce(multifilter_change, 10);


function multifilter_kill(event) {
    event.preventDefault();
    controls = $(event.delegateTarget);
    var li = $(event.currentTarget).closest('li')
    var select = li.find('select');
    select.val(-1);
    multifilter_update(controls);
}

var multifilter_kill_debounced = _.debounce(multifilter_kill, 10);


$.fn.multifilter = function(options) {
    $(this).each(function(i, element) {
        var element = $(element);
        var options = $('option', element);
        var selected = $('option:selected', element);
        var controls = init_special_select(element, 'multifilter');

        $.each(selected, function(k, v) {
            var li = create_dropdown(options, v);
            li.appendTo($('ul', controls));
        })
        var li = create_dropdown(options);
        li.appendTo($('ul', controls));

        controls.on('change', 'select', multifilter_change_debounced);
        controls.on('click', 'a.kill', multifilter_kill_debounced);
    });
}


/* --------------------------------
 * CHECKGROUP
 * ------------------------------ */

function create_check(value, selected, title, element) {
    if (selected) {
        var ch = ' checked';
    } else {
        var ch = '';
    }
    check_id = 'check_' + element.attr('name') + '_' + value;
    var li = jQuery('<li/>');
    var input_attrs = {
        'v': value,
        id: check_id,
        type: 'checkbox'
    }
    if (selected) {
        input_attrs['checked'] = true;
    }
    var input = jQuery('<input/>', input_attrs);
    var label = jQuery('<label/>', {
        'for': check_id,
        'text': title,
    });
    input.appendTo(li);
    label.appendTo(li);
    var br = jQuery('<br/>');
    br.appendTo(li);
    return li;
}


function checkgroup_change(event) {
    event.preventDefault();
    var check = $(event.currentTarget);
    var controls = $(event.delegateTarget);
    var orig = $('select', controls);
    var option = $('option[value=' + check.attr('v') + ']', orig);

    var o = orig.val();
    if (o == null) {
        var o = [];
    }
    if (check.attr('checked')) {
        o.push(check.attr('v'));
        orig.val(o);
    } else {
        orig.val(jQuery.grep(o, function(value) {
          return value != check.attr('v');
        }));
    }
};

var checkgroup_change_debounced = _.debounce(checkgroup_change, 10);


$.fn.checkgroup = function(options) {
    $(this).each(function(i, element) {
        var element = $(element);
        var options = $('option', element);
        var selected = $('option:selected', element);
        var controls = init_special_select(element, 'checkgroup');
        $.each(options, function(k, option) {
            title = $(option).text();
            $('ul', controls).append(create_check(option.value, option.selected,
                title, element));
        });
        controls.on('change', 'input', checkgroup_change);
    });
};