define(function(require, exports, module){

	var znode = require('znode')
	var ZH = znode.ZH, goog = znode.goog;

	var writeLog = function(msg) {
		if (window.console) {
			console.log(msg)
		}	
	}
	
	writeLog('TestNode loaded!!!');

	var myTestNode = function(opt_meta, opt_options, opt_domHelper) {
		goog.base(this, opt_meta, opt_options, opt_domHelper)
	}

	goog.inherits(myTestNode, ZH.ui.LiveComponent)

	myTestNode.prototype.decorateInternal = function(element) {
		goog.base(this, 'decorateInternal', element)

		this.element_.innerHTML = '<h1>小毛主席万岁！！！</h1>'
	}

	module.exports = myTestNode;

	ZH.core.Registry.getInstance().registType('test_node', module.exports)

})