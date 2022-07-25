
from django.shortcuts import render ,get_object_or_404

from django.http import JsonResponse
from . models import *
import json
import datetime
from . utils import cookieCart ,cartData ,guestOrder

# Create your views here.

def store(request): 
    data = cartData(request)
    cartItems = data['cartItems']
    

    products = Product.objects.all()
    context = { 'products' : products ,'cartItems' : cartItems}
    return render(request , 'store.html' , context) #src\templates\store.html

def detail_view(request,id):
    product = get_object_or_404(Product,id=id)
    photos = PostImage.objects.filter(product=product)
    

    data = cartData(request)
    cartItems = data['cartItems']
    #items = data['items']
    return render(request , 'store/detail.html' ,{
        'product' :product,
        'photos':photos,
        
        'cartItems' :cartItems
    })



def cart(request):

    data = cartData(request)
    order = data['order']
    cartItems = data['cartItems']
    items = data['items']
      
      
  
    context = {'items' : items , 'order' :order ,'cartItems' : cartItems ,'shipping' :False}
    return render(request , 'store/chart.html' , context)

def checkout(request):
    data = cartData(request)
    order = data['order']
    cartItems = data['cartItems']
    items = data['items']
  
    context = {'items' : items , 'order' :order ,'cartItems' : cartItems ,'shipping' :False}
    return render(request , 'store/checkout.html' , context)




def updateItem(request):
    data =json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action: ' ,action)
    print('Product:' ,productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order,created = Order.objects.get_or_create(customer=customer ,complete=False)

    orderItem , created = OrderItem.objects.get_or_create(order=order , product=product)
   

    if action == 'add':
        orderItem.quantity = (orderItem.quantity +1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity -1)

    orderItem.save()  

    if orderItem.quantity <=0:
        orderItem.delete() 
    return JsonResponse('item was added' ,safe=False)


def processOrder(request):
    print('Data: ' ,request.body)

    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer ,complete=False)
      

    else:

        customer , order = guestOrder(request , data)
       

        total = float(data['form']['total'])
        order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
            order.complete =True
    order.save()

    
    if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
    return JsonResponse('Payment Submitted..' ,safe=False)