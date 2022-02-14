/*
 * Copyright (c) 2013, Divio AG
 * Licensed under BSD
 * http://github.com/divio/djangocms-boilerplate-webpack
 */

import $ from 'jquery';
// import ButtonGroup from 'components/button-group';
import GridLayout from 'components/grid-layout'
import { iconTemplate } from 'components/templates'


$(() => {
    // Row plugin
        const row = $('.djangocms-frontend-row')
    if (row.length) {
        const static_url = row.data().static;

        new GridLayout({
             selector: `
                .form-row.field-row_cols_xs
            `,
            sizes:  row.data().sizes,
            icons:  row.data().icons,
            rows:   row.data().rows,
            links:  row.data().links,
            static: static_url,
        });
        $('.form-row.field-create > div').before(
            iconTemplate('columns', static_url)
        );
    }

    // Column plugin
    const column = $('.djangocms-frontend-column');
    if (column.length) {
        const static_url = column.data().static;

        // Bootstrap 5 Grid Column - Responsive Settings
        new GridLayout({
            selector: `
                .form-row.field-xs_col,
                .form-row.field-xs_order,
                .form-row.field-xs_offset,
                .form-row.field-xs_ms,
                .form-row.field-xs_me
            `,
            sizes: column.data().sizes,
            icons: column.data().icons,
            rows: column.data().rows,
            reset: column.data().reset,
            links: column.data().links,
            static: static_url,
        });
    }
});
