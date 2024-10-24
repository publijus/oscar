from decimal import Decimal as D
from oscar.apps.shipping import methods
from django.utils.translation import gettext_lazy as _

class Standard(methods.FixedPrice):
    code = 'standard'
    name = _('Standartinis pristatymas')
    charge_excl_tax = D('5.00')
    charge_incl_tax = D('6.05')

class Express(methods.FixedPrice):
    code = 'express'
    name = _('Skubus pristatymas')
    charge_excl_tax = D('10.00')
    charge_incl_tax = D('12.10')