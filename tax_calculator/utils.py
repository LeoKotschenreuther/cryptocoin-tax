class AssetSale(object):
    def __init__(self, property, aquired_at, sold_at, proceeds, basis):
        self.property = property
        self.aquired_at = aquired_at
        self.sold_at = sold_at
        self.proceeds = proceeds
        self.basis = basis
        self.gain_loss = proceeds - basis

    # is_loss returns whether the AssetSale is a loss
    def is_loss(self):
        return self.gain_loss < 0
