{
    'name': 'Ecommerce Discount',
    'version': '1.0',
    'sequence': 10,
    'description': """
    Ecommerce discount module
    """,
    'category': 'Extra Tools',
    'depends': ['stock', 'website_sale', 'stock_delivery'],
    'data': [
        'views/product_template.xml',
        'views/template.xml'
    ],
    'license': 'LGPL-3',
}
