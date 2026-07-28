import random

from django.shortcuts import render, redirect
from Backend.models import roomnamedb, roomtypedb, staffdb
from webapp.models import customercontactdb, bookingdb, Registerdb, Totaldb
from django.contrib import messages
import razorpay


# Create your views here.
def home_page(request):
    cat = roomtypedb.objects.all()
    return render(request, "1home.html", {'cat': cat})


def about_page(request):
    cat = staffdb.objects.all()
    return render(request, "2about.html", {'cat': cat})


def services_page(request):
    return render(request, "3services.html")


def rooms_page(request):
    return render(request, "4rooms.html")


def advanced_search_page(request):
    """Render the advanced room search page"""
    room_types = roomtypedb.objects.all()
    return render(request, "14advanced_room_search.html", {'room_types': room_types})


def project_report_page(request):
    """Render a printable BCA project report page (BCSP-064)."""
    return render(request, 'project_report.html', {})


def project_report_doc(request):
    """Download the BCA project report as a Word-compatible (.doc) file.

    Transforms the HTML template for Microsoft Word compatibility:
    - Replaces CSS variables with hardcoded hex values
    - Replaces CSS Grid/Flexbox layouts with tables
    - Removes browser-only elements (toolbar)
    - Adds Word XML namespace and document settings
    """
    import re
    from django.template.loader import render_to_string
    html = render_to_string('project_report.html', {})

    # ── 1. Replace <style> block with Word-compatible CSS ──
    word_css = (
        '<style>\n'
        'body{font-family:"Georgia","Times New Roman",Times,serif;'
        'color:#1f2937;line-height:2;font-size:14pt;margin:0;padding:0;}\n'
        'p{margin:6pt 0;}\n'
        '.toolbar{display:none;mso-hide:all;}\n'
        '.btn{display:none;}\n'
        '.page{margin:0 auto;padding:0;}\n'
        'h1.chapter{font-family:"Segoe UI",Arial,Helvetica,sans-serif;'
        'font-size:22pt;color:#0f172a;border-bottom:3pt double #2563eb;'
        'padding-bottom:8pt;margin:36pt 0 18pt 0;page-break-before:always;page-break-after:avoid;}\n'
        'h2.section{font-family:"Segoe UI",Arial,Helvetica,sans-serif;'
        'font-size:17pt;color:#1e3a8a;margin:28pt 0 12pt 0;'
        'page-break-after:avoid;}\n'
        'h3.subsec{font-family:"Segoe UI",Arial,Helvetica,sans-serif;'
        'font-size:14pt;color:#334155;margin:20pt 0 10pt 0;font-weight:bold;'
        'page-break-after:avoid;}\n'
        'h4.subsub{font-size:13pt;color:#475569;font-weight:bold;'
        'margin:14pt 0 8pt 0;page-break-after:avoid;}\n'
        '.cover-page{text-align:center;page-break-after:always;'
        'padding-top:60pt;}\n'
        '.cover-page .univ{font-size:18pt;font-weight:bold;color:#0f172a;'
        'letter-spacing:1pt;}\n'
        '.cover-page .school{font-size:13pt;color:#64748b;'
        'margin:4pt 0 30pt 0;}\n'
        '.cover-page .title{font-size:24pt;font-weight:bold;color:#1e3a8a;'
        'margin:30pt 0 12pt 0;line-height:1.4;}\n'
        '.cover-page .sub{font-size:13pt;margin:12pt 0;}\n'
        'table{width:100%;border-collapse:collapse;margin:12pt 0;'
        'font-size:12pt;line-height:1.6;}\n'
        'th,td{border:1pt solid #94a3b8;padding:7pt 10pt;text-align:left;'
        'vertical-align:top;}\n'
        'th{background:#eff6ff;color:#0f172a;font-weight:bold;'
        'font-family:"Segoe UI",Arial,Helvetica,sans-serif;}\n'
        'ul,ol{margin:8pt 0 8pt 24pt;padding:0;}\n'
        'li{margin-bottom:6pt;}\n'
        'pre{background:#f1f5f9;border:1pt solid #dbe3ee;padding:12pt 14pt;'
        'font-family:"Courier New",monospace;font-size:10pt;'
        'line-height:1.55;margin:10pt 0;white-space:pre-wrap;'
        'word-wrap:break-word;}\n'
        'code{font-family:"Courier New",monospace;font-size:10pt;'
        'background:#f1f5f9;padding:1pt 4pt;}\n'
        '.fig{text-align:center;margin:16pt 0;}\n'
        '.fig-caption{font-size:11pt;color:#64748b;font-style:italic;'
        'margin-top:6pt;}\n'
        '.hl{padding:14pt 16pt;border-left:5pt solid #16a34a;'
        'background:#f0fdf4;margin:14pt 0;}\n'
        '.warn{border-left-color:#eab308;background:#fefce8;}\n'
        '.info{border-left-color:#2563eb;background:#eff6ff;}\n'
        '.sig-line{margin-top:60pt;border-top:1pt solid #334155;'
        'padding-top:8pt;font-weight:bold;}\n'
        '.toc ol{list-style:none;margin:0;padding:0;}\n'
        '.toc li{padding:5pt 0;border-bottom:1pt dotted #dbe3ee;}\n'
        '.toc li ul{list-style:disc;margin-top:4pt;padding-left:20pt;}\n'
        '.toc li ul li{border-bottom:none;padding:2pt 0;}\n'
        '.pb{page-break-after:always;}\n'
        '@page{size:210mm 297mm;margin:20mm 22mm 20mm 28mm;'
        'mso-page-orientation:portrait;}\n'
        '@page Section1{mso-header-margin:14.2pt;'
        'mso-footer-margin:14.2pt;mso-paper-source:0;}\n'
        'div.page{page:Section1;}\n'
        '</style>'
    )
    html = re.sub(r'<style>.*?</style>', word_css, html,
                  flags=re.DOTALL, count=1)

    # ── 2. Replace CSS variables in inline styles ──
    for var, val in {
        'var(--pri)': '#1e3a8a', 'var(--sec)': '#0f172a',
        'var(--acc)': '#2563eb', 'var(--mut)': '#64748b',
        'var(--bg)': '#f8fafc', 'var(--bdr)': '#dbe3ee',
        'var(--ok)': '#16a34a',
        'var(--font-main)': '"Georgia","Times New Roman",Times,serif',
        'var(--font-head)': '"Segoe UI",Arial,sans-serif',
    }.items():
        html = html.replace(var, val)

    # ── 3. Remove toolbar HTML ──
    tb = html.find('<div class="toolbar">')
    pg = html.find('<div class="page">')
    if tb != -1 and pg != -1 and tb < pg:
        html = html[:tb] + html[pg:]

    # ── 4. Replace meta-grid (CSS Grid) → Word table ──
    mg_start = html.find('<div class="meta-grid">')
    if mg_start != -1:
        depth, i, mg_end = 0, mg_start, -1
        while i < len(html) and i < mg_start + 3000:
            if html[i:i+4] == '<div':
                depth += 1
            elif html[i:i+6] == '</div>':
                depth -= 1
                if depth == 0:
                    mg_end = i + 6
                    break
            i += 1
        if mg_end != -1:
            new_meta = (
                '<table width="100%" cellpadding="0" cellspacing="0"'
                ' style="margin:30pt auto;max-width:520pt;border:none;">\n'
                '    <tr>\n'
                '      <td width="50%" valign="top" style="border:1pt solid'
                ' #dbe3ee;padding:16pt;text-align:left;">\n'
                '        <strong style="display:block;margin-bottom:4pt;'
                'color:#1e3a8a;font-family:Segoe UI,Arial,sans-serif;">'
                'Submitted By</strong>\n'
                '        <div>Name: <strong>Nikhil P N</strong></div>\n'
                '        <div>Enrolment No: <strong>2350526613</strong>'
                '</div>\n'
                '        <div>Programme: BCA</div>\n'
                '        <div>Study Centre Code: ___________</div>\n'
                '        <div>Regional Centre: <strong>IGNOU Kolkata'
                ' Regional Centre</strong></div>\n'
                '        <div>Address: ___________</div>\n'
                '      </td>\n'
                '      <td width="50%" valign="top" style="border:1pt solid'
                ' #dbe3ee;padding:16pt;text-align:left;">\n'
                '        <strong style="display:block;margin-bottom:4pt;'
                'color:#1e3a8a;font-family:Segoe UI,Arial,sans-serif;">'
                'Under the Guidance of</strong>\n'
                '        <div>Guide Name: ___________</div>\n'
                '        <div>Designation: ___________</div>\n'
                '        <div>Qualification: ___________</div>\n'
                '        <div>Address: ___________</div>\n'
                '        <div>Academic Year: <strong>2025 \u2013 2026'
                '</strong></div>\n'
                '      </td>\n'
                '    </tr>\n'
                '  </table>'
            )
            html = html[:mg_start] + new_meta + html[mg_end:]

    # ── 5. Replace sig-grid (CSS Grid) → Word table ──
    sg_start = html.find('<div class="sig-grid">')
    if sg_start != -1:
        depth, i, sg_end = 0, sg_start, -1
        while i < len(html) and i < sg_start + 2000:
            if html[i:i+4] == '<div':
                depth += 1
            elif html[i:i+6] == '</div>':
                depth -= 1
                if depth == 0:
                    sg_end = i + 6
                    break
            i += 1
        if sg_end != -1:
            new_sig = (
                '<table width="100%" cellpadding="0" cellspacing="0"'
                ' style="margin-top:32pt;border:none;">\n'
                '    <tr>\n'
                '      <td width="50%" valign="top" style="border:none;'
                'padding:0 10pt;">\n'
                '        <div class="sig-line">Signature of the Student'
                '</div>\n'
                '        <div style="color:#64748b">Name: Nikhil P N<br>'
                'Enrolment No: 2350526613<br>Date: ___________</div>\n'
                '      </td>\n'
                '      <td width="50%" valign="top" style="border:none;'
                'padding:0 10pt;">\n'
                '        <div class="sig-line">Signature of the Guide'
                '</div>\n'
                '        <div style="color:#64748b">Name: ___________<br>'
                'Designation: ___________<br>Address: ___________<br>'
                'Date: ___________</div>\n'
                '      </td>\n'
                '    </tr>\n'
                '  </table>'
            )
            html = html[:sg_start] + new_sig + html[sg_end:]

    # ── 6. Replace DFD diagram (Flexbox) → Word table ──
    dfd_pos = html.find('Figure 8.1')
    if dfd_pos != -1:
        fig_start = html.rfind('<div class="fig">', 0, dfd_pos)
        if fig_start != -1:
            cap_close = html.find('</div>', dfd_pos)
            fig_close = html.find('</div>', cap_close + 6)
            fig_end = fig_close + 6
            new_dfd = (
                '<div class="fig">\n'
                '  <table width="100%" cellpadding="8" cellspacing="0"'
                ' style="border:2pt solid #2563eb;margin:0 auto;'
                'max-width:600pt;">\n'
                '    <tr>\n'
                '      <td width="18%" valign="middle" style="border:2pt'
                ' solid #1e3a8a;padding:14pt;background:#eff6ff;'
                'font-weight:bold;text-align:center;">\n'
                '        CUSTOMER<br><span style="font-weight:normal;'
                'font-size:10pt">(External Entity)</span>\n'
                '      </td>\n'
                '      <td width="18%" valign="middle" style="text-align:'
                'center;border:none;">\n'
                '        <div style="font-size:10pt;color:#64748b;">'
                'Registration, Login, Search,<br>Booking, Payment,'
                ' Contact, Chat</div>\n'
                '        <div style="font-size:20pt;">&rarr;</div>\n'
                '        <div style="font-size:20pt;">&larr;</div>\n'
                '        <div style="font-size:10pt;color:#64748b;">'
                'Room details, Booking confirmation,<br>Search results,'
                ' Chat responses, PDF</div>\n'
                '      </td>\n'
                '      <td width="28%" valign="middle" style="border:3pt'
                ' solid #1e3a8a;padding:10pt;background:#dbeafe;'
                'text-align:center;font-weight:bold;font-size:12pt;'
                'line-height:1.3;">\n'
                '        Hotel Room<br>Booking<br>System<br>'
                '<span style="font-size:9pt;font-weight:normal">'
                '(Process 0.0)</span>\n'
                '      </td>\n'
                '      <td width="18%" valign="middle" style="text-align:'
                'center;border:none;">\n'
                '        <div style="font-size:10pt;color:#64748b;">'
                'Room/Staff/Type CRUD,<br>View bookings, View payments'
                '</div>\n'
                '        <div style="font-size:20pt;">&larr;</div>\n'
                '        <div style="font-size:20pt;">&rarr;</div>\n'
                '        <div style="font-size:10pt;color:#64748b;">'
                'Reports, Records,<br>Notifications, Chatbot logs</div>\n'
                '      </td>\n'
                '      <td width="18%" valign="middle" style="border:2pt'
                ' solid #1e3a8a;padding:14pt;background:#eff6ff;'
                'font-weight:bold;text-align:center;">\n'
                '        ADMINISTRATOR<br><span style="font-weight:normal;'
                'font-size:10pt">(External Entity)</span>\n'
                '      </td>\n'
                '    </tr>\n'
                '  </table>\n'
                '  <div class="fig-caption">Figure 8.1 \u2013 DFD Level-0'
                ' (Context Diagram)</div>\n'
                '</div>'
            )
            html = html[:fig_start] + new_dfd + html[fig_end:]

    # ── 7. Clean remaining inline styles unsupported by Word ──
    for prop in [
        'display:flex;', 'display:inline-flex;', 'display:inline-block;',
        'align-items:center;', 'justify-content:center;',
        'justify-content:space-between;',
        'gap:30pt;', 'gap:28pt;', 'gap:16pt;', 'gap:10pt;', 'gap:8px;',
        'flex-wrap:wrap;',
        'border-radius:50%;', 'border-radius:12pt;',
        'border-radius:8pt;', 'border-radius:6pt;', 'border-radius:3pt;',
        'border-radius:999px;', 'border-radius:4px;',
        'backdrop-filter:blur(8px);',
    ]:
        html = html.replace(prop, '')

    # ── 8. Add Word XML namespace to <html> tag ──
    html = html.replace(
        '<html lang="en">',
        '<html xmlns:o="urn:schemas-microsoft-com:office:office" '
        'xmlns:w="urn:schemas-microsoft-com:office:word" '
        'xmlns="http://www.w3.org/TR/REC-html40" lang="en">'
    )

    # ── 9. Add Word document settings before </head> ──
    word_head = (
        '<!--[if gte mso 9]>\n'
        '<xml>\n'
        '<o:OfficeDocumentSettings>'
        '<o:AllowPNG/>'
        '</o:OfficeDocumentSettings>\n'
        '</xml>\n'
        '<xml>\n'
        '<w:WordDocument>'
        '<w:View>Print</w:View>'
        '<w:Zoom>100</w:Zoom>'
        '<w:DoNotOptimizeForBrowser/>'
        '</w:WordDocument>\n'
        '</xml>\n'
        '<![endif]-->\n'
    )
    html = html.replace('</head>', word_head + '</head>')

    response = HttpResponse(html, content_type='application/msword')
    response['Content-Disposition'] = (
        'attachment; filename="BCSP064_Project_Report_Nikhil_PN.doc"'
    )
    return response


def customer_contact_page(request):
    return render(request, "5contact.html")


def save_customer_contact_page(request):
    if request.method == "POST":
        na = request.POST.get('cname')
        em = request.POST.get('cemail')
        cn = request.POST.get('cnumber')
        cs = request.POST.get('csubject')
        cm = request.POST.get('cmessage')
        obj = customercontactdb(CONTACTNAME=na, CONTACTEMAIL=em, CONTACTNUMBER=cn, CONTACTSUBJECT=cs, CONTACTMESSAGE=cm)
        obj.save()
        messages.success(request, "Message Send successfully")
        return redirect(customer_contact_page)


# for getting specific roomsname(roomnumber1,roomnumber2)  inherited from roomtype(luxury,specific,lowclass)
# Backend models(roomnamedb) connected to Webapp  page and showing  someparticular category added to luxury type like wise..

def filtered_room_name(request, room_name):
    # Try to get roomtypedb by ID first (new links), then by ROOMTYPE name (legacy links)
    try:
        room_type = roomtypedb.objects.get(id=int(room_name))
    except (ValueError, roomtypedb.DoesNotExist):
        try:
            room_type = roomtypedb.objects.get(ROOMTYPE__iexact=room_name)
        except roomtypedb.DoesNotExist:
            return render(request, "6roomname_filtered.html", {'data': [], 'error': 'Room type not found'})
    
    data = roomnamedb.objects.filter(ROOMTYPE=room_type)
    return render(request, "6roomname_filtered.html", {'data': data})


def save_room_page(request):
    return render(request, "7savedroom.html")


def booking_page(request, pro_id):
    data = bookingdb.objects.filter(CUSTOMERNAME=request.session['USERNAME'])
    cat = roomnamedb.objects.get(id=pro_id)
    return render(request, "7booking.html", {'cat': cat, 'data': data})


def save_room_page(request):
    global total
    data = bookingdb.objects.filter(CUSTOMERNAME=request.session['USERNAME'])
    subtotal = 0
    tax = 100
    total = 0

    for d in data:
        subtotal = subtotal + d.TOTALPRICE
        if subtotal > 5000:
            tax = 10
        else:
            tax = 20
        total = subtotal + tax

    return render(request, "7savedroom.html", {'data': data, 'subtotal': subtotal, 'total': total, 'tax': tax})


def save_roompages_input(request):
    if request.method == "POST":
        na = request.POST.get('customername')
        mb = request.POST.get('customermobile')  # Now CharField, no conversion needed
        tl = request.POST.get('totalprice')
        
        # Optionally link to the last booking made by this customer
        last_booking = None
        if 'USERNAME' in request.session:
            last_booking = bookingdb.objects.filter(
                CUSTOMERNAME=request.session['USERNAME']
            ).order_by('-id').first()
        
        obj = Totaldb(
            BOOKING=last_booking,
            CUSTOMERNAME=na, 
            MOBILE=mb,  # Now CharField
            TOTALPRICE=int(tl) if tl else None
        )
        obj.save()
        return redirect(payment_page)


def delete_item(request, pro_id):
    x = bookingdb.objects.filter(id=pro_id)
    x.delete()
    messages.warning(request, "Room deleted successfully")
    return redirect(save_room_page)


def save_booking_page(request, CONTACTEMAIL=None):
    if request.method == "POST":
        na = request.POST.get('bname')
        em = request.POST.get('bemail')
        chn = request.POST.get('bcheckin')
        cho = request.POST.get('bcheckout')
        ta = request.POST.get('btotaladults')
        tc = request.POST.get('btotalchilds')
        sr_id = request.POST.get('bselectroom')  # This is now the room ID
        sre = request.POST.get('bspecialrequest')
        tp = request.POST.get('btotalprice')

        # Parse dates from string to proper date objects
        from datetime import datetime
        try:
            checkin_date = datetime.strptime(chn, '%Y-%m-%d').date() if '-' in chn else datetime.strptime(chn, '%m/%d/%Y').date()
            checkout_date = datetime.strptime(cho, '%Y-%m-%d').date() if '-' in cho else datetime.strptime(cho, '%m/%d/%Y').date()
        except (ValueError, TypeError):
            messages.error(request, "Invalid date format.")
            return redirect('save_room_page')

        # Validate: checkin must be before checkout
        if checkin_date >= checkout_date:
            messages.error(request, "Check-out date must be after check-in date.")
            return redirect('save_room_page')

        # Validate: checkin must not be in the past
        from datetime import date
        if checkin_date < date.today():
            messages.error(request, "Check-in date cannot be in the past.")
            return redirect('save_room_page')

        # obj = bookingdb(CUSTOMERNAME=na, CONTACTEMAIL=em, CHECKIN=chn, CHECKOUT=cho, TOTALADULTS=ta, TOTALCHILDS=tc,
        #                 SELECTROOM=sr, SPECIALREQUEST=sre, TOTALPRICE=tp)
        # # Check for overlapping bookings
        # overlapping_bookings = bookingdb.objects.filter(
        #     SELECTROOM=sr,
        #     CHECKIN=chn,
        #     CHECKOUT=cho
        # )
        #
        # if overlapping_bookings.exists():
        #     messages.error(request, "The selected room is already booked for the specified dates.")
        #     return redirect('save_room_page')  # Redirect back to the booking form page
        #
        # # If no overlap, save the booking
        #
        # messages.success(request, "saved room successfully")
        #
        #
        #
        # obj.save()
        #
        # messages.success(request, "Room booked successfully.")
        # subject = "Conragatulations roombooked"
        # message = f"Dear customer you have booked a room succesfully :   Thank you "
        # send_mail(subject, message, EMAIL_HOST_USER, [obj.CONTACTEMAIL], fail_silently=True, )
        #
        # return redirect(save_room_page)
        # Get the room object from the ID
        try:
            room_obj = roomnamedb.objects.get(id=sr_id)
        except roomnamedb.DoesNotExist:
            messages.error(request, "Invalid room selection.")
            return redirect('save_room_page')
        
        # Check for overlapping bookings with the ForeignKey and DateField
        overlapping_bookings = bookingdb.objects.filter(
            SELECTROOM=room_obj
        ).filter(
            CHECKIN__lte=checkout_date,
            CHECKOUT__gte=checkin_date
        )

        if overlapping_bookings.exists():
            messages.error(request, "The selected room is already booked for the specified dates.")
            return redirect('save_room_page')  # Redirect back to the booking form page
        else:
            # Get the customer if logged in
            customer_obj = None
            if 'USERNAME' in request.session:
                try:
                    customer_obj = Registerdb.objects.get(USERNAME=request.session['USERNAME'])
                except Registerdb.DoesNotExist:
                    pass

            # If no overlap, save the booking
            obj = bookingdb(
                CUSTOMER=customer_obj,
                CUSTOMERNAME=na,
                CONTACTEMAIL=em,
                CHECKIN=checkin_date,
                CHECKOUT=checkout_date,
                TOTALADULTS=int(ta) if ta else None,
                TOTALCHILDS=int(tc) if tc else None,
                SELECTROOM=room_obj,  # Now a ForeignKey
                SPECIALREQUEST=sre,
                TOTALPRICE=int(tp) if tp else None
            )
            obj.save()

            messages.success(request, "Room booked successfully.")

            # Send confirmation email
            subject = "Congratulations roombooked"
            message = f"Dear customer you have booked a room succesfully :   Thank you & have a nice day ,Hoteliers"
            send_mail(subject, message, EMAIL_HOST_USER, [obj.CONTACTEMAIL], fail_silently=True, )
            return redirect('save_room_page')


        return redirect('save_room_page')  # If not POST, just redirect

def rooms_pages_new(request):
    cat = roomtypedb.objects.all()
    return render(request, "8onlyroom.html", {'cat': cat})


def ourteam_page(request):
    cat = staffdb.objects.all()
    return render(request, "9ourteam.html", {'cat': cat})


def testimonial_page(request):
    return render(request, "10testimonial.html")


# login_page
def signup_page(request):
    return render(request, "11signup.html")


def signin_page(request):
    return render(request, "12userlogin.html")


# saving password,confirmpassword to database from signup_page
def save_user(request):
    if request.method == "POST":
        na = request.POST.get('name')
        em = request.POST.get('email')
        p1 = request.POST.get('pass1')
        p2 = request.POST.get('pass2')
        hashed = make_password(p1)
        obj = Registerdb(USERNAME=na, EMAIL=em, PASSWORD=hashed, CONFIRMPASSWORD=hashed)
        obj.save()
        messages.success(request, "signup successfully")
        return redirect(signin_page)


def user_login_page(request):
    if request.method == "POST":
        un = request.POST.get('uname')
        pswd = request.POST.get('upassword')
        try:
            user = Registerdb.objects.get(USERNAME=un)
            if check_password(pswd, user.PASSWORD):
                request.session['USERNAME'] = un
                request.session['PASSWORD'] = pswd
                messages.success(request, "signin successfully")
                return redirect(home_page)
            else:
                messages.warning(request, "signin failed")
                return redirect(signin_page)
        except Registerdb.DoesNotExist:
            messages.warning(request, "signin failed")
            return redirect(signin_page)

    # for deleteing session userlogout


def userlogout_page(request):
    del request.session['USERNAME']
    del request.session['PASSWORD']
    messages.success(request, "signout successfully")
    return redirect(home_page)


# for payment
def payment_page(request):
    customer = Totaldb.objects.order_by('-id').first()
    payy = customer.TOTALPRICE
    amount = int(payy * 100)
    payy_str = str(amount)
    for i in payy_str:
        print(i)
    if request.method == "POST":
        order_currency = 'INR'
        client = razorpay.Client(auth=('rzp_test_klfWwvjaFXjXmC', 's9P7dwOwYckK352FfRJOXIRV'))
        payment = client.order.create({'amount': amount, 'currency': order_currency, 'payment_capture': '1'})

    return render(request, "payment.html", {'customer': customer, 'payy_str': payy_str})


from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa

from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa


def generate_pdf(request):
    # Data to pass to the template
    username = request.session.get('USERNAME', 'Guest')

    # Render the template with context
    context = {
        'username': username,
        'data': 'Your data here',
    }

    # Render the HTML template with context data
    html_string = render_to_string('your_template.html', context)

    # Create a PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    # Convert HTML to PDF
    pisa_status = pisa.CreatePDF(html_string, dest=response)

    # Return the response
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
    return response


from django.core.mail import send_mail
from django.core.mail import EmailMessage
from Hotelierss.settings import EMAIL_HOST_USER
from django.core.mail import EmailMessage







 #for generating otp starts here
def generate_otp(request):
     otp=random.randint(10000,55555)
     return(otp)
def reset_password_email_verification_page(request):
    return render(request,"15password_reset_email.html")


def reset_password_email_verification(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if Registerdb.objects.filter(EMAIL=email).exists():
            user = Registerdb.objects.get(EMAIL=email)
            u_otp = generate_otp(request)
            request.session['otp'] = u_otp
            subject = "Forgot Password"
            message = f"Dear user OTP for reset your account password is : {u_otp}   Thank you , Hoteliers"
            send_mail(subject, message, EMAIL_HOST_USER, [email], fail_silently=True, )  # send otp to mail
            context = {
                'message': "An OTP sent to your registered email id.",
                'user': user,
            }
            return render(request, "16password_reset_otp.html", context)
        else:
            # Show error on the email verification page instead
            return render(request, "15password_reset_email.html", {'error': "Sorry..Invalid email id"})
    else:
        return redirect("home")

def passwordReset_verify_otp(request,user_id):
    user = Registerdb.objects.get(id=user_id)
    if request.method == "POST":
        u_otp = str(request.POST.get('otp')).strip() #removing unwanted space for the otp, if we copy paste the progra,m
        s_otp = str(request.session.get('otp')).strip() # get stored otp
        if u_otp == s_otp:  # verifying two otp
            context = {
                'user': user,
                'username': user.USERNAME
            }
            return render(request, "17reset_password.html", context)
        else:
            context = {
                'error': "OTP does not match.!!",
                'user': user,
                'username': user.USERNAME
            }
            return render(request, "16password_reset_otp.html", context)
    else:
        return redirect("user_login_page")

from django.contrib.auth.hashers import make_password, check_password

def hash_existing_passwords():
    """One-time migration: hash all plain-text passwords in Registerdb."""
    from webapp.models import Registerdb
    for user in Registerdb.objects.all():
        if not user.PASSWORD.startswith('pbkdf2_'):
            user.PASSWORD = make_password(user.PASSWORD)
            user.save(update_fields=['PASSWORD'])

# Run on startup for this session (no-op if already hashed)
hash_existing_passwords()

def reset_password(request, username):
    if request.method == "POST":
        try:
            user = Registerdb.objects.get(USERNAME=username)
        except Registerdb.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect("user_login_page")
        
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            try:
                hashed = make_password(password1)
                Registerdb.objects.filter(USERNAME=username).update(PASSWORD=hashed)
                messages.success(request, "Your password has been reset successfully! "
                                          "You can now log in with your new password.")
                subject = "Password Changed"
                message = f"Dear user, your password has been recently changed. Thank you, Team t4Text"
                send_mail(subject, message, EMAIL_HOST_USER, [user.EMAIL],
                          fail_silently=True)  # Send email notification
                messages.success(request, "Reset password successfully")
                return redirect("user_login_page")
            except Registerdb.DoesNotExist:
                messages.error(request, "User not found.")
                return redirect("user_login_page")
        else:
            return render(request, "17reset_password.html",
                          {'error': "Sorry, passwords do not match!", 'user': user, 'username': username})
    else:
        try:
            user = Registerdb.objects.get(USERNAME=username)
            return render(request, "17reset_password.html", {'user': user, 'username': username})
        except Registerdb.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect("user_login_page")