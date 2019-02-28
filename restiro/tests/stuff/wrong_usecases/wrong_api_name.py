

class Seller:

    def post(self):
        """
        @api {get}
        @apiVersion 1.0.0
        @apiGroup Seller

        @apiPermission
        @apiPermission

        @apiUrlParam {Integer} sellerId
        """
        return self

    def get(self):
        """
        @api {get} /seller Get sellers list
        @apiVersion 1.0.0
        @apiGroup Seller

        @apiQueryParam {String} [sort]
        """
        """
        @api {get} /seller/:sellerId Get a seller
        @apiVersion 1.0.0
        @apiGroup Seller

        @apiUrlParam {Integer} sellerId
        """
        return self
