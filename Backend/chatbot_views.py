from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, timedelta
from Backend.models import roomnamedb, roomtypedb, staffdb, ChatbotResponse, ChatbotConversation, Notification
from webapp.models import bookingdb

@csrf_exempt
@require_http_methods(["POST"])
def chatbot_query(request):
    """
    Handle chatbot queries and return intelligent responses
    """
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip().lower()
        username = data.get('username', 'Guest')
        
        if not user_message:
            return JsonResponse({'error': 'Empty message'}, status=400)
        
        # Determine query type and get response
        response_data = generate_chatbot_response(user_message, username)
        
        # Save conversation
        ChatbotConversation.objects.create(
            username=username,
            user_message=data.get('message'),
            bot_response=response_data['response'],
            query_type=response_data.get('query_type', 'general')
        )
        
        return JsonResponse({
            'response': response_data['response'],
            'query_type': response_data.get('query_type', 'general'),
            'suggestions': response_data.get('suggestions', []),
            'data': response_data.get('data', [])
        })
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def generate_chatbot_response(user_message, username):
    """
    Generate intelligent chatbot response based on user query
    """
    response = {
        'response': '',
        'query_type': 'general',
        'suggestions': [],
        'data': []
    }
    
    # Keywords for different query types
    room_keywords = ['room', 'price', 'availability', 'rooms', 'bed', 'luxury', 'deluxe', 'suite']
    staff_keywords = ['staff', 'team', 'manager', 'receptionist', 'housekeeper', 'chef']
    booking_keywords = ['booking', 'reserve', 'book', 'reservation', 'check-in', 'check-out', 'cancel']
    
    # Check query type
    if any(keyword in user_message for keyword in room_keywords):
        return handle_room_query(user_message, username, response)
    elif any(keyword in user_message for keyword in staff_keywords):
        return handle_staff_query(user_message, username, response)
    elif any(keyword in user_message for keyword in booking_keywords):
        return handle_booking_query(user_message, username, response)
    else:
        return handle_general_query(user_message, username, response)


def handle_room_query(user_message, username, response):
    """Handle queries about rooms"""
    response['query_type'] = 'room'
    
    # Search for specific room keywords
    if 'price' in user_message:
        response['response'] = "We offer rooms at various price points. Our prices range from budget-friendly to premium luxury. What's your budget?"
        response['suggestions'] = ['Show me budget rooms', 'Show me luxury rooms', 'Show me all rooms']
    
    elif 'available' in user_message or 'availability' in user_message:
        response['response'] = "Our rooms are available for booking! Please enter your check-in and check-out dates to check availability."
        response['suggestions'] = ['Show available dates', 'Search by date range']
    
    elif 'luxury' in user_message or 'deluxe' in user_message or 'suite' in user_message:
        rooms = roomnamedb.objects.filter(
            ROOMTYPE__ROOMTYPE__icontains='luxury'
        ) if 'luxury' in user_message else roomnamedb.objects.all()
        
        room_list = [{
            'id': room.id,
            'name': room.ROOMNAME,
            'type': room.ROOMTYPE.ROOMTYPE,
            'price': room.ROOMPRICE,
            'image': room.ROOMIMAGE.url if room.ROOMIMAGE else None
        } for room in rooms[:5]]
        
        response['response'] = f"Here are our {room_list[0]['type'] if room_list else 'available'} rooms."
        response['data'] = room_list
        response['suggestions'] = ['View details', 'Check availability', 'Book now']
    
    else:
        # General room info
        all_rooms = roomnamedb.objects.all()
        response['response'] = f"We have {all_rooms.count()} rooms available. Would you like to search by room type, price range, or availability?"
        response['suggestions'] = ['Show all rooms', 'Search by type', 'Search by price', 'Search by dates']
    
    return response


def handle_staff_query(user_message, username, response):
    """Handle queries about staff"""
    response['query_type'] = 'staff'
    
    staff_members = staffdb.objects.all()
    
    if 'team' in user_message or 'staff' in user_message:
        response['response'] = f"We have a dedicated team of {staff_members.count()} professional staff members ready to assist you."
        
        staff_list = [{
            'id': staff.id,
            'name': staff.STAFFNAME,
            'designation': staff.STAFFDESIGNATION,
            'image': staff.STAFFIMAGE.url if staff.STAFFIMAGE else None
        } for staff in staff_members]
        
        response['data'] = staff_list
        response['suggestions'] = ['View all staff', 'Contact us', 'Speak to manager']
    
    else:
        response['response'] = "Our team is here to help! What would you like to know about our staff?"
        response['suggestions'] = ['View team', 'Contact reception', 'Speak to manager']
    
    return response


def handle_booking_query(user_message, username, response):
    """Handle queries about bookings"""
    response['query_type'] = 'booking'
    
    if 'cancel' in user_message:
        response['response'] = "To cancel a booking, please log in to your account or contact our support team. We'll help you with the cancellation process."
        response['suggestions'] = ['Login to account', 'Contact support', 'View my bookings']
    
    elif 'check-in' in user_message or 'check out' in user_message.replace('-', ' '):
        response['response'] = "Check-in time is 2:00 PM and check-out time is 11:00 AM. Early check-in and late check-out may be available upon request."
        response['suggestions'] = ['Request early check-in', 'Request late check-out']
    
    else:
        response['response'] = "We're happy to help with your booking! Would you like to make a new reservation, modify an existing one, or have questions about our policies?"
        response['suggestions'] = ['Make new booking', 'Modify booking', 'View my bookings', 'Cancellation policy']
    
    return response


def handle_general_query(user_message, username, response):
    """Handle general queries"""
    response['query_type'] = 'general'
    
    general_responses = {
        'hello': "Hello! 👋 Welcome to our hotel. How can I help you today?",
        'hi': "Hi there! 👋 Looking for a room? We'd love to help!",
        'help': "I can help you with: 🏨 Room information, 👥 Staff details, 📅 Bookings, and more. What would you like to know?",
        'contact': "You can reach us at the front desk or use the contact form. How can we assist?",
        'thank you': "You're welcome! Is there anything else I can help with?",
        'thanks': "Happy to help! Anything else?"
    }
    
    # Find matching general response
    for keyword, reply in general_responses.items():
        if keyword in user_message:
            response['response'] = reply
            response['suggestions'] = ['Browse rooms', 'Make booking', 'Contact us']
            return response
    
    # Default response
    response['response'] = "I'm not sure about that. Can you provide more details? I can help with rooms, bookings, and staff information."
    response['suggestions'] = ['Browse rooms', 'Make booking', 'View staff']
    
    return response


@csrf_exempt
@require_http_methods(["POST"])
def rate_response(request):
    """Rate the chatbot response"""
    try:
        data = json.loads(request.body)
        conversation_id = data.get('conversation_id')
        rating = data.get('rating')
        
        conversation = ChatbotConversation.objects.get(id=conversation_id)
        conversation.rating = rating
        conversation.save()
        
        return JsonResponse({'success': True, 'message': 'Thank you for your feedback!'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def search_rooms(request):
    """
    Advanced room search with filters
    Query parameters: name, room_type, min_price, max_price, check_in, check_out
    """
    try:
        rooms = roomnamedb.objects.all()
        
        # Filter by room name
        room_name = request.GET.get('name', '').strip()
        if room_name:
            rooms = rooms.filter(ROOMNAME__icontains=room_name)
        
        # Filter by room type
        room_type = request.GET.get('room_type')
        if room_type:
            rooms = rooms.filter(ROOMTYPE__id=room_type)
        
        # Filter by price range
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        
        if min_price:
            rooms = rooms.filter(ROOMPRICE__gte=int(min_price))
        if max_price:
            rooms = rooms.filter(ROOMPRICE__lte=int(max_price))
        
        # Filter by availability dates
        check_in = request.GET.get('check_in')
        check_out = request.GET.get('check_out')
        
        available_rooms = []
        for room in rooms:
            is_available = True
            if check_in and check_out:
                check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
                check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
                
                # Check if room has conflicting bookings
                conflicting_bookings = bookingdb.objects.filter(
                    SELECTROOM=room,
                    CHECKIN__lte=check_out_date,
                    CHECKOUT__gte=check_in_date
                )
                is_available = not conflicting_bookings.exists()
            
            if is_available:
                available_rooms.append(room)
        
        # Format response
        room_list = [{
            'id': room.id,
            'name': room.ROOMNAME,
            'type': room.ROOMTYPE.ROOMTYPE if room.ROOMTYPE else 'Standard',
            'price': room.ROOMPRICE,
            'description': room.ROOMDESCRIPTION,
            'image': room.ROOMIMAGE.url if room.ROOMIMAGE else None,
            'type_image': room.ROOMTYPE.ROOMTYPEIMAGE.url if room.ROOMTYPE and room.ROOMTYPE.ROOMTYPEIMAGE else None
        } for room in available_rooms]
        
        return JsonResponse({
            'success': True,
            'count': len(room_list),
            'rooms': room_list
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def get_notifications(request):
    """Get unread notifications for user"""
    try:
        username = request.GET.get('username')
        if not username:
            return JsonResponse({'error': 'Username required'}, status=400)
        
        notifications = Notification.objects.filter(
            username=username,
            is_read=False
        ).order_by('-created_at')[:10]
        
        notification_list = [{
            'id': n.id,
            'type': n.notification_type,
            'title': n.title,
            'message': n.message,
            'created_at': n.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for n in notifications]
        
        return JsonResponse({
            'success': True,
            'count': notifications.count(),
            'notifications': notification_list
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def mark_notification_read(request):
    """Mark notification as read"""
    try:
        data = json.loads(request.body)
        notification_id = data.get('notification_id')
        
        notification = Notification.objects.get(id=notification_id)
        notification.is_read = True
        notification.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
