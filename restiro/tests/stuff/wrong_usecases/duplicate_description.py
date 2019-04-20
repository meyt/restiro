

class Seller:

    def post(self):
        """
        @api {post} /seller post sellers list
        @apiVersion 1.0.0
        @apiGroup Seller

        @apiPermission
        @apiPermission

        @apiDescription Add a seller
        @apiDescription SellerId is unique

        @apiUrlParam {Integer} sellerId
        """
        return self
