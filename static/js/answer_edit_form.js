define(function(require, exports, module){

	var znode = require('znode')
	var ZH = znode.ZH, goog = znode.goog;

	var EditForm = function(opt_meta, opt_options, opt_domHelper) {
		goog.base(this, opt_meta, opt_options, opt_domHelper)
	}

	goog.inherits(EditForm, ZH.ui.LiveComponent)

	EditForm.prototype.decorateInternal = function(element) {
		goog.base(this, 'decorateInternal', element)

	}

	module.exports = node;

	ZH.core.Registry.getInstance().registType('answer_edit_form', module.exports)

})