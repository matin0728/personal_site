define(function(require, exports, module){

	var znode = require('znode')
	var ZH = znode.ZH, goog = znode.goog;

	var N = function(opt_meta, opt_options, opt_domHelper) {
		goog.base(this, opt_meta, opt_options, opt_domHelper)
	}

	N.typeString = 'test_node_2'

	goog.inherits(N, ZH.ui.LiveComponent)

	N.prototype.typeString_ = N.typeString

	N.prototype.decorateInternal = function(element) {
		goog.base(this, 'decorateInternal', element)

		this.element_.innerHTML = '<h4>This is a TestNode2 instance@</h4>' + this.getId()
	}

	module.exports = N;

	ZH.core.Registry.getInstance().registType(N.typeString, module.exports)

})