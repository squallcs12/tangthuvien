from lettuce_setup.function import *
from thankshop import models

@before.all
def clear_login_history():
    for row in models.UserDailyLoginHistory.objects.all():
        row.delete()
    for row in models.ThankPoint.objects.all():
        row.delete()
    for row in models.ThankPointHistory.objects.all():
        row.delete()
