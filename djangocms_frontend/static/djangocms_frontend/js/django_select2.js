'use strict';
jQuery(document).ready(function () {
    if (jQuery.fn.jquery == CMS.$.fn.jquery) {
        const $ = CMS.$;
    } else {
        const $ = jQuery;
    }

    var init = function ($element, options) {
        $element.select2(options)
    }

    var initHeavy = function ($element, options) {
        console.log("initHeavy", $.fn.jquery);

        var settings = $.extend({
            ajax: {
                data: function (params) {
                    var result = {
                        term: params.term,
                        page: params.page,
                        field_id: $element.data('field_id')
                    }

                    var dependentFields = $element.data('select2-dependent-fields')
                    if (dependentFields) {
                        dependentFields = dependentFields.trim().split(/\s+/)
                        $.each(dependentFields, function (i, dependentField) {
                            result[dependentField] = $('[name=' + dependentField + ']', $element.closest('form')).val()
                        })
                    }

                    return result
                },
                processResults: function (data, page) {
                    return {
                        results: data.results,
                        pagination: {
                            more: data.more
                        }
                    }
                }
            }
        }, options)

        $element.select2(settings)
    }

    $.fn.djangoSelect2 = function (options) {
        var settings = $.extend({}, options)
        $.each(this, function (i, element) {
            console.log("$element", $.fn.jquery);
            var $element = $(element)
            if ($element.hasClass('django-select2-heavy')) {
                initHeavy($element, settings)
            } else {
                init($element, settings)
            }
            $element.on('select2:select', function (e) {
                var name = $(e.currentTarget).attr('name')
                $('[data-select2-dependent-fields=' + name + ']').each(function () {
                    $(this).val('').trigger('change')
                })
            })
        })
        return this
    }

    $(function () {
        $('.django-select2').djangoSelect2()
    })
})
