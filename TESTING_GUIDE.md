# Quick Start Guide - Testing Chatbot & Search Features

## 🚀 Getting Started

### 1. Start the Django Server
```bash
cd /home/nikhil/roombookings/Hoteliers_Myproject
python manage.py runserver
```

Open browser: `http://127.0.0.1:8000/`

---

## 💬 Testing the Chatbot

### Step 1: Access Chatbot Widget
- Visit the homepage
- Look for the purple chatbot button (💬) in the bottom-right corner
- Click to open the chat interface

### Step 2: Test Different Queries

#### Room Queries:
```
- "Show me luxury rooms"
- "What's the price of your rooms?"
- "Do you have available rooms?"
- "Show me deluxe suites"
```

#### Staff Queries:
```
- "Tell me about your team"
- "Who works here?"
- "Show me your staff"
```

#### Booking Queries:
```
- "How do I make a booking?"
- "What's the check-in time?"
- "Can I cancel my booking?"
```

#### General Queries:
```
- "Hello"
- "Hi there"
- "Help"
- "Contact us"
```

### Step 3: Test Features
- ✅ Click suggested action buttons
- ✅ View room cards with images
- ✅ Rate responses (1-5 stars)
- ✅ Check message timestamps

---

## 🔍 Testing Advanced Room Search

### Step 1: Access Search Page
- Click "🔍 Smart Search" in navigation menu
- Or go to: `http://127.0.0.1:8000/advanced_search/`

### Step 2: Test Filters Individually

#### Test Room Name Filter:
1. Enter "Deluxe" in Room Name field
2. Click "Search Rooms"
3. Should show rooms with "Deluxe" in name

#### Test Room Type Filter:
1. Select a Room Type from dropdown
2. Click "Search Rooms"
3. Should show only rooms of that type

#### Test Price Range Filter:
1. Set Min Price: 2000
2. Set Max Price: 5000
3. Click "Search Rooms"
4. Results should fall within range

#### Test Date Range Filter:
1. Set Check-in: 2024-02-15
2. Set Check-out: 2024-02-20
3. Click "Search Rooms"
4. Should show only available rooms

### Step 3: Test Combined Filters
1. Select Room Type: Luxury
2. Set Price Range: 3000-6000
3. Set Check-in/out dates
4. Click "Search Rooms"
5. Should show results matching ALL criteria

### Step 4: Test Other Features
- ✅ Click "Reset Filters" to clear all
- ✅ Click "Book Now" on any room
- ✅ Check active filter display
- ✅ Test on mobile screen

---

## 🔔 Testing Notifications (Admin)

### Step 1: Create Notification in Admin
1. Go to: `http://127.0.0.1:8000/admin/`
2. Login with superuser credentials
3. Navigate to Backend → Notifications
4. Click "Add Notification"
5. Fill in details:
   - Username: (your username)
   - Notification Type: "booking"
   - Title: "Your booking is confirmed"
   - Message: "Room 101 reserved"
6. Click Save

### Step 2: Check Notification Badge
1. Open chatbot
2. Should see notification count badge
3. Notification appears in list

---

## 📊 Testing Admin Panel

### 1. Access Admin Panel
- URL: `http://127.0.0.1:8000/admin/`
- Login with superuser account

### 2. Manage Chatbot Responses
- Backend → Chatbot Responses
- Create new response with keywords
- Test by asking chatbot those keywords

### 3. View Chatbot Conversations
- Backend → Chatbot Conversations
- See all user messages and bot responses
- Check user ratings

### 4. Manage Notifications
- Backend → Notifications
- Create/edit/delete notifications
- Filter by type or read status

---

## 🐛 Troubleshooting

### Issue: Chatbot button not visible
**Solution:**
```bash
# Clear cache and hard refresh
python manage.py collectstatic --clear --noinput
# Restart server
```

### Issue: Search returns no results
**Solution:**
1. Verify rooms exist: Admin → Backend → Room Names
2. Check room prices are set
3. Try without date filters first

### Issue: API returns 404 error
**Solution:**
- Verify URLs are registered in `Backend/urls.py`
- Check endpoint paths match the code
- Restart Django server

### Issue: Static files not loading
**Solution:**
```bash
python manage.py collectstatic --noinput
```

---

## 📝 API Testing with cURL

### Test Chatbot API
```bash
curl -X POST http://127.0.0.1:8000/Backend/api/chatbot/query/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Show me luxury rooms",
    "username": "testuser"
  }'
```

### Test Search API
```bash
curl "http://127.0.0.1:8000/Backend/api/search/rooms/?name=Deluxe&min_price=2000&max_price=5000"
```

### Test Notifications API
```bash
curl "http://127.0.0.1:8000/Backend/api/notifications/?username=testuser"
```

---

## ✨ Features Checklist

### Chatbot Features:
- [ ] Widget appears on all pages
- [ ] Can type and send messages
- [ ] Gets intelligent responses
- [ ] Shows suggested actions
- [ ] Displays room cards
- [ ] Allows rating responses
- [ ] Shows notification badge
- [ ] Works on mobile

### Search Features:
- [ ] Filter by room name
- [ ] Filter by room type
- [ ] Filter by price range
- [ ] Filter by availability dates
- [ ] Show active filters
- [ ] Displays room cards
- [ ] Book Now buttons work
- [ ] Reset filters works
- [ ] Responsive design works

### Admin Features:
- [ ] Can create chatbot responses
- [ ] Can view conversations
- [ ] Can manage notifications
- [ ] Can edit notifications
- [ ] Can delete notifications
- [ ] Search functions work
- [ ] Filtering works

---

## 📚 Documentation References

For detailed API documentation, see: `CHATBOT_SEARCH_DOCUMENTATION.md`

---

## 🎯 Performance Notes

- Chatbot responses cached for better performance
- Search uses database indexes for speed
- Notifications use efficient queries
- Mobile optimized for fast loading

---

## 💡 Tips

1. **For Testing**: Use "Super User" admin account
2. **Bulk Room Data**: Add multiple rooms in admin for better search testing
3. **Date Testing**: Use future dates for availability testing
4. **Cache Clear**: Use `CTRL+SHIFT+R` for hard refresh

---

## 📞 Support

If you encounter any issues:
1. Check the Troubleshooting section
2. Review documentation
3. Check Django logs: `python manage.py runserver --verbosity 2`
4. Verify database migrations: `python manage.py migrate`
