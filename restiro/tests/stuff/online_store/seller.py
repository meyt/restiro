

class Seller:

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

    def post(self):
        """
        @api {get} /seller/:sellerId Get a seller
        @apiVersion 1.0.0
        @apiGroup Seller
        
        @apiPermission
        @apiPermission
        
        @apiUrlParam {Integer} sellerId
        """
        return self


class SellerV2:

    def delete(self):
        """
        @api {delete} /seller/:sellerId Delete a seller
        @apiVersion 2.0.0
        @apiGroup Seller

        @apiUrlParam {Integer} sellerId
        """
        return self
