from datetime import datetime
from django.conf import settings

def default(req):
    return {
        'PRODUCT_NAME': settings.PRODUCT_NAME,
        'PRODUCT_DESCRIPTION': settings.PRODUCT_DESCRIPTION,
        'COMPANY': settings.COMPANY,
        'YEAR': datetime.today().year,
    }
