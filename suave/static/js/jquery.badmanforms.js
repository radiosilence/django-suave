(function($, undefined) {

    /* --------------------------------
     * LIMIT SELECTS BASED ON OBJECT
     * --------------------------------*/

    $.fn.selimit = function(mapping, selector_child, selector_group) {
        if (!selector_group) {
            selector_group = 'body';
        }
        var limit = function() {
            var $this = $(this);
            var parent_sel = $this.find('option:selected');
            var $children = $this.closest(selector_group).find(selector_child);
            $children.xeach(function() {
                var child = this;
                var $child = $(child);
                if (parent_sel.length > 0) {
                    sel = parent_sel[0].value
                    if (sel == '') {
                        sel = -1;
                    }
                }

                if (sel == -1) {
                    $child.attr('disabled', 'disabled');
                    $child.val('');
                    return false;
                } else {
                    $child.removeAttr('disabled');
                }

                var parents = mapping[sel];
                var allowed = {}
                $(parents).xeach(function() {
                    allowed[this] = true;
                });

                var selected = $child.find('option:selected')[0];
                if (!allowed[selected.value]) {
                    $child.val('');
                }

                $child.find('option').xeach(function() {
                    if (allowed[this.value] || !this.value) {
                        this.style.display = 'block';
                    } else {
                        this.style.display = 'none';
                    }
                });
            });
        }
        this.xeach(limit);
        this.xeach(function() {
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
            'class': type
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



    $.fn.multifilter = function(o) {
        o = $.extend({
            onChange: function(event) {}
        }, o);

        var killa = function(li) {
            var a = jQuery('<a/>', {
                href: 'javascript:void(0)',
                html: 'x',
                'class': 'kill'
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
                    text: $this.text()
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


            var ov = [];
            $('ul li', controls).xeach(function(v) {
                var $this = $(this);
                var select = $this.find('select');
                if (select.val() != -1) {
                    ov.push(select.val());
                    if ($('a', $this).length == 0) {
                        killa($this);
                    }
                }
            });
            orig.val(ov);
            var li = create_dropdown($('option', orig));
            li.appendTo(ul);
        }


        var multifilter_change = function(event) {
            event.preventDefault();
            var select = $(event.currentTarget);
            var controls = $(event.delegateTarget);

            multifilter_update(controls);
            o.onChange(event);
        }


        var multifilter_kill = function(event) {
            event.preventDefault();
            controls = $(event.delegateTarget);
            var li = $(event.currentTarget).closest('li')
            var select = li.find('select');
            select.val(-1);
            multifilter_update(controls);
            o.onChange(event);
        }
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
    $.fn.checkgroup = function(o) {
        o = $.extend({
            onChange: function(event) {}
        }, o);

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
                'text': title
            });
            input.appendTo(li);
            label.appendTo(li);
            var br = jQuery('<br/>');
            br.appendTo(li);
            return li;
        }


        var checkgroup_change = function(event) {
            var check = $(event.currentTarget)
              , controls = $(event.delegateTarget)
              , orig = $('select', controls)
              , option = $('option[value=' + check.attr('v') + ']', orig)
              , ov = orig.val()
              ;

            if (ov == null) {
                var ov = [];
            }
            if (check.attr('checked')) {
                ov.push(check.attr('v'));
                orig.val(ov);
            } else {
                orig.val(jQuery.grep(ov, function(value) {
                  return value != check.attr('v');
                }));
            }
            o.onChange(event);
        };

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
                checkgroup_change(event);
            });
        });
    };

})(jQuery);