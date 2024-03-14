from django.http import JsonResponse
from django.template.loader import render_to_string
from carts.models import Cart
from carts.utils import get_user_carts
from goods.models import Products


def add_to_cart(request):
    user = request.user if request.user.is_authenticated else None
    session_key = request.session.session_key if not user else None
    product = Products.objects.get(id=request.POST.get("product_id"))

    cart, created = Cart.objects.get_or_create(
        session_key=session_key,
        user=user,
        product=product,
        defaults={'quantity': 1},
    )

    if not created:
        cart.quantity += 1
        cart.save()

    return render_user_cart(request, message='Товар добавлен в корзину')


def change_cart(request):
    cart = Cart.objects.get(id=request.POST.get("cart_id"))
    cart.quantity = request.POST.get("quantity")
    cart.save()

    return render_user_cart(request, message='Количество изменено', quantity=cart.quantity)


def remove_from_cart(request):
    cart = Cart.objects.get(id=request.POST.get("cart_id"))
    quantity = cart.quantity
    cart.delete()

    return render_user_cart(request, message='Товар удален', quantity_deleted=quantity)


def render_user_cart(request, message, **kwargs):
    user_cart = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": user_cart}, request=request, )

    response_data = {"message": message, "cart_items_html": cart_items_html}
    response_data.update(kwargs)

    return JsonResponse(response_data)