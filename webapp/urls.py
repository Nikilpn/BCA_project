from django.urls import path
from webapp import views


urlpatterns=[
    path('',views.home_page,name="home"),
    path('about/', views.about_page, name="about"),
    path('project-report/', views.project_report_page, name="project_report"),
    path('project-report/doc/', views.project_report_doc, name="project_report_doc"),

    path('services_page/', views.services_page, name="services_page"),
    path('rooms_page/', views.rooms_page, name="rooms_page"),
    path('advanced_search/', views.advanced_search_page, name="advanced_search"),

    #contact hotel by customer
    path('customer_contact_page/', views.customer_contact_page, name="customer_contact_page"),
    path('save_customer_contact_page/', views.save_customer_contact_page, name="save_customer_contact_page"),

#for getting specific roomsname(roomnumber1,roomnumber2)  inherited from roomtype(luxury,specific,lowclass)
    path('filtered_room_name/<room_name>/', views.filtered_room_name, name="filtered_room_name"),

    path('save_booking_page/', views.save_booking_page, name="save_booking_page"),

    path('booking_page/<int:pro_id>/', views.booking_page, name="booking_page"),
    path('delete_item/<int:pro_id>/', views.delete_item, name="delete_item"),
    path('save_room_page/', views.save_room_page, name="save_room_page"),
    # for saving room input details

    path('save_roompages_input/', views.save_roompages_input, name="save_roompages_input"),
#room page for webapp
    path('rooms_pages_new/', views.rooms_pages_new, name="rooms_pages_new"),
    #testimonial,ourteam page for webapp
    path('ourteam_page/', views.ourteam_page, name="ourteam_page"),
    path('testimonial_page/', views.testimonial_page, name="testimonial_page"),

    #signuppage & signin page
    path('signup_page/', views.signup_page, name="signup_page"),
    path('signin_page/', views.signin_page, name="signin_page"),

#saving signup_page to database
    path('save_user/', views.save_user, name="save_user"),

#userlogin_page by using password
    path('user_login_page/', views.user_login_page, name="user_login_page"),
    # for deleteing session userlogout
    path('userlogout_page/', views.userlogout_page, name="userlogout_page"),

    #for payment
    path('payment_page/', views.payment_page, name="payment_page"),
    path('generate_pdf/', views.generate_pdf, name="generate_pdf"),


    #for password reset
    path('reset_password_email_verification_page/', views.reset_password_email_verification_page,
         name="reset_password_email_verification_page"),
    path('reset_password_email_verification/', views.reset_password_email_verification, name="reset_password_email_verification"),


    path('passwordReset_verify_otp/<int:user_id>/', views.passwordReset_verify_otp,name="passwordReset_verify_otp"),
    path('reset_password/<str:username>', views.reset_password, name='reset_password'),
]