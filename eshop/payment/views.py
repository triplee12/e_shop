"""Payment views."""

import braintree
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from orders.models import Order
from .tasks import payment_completed

# instantiate the Braintree payment gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


def payment_process(request):
    """Payment process."""
    order_id = request.session.get("order_id")
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()

    if request.method == "POST":
        # retrieve the nonce
        nonce = request.POST.get("payment_method_nonce", None)
        # create and submit transaction
        result = gateway.transaction.sale(
            {
                'amount': f'{total_cost}',
                'payment_method_nonce': nonce,
                'options': {
                    'submit_for_settlement': True
                }
            }
        )
        if result.is_success:
            # mark the order as paid
            order.paid = True
            # store the unique transaction identifier
            order.braintree_id = result.transaction.id
            order.save()
            # launch asynchronous task
            payment_completed.delay(order.id)
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        # generate a new transaction token
        client_token = gateway.client_token.generate()
        return render(
            request,
            "payment/process.html",
            {
                'order': order,
                "client_token": client_token
            }
        )


def payment_done(request):
    """Payment done."""
    return render(request, 'payment/done.html')


def payment_canceled(request):
    """Payment canceled."""
    return render(request, 'payment/canceled.html')
