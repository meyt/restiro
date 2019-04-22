
"""
@apiDefine ProductGetParams

@apiSuccess title
@apiQueryParam model
@apiQueryParam purchasable
@apiQueryParam manufacturedAt
"""


class Product:

    def get(self):
        """
        @api {get} /product Get all products
        @apiVersion 1.0.0
        @apiGroup Product

        @apiPermission god
        @apiPermission operator

        @apiQueryParam [sort]
        
        @apiUse ProductGetParams Some product params
        """
        """
        @api {get} /product/:productId Get a seller
        @apiVersion 1.0.0
        @apiGroup Product

        @apiUrlParam {Integer} productId
        """
        return self

    def put(self):
        """
        @api {put} /product/:productId Update a product
        @apiVersion 1.0.0
        @apiGroup Product

        @apiUrlParam {Integer} productId
        
        @apiParam {String} title (Product title)
        @apiParam {String} model Product Model 
        @apiParam {Boolean} purchasable Can purchase this product
        @apiParam {DateTime} manufacturedAt When product manufactured
        """
        return self

    def delete(self):
        """
        @api {delete} /product/:productId Delete a product
        @apiVersion 1.0.0
        @apiGroup Product

        @apiUrlParam productId Product ID
        
        @apiHeadParam Authorization Access Token
        
        @apiDescription
        Delete a product with product ID, but actually its
                        marked as deleted.
                         
                        After review the product can delete permanently.
                        
                        List of products cannot delete:
                        - Products purchased on time
                        - Products related to a `seller`
        """
        return self
