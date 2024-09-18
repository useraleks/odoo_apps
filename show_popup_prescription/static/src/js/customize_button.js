/** @odoo-module **/

import ProductScreen from "point_of_sale.ProductScreen"
import Registries from "point_of_sale.Registries"
console.log("Owl examples")

const CustomProductScreen = (ProductScreen) => class extends ProductScreen{

    setup(){
        super.setup()
        
    }

    async _clickProduct(event){
        await super._clickProduct(...arguments)
        console.log("_clickProduct override ok", event.detail)
        const product_id = await this.rpc({
            model: 'product.product',
            method: 'search_read',
            args: [[['id', '=', event.detail.id],], ['id', 'display_name', 'need_prescription' , 'qty_available', 'virtual_available']],
            context: this.env.session.user_context,
        })
        if (product_id[0].need_prescription === true) {
            this.showPopup("ConfirmPopup",{
                title:"Advertencia de Producto",
                body:"Se necesita receta para el producto",
                confirmText:"Ok",
            });
        }

    }
}

Registries.Component.extend(ProductScreen, CustomProductScreen)