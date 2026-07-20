from django.shortcuts import render,redirect
from Backend.models import roomtypedb,roomnamedb,staffdb
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from webapp.models import bookingdb,customercontactdb,Totaldb
from django.contrib import messages

# Create your views here.
def index_page(request):
    return render(request,"0index.html")

#roomtypeDB with roomtype_page
def roomtype_page(request):
    return render(request,"1roomtype.html")
def save_roomtype_page(request):
    if request.method == "POST":
        rt=request.POST.get('roomtype')
        ds = request.POST.get('description')
        img=request.FILES['images']
        obj=roomtypedb(ROOMTYPE=rt,DESCRIPTION=ds,ROOMTYPEIMAGE=img)
        obj.save()
        messages.success(request,"Roomtype saved succesfully")
        return redirect(roomtype_page)
def display_roomtype_page(request):
    cat = roomtypedb.objects.all()
    return render(request,"2displayroomtype.html",{'cat':cat})

def edit_roomtype_page(request,prop_id):
    cat = roomtypedb.objects.get(id=prop_id)
    return render(request,"3editroomtype.html",{'cat':cat})

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

def delete_page(request,del_id):
    x=roomtypedb.objects.filter(id=del_id)
    x.delete()
    messages.success(request, "Data deleted succesfully")
    return redirect(display_roomtype_page)

# #------------Hotelsdb--roomoperations--------------
def room_number_page(request):
    pro=roomtypedb.objects.all()
    return render(request,"4roomnumber.html",{'pro':pro})

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
def display_room_number_page(request):
    pro = roomnamedb.objects.all()
    return render(request,"5displayroomnumber.html",{'pro':pro})

def edit_room_number_page(request,Edit_id):
    pro=roomnamedb.objects.get(id=Edit_id)
    cat=roomtypedb.objects.all()

    return render(request,"6edit_roomnumber.html",{'pro':pro,'cat':cat})

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
        if User.objects.filter(username__contains=un).exists():
            x=authenticate(username=un,password=pwd)
            if x is not None:
                login(request,x)
                request.session['username']=un
                request.session['password']=pwd
                return redirect(index_page)
            else:
                messages.warning(request, "Login failed")
                return redirect(login_page_admin)
        else:
            messages.success(request, "login succesfully")
            return redirect(login_page_admin)


def admin_logout(request):
    del request.session['username']
    del request.session['password']
    messages.success(request, "Logout sucessfully")
    return redirect(login_page_admin)

#Displaying Webapp(customersendingcontactmessage) in to Backend (8customercontacthtml page)
#connecting Webapp(db) and Backend

from webapp.models import customercontactdb
def contact_details_page(request):
    data=customercontactdb.objects.all()
    return render(request,"8customercontact.html",{'data':data})

def delete_customer_contact_details_page(request,del_id):
    x=customercontactdb.objects.filter(id=del_id)
    x.delete()
    return redirect(contact_details_page)
#adding staff details for customers
def staff_details_page(request):
    return render(request,"9staffdetails.html")

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
def display_staff_page(request):
    staff = staffdb.objects.all()
    return render(request,"10displaystaff.html",{'staff':staff})

def edit_STAFF_page(request,Edit_id):
    pro=staffdb.objects.get(id=Edit_id)

    return render(request,"11editstaff.html",{'pro':pro})

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

def delete_staff_page(request,del_id):
    x=staffdb.objects.filter(id=del_id)
    x.delete()
    messages.success(request, "Staffs details deleted successfully")
    return redirect(display_staff_page)

#full details of customers booked
def detailsbooked_page(request):
    data=bookingdb.objects.all()
    return render(request,"12detailsbooked.html",{"data":data})
def deletebooked_details(request,del_id):
    x=bookingdb.objects.filter(id=del_id)
    x.delete()
    return redirect(detailsbooked_page)

#total amount of moneypayed by customer (displaypage)

def customertotalamount_page(request):
    data=Totaldb.objects.all()
    return render(request,"13fewdetails.html",{'data':data})
def deletecustomertotalamount_page(request,del_id):
    x=Totaldb.objects.filter(id=del_id)
    x.delete()
    return redirect(customertotalamount_page)
