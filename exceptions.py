class ProductNotFoundException(Exception):
    def __init__(self, product_id: int):
        self.product_id = product_id