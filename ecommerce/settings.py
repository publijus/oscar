import os
from oscar.defaults import *
from pathlib import Path
from django.utils.translation import gettext_lazy as _
import dj_database_url


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'jūsų-slaptas-raktas-čia')

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'oscar.config.Shop',
    'oscar.apps.analytics.apps.AnalyticsConfig',
    'oscar.apps.checkout.apps.CheckoutConfig',
    'oscar.apps.address.apps.AddressConfig',
    'ecommerce.apps.shipping.apps.ShippingConfig',
    # 'oscar.apps.shipping.apps.ShippingConfig',
    'oscar.apps.catalogue.apps.CatalogueConfig',
    'oscar.apps.catalogue.reviews.apps.CatalogueReviewsConfig',
    'oscar.apps.communication.apps.CommunicationConfig',
    'oscar.apps.partner.apps.PartnerConfig',
    'oscar.apps.basket.apps.BasketConfig',
    'oscar.apps.payment.apps.PaymentConfig',
    'oscar.apps.offer.apps.OfferConfig',
    'oscar.apps.order.apps.OrderConfig',
    'oscar.apps.customer.apps.CustomerConfig',
    'oscar.apps.search.apps.SearchConfig',
    'oscar.apps.voucher.apps.VoucherConfig',
    'oscar.apps.wishlists.apps.WishlistsConfig',
    'oscar.apps.dashboard.apps.DashboardConfig',
    'oscar.apps.dashboard.reports.apps.ReportsDashboardConfig',
    'oscar.apps.dashboard.users.apps.UsersDashboardConfig',
    'oscar.apps.dashboard.orders.apps.OrdersDashboardConfig',
    'oscar.apps.dashboard.catalogue.apps.CatalogueDashboardConfig',
    'oscar.apps.dashboard.offers.apps.OffersDashboardConfig',
    'oscar.apps.dashboard.partners.apps.PartnersDashboardConfig',
    'oscar.apps.dashboard.pages.apps.PagesDashboardConfig',
    'oscar.apps.dashboard.ranges.apps.RangesDashboardConfig',
    'oscar.apps.dashboard.reviews.apps.ReviewsDashboardConfig',
    'oscar.apps.dashboard.vouchers.apps.VouchersDashboardConfig',
    'oscar.apps.dashboard.communications.apps.CommunicationsDashboardConfig',
    'oscar.apps.dashboard.shipping.apps.ShippingDashboardConfig',
    'widget_tweaks',
    'sorl.thumbnail',
    'django_tables2',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.locale.LocaleMiddleware',  # Added LocaleMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'oscar.apps.basket.middleware.BasketMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',

]

ROOT_URLCONF = 'ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'oscar.apps.search.context_processors.search_form',
                'oscar.apps.checkout.context_processors.checkout',
                'oscar.apps.communication.notifications.context_processors.notifications',
                'oscar.core.context_processors.metadata',
                # Pašalinkite šią eilutę:
                # 'django_tables2.context_processors.django_tables2',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce.wsgi.application'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        conn_max_age=600
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'lt'
TIME_ZONE = 'Europe/Vilnius'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    'oscar.apps.customer.auth_backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

OSCAR_INITIAL_ORDER_STATUS = 'Naujas'
OSCAR_INITIAL_LINE_STATUS = 'Naujas'
OSCAR_ORDER_STATUS_PIPELINE = {
    'Naujas': ('Apmokėtas', 'Atšauktas',),
    'Apmokėtas': ('Išsiųstas', 'Atšauktas',),
    'Išsiųstas': ('Pristatytas', 'Atšauktas',),
    'Pristatytas': (),
    'Atšauktas': (),
}

# Pridėkite/arba atnaujinkite šias eilutes
OSCAR_CURRENCY_FORMAT = {
    'EUR': {
        'currency_digits': True,
        'format': '€ #,##0.00',
    },
}

# Jei norite rodyti kainas su PVM
OSCAR_TRACK_STOCK_LEVELS = True
OSCAR_DEFAULT_CURRENCY = 'EUR'

# OSCAR_SHIPPING_METHODS = [
#     {
#         'name': _('Nemokamas pristatymas'),
#         'description': _('Nemokamas pristatymas užsakymams virš 50 EUR'),
#         'charge': 0,
#         'code': 'free-shipping',
#     },
#     {
#         'name': _('Standartinis pristatymas'),
#         'description': _('Pristatymas per 3-5 darbo dienas'),
#         'charge': 5.99,
#         'code': 'standard-shipping',
#     },
#     {
#         'name': _('Skubus pristatymas'),
#         'description': _('Pristatymas per 1-2 darbo dienas'),
#         'charge': 9.99,
#         'code': 'express-shipping',
#     }
# ]

# OSCAR_SHIPPING_METHOD_CHOICES = [
#     ('free-shipping', _('Nemokamas prist')),
#     ('standard-shipping', _('Standartinis pristatymas')),
#     ('express-shipping', _('Skubus pristatymas')),
# ]

# Pridėkite šį šalių sąrašą
OSCAR_SHOP_COUNTRIES = [
    ('LT', _('Lietuva')),
    ('LV', _('Latvija')),
    ('EE', _('Estija')),
    ('PL', _('Lenkija')),
    ('DE', _('Vokietija')),
    ('GB', _('Jungtinė Karalystė')),
    ('US', _('Jungtinės Amerikos Valstijos')),
]

# Nustatykite numatytąją šalį
OSCAR_DEFAULT_COUNTRY = 'LT'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # Added DEFAULT_AUTO_FIELD

# Pridėkite šias eilutes prie failo pabaigos

# Įsitikinkite, kad ši eilutė yra pašalinta arba užkomentuota
# OSCAR_ALLOW_ANON_CHECKOUT = True

# Pridėkite šį nustatymą
OSCAR_SHIPPING_ENABLED = True
OSCAR_SHIPPING_METHOD_ENABLED = True
OSCAR_SHIPPING_REPOSITORY = 'ecommerce.apps.shipping.repository.Repository'

# # Pridėkite šį nustatymą
# OSCAR_REQUIRED_ADDRESS_FIELDS = ('first_name', 'last_name', 'line1', 'line4', 'postcode', 'country')

OSCAR_SEND_REGISTRATION_EMAIL = False
OSCAR_SEND_REGISTRATION_EMAIL = False
OSCAR_SEND_ORDER_CONFIRMATION_EMAIL = False
OSCAR_SEND_ORDER_EMAIL_SUBJECT = ''

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
