define(function(require, exports, module){

	var znode = require('znode')
	var ZH = znode.ZH, goog = znode.goog;

	var N = function(opt_meta, opt_options, opt_domHelper) {
		goog.base(this, opt_meta, opt_options, opt_domHelper)
	}

	N.typeString = 'answer_edit_form'

	goog.inherits(N, ZH.ui.LiveComponent)

	N.prototype.typeString_ = N.typeString

	N.prototype.decorateInternal = function(element) {
		goog.base(this, 'decorateInternal', element)

		this.btnSubmitAnswer_ = this.getElementByClass('action-anchor')
		this.getHandler().listen(this.getElementByClass('answer-post-form'), 'submit', this.onSubmit_)
	}

	N.prototype.onSubmit_ = function(e) {
		var f = e.target // the form
		var formValues = goog.dom.forms.getFormDataMap(e.target)

		var actionEvent = this.createActionEventFromElement(this.btnSubmitAnswer_)
		actionEvent.getRequest().setPostData(formValues)

		// The form self don't need to be update.
		actionEvent.preventLiveMutate()

		this.dispathActionEvent(this.createActionEventFromElement(this.btnSubmitAnswer_))
		//return false to prevent default form action.
		return false
	}

	module.exports = N;

	ZH.core.Registry.getInstance().registType(N.typeString, module.exports)

})