odoo.define('skit_pos_restaurant.pos_screen', function (require) {
"use strict";

var chrome = require('point_of_sale.chrome');
var gui = require('point_of_sale.gui');
var screens = require('point_of_sale.screens');
var PopupWidget = require('point_of_sale.popups');
var core = require('web.core');

var QWeb = core.qweb;
var _t = core._t;

chrome.OrderSelectorWidget.include({
	   
    hide: function(){
        this.$el.addClass('oe_invisible');
    },
    show: function(){
        this.$el.removeClass('oe_invisible');
    },
    
});
// Add the FloorScreen to the GUI, and set it as the default screen
chrome.Chrome.include({
    build_widgets: function(){
        this._super();
        if (this.pos.config.iface_floorplan && !this.pos.config.is_kitchen) {
            this.gui.set_startup_screen('floors');
        }
        else {
        	this.gui.set_startup_screen('products');
        }
    },
    
});
});