(function($, undefined) {

    /* --------------------------------
     * LIMIT SELECTS BASED ON OBJECT
     * --------------------------------*/

    $.fn.selimit = function(reference, selector_child, selector_group) {
        if (!selector_group) {
            selector_group = 'body';
        }
        var limit = function() {
            var $this = $(this);
            var parent_sel = $this.find('option:selected');
            var $child = $this.closest(selector_group).find(selector_child);
            var child = $child[0];
            if (parent_sel.length > 0){
                parent_sel = parent_sel[0].value
                if (parent_sel == '') {
                    parent_sel = -1;
                }
            } else {
                return false;
            }
            var selected = $child.find('option:selected')[0];

            var contacts = reference[parent_sel];
            if ($.inArray(parseInt(selected.value), contacts) == -1) {
                $child.val('');
            }
            $.each($child.find('option'), function(k, option) {
                if ($.inArray(parseInt(option.value), contacts) !== -1 || !option.value) {
                    $(option).show();
                } else {
                    $(option).hide();
                }
            });
            if (parent_sel == -1) {
                $child.attr('disabled', 'disabled');
            } else {
                $child.removeAttr('disabled');
            }
        }
        this.each(limit);
        this.each(function() {
            $(this).on('change', limit);
        })
    };

    /* --------------------------------
     * FAST EACHTING
     * --------------------------------*/

    $.fn.xeach = function(callback) {
        for(var i=0,len=this.length; value=this[i], i<len; i++) {
            callback.apply(value);
        }
    };


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
        options.xeach(function() {
            $this = $(this);
            var option = jQuery('<option/>', {
                value: this.value,
                text: $this.text(),
            });
            if (this.value == selected.value) {
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

        $('ul li', controls).xeach(function() {
            $this = $(this);
            var select = $('select', $this);
            if (select.val() > 0) {
            } else {
                select.closest('li').remove();
                select.remove();
            }
        })


        var o = [];
        $('ul li', controls).xeach(function(v) {
            var $this = $(this);
            var select = $this.find('select');
            if (select.val() != -1) {
                o.push(select.val());
                if ($('a', $this).length == 0) {
                    killa($this);
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


    $.fn.multifilter = function(o) {
        o = $.extend({
            onChange: function(event) {},
        }, o);

        this.xeach(function() {
            var $this = $(this)
              , options = $('option', $this)
              , selected = $('option:selected', $this)
              , controls = init_special_select($this, 'multifilter')
              ;

            selected.xeach(function() {
                var $this = $(this);
                var li = create_dropdown(options, this);
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
        check_id = 'check_' + element.parent().attr('name') + '_' + value;
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


    var checkgroup_change = function(event, callback) {
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
        callback(event);
    };
    $.fn.checkgroup = function(o) {
        o = $.extend({
            onChange: function(event) {},
        }, o);
        this.xeach(function() {
            var $this = $(this)
              , options = $('option', $this)
              , selected = $('option:selected', $this)
              , controls = init_special_select($this, 'checkgroup')
              ;

            options.xeach(function() {
                var $this = $(this);
                title = $this.text();
                $('ul', controls).append(create_check(
                    this.value,
                    this.selected,
                    title, $this
                ));
            });
            controls.on('change', 'input', function(event) {
                event.preventDefault();
                checkgroup_change(event, o.onChange);
            });
        });
    };

})(jQuery);