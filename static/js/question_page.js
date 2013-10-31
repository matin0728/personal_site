define(function(require, exports, module){

	var znode = require('znode')
	var ZH = znode.ZH, goog = znode.goog;

	var N = function(opt_meta, opt_options, opt_domHelper) {
		goog.base(this, opt_meta, opt_options, opt_domHelper)
	}

	N.typeString = 'question_page'

	goog.inherits(N, ZH.ui.LiveComponent)

	N.prototype.typeString_ = N.typeString

	N.prototype.decorateInternal = function(element) {
		goog.base(this, 'decorateInternal', element)

		this.getHandler().listen(this, ZH.ui.LiveComponent.EventType.ACTION, this.onActionEvent_)
	}

	N.prototype.onActionEvent_ = function(e) {
		if (e.actionName === 'create-answer') {
			var answerList = this.findChildByName('normal_answers');
			e.getRequest().setPostParam('answer_list_wrap_id', answerList.getId())
		}
	}

	module.exports = N;

	ZH.core.Registry.getInstance().registType(N.typeString, module.exports)

})