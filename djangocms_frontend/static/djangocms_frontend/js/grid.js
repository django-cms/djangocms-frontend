/**
 * @class GridLayout
 * @public
 */
class GridLayout {
    /**
     * @method constructor
     * @param {Object} options
     * @param {Array} options.sizes
     * @param {Array} options.icons
     * @param {Array} options.row
     * @param {String} options.reset
     * @param {String} options.static
     * @param {string} options.selector
     */
    constructor(options) {
        this.options = options;

        this.setHeader();
        this.setColumn();
        this.setReset();
    }

    /**
     * @method setHeader
     */
    setHeader() {
        const container = document.querySelectorAll('.form-row.field-xs_col .fieldBox, .form-row.field-row_cols_xs .fieldBox');
        const wrapper = wrapper => `<div class="icon-thead">${wrapper}</div>`;
        const icons = (icon, title = '') => `
            <span class="icon icon-${icon}" title="${title}"></span>
            <span class="icon-title">${title}</span>`

        for (const icon of this.options.icons) {
            const tmp = icons(icon, this.options.sizes[this.options.icons.indexOf(icon)]);
            container[this.options.icons.indexOf(icon)].insertAdjacentHTML('afterbegin', wrapper(tmp));
        }
    }

    /**
     * @method setColumn
     */
    setColumn() {
        const infoIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="icon-info icon-primary" viewBox="0 0 16 16"><path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16m.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2"/></svg>';
        const template = (text = '', link = '#') => (
            '<div class="field-box field-box-label">' +
            (link != "#" ? `<a href="${link}" target="_blank">` : '')
            + text
            + (link != "#" ? ` ${infoIcon}</a>` : "")
            + '</div>'
        );
        const container = document.querySelectorAll(this.options.selector);
        const links = this.options.links;

        Array.from(container).forEach((item, index) => {
            item.insertAdjacentHTML('afterbegin', template(this.options.rows[index], links[index]));
        });
    }

    /**
     * @method setReset
     */
    setReset() {
        const container = document.querySelector('.form-row.field-xs_col');
        const wrapper = container.closest('fieldset');
        const template = (text = this.options.reset) => `
            <a href="#" class="btn grid-reset">${text}</a>
        `;
        const button = document.createElement('div');
        button.innerHTML = template();

        button.firstElementChild.addEventListener('click', function (event) {
            event.preventDefault();
            wrapper.querySelectorAll('input').forEach(input => {
                input.classList.remove("auto");
                input.value = '';
            });
            wrapper.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
                checkbox.checked = false;
            });
        });
        container.append(button.firstElementChild);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // Row plugin

    const row = document.querySelector('.djangocms-frontend-row');
    const iconTemplate = (icon, title = '') => `<span class="icon icon-${icon}" title="${title}"></span>`
    if (row) {
        const static_url = row.dataset.static;

        new GridLayout({
             selector: `
                .form-row.field-row_cols_xs
            `,
            sizes:  JSON.parse(row.dataset.sizes),
            icons:  JSON.parse(row.dataset.icons),
            rows:   JSON.parse(row.dataset.rows),
            links:  JSON.parse(row.dataset.links),
            static: static_url,
        });
        const createRow = document.querySelector('.form-row.field-create > div');

        if (createRow) {
            createRow.insertAdjacentHTML('beforebegin', iconTemplate('columns'));
        }
    }

    // Column plugin
    const column = document.querySelector('.djangocms-frontend-column');
    if (column) {
        const static_url = column.dataset.static;

        // Bootstrap 5 Grid Column - Responsive Settings
        new GridLayout({
            selector: `
                .form-row.field-xs_col,
                .form-row.field-xs_order,
                .form-row.field-xs_offset,
                .form-row.field-xs_ms,
                .form-row.field-xs_me
            `,
            sizes: JSON.parse(column.dataset.sizes),
            icons: JSON.parse(column.dataset.icons),
            rows: JSON.parse(column.dataset.rows),
            reset: column.dataset.reset,
            links: JSON.parse(column.dataset.links),
            static: static_url,
        });
    }

});
