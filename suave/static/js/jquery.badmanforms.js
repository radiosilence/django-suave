(function($) {
    /* --------------------------------
     * GENERIC TING
     * ------------------------------ */
    var init_special_select = function($this, type) {
        var controls = jQuery('<div/>', {
            class: type,
        });
        jQuery('<ul/>').appendTo(controls);
        hide = jQuery('<div/>').appendTo(controls).hide();
        controls.insertBefore($this);
        $this.addClass('orig');
        $this.appendTo(hide);
        return controls;
    }


    /* --------------------------------
     * MULTIFILTER
     * ------------------------------ */

    var killa = function(li) {
        var a = jQuery('<a/>', {
            href: 'javascript:void(0)',
            html: 'x',
            class: 'kill',
        });
        a.appendTo(li);
    }


    var create_dropdown = function(options, selected) {
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


    var multifilter_update = function(controls) {
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


    var multifilter_change = function(event) {
        event.preventDefault();
        var select = $(event.currentTarget);
        var controls = $(event.delegateTarget);

        multifilter_update(controls);
    }


    var multifilter_kill = function(event) {
        event.preventDefault();
        controls = $(event.delegateTarget);
        var li = $(event.currentTarget).closest('li')
        var select = li.find('select');
        select.val(-1);
        multifilter_update(controls);
    }


    $.fn.multifilter = function(config) {
        config = config || {};

        this.each(function() {
            var $this = $(this)
              , options = $('option', $this)
              , selected = $('option:selected', $this)
              , controls = init_special_select($this, 'multifilter')
              ;

            $.each(selected, function(k, v) {
                var li = create_dropdown(options, v);
                li.appendTo($('ul', controls));
            })
            var li = create_dropdown(options);
            li.appendTo($('ul', controls));

            controls.on('change', 'select', multifilter_change);
            controls.on('click', 'a.kill', multifilter_kill);
        });
    }


    /* --------------------------------
     * CHECKGROUP
     * ------------------------------ */

    var create_check = function(value, selected, title, element) {
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


    var checkgroup_change = function(event) {
        event.preventDefault();
        var check = $(event.currentTarget)
          , controls = $(event.delegateTarget)
          , orig = $('select', controls)
          , option = $('option[value=' + check.attr('v') + ']', orig)
          , o = orig.val()
          ;

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


    $.fn.checkgroup = function(config) {
        config = config || {};

        this.each(function() {
            var $this = $(this)
              , options = $('option', $this)
              , selected = $('option:selected', $this)
              , controls = init_special_select($this, 'checkgroup')
              ;

            $.each(options, function(k, option) {
                title = $(option).text();
                $('ul', controls).append(create_check(
                    option.value,
                    option.selected,
                    title, $this
                ));
            });
            controls.on('change', 'input', checkgroup_change);
        });
    };

})(jQuery);