from lettuce_setup.function import *
from thankshop import models
from thankshop.features.factories import ItemFactory, ThankFactory

@before.all
def clear_login_history():
    clean_models = []
    clean_models.append(models.UserDailyLoginHistory)
    clean_models.append(models.ThankPoint)
    clean_models.append(models.ThankPointHistory)
    clean_models.append(models.Item)
    clean_models.append(models.Package)
    clean_models.append(models.UserItem)
    for model in clean_models:
        for row in model.objects.all():
            row.delete()

    for i in range(0, 4):
        ItemFactory().save()

    for i in range(0, 4):
        ThankFactory().save()
