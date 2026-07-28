from django.shortcuts import render,redirect
from Backend.models import roomtypedb,roomnamedb,staffdb
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from webapp.models import bookingdb,customercontactdb,Totaldb
from django.contrib import messages
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@login_required(login_url='/Backend/login_page_admin/')
def index_page(request):
    return render(request,"0index.html")

#roomtypeDB with roomtype_page
@login_required(login_url='/Backend/login_page_admin/')
def roomtype_page(request):
    return render(request,"1roomtype.html")
@login_required(login_url='/Backend/login_page_admin/')
def save_roomtype_page(request):
    if request.method == "POST":
        rt=request.POST.get('roomtype')
        ds = request.POST.get('description')
        img=request.FILES.get('images')
        if not img:
            messages.error(request, "Image is required")
            return redirect(roomtype_page)
        obj=roomtypedb(ROOMTYPE=rt,DESCRIPTION=ds,ROOMTYPEIMAGE=img)
        obj.save()
        messages.success(request,"Roomtype saved succesfully")
        return redirect(roomtype_page)
@login_required(login_url='/Backend/login_page_admin/')
def display_roomtype_page(request):
    cat = roomtypedb.objects.all()
    return render(request,"2displayroomtype.html",{'cat':cat})

@login_required(login_url='/Backend/login_page_admin/')
def edit_roomtype_page(request,prop_id):
    cat = roomtypedb.objects.get(id=prop_id)
    return render(request,"3editroomtype.html",{'cat':cat})

@login_required(login_url='/Backend/login_page_admin/')
def update_roomtype_page(request,prop_id):
    if request.method == "POST":
        rt = request.POST.get('roomtype')
        ds = request.POST.get('description')
        try:
            img=request.FILES['images']
            fs=FileSystemStorage()
            file=fs.save(img.name,img)
        except MultiValueDictKeyError:
            file=roomtypedb.objects.get(id=prop_id).ROOMTYPEIMAGE
        roomtypedb.objects.filter(id=prop_id).update(ROOMTYPE=rt,DESCRIPTION=ds,ROOMTYPEIMAGE=file)
        messages.success(request, "Roomtype Edited succesfully")
        return redirect(display_roomtype_page)

@login_required(login_url='/Backend/login_page_admin/')
def delete_page(request,del_id):
    x=roomtypedb.objects.filter(id=del_id)
    x.delete()
    messages.success(request, "Data deleted succesfully")
    return redirect(display_roomtype_page)

# #------------Hotelsdb--roomoperations--------------
@login_required(login_url='/Backend/login_page_admin/')
def room_number_page(request):
    pro=roomtypedb.objects.all()
    return render(request,"4roomnumber.html",{'pro':pro})

@login_required(login_url='/Backend/login_page_admin/')
def save_room_number_page(request):
    if request.method == "POST":
        rt_id = request.POST.get('roomtype')  # This might be ID or name
        ds = request.POST.get('roomdescription')
        rp = request.POST.get('roomprice')
        rnn = request.POST.get('roomname')
        
        # Handle optional image file
        img = None
        try:
            img = request.FILES.get('roomimage')
        except (KeyError, MultiValueDictKeyError):
            pass
        
        if not img:
            messages.error(request, "Room image is required")
            return redirect(room_number_page)
        
        # Try to get room type - handle both ID and name for backward compatibility
        room_type = None
        try:
            # Try as ID first
            room_type = roomtypedb.objects.get(id=int(rt_id))
        except (ValueError, roomtypedb.DoesNotExist):
            try:
                # Fallback: try as name
                room_type = roomtypedb.objects.get(ROOMTYPE__iexact=rt_id)
            except roomtypedb.DoesNotExist:
                messages.error(request, "Invalid room type selected")
                return redirect(room_number_page)
        
        obj = roomnamedb(ROOMTYPE=room_type, ROOMDESCRIPTION=ds, ROOMIMAGE=img, ROOMPRICE=rp, ROOMNAME=rnn)
        obj.save()
        messages.success(request, "Room saved succesfully")
        return redirect(room_number_page)
@login_required(login_url='/Backend/login_page_admin/')
def display_room_number_page(request):
    pro = roomnamedb.objects.all()
    return render(request,"5displayroomnumber.html",{'pro':pro})

@login_required(login_url='/Backend/login_page_admin/')
def edit_room_number_page(request,Edit_id):
    pro=roomnamedb.objects.get(id=Edit_id)
    cat=roomtypedb.objects.all()

    return render(request,"6edit_roomnumber.html",{'pro':pro,'cat':cat})

@login_required(login_url='/Backend/login_page_admin/')
def update_room_number_page(request,prop_id):
    if request.method == "POST":
        rt_id = request.POST.get('roomtype')  # This might be ID or name
        ds = request.POST.get('roomdescription')
        rp = request.POST.get('roomprice')
        rnn = request.POST.get('roomname')

        try:
            img = request.FILES['roomimage']
            fs=FileSystemStorage()
            file=fs.save(img.name,img)
        except MultiValueDictKeyError:
            file=roomnamedb.objects.get(id=prop_id).ROOMIMAGE
        
        # Try to get room type - handle both ID and name for backward compatibility
        room_type = None
        try:
            # Try as ID first
            room_type = roomtypedb.objects.get(id=int(rt_id))
        except (ValueError, roomtypedb.DoesNotExist):
            try:
                # Fallback: try as name
                room_type = roomtypedb.objects.get(ROOMTYPE__iexact=rt_id)
            except roomtypedb.DoesNotExist:
                messages.error(request, "Invalid room type selected")
                return redirect(display_room_number_page)
        
        roomnamedb.objects.filter(id=prop_id).update(ROOMTYPE_id=room_type.id, ROOMDESCRIPTION=ds, ROOMIMAGE=file, ROOMPRICE=rp, ROOMNAME=rnn)
        messages.success(request, "Rooms Details updated")
        return redirect(display_room_number_page)

@login_required(login_url='/Backend/login_page_admin/')
def delete_room_number_page(request,del_id):
    x=roomnamedb.objects.filter(id=del_id)
    x.delete()
    messages.success(request, "Data deleted succesfully")
    return redirect(display_room_number_page)


def login_page_admin(request):
    return render(request,"7login.html")

def admin_login(request):
    if request.method=="POST":
        un=request.POST.get('username')
        pwd = request.POST.get('pass')
        if User.objects.filter(username=un).exists():
            x=authenticate(username=un,password=pwd)
            if x is not None:
                login(request,x)
                request.session['username']=un
                messages.success(request, "Login successful")
                return redirect(index_page)
            else:
                messages.warning(request, "Login failed - Invalid password")
                return redirect(login_page_admin)
        else:
            messages.warning(request, "Login failed - Username not found")
            return redirect(login_page_admin)


def admin_logout(request):
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, "Logout sucessfully")
    return redirect(login_page_admin)

#Displaying Webapp(customersendingcontactmessage) in to Backend (8customercontacthtml page)
#connecting Webapp(db) and Backend

@login_required(login_url='/Backend/login_page_admin/')
def contact_details_page(request):
    data=customercontactdb.objects.all()
    return render(request,"8customercontact.html",{'data':data})

@login_required(login_url='/Backend/login_page_admin/')
def delete_customer_contact_details_page(request,del_id):
    x=customercontactdb.objects.filter(id=del_id)
    x.delete()
    return redirect(contact_details_page)
#adding staff details for customers
@login_required(login_url='/Backend/login_page_admin/')
def staff_details_page(request):
    return render(request,"9staffdetails.html")

@login_required(login_url='/Backend/login_page_admin/')
def save_staff_page(request):
    if request.method == "POST":
        sn=request.POST.get('sname')
        sd = request.POST.get('sdesignation')
        sf = request.POST.get('sfacebook')
        sin=request.POST.get('sinstagram')
        img=request.FILES['simage']
        obj=staffdb(STAFFNAME=sn,STAFFDESIGNATION=sd,STAFFACEBOOK=sf,STAFFINSTA=sin,STAFFIMAGE=img)
        obj.save()
        messages.success(request, "Staffs saved successfully")
        return redirect(staff_details_page)
@login_required(login_url='/Backend/login_page_admin/')
def display_staff_page(request):
    staff = staffdb.objects.all()
    return render(request,"10displaystaff.html",{'staff':staff})

@login_required(login_url='/Backend/login_page_admin/')
def edit_STAFF_page(request,Edit_id):
    pro=staffdb.objects.get(id=Edit_id)

    return render(request,"11editstaff.html",{'pro':pro})

@login_required(login_url='/Backend/login_page_admin/')
def update_staff_page(request,prop_id):
    if request.method == "POST":
        sn = request.POST.get('sname')
        sd = request.POST.get('sdesignation')
        sf = request.POST.get('sfacebook')
        sin = request.POST.get('sinstagram')

        try:
            img = request.FILES['simage']
            fs=FileSystemStorage()
            file=fs.save(img.name,img)
        except MultiValueDictKeyError:
            file=staffdb.objects.get(id=prop_id).STAFFIMAGE
        staffdb.objects.filter(id=prop_id).update(STAFFNAME=sn,STAFFDESIGNATION=sd,STAFFACEBOOK=sf,STAFFINSTA=sin,STAFFIMAGE=file)
        messages.success(request, "Staffs Details updated")
        return redirect(display_staff_page)

@login_required(login_url='/Backend/login_page_admin/')
def delete_staff_page(request,del_id):
    x=staffdb.objects.filter(id=del_id)
    x.delete()
    messages.success(request, "Staffs details deleted successfully")
    return redirect(display_staff_page)

#full details of customers booked
@login_required(login_url='/Backend/login_page_admin/')
def detailsbooked_page(request):
    data=bookingdb.objects.all()
    return render(request,"12detailsbooked.html",{"data":data})
@login_required(login_url='/Backend/login_page_admin/')
def deletebooked_details(request,del_id):
    x=bookingdb.objects.filter(id=del_id)
    x.delete()
    return redirect(detailsbooked_page)

#total amount of moneypayed by customer (displaypage)

@login_required(login_url='/Backend/login_page_admin/')
def customertotalamount_page(request):
    data=Totaldb.objects.all()
    return render(request,"13fewdetails.html",{'data':data})
@login_required(login_url='/Backend/login_page_admin/')
def deletecustomertotalamount_page(request,del_id):
    x=Totaldb.objects.filter(id=del_id)
    x.delete()
    return redirect(customertotalamount_page)


# ── Auth Token API for Backend Registration and Login ──

@csrf_exempt
def admin_register(request):
    """Register a new admin user and return an auth token."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.POST
        username = data.get('username')
        email = data.get('email', '')
        password = data.get('password')
        if not username or not password:
            return JsonResponse({'error': 'Username and password required'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        user = User.objects.create_user(username=username, email=email, password=password)
        token, _ = Token.objects.get_or_create(user=user)
        login(request, user)
        return JsonResponse({
            'token': token.key,
            'user_id': user.id,
            'username': user.username
        }, status=201)
    return JsonResponse({'error': 'POST required'}, status=405)


@csrf_exempt
def admin_token_login(request):
    """Authenticate admin user and return an auth token."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.POST
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username'] = username
            token, _ = Token.objects.get_or_create(user=user)
            return JsonResponse({
                'token': token.key,
                'user_id': user.id,
                'username': user.username
            })
        return JsonResponse({'error': 'Invalid credentials'}, status=401)
    return JsonResponse({'error': 'POST required'}, status=405)
