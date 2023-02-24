from _pydecimal import Decimal

from rest_framework import viewsets, response
from rest_framework.permissions import IsAuthenticated
from .serializers import CartSerializer

from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from .models import CartItemShop, Cart, Product, WishItemShop


def save_product_in_cart(request, product_id):
    cart = fill_card_in_session(request)
    if request.user.is_authenticated:
        cart_items = CartItemShop.objects.filter(cart__user = request.user,
                                                 product__id = product_id)
        if cart_items:
            cart_item = cart_items[0]
            cart_item.quantity += 1
        else:
            product = get_object_or_404(Product, id = product_id)
            cart_user = get_object_or_404(Cart, user = request.user)
            cart_item = CartItemShop(cart = cart_user, product = product)
        cart_item.save()

    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart


def save_product_in_wish(request, product_id):
    wish = fill_wish_card_in_session(request)
    if request.user.is_authenticated:
        wish_items = WishItemShop.objects.filter(wish__user = request.user,
                                                 wish_product__id = product_id)
        if wish_items:
            wish_item = wish_items[0]
            wish_item.wish_quantity += 1
        else:
            product = get_object_or_404(Product, id = product_id)
            wish_user = get_object_or_404(Cart, user = request.user)
            wish_item = WishItemShop(wish = wish_user, wish_product = product)
        wish_item.save()

    wish[str(product_id)] = wish.get(str(product_id), 0) + 1
    request.session['wish'] = wish


def fill_card_in_session(request):
    cart = request.session.get('cart', {})
    if request.user.is_authenticated and not cart:
        cart_items = CartItemShop.objects.filter(cart__user = request.user)
        for item in cart_items:
            cart[item.product.id] = item.quantity
        request.session['cart'] = cart
    return cart


def fill_wish_card_in_session(request):
    wish = request.session.get('wishlist', {})
    if request.user.is_authenticated and not wish:
        wish_items = WishItemShop.objects.filter(wish__user = request.user)
        for item in wish_items:
            wish[str(item.wish_product.id)] = item.wish_quantity
        request.session['wishlist'] = wish
    return wish


def fill_id_card_in_session(request):
    id_cart = request.session.get('id_cart', None)
    if request.user.is_authenticated and not id_cart:
        id_cart = Cart.objects.get(user = request.user).id
        request.session['id_cart'] = id_cart
    return id_cart


class CartView(View):

    def get(self, request):
        cart = fill_card_in_session(request)
        if cart:
            products = Product.objects.filter(id__in = cart.keys())
            data = [{"product": product, "quantity": cart[str(product.id)], 'id': product.id} for product in products]
            print(data)
        else:
            data = []
        total_price_no_discount = sum(item['product'].price * int(item['quantity'])
                                      for item in data)
        if not total_price_no_discount:
            total_price_no_discount = 0
        total_discount = sum(item['product'].price * item['product'].discount * item['quantity']
                             for item in data if item['product'].discount is not None) / 100
        if not total_discount:
            total_discount = 0
        total_sum = total_price_no_discount - total_discount
        context = {'cart_items': data,
                   'total_price_no_discount': total_price_no_discount,
                   'total_discount': total_discount,
                   'total_sum': total_sum,
                   }
        return render(request, 'cart_shop/cart.html', context)


class WishlistView(View):
    def get(self, request):
        if request.user.is_authenticated:
            wish = fill_wish_card_in_session(request)
            if wish:
                products = Product.objects.filter(id__in = wish.keys())
                #print(products[0].id)
                data = [{"product": product, "quantity": wish[str(product.id)], 'id': product.id} for product in products]
                print(data)
            else:
                data = []
            total_price_no_discount = sum(item['product'].price * item['quantity']
                                          for item in data)
            if not total_price_no_discount:
                total_price_no_discount = 0
            total_discount = sum(item['product'].price * item['product'].discount * item['quantity']
                                 for item in data if item['product'].discount is not None) / 100
            print(total_discount)
            if not total_discount:
                total_discount = 0
            total_sum = total_price_no_discount - total_discount
            print(total_sum)
            context = {'wish_items': data,
                       'total_price_no_discount': total_price_no_discount,
                       'total_discount': total_discount,
                       'total_sum': total_sum,
                       }
            return render(request, 'cart_shop/wishlist.html', context)
        else:
            return redirect('auth_shop:auth_shop')


class ViewCartBuy(View):
    def get(self, request, product_id):
        save_product_in_cart(request, product_id)
        return redirect('cart_shop:cart')


class ViewCartAdd(View):
    def get(self, request, product_id):
        save_product_in_cart(request, product_id)
        return redirect('home:index')


class ViewCartDel(View):
    def get(self, request, item_id):
        cart = fill_card_in_session(request)
        cart_id = fill_id_card_in_session(request)
        if request.user.is_authenticated:
            cart_item = get_object_or_404(CartItemShop, cart__id = cart_id, product__id = item_id)
            cart_item.delete()
        cart.pop(str(item_id))
        request.session["cart"] = cart
        return redirect('cart_shop:cart')


class ViewWishAdd(View):
    def get(self, request, product_id):
        if request.user.is_authenticated:
            save_product_in_wish(request, product_id)
            return redirect('home:index')
        else:
            return redirect('auth_shop:auth_shop')


class ViewWishDel(View):
    def get(self, request, item_id):
        if request.user.is_authenticated:
            wish = fill_wish_card_in_session(request)
            cart_id = fill_id_card_in_session(request)
            wish_item = get_object_or_404(WishItemShop, wish__id = cart_id, wish_product__id = item_id)
            wish_item.delete()
            wish.pop(str(item_id))
            request.session["wish"] = wish
            return redirect('cart_shop:wishlist')
        else:
            return redirect('auth_shop:auth_shop')


class CartViewSet(viewsets.ModelViewSet):
    queryset = CartItemShop.objects.all()
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(cart__user = self.request.user)

    def create(self, request, *args, **kwargs):
        cart_items = CartItemShop.objects.filter(cart__user = request.user,
                                                 product__id = request.data.get('product'))
        if cart_items:
            cart_item = cart_items[0]
            if request.data.get('quantity'):
                cart_item.quantity += request.data.get('quantity')
            else:
                cart_item.quantity += 1
        else:
            product = get_object_or_404(Product, id = request.data.get('product'))
            cart_user = get_object_or_404(Cart, user = request.user)

            if request.data.get('quantity'):
                cart_item = CartItemShop(cart = cart_user, product = product, quantity = request.data.get('quantity'))
            else:
                cart_item = CartItemShop(cart = cart_user, product = product)
        cart_item.save()
        return response.Response({'message': 'Product added to cart'}, status=201)

    def update(self, request, *args, **kwargs):
        cart_item = get_object_or_404(CartItemShop, id = kwargs['pk'])
        if request.data.get('quantity'):
            cart_item.quantity = request.data['quantity']
        if request.data.get('product'):
            product = get_object_or_404(Product, id = request.data['product'])
            cart_item.product = product
        cart_item.save()
        return response.Response({'message': 'Product change to cart'}, status = 201)

    def destroy(self, request, *args, **kwargs):
        cart_item = get_object_or_404(CartItemShop, id = kwargs['pk'])
        cart_item.delete()
        return response.Response({'message': 'Product delete from cart'}, status = 201)