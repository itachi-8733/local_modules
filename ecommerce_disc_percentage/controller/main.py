from odoo.http import request, route

from odoo.addons.website_sale.controllers.variant import WebsiteSaleVariantController
from odoo.addons.website_sale.controllers.product_configurator import WebsiteSaleProductConfiguratorController

#update the price for Popup in website for single product template with attribute
class SaleProductConfiguratorControllerInherit(WebsiteSaleProductConfiguratorController):
    def website_sale_product_configurator_get_values(self, *args, **kwargs):
        res = super().website_sale_product_configurator_get_values(*args, **kwargs)
        for product in res.get('products'):
            product_template = request.env['product.template'].browse(
                product['product_tmpl_id'] and int(product['product_tmpl_id']))

            if product.get('price') != product_template.discount_amount:
                price_extra = 0.0

                for line in product.get('attribute_lines', []):
                    for value in line.get('attribute_values', []):
                        if value.get('id') in line.get('selected_attribute_value_ids', []):
                            price_extra += value.get('price_extra', 0.0)

                product['price'] = product_template.discount_amount + price_extra

                res.update({
                    'custom_discount': product_template.discount_percentage if product_template else 0.0,
                    'custom_price': product.get('price', 0.0),
                    'product_price': product.get('price', 0.0),
                })
        return  res

# update the price on website for single product template 
class WebsiteSaleStockVariantControllerInherit(WebsiteSaleVariantController):

    @route()
    def get_combination_info_website(self, *args, **kwargs):
        res = super().get_combination_info_website(*args, **kwargs)
        product_template = request.env['product.template'].browse(
            res['product_template_id'] and int(res['product_template_id']))

        if res.get('list_price') != product_template.discount_amount:

            res['list_price'] = product_template.discount_amount
            if res.get('price_extra'):
                res['price'] = product_template.discount_amount + res['price_extra']
            else:
                res['price'] = product_template.discount_amount

        res.update({
            'custom_discount': product_template.discount_percentage,
            'custom_price': res['price'],
            'product_price': res['price'],
        })
        return res