odoo.define("pos_gift_card.GiftCardPopup", function (require) {
  "use strict";

  const { useState, useRef, onPatched, useComponent} = owl.hooks;
  const AbstractAwaitablePopup = require("point_of_sale.AbstractAwaitablePopup");
  const Registries = require("point_of_sale.Registries");

  class GiftCardPopup extends AbstractAwaitablePopup {
    constructor() {
      super(...arguments);
      this.state = useState({
        giftCardConfig: this.env.pos.config.gift_card_settings,
        showBarcodeGeneration: false,
        showNewGiftCardMenu: false,
        showUseGiftCardMenu: false,
        showGiftCardDetails: false,
        amountToSet: 0,
        giftCardBarcode: "",
      });
      this.useAutoFocus(this.state);
    }

    useAutoFocus(state) {
      const component = useComponent();
      let hasFocused = false;
      function autofocus() {
          if (state.showBarcodeGeneration) {
              // Should autofocus here but only if it hasn't autofocus yet.
              if (!hasFocused) {
                  const elem = component.el.querySelector(`.giftCardPopupInput`);
                  if (elem) {
                      elem.focus();
                      hasFocused = true;
                  }
              }
          } else {
              // When changing showBarcodeGeneration to false, we reset hasFocused.
              hasFocused = false;
          }
      }
      onPatched(autofocus);
  }

    switchBarcodeView() {
      this.state.showBarcodeGeneration = !this.state.showBarcodeGeneration;
      if (this.state.showUseGiftCardMenu)
        this.state.showUseGiftCardMenu = false;
      if (this.state.showGiftCardDetails)
        this.state.showGiftCardDetails = false;
    }

    switchToUseGiftCardMenu() {
      this.switchBarcodeView();
      this.state.showUseGiftCardMenu = true;
    }

    switchToShowGiftCardDetails() {
      this.switchBarcodeView();
      this.state.showGiftCardDetails = true;
    }

    async addGiftCardProduct(giftCard) {
      let gift =
        this.env.pos.db.product_by_id[
          this.env.pos.config.gift_card_product_id[0]
        ];

      let can_be_sold = true;
      if (giftCard) {
        can_be_sold = !(giftCard.buy_pos_order_line_id || giftCard.buy_line_id);
      }

      if (can_be_sold) {
        await this.env.pos.get_order().add_product(gift, {
          price: this.state.amountToSet,
          quantity: 1,
          merge: false,
          generated_gift_card_ids: giftCard ? giftCard.id : false,
          extras: { price_automatically_set: true },
        });
      } else {
        await this.showPopup('ErrorPopup', {
          'title': this.env._t('This gift card has already been sold'),
          'body': this.env._t('You cannot sell a gift card that has already been sold'),
        });
      }
    }

    async getGiftCard() {
      if (this.state.giftCardBarcode == "") return;

      let giftCard = await this.rpc({
          model: "gift.card",
          method: "search_read",
          args: [[["code", "=", this.state.giftCardBarcode]]],
        });
        if (giftCard.length) {
          giftCard = giftCard[0];
        } else {
          return false;
        }

      return giftCard;
    }

    async scanAndUseGiftCard() {
      let giftCard = await this.getGiftCard();
      if (!giftCard) return;

      if (this.state.giftCardConfig === "scan_use")
        this.state.amountToSet = giftCard.initial_amount;

      await this.addGiftCardProduct(giftCard);
      this.cancel();
    }

    async generateBarcode() {
      await this.addGiftCardProduct(false);
      this.confirm();
    }

    async isGiftCardAlreadyUsed() {
      let order = this.env.pos.get_order();
      let giftProduct =
        this.env.pos.db.product_by_id[
          this.env.pos.config.gift_card_product_id[0]
        ];

      const gitfCard = await this.getGiftCard();
      return order.get_orderlines().filter(
          line => line.get_product().id === giftProduct.id
          && line.price < 0
          && line.gift_card_id === (gitfCard).id
      );
    }

    getPriceToRemove(giftCard) {
      let currentOrder = this.env.pos.get_order();
      return currentOrder.get_total_with_tax() > giftCard.balance
        ? -giftCard.balance
        : -currentOrder.get_total_with_tax();
    }

    async payWithGiftCard() {
      let giftCard = await this.getGiftCard();
      if (!giftCard) return;

      let gift =
        this.env.pos.db.product_by_id[
          this.env.pos.config.gift_card_product_id[0]
        ];

      let currentOrder = this.env.pos.get_order();
      let lineUsed = await this.isGiftCardAlreadyUsed()
      if (lineUsed)
        lineUsed.forEach(line => currentOrder.remove_orderline(line));

      /**
       * Obtain the total amount to pay that can be covered by a gift card (if
       * the balance of the gift card allows to cover the total of the order
       * will be the total of the order, otherwise will be the balance of the
       * gift card) and the total of the order that includes all lines.
       * */
      let total_amount_to_pay = this.getPriceToRemove(giftCard);
      let current_order_total = currentOrder.get_total_with_tax();
      if (!current_order_total) return;

      // Add one gift card payment line per tax group
      let linesByTax = currentOrder.get_orderlines_grouped_by_tax_ids();
      for (let [tax_ids_key, lines] of Object.entries(linesByTax)) {
        // NOTE: `tax_ids` is an Array of tax ids that apply to the `lines`.
        // That is, the use case of products with more than one tax is supported.
        let tax_ids = tax_ids_key.split(",").filter(id => id !== "").map(id => Number(id));

        // We need to obtain which is the percentage that the lines cover of the
        // total of the order to cover the same percentage of the payment
        let baseToPay = currentOrder.calculate_base_amount(tax_ids, lines);
        let basePercentage = baseToPay * 100 / current_order_total;

        // We add the price as manually set to avoid recomputation when changing customer.
        let payment_amount = basePercentage * total_amount_to_pay / 100;
        if (payment_amount < 0) {
          let tax_description = (
            tax_ids.length ?
            _.str.sprintf(
                this.env._t("Tax: %s"),
                tax_ids.map(
                    taxId => this.env.pos.taxes_by_id[taxId].name
                ).join(", "))
            : this.env._t("No tax")
          );
          await currentOrder.add_product(gift, {
            price: payment_amount,
            quantity: 1,
            tax_ids: tax_ids,
            merge: false,
            description: tax_description,
            gift_card_id: giftCard.id,
            extras: {
                price_automatically_set: true,
            },
          });
        }
      }

      this.cancel();
    }

    async ShowRemainingAmount() {
      let giftCard = await this.getGiftCard();
      if (!giftCard) return;

      this.state.amountToSet = giftCard.balance;
    }
  }
  GiftCardPopup.template = "GiftCardPopup";

  Registries.Component.add(GiftCardPopup);

  return GiftCardPopup;
});
