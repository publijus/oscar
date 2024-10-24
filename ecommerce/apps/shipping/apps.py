from oscar.apps.shipping import apps as shipping_apps
from oscar.core.loading import is_model_registered

class ShippingConfig(shipping_apps.ShippingConfig):
    name = 'ecommerce.apps.shipping'

    def ready(self):
        super().ready()
        from oscar.apps.shipping.models import WeightBased, OrderAndItemCharges, WeightBand

        if not is_model_registered('shipping', 'WeightBased'):
            class WeightBased(WeightBased):
                pass

        if not is_model_registered('shipping', 'OrderAndItemCharges'):
            class OrderAndItemCharges(OrderAndItemCharges):
                pass

        if not is_model_registered('shipping', 'WeightBand'):
            class WeightBand(WeightBand):
                pass