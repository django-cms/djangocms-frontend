import $ from 'jquery';

/**
 * @class GridLayout
 * @public
 */
export default class GridLayout {
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
        let container = $('.form-row.field-xs_col .fieldBox, .form-row.field-row_cols_xs .fieldBox');
        let wrapper = wrapper => `<div class="icon-thead">${wrapper}</div>`;
        let icons = (icon, title = '') => `
            <span class="icon icon-${icon}" title="${title}"></span>
            <span class="icon-title">${title}</span>`
        let tmp = '';
        this.options.icons.forEach(function (item, index) {
            tmp = icons(item, this.options.sizes[index]);
            container.eq(index).prepend(wrapper(tmp));
        }, this);
    }

    /**
     * @method setColumn
     */
    setColumn() {
        let template = (text = '', link = '#') =>
            '<div class="field-box field-box-label">' +
            (link != "#" ? `<a href="${link}" target="_blank" class="d-inline-block text-right">` : '')
            + text
            + (link != "#" ? ' <span class="icon icon-info icon-primary"></span></a>' : "")
            + "</div>";
        let container = $(this.options.selector);
        let links = this.options.links;

        container.toArray().forEach(function (item, index) {
            $(item).prepend(template(this.options.rows[index], links[index]));
        }, this);
    }

    /**
     * @method setReset
     */
    setReset() {
        let container = $('.form-row.field-xs_col');
        let wrapper = container.closest('fieldset');
        let template = (text = this.options.reset) => `
            <a href="#" class="btn grid-reset">${text}</a>
        `;
        let button = $(template());

        button.on('click', function (event) {
            event.preventDefault();
            wrapper.find('input').removeClass("auto").val('');
            wrapper.find('input[type="checkbox"]').prop('checked', false);
        });

        container.append(button);
    }
}
