define(function(require, exports, module){

	var znode = require('znode')
	var ZH = znode.ZH, goog = znode.goog;

	var writeLog = function(msg) {
		if (window.console) {
			console.log(msg)
		}	
	}
	
	writeLog('TestNode loaded!!!');

	var N = function(opt_meta, opt_options, opt_domHelper) {
		goog.base(this, opt_meta, opt_options, opt_domHelper)
	}

	N.typeString = 'test_node'

	goog.inherits(N, ZH.ui.LiveComponent)

	N.prototype.typeString_ = N.typeString

	N.prototype.decorateInternal = function(element) {
		goog.base(this, 'decorateInternal', element)

		this.element_.innerHTML = '<h1>小毛主席万岁！！！</h1>'
	}

	module.exports = N;

	ZH.core.Registry.getInstance().registType(N.typeString, module.exports)

})