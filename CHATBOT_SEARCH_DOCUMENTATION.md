# Hotel Booking System - Chatbot & Advanced Search Features

## Overview
This document describes the new chatbot and advanced room search features added to the hotel booking system.

## New Features

### 1. **AI-Powered Chatbot Assistant** 💬
An intelligent chatbot that helps users by answering queries about:
- **Room Information**: Details, pricing, availability, and types
- **Staff & Services**: Team information and available services
- **Bookings**: Reservation policies, check-in/out times, cancellations
- **General Questions**: Hotel information and FAQs

#### Features:
- Real-time messaging interface (fixed widget on bottom-right)
- Intelligent query classification (room/staff/booking/general)
- Suggested quick actions
- Room cards with image and pricing
- Conversation history tracking
- User ratings for responses
- Notification badges

#### Accessing the Chatbot:
- The chatbot appears as a floating button (💬) on every page
- Click to open the chat interface
- Type your question or click suggested actions
- Rate helpful responses to improve the chatbot

### 2. **Advanced Room Search** 🔍
A comprehensive search interface with multiple filtering options to find the perfect room.

#### Search Filters:
1. **Room Name**: Search by specific room names
2. **Room Type**: Filter by luxury, deluxe, standard, budget
3. **Price Range**: Set minimum and maximum price per night
4. **Availability Dates**: Check-in and check-out dates for real availability

#### Features:
- Real-time filtering with AJAX
- Responsive grid layout
- Quick booking buttons
- No results handling with suggestions
- Active filter display
- Loading indicators
- Mobile-optimized interface

#### Accessing Advanced Search:
- Click "🔍 Smart Search" in the navigation menu
- Or visit: `/advanced_search/`
- Use filters to narrow down results
- Click "Book Now" on any room to proceed with booking

### 3. **Notification System** 🔔
Real-time notifications for users about:
- Booking confirmations
- Booking cancellations
- Room availability changes
- Price drops
- System alerts

#### Features:
- Unread notification badge
- Notification history
- Mark as read functionality
- Automatic cleanup of old notifications

## Models & Database

### New Models:

#### **ChatbotResponse**
```python
- query_type: Type of query (room, staff, booking, general)
- keyword: Keywords to match
- response: Bot's response text
- is_active: Enable/disable response
- created_at: Creation timestamp
```

#### **ChatbotConversation**
```python
- username: User who initiated chat
- user_message: User's question
- bot_response: Bot's response
- query_type: Classified query type
- rating: User rating (1-5)
- created_at: Timestamp
```

#### **Notification**
```python
- username: Target user
- notification_type: Type of notification
- title: Notification title
- message: Notification message
- is_read: Read status
- related_object_id: Related room/booking ID
- related_object_type: Type of related object
- created_at: Timestamp
```

## API Endpoints

### Chatbot APIs:

#### **POST** `/Backend/api/chatbot/query/`
Send a message to the chatbot
```json
Request:
{
    "message": "Show me luxury rooms",
    "username": "john_doe"
}

Response:
{
    "response": "Here are our luxury rooms...",
    "query_type": "room",
    "suggestions": ["View details", "Check availability"],
    "data": [...]
}
```

#### **POST** `/Backend/api/chatbot/rate/`
Rate a chatbot response
```json
Request:
{
    "conversation_id": 123,
    "rating": 5
}

Response:
{
    "success": true,
    "message": "Thank you for your feedback!"
}
```

### Search APIs:

#### **GET** `/Backend/api/search/rooms/`
Search and filter rooms
```
Parameters:
- name: Room name (optional)
- room_type: Room type ID (optional)
- min_price: Minimum price (optional)
- max_price: Maximum price (optional)
- check_in: Check-in date YYYY-MM-DD (optional)
- check_out: Check-out date YYYY-MM-DD (optional)

Response:
{
    "success": true,
    "count": 5,
    "rooms": [
        {
            "id": 1,
            "name": "Deluxe Suite",
            "type": "Luxury",
            "price": 5000,
            "description": "...",
            "image": "/media/...",
            "type_image": "/media/..."
        }
    ]
}
```

### Notification APIs:

#### **GET** `/Backend/api/notifications/?username=john_doe`
Get unread notifications
```
Response:
{
    "success": true,
    "count": 3,
    "notifications": [
        {
            "id": 1,
            "type": "booking",
            "title": "Booking Confirmed",
            "message": "Your booking for room 101 is confirmed",
            "created_at": "2024-01-15 14:30:00"
        }
    ]
}
```

#### **POST** `/Backend/api/notifications/mark-read/`
Mark notification as read
```json
Request:
{
    "notification_id": 1
}

Response:
{
    "success": true
}
```

## Admin Panel Management

Access the Django admin panel to manage chatbot and notification features:

### **Chatbot Responses Management**
- Location: Django Admin → Backend → Chatbot Responses
- Create, edit, and delete predefined responses
- Manage keywords for better matching
- Enable/disable specific responses

### **Chatbot Conversations**
- Location: Django Admin → Backend → Chatbot Conversations
- View conversation history
- Track user ratings
- Identify common queries for improvement

### **Notifications**
- Location: Django Admin → Backend → Notifications
- View all notifications
- Filter by type and read status
- Manually send notifications to users
- Track notification engagement

## Usage Examples

### Example 1: Customer searching for budget rooms
1. Click "🔍 Smart Search" in navigation
2. Set Price Range: Min: 1000, Max: 2500
3. Click "Search Rooms"
4. Browse results and click "Book Now"

### Example 2: Asking chatbot about luxury rooms
1. Click the chatbot button (💬)
2. Type: "Show me luxury rooms"
3. Chatbot displays matching rooms
4. Click on room card to view details

### Example 3: Checking room availability
1. Go to Advanced Search
2. Select Check-in: 2024-02-01
3. Select Check-out: 2024-02-05
4. Available rooms are automatically filtered

## Technical Implementation

### Frontend Technologies:
- HTML5 for semantic markup
- CSS3 for responsive styling with gradients and animations
- JavaScript (Vanilla) for interactivity and AJAX calls
- Bootstrap for grid layout

### Backend Technologies:
- Django ORM for database operations
- Django REST framework patterns for API design
- Python for query logic and filtering
- SQLite database

### Key Features:
- Responsive design (mobile-first)
- Progressive enhancement
- CSRF protection on POST requests
- Error handling and user feedback
- Accessibility features (ARIA labels)
- Performance optimized (lazy loading, pagination ready)

## Future Enhancements

1. **AI Integration**: Integrate with OpenAI/GPT for more intelligent responses
2. **Multi-language Support**: Add language selection for international guests
3. **Voice Chatbot**: Speech-to-text and text-to-speech capabilities
4. **Recommendation Engine**: ML-based room recommendations
5. **Real-time Chat**: WebSocket for instant notifications
6. **Analytics Dashboard**: Track chatbot performance and user behavior
7. **Calendar Integration**: Visual availability calendar
8. **Payment Integration**: Direct payment from search results

## Troubleshooting

### Chatbot not appearing?
- Clear browser cache
- Check if templates include the chatbot widget
- Verify static files are served correctly

### Search not returning results?
- Check that room data exists in database
- Verify room type IDs in filters
- Check date ranges for availability conflicts

### Notifications not showing?
- Ensure username is correct
- Check if notifications are created in database
- Verify user is logged in

## Database Maintenance

### Backup Chatbot Data:
```bash
python manage.py dumpdata Backend.ChatbotConversation > chatbot_conversations.json
python manage.py dumpdata Backend.ChatbotResponse > chatbot_responses.json
```

### Clear Old Conversations:
```bash
python manage.py shell
from Backend.models import ChatbotConversation
from datetime import datetime, timedelta
old_conversations = ChatbotConversation.objects.filter(
    created_at__lt=datetime.now() - timedelta(days=90)
)
old_conversations.delete()
```

## Performance Tips

1. Index frequently searched fields
2. Cache common chatbot responses
3. Paginate search results for large datasets
4. Use query optimization (select_related, prefetch_related)
5. Implement search result caching

## Support

For issues or feature requests, please contact the development team.
