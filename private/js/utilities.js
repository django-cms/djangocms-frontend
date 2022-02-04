/*
 * Copyright (c) 2013, Divio AG
 * Licensed under BSD
 * http://github.com/divio/djangocms-boilerplate-webpack
 */

import $ from 'jquery';
import ButtonGroup from 'components/button-group';


$(() => {
    // Row plugin
    if ($('.djangocms-frontend-spacing').length) {
        const static_url = $('.djangocms-frontend-spacing').data().static;

        new ButtonGroup({
            static: static_url,
            select: '#id_space_property',
        });
        new ButtonGroup({
            static: static_url,
            select: '#id_space_sides',
        });
        new ButtonGroup({
            static: static_url,
            select: '#id_space_size',
        });
        new ButtonGroup({
            static: static_url,
            select: '#id_space_device',
            icons: ['align-reset', 'size-xs', 'size-sm', 'size-md', 'size-lg', 'size-xl', 'size-xxl'],
        });
    }
    if ($('.djangocms-frontend-tabs').length) {
        const static_url = $('.djangocms-frontend-tabs').data().static;

        new ButtonGroup({
            static: static_url,
            select: '#id_tab_padding_size',
        });
        new ButtonGroup({
            static: static_url,
            select: '#id_tab_padding_side',
        });
    }
});
