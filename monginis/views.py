from django.http import HttpResponse,HttpResponseRedirect # type: ignore
from django.shortcuts import redirect, render,get_object_or_404 # type: ignore
import qrcode # type: ignore
from django.contrib.auth.models import User
from django.core.mail import send_mail # type: ignore
from io import BytesIO
from django.db import transaction
from django.contrib import messages # type: ignore
from myapp.models import Brownie, Chocolate, Chocolate_bouquet, Muffin, Order, Packaged_cake, Pastry, Product, Registration
from myapp.models import Cake
from myapp.models import Donut
from django.contrib.auth.hashers import check_password # type: ignore
from django.http import JsonResponse # type: ignore
from django.core.exceptions import ObjectDoesNotExist # type: ignore
from django.contrib.auth.hashers import make_password # type: ignore
from django.contrib import messages # type: ignore
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
import json
from decimal import Decimal
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from myapp.models import Payment,OrderCart,OrderCartItem,Profile,Cart,Order, Packaged_cake, Cake, Donut, Pastry, Brownie, Chocolate, Muffin, Chocolate_bouquet,Category


def index(request):
    return render(request,"index.html")

def product(request):
    return render(request,"product.html")

def about(request):
    return render(request,"about.html")

def blog(request):
    return render(request,"blog.html")

def product(request):
   products = Product.objects.all() 
   return render(request, 'product.html', {'products': products}) 

def cake_list(request):
    cakes = Cake.objects.all() 
    return render(request, 'cake.html', {'cakes': cakes}) 

def pastry_list(request):
    pastries = Pastry.objects.all()  
    return render(request, 'pastry.html', {'pastries': pastries})  


def packaged_cake_list(request):
    packaged_cakes=Packaged_cake.objects.all()
    return render(request,"package.html",{'packaged_cakes':packaged_cakes})

def brownie_list(request):
    brownies = Brownie.objects.all() 
    return render(request,"brownie.html",{'brownies': brownies})

def chocolate_list(request):
    chocolates = Chocolate.objects.all() 
    return render(request,"choco.html",{'chocolates': chocolates})

def muffin_list(request):
    muffins = Muffin.objects.all() 
    return render(request,"muffins.html",{'muffins': muffins})

def donuts_list(request):
    donuts=Donut.objects.all()
    return render(request,"donuts.html", {'donuts': donuts})

def category_list(request):
    categories = Category.objects.all()
    return render(request, "product.html", {'categories': categories})

def chocolate_bouquet_list(request):
    chocolate_bouquet = Chocolate_bouquet.objects.all() 
    return render(request, "chocolate_bouquet.html", {'chocolate_bouquets': chocolate_bouquet})

def history(request):
    return render(request,"history.html")

def header(request):
    return render(request,"header.html")


def header1(request):
    return render(request,"header1.html")

def footer(request):
    return render(request,"footer.html")


def order(request):
    return render(request,"order.html")

@login_required
def cart(request):
    return render(request,"cart.html")

def registration(request):
    return render(request,"registration.html")

@login_required
def add_to_cart(request):
    if request.method == "POST":
        cake_id = request.POST.get('cake_id')
        cake = Cake.objects.get(id=cake_id)
        
       
        cart = request.session.get('cart', {})
        
        
        if cake_id in cart:
            cart[cake_id]['quantity'] += 1
        else:
            cart[cake_id] = {
                'name': cake.name,
                'price': cake.price,
                'quantity': 1,
                'image': cake.image.url,
            }
        

        request.session['cart'] = cart
        request.session.modified = True
        
        return JsonResponse({'message': 'Added to cart'})
    return JsonResponse({'message': 'Invalid request'}, status=400)

def generate_payment_qr(request):
    qr_data = "Your Payment Link or Details Here"
    qr = qrcode.make(qr_data)

    response = HttpResponse(content_type="image/png")
    qr.save(response, "PNG")
    return response

def payment(request):
    return render(request,"payment.html")

def order_successful(request):
    return render(request,"order_successful.html")

def visit(request):
    return render(request,"visit.html")

def success(request):
    if request.method == "POST":
        user_name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        mob_num = request.POST.get('mob_num')
        city = request.POST.get('city')

       
        if Registration.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('registration.html')

        if User.objects.filter(username=user_name).exists():
            messages.error(request, "Username is already taken.")
            return redirect('registration.html')

        # Create User instance & set password correctly
        user = User.objects.create(username=user_name, email=email)
        user.set_password(password)  
        user.save() 

        # Create Registration instance
        registration = Registration(
            user=user,
            email=email,
            gender=gender,
            mob_num=mob_num,
            city=city
        )
        registration.save()

        messages.success(request, "Registration successful! Please log in.")
        return redirect('login')

    return render(request, 'registration.html')


@login_required
def cart_view(request):
    if request.method == "GET":
        pname = request.GET.get("name")
        pprice = request.GET.get("price")

        if pname and pprice:
            try:
               
                cart_item = Cart(pname=pname, pprice=float(pprice))  
                cart_item.save()

                return JsonResponse({"message": "Item added to cart successfully!"})

            except Exception as e:
                return JsonResponse({"error": f"Database Error: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=40.0)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('login_user')  
        password = request.POST.get('login_pass')  

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  
            messages.success(request, f"Welcome, {user.username}!")

            
            profile, created = Profile.objects.get_or_create(user=user)

            return redirect("profile")  

        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')


def logout_view(request):
    request.session.flush()  
    messages.success(request, "You have been logged out.")
    return redirect('login')

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    ordercart_orders = OrderCart.objects.filter(user=request.user).order_by('-created_at')
    order_orders = Order.objects.filter(user=request.user).order_by('-created_at')


    all_orders = list(ordercart_orders) + list(order_orders) 

    return render(request, "profile.html", {"profile": profile, "orders": all_orders})


@login_required
def order_view(request):
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        prnm = request.POST.get('prnm', '').strip()
        prp = request.POST.get('prp', '0').strip()
        qty = request.POST.get('qty', '1').strip()
        no = request.POST.get('no', '').strip()
        pin = request.POST.get('pincode', '').strip()
        city = request.POST.get('city', '').strip()
        address = request.POST.get('address', '').strip()
        payment_method = request.POST.get('paymentMethod', '').strip()

        
        if not all([name, prnm, no, pin, city, address, payment_method]):
            messages.error(request, "All fields are required.")
            return redirect('order')

        try:
            prp = Decimal(prp)
            qty = int(qty)
            if prp <= 0 or qty <= 0:
                raise ValueError("Price and quantity must be greater than zero.")
            tp = prp * qty 
        except ValueError:
            messages.error(request, "Invalid price or quantity.")
            return redirect('order')

       
        order = Order.objects.create(
            user=request.user,
            name=name,
            pnm=prnm,
            prp=prp,
            qty=qty,
            tp=tp,
            no=no,
            pin=pin,
            city=city,
            address=address,
            order_status="pending"
        )

       
        Payment.objects.create(
            user=request.user,
            order=order,
            amount=tp,
            payment_method=payment_method
        )

        messages.success(request, "Order placed successfully!")

      
        if payment_method == "qr":
            return redirect(f'/payment/?tp={tp}')  
        else:
            return redirect('order_successful')  

    return render(request, 'order.html')

def download_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order_id}.pdf"'

   
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    p.setFillColorRGB(0.95, 0.95, 0.95)  
    p.rect(0, 0, width, height, fill=True, stroke=False)

  
    p.setFont("Helvetica-Bold", 22)
    p.setFillColor(colors.darkblue)
    p.drawCentredString(width / 2, height - 50, "Monginis Cake Shop")

 
    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(colors.black)
    p.drawString(50, height - 100, f"Invoice No: {order.id}")
    p.drawString(50, height - 120, f"Customer: {order.name}")
    p.drawString(50, height - 140, f"Address: {order.address}, {order.city}, {order.pin}")
    p.drawString(50, height - 160, f"Mobile: {order.no}")
   

    p.setStrokeColor(colors.black)
    p.line(50, height - 190, width - 50, height - 190)

    y_position = height - 220
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(colors.darkred)
    p.drawString(50, y_position, "Product Name")
    p.drawString(300, y_position, "Qty")
    p.drawString(400, y_position, "Price")
    p.drawString(500, y_position, "Total")

    p.setStrokeColor(colors.black)
    p.line(50, y_position - 10, width - 50, y_position - 10)

    y_position -= 30
    p.setFont("Helvetica", 12)
    p.setFillColor(colors.black)
    p.drawString(50, y_position, order.pnm)
    p.drawString(300, y_position, str(order.qty))
    p.drawString(400, y_position, f"₹ {order.prp}")
    p.drawString(500, y_position, f"₹ {order.tp}")

    y_position -= 40
    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(colors.darkblue)
    p.drawString(400, y_position, "Grand Total:")
    p.setFillColor(colors.black)
    p.drawString(500, y_position, f"₹ {order.tp}")

    p.showPage()
    p.save()

    return response

@csrf_exempt
@login_required  
def orderpage_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            customer_name = data.get("customer_name")
            address = data.get("address")
            pin = data.get("pin")
            city = data.get("city")
            mobile = data.get("mobile")
            paymentMethod = data.get("paymentMethod")
            totalAmount = data.get("totalAmount")
            items = data.get("items", [])

            if not all([customer_name, address, pin, city, mobile, paymentMethod, totalAmount]) or not items:
                return JsonResponse({"success": False, "message": "Missing required fields or empty cart!"}, status=400)

            with transaction.atomic():
                
                order = OrderCart.objects.create(
                    user=request.user, 
                    customer_name=customer_name,
                    address=address,
                    pin=pin,
                    city=city,
                    mobile=mobile,
                    paymentMethod=paymentMethod,
                    totalAmount=totalAmount,
                )

               
                order_items = [
                    OrderCartItem(
                        order=order,
                        item_name=item["name"],
                        item_price=item["price"],
                        quantity=item["quantity"],
                        item_image=item["image"]
                    )
                    for item in items
                ]
                OrderCartItem.objects.bulk_create(order_items)

            return JsonResponse({"success": True, "order_id": order.id, "message": "Order placed successfully!"})

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)

    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)

User = get_user_model()  

def forgot_password_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'forgot_password.html')

        try:
            user_registration = Registration.objects.get(user_name=username)
        except ObjectDoesNotExist:
            messages.error(request, "User not found.")
            return render(request, 'forgot_password.html')

        if user_registration.user:
            user_registration.user.set_password(new_password) 
            user_registration.user.save()

   
        user_registration.password = make_password(new_password)
        user_registration.save()

        messages.success(request, "Password successfully updated! Please log in.")
        return redirect('login')  

    return render(request, 'forgot_password.html')

chat_responses = {
    "hi": "Hello! Welcome to Monginis Cake Shop. How can I assist you?",
    "hello": "Hello! How can I help you today?",
    "hey": "Hey there! Need any assistance?",
    "menu": "We have chocolate, vanilla, red velvet, fruit cakes, and more! What would you like?",
    "order": "You can place an order on our website, visit our store, or contact us on WhatsApp.",
    "delivery": "We offer home delivery within the city. Charges depend on your location.",
    "location": "We are located at Rajkamal Chowk, Amreli. Find us on Google Maps!",
    "bye": "Goodbye! Have a sweet day! 🍰",
}

def get_product_price(user_message):
    """Search for the product in all models and return its price if found."""
    models = [Cake, Pastry, Donut, Packaged_cake, Brownie, Chocolate, Muffin, Chocolate_bouquet]
    
    matching_products = []

    for model in models:
        products = model.objects.filter(name__icontains=user_message) 
        for product in products:
            matching_products.append(f"{product.name}: ₹{product.price:.2f}")

    if matching_products:
        return "Here are the prices:\n" + "\n".join(matching_products)
    
    return None 

def chatbot_response(request):
    """Handles chatbot responses including predefined replies and dynamic price fetching."""
    user_message = request.GET.get("message", "").strip().lower()


    for key in chat_responses.keys():
        if key in user_message:
            return JsonResponse({"response": chat_responses[key]})

    response = get_product_price(user_message)
    if response:
        return JsonResponse({"response": response})

    return JsonResponse({"response": "I'm not sure about that. Ask me about cakes, orders, or store details!"})
