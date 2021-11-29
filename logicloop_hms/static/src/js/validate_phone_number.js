odoo.define('logicloop_hms.validate_phone_number', function (require){
'use strict';
alert("ok");
var FieldPhone = require('web.basic_fields').FieldPhone;
var core = require('web.core');
var field_registry = require('web.field_registry');
var ajax = require('web.ajax');
var rpc = require('web.rpc');
var _t = core._t;
var QWeb = core.qweb;
var ValidateMobileNumber = FieldPhone.extend({
     className: 'o_field_intl_phone',
    resetOnAnyFieldChange: true,
    error_message: _t("not a valid mobile Number"),
     _render: function () {
        let response = null;
        this._super.apply (this, arguments);


        var access_key = '740609c0c770703d7fd0b2bc8f4324af'
        var phone_number = this.value
        $.ajax({
        url: 'http://apilayer.net/api/validate?access_key=' + access_key + '&number=' + phone_number + '&country_code=IN',
        dataType: 'jsonp',
        success: function(json) {
        response = json.valid
        // Access and use your preferred validation result objects
        console.log(json.valid);
         console.log(response);

    }
});



console.log(response);
this.$el.html(QWeb.render('ValidateMobileNumber', {
     embedCode :this.value
    }));
if(response == true){
    this.$el.attr({ 'style': 'color:red'});
}
else{
 this.$el.attr({'style': 'color:green'});

}




        },



});
field_registry.add('verified-mobile-number', ValidateMobileNumber)
});
