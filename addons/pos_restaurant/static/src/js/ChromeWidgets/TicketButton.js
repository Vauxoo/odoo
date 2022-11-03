odoo.define('pos_restaurant.TicketButton', function (require) {
    'use strict';

    const TicketButton = require('point_of_sale.TicketButton');
    const Registries = require('point_of_sale.Registries');
    const { posbus } = require('point_of_sale.utils');

    const PosResTicketButton = (TicketButton) =>
        class extends TicketButton {
            async onClick() {
                if (this.env.pos.config.iface_floorplan && !this.props.isTicketScreenShown && !this.env.pos.table) {
                    await this._syncAllFromServer();
                    this.showScreen('TicketScreen');
                } else {
                    super.onClick();
                }
            }
            async _syncAllFromServer() {
                const pos = this.env.pos;
                try {
                    const orders_by_table = await this.rpc({
                        model: 'pos.config',
                        method: 'get_all_table_draft_orders',
                        args: [pos.config.id],
                        kwargs: {context: pos.session.user_context},
                    }, {
                        timeout: 7500,
                        shadow: false,
                    });
                    Object.entries(orders_by_table).forEach(([table_id, server_orders]) => {
                        const orders = pos.get_table_orders(pos.tables_by_id[table_id]);
                        pos._replace_orders(orders, server_orders);
                    });
                } catch (e) {
                    await this.showPopup('ErrorPopup', {
                        title: this.env._t('Connection Error'),
                        body: this.env._t('Due to a connection error, the orders are not synchronized.'),
                    });
                }
            }
            mounted() {
                posbus.on('table-set', this, this.render);
            }
            willUnmount() {
                posbus.off('table-set', this);
            }
            /**
             * If no table is set to pos, which means the current main screen
             * is floor screen, then the order count should be based on all the orders.
             */
            get count() {
                if (!this.env.pos || !this.env.pos.config) return 0;
                if (this.env.pos.config.iface_floorplan && !this.env.pos.table) {
                    return this.env.pos.get('orders').models.length;
                } else {
                    return super.count;
                }
            }
        };

    Registries.Component.extend(TicketButton, PosResTicketButton);

    return TicketButton;
});
