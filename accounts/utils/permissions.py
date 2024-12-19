# from django.conf import settings
#
# logger = settings.LOGGING
import logging
logger = logging.getLogger("console_file")

def validate_user_permissions(request):
    if request.user.is_authenticated:
        return True
    else:
        return False
