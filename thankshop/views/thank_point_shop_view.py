'''
Created on Dec 8, 2013

@author: antipro
'''
from django.template.response import TemplateResponse
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext as _
import paypalrestsdk
from django.conf import settings

paypalrestsdk.configure({
    'mode': settings.PAYPAL_MODE,
    'client_id': settings.PAYPAL_CLIENT_ID,
    'client_secret': settings.PAYPAL_CLIENT_SECRET,
})

from thankshop import models
from django.contrib.auth.decorators import login_required

@login_required
def index(request, template="thankshop/thank_point_shop.html"):
    data = {}

    packages = models.Package.objects.all().order_by('price')
    data['packages'] = packages

    return TemplateResponse(request, template, data)

@login_required
def buy(request, package_id):
    package = models.Package.objects.get(pk=package_id)

    payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {"payment_method": "paypal" },
                "redirect_urls": {
                    "return_url": request.build_absolute_uri(reverse('thankshop_thank_point_paypal_return')),
                    "cancel_url": request.build_absolute_uri(reverse('thankshop_thank_point_paypal_cancel'))
                },
                "transactions": [ {
                    "amount": {
                        "total": str(package.price),
                        "currency": "USD"
                    },
                    "description": "creating a payment",
                    "item_list": {
                        "items":[
                            {
                                "quantity":"1",
                                "name":"Hat",
                                "price": str(package.price),
                                "sku":package.sku,
                                "currency":"USD"
                            }
                        ]
                    }
                }]
    })

    payment.create()

    request.session['paypal_id'] = payment.id

    return HttpResponseRedirect(payment.links[1].href)

@login_required
def paypal_return(request):
    payment = paypalrestsdk.Payment.find(request.session['paypal_id'])
    payment.execute({"payer_id": request.GET['PayerID']})

    if payment.state == 'approved':
        item_sku = payment.transactions[0].item_list['items'][0]['sku']
        package = models.Package.objects.get(sku=item_sku)
        thank_point = request.user.thank_point
        thank_point.increase_thank_points(package.points, item_sku)

        messages.success(request, _("%(number)d thank points was added to your account.") % {'number': package.points})
        del request.session['paypal_id']

        return HttpResponseRedirect(reverse('thankshop_thank_point_shop'))

@login_required
def paypal_cancel(request):
    del request.session['paypal_id']

    return HttpResponseRedirect(reverse('thankshop_thank_point_shop'))
