/*
Script: piaportforward.js
    The client-side javascript code for the PIAPortForward plugin.

Copyright:
    (C) None 2009 <nospam@spam.org>
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3, or (at your option)
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, write to:
        The Free Software Foundation, Inc.,
        51 Franklin Street, Fifth Floor
        Boston, MA  02110-1301, USA.

    In addition, as a special exception, the copyright holders give
    permission to link the code of portions of this program with the OpenSSL
    library.
    You must obey the GNU General Public License in all respects for all of
    the code used other than OpenSSL. If you modify file(s) with this
    exception, you may extend this exception to your version of the file(s),
    but you are not obligated to do so. If you do not wish to do so, delete
    this exception statement from your version. If you delete this exception
    statement from all source files in the program, then also delete it here.
*/

Ext.ns('Deluge.ux.preferences');

/**
 * @class Deluge.ux.preferences.PIAPortForwardPage
 * @extends Ext.Panel
 */
Deluge.ux.preferences.PIAPortForwardPage = Ext.extend(Ext.Panel, {

    title: _('PIAPortForward'),
    layout: 'fit',
    border: false,

    initComponent: function () {
        Deluge.ux.preferences.PIAPortForwardPage.superclass.initComponent.call(this);

        this.form = this.add({
            xtype: 'form',
            layout: 'form',
            border: false,
            autoHeight: true
        });

        fieldset = this.form.add({
            xtype: 'fieldset',
            border: false,
            title: '',
            autoHeight: true,
            labelAlign: 'top',
            labelWidth: 80,
            defaultType: 'textfield'
        });

        this.username = fieldset.add({
            fieldLabel: _('Username:'),
            labelSeparator: '',
            name: 'username',
            width: '97%'
        });

        this.password = fieldset.add({
            fieldLabel: _('Password:'),
            labelSeparator: '',
            name: 'password',
            width: '97%'
        });

        this.on('show', this.updateConfig, this);
    },

    onApply: function () {
        // build settings object
        var config = {}

        config['pia_username'] = this.username.getValue();
        config['pia_password'] = this.password.getValue();

        deluge.client.piaportforward.set_config(config);
    },

    onOk: function () {
        this.onApply();
    },

    updateConfig: function () {
        deluge.client.piaportforward.get_config({
            success: function (config) {
                this.username.setValue(config['pia_username']);
                this.password.setValue(config['pia_password']);
            },
            scope: this
        });
    }
});


Deluge.plugins.PIAPortForwardPlugin = Ext.extend(Deluge.Plugin, {

    name: 'PIAPortForward',

    onDisable: function () {
        deluge.preferences.removePage(this.prefsPage);
    },

    onEnable: function () {
        this.prefsPage = deluge.preferences.addPage(new Deluge.ux.preferences.PIAPortForwardPage());
    }
});
Deluge.registerPlugin('PIAPortForward', Deluge.plugins.PIAPortForwardPlugin);
