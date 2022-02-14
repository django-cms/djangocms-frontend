/*
 * Copyright (c) 2013, Divio AG
 * Licensed under BSD
 * http://github.com/divio/djangocms-boilerplate-webpack
 */

// import 'bootstrap/js/dist/alert'
import $ from 'jquery';
import PreviewGenerator from 'components/preview-generator';


window.djangoCMSFrontend = {
    $,
};

$(() => {
    // IMAGE PREVIEW
    if ($('.djangocms-frontend-link').length) {
        new PreviewGenerator({
            container: '.djangocms-frontend-link',
            title: $('.djangocms-frontend-link').data().preview,
        });
    }
});
