CMS.$(document).ready(function () {
    const set_auto_class = function(item) {
        if(item.val() !== "" && item.val() == 0) {
            item.addClass("auto");
            item.val("0");
        } else {
            item.removeClass("auto");
        }
    }
    var input_fields = CMS.$('input[type="number"].auto-field');
    var span = $("<span></span>").css("font-size", input_fields.css("font-size"));
    input_fields
        .after(span)
        .keypress(function(event) {
                if(event.which === 97 || event.which === 65) {
                    CMS.$(this).val("0");
                    set_auto_class(CMS.$(this));
                    event.preventDefault();
                }
            })
        .change(function(event) {
                set_auto_class(CMS.$(this));
             })
        .keyup(function(event) {
                set_auto_class(CMS.$(this));
            })
        .each(function(no, item) {
            set_auto_class(CMS.$(item));
            CMS.$(item.nextSibling).click(function() {
                console.log("CLICK");
                this.previousSibling.focus();
            });
        }
    )
});
