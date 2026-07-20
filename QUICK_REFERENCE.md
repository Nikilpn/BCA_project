# 🎯 Quick Reference Card - Chatbot & Search Features

## 🚀 Quick Start

| Action | URL/Location |
|--------|--------------|
| **Homepage** | `http://127.0.0.1:8000/` |
| **Advanced Search** | `http://127.0.0.1:8000/advanced_search/` |
| **Admin Panel** | `http://127.0.0.1:8000/admin/` |

---

## 💬 Chatbot Commands to Try

### Room Queries
```
"Show me luxury rooms"
"What's the price?"
"Are there available rooms?"
"Show me deluxe suites"
"What room types do you have?"
```

### Staff Queries
```
"Tell me about your team"
"Show me your staff"
"Who works here?"
```

### Booking Queries
```
"How do I book?"
"What's check-in time?"
"Can I cancel?"
"What's the cancellation policy?"
```

### General
```
"Hello"
"Hi there"
"Help me"
"Contact you"
```

---

## 🔍 Advanced Search Usage

| Filter | Example |
|--------|---------|
| **Room Name** | "Deluxe Room A" |
| **Room Type** | Select from dropdown |
| **Min Price** | 2000 |
| **Max Price** | 5000 |
| **Check-in** | 2024-02-15 |
| **Check-out** | 2024-02-20 |

**Tip:** Combine filters for best results!

---

## 🔧 Admin Tasks

### Manage Chatbot Responses
```
Admin → Backend → Chatbot Responses
→ Add keywords and responses
→ Enable/disable responses
```

### View Conversations
```
Admin → Backend → Chatbot Conversations
→ See all user queries
→ Check ratings
```

### Send Notifications
```
Admin → Backend → Notifications
→ Create new notification
→ Select user and type
```

---

## 📊 API Endpoints for Developers

### Send Chatbot Query
```bash
curl -X POST http://localhost:8000/Backend/api/chatbot/query/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Show me luxury rooms",
    "username": "guest_user"
  }'
```

### Search Rooms
```bash
curl "http://localhost:8000/Backend/api/search/rooms/?name=Deluxe&min_price=2000&max_price=5000"
```

### Get Notifications
```bash
curl "http://localhost:8000/Backend/api/notifications/?username=john_doe"
```

---

## 🎨 Customization Quick Tips

### Change Chatbot Colors
Edit in `Backend/templates/chatbot_widget.html`:
```css
/* Change primary color */
background: linear-gradient(135deg, #YOUR_COLOR_1 0%, #YOUR_COLOR_2 100%);
```

### Change Room Type Options
Edit `webapp/templates/14advanced_room_search.html`:
```html
<option value="1">Your Room Type</option>
```

---

## 🐛 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Chatbot button not visible | Hard refresh (Ctrl+Shift+R) |
| Search returns no results | Add rooms in admin first |
| API returns 404 | Verify URL paths in urls.py |
| Static files not loading | Run `python manage.py collectstatic` |

---

## 📋 Feature Checklist

### Chatbot
- [ ] Widget appears on homepage
- [ ] Can type messages
- [ ] Gets responses
- [ ] Shows suggestions
- [ ] Can rate responses
- [ ] Mobile-friendly

### Search
- [ ] Can filter by name
- [ ] Can filter by type
- [ ] Can filter by price
- [ ] Can filter by dates
- [ ] Shows results
- [ ] Book buttons work
- [ ] Reset works
- [ ] Mobile-friendly

### Admin
- [ ] Can create responses
- [ ] Can view conversations
- [ ] Can send notifications
- [ ] Search/filter works

---

## 📞 Documentation Files

| File | Purpose |
|------|---------|
| `CHATBOT_SEARCH_DOCUMENTATION.md` | Complete API docs |
| `TESTING_GUIDE.md` | Testing procedures |
| `IMPLEMENTATION_SUMMARY.md` | Overview & features |
| `README.md` | General project info |

---

## 🎯 Performance Tips

1. **Cache common responses** - In admin, use popular keywords
2. **Index database** - Done automatically on model creation
3. **Minimize API calls** - Use combined filters in search
4. **Clear browser cache** - For CSS/JS updates
5. **Monitor conversations** - Track in admin for improvements

---

## 🔐 Security Reminders

- ✅ Always use HTTPS in production
- ✅ Keep SECRET_KEY in .env file
- ✅ Don't expose database credentials
- ✅ Use CSRF tokens (automatic)
- ✅ Validate user input (automatic)
- ✅ Rate limit API endpoints (configure if needed)

---

## 📱 Mobile Testing

**Responsive breakpoints:**
- Desktop: 1200px+ ✅
- Tablet: 768px-1199px ✅
- Mobile: < 768px ✅

**Test on:**
- iPhone/iPad
- Android devices
- Chrome DevTools mobile view

---

## 🚀 Deployment Checklist

Before deploying to production:

- [ ] Set `DEBUG = False` in .env
- [ ] Update `ALLOWED_HOSTS` in settings
- [ ] Run migrations: `python manage.py migrate`
- [ ] Collect static files: `python manage.py collectstatic --noinput`
- [ ] Create superuser: `python manage.py createsuperuser`
- [ ] Test API endpoints
- [ ] Enable HTTPS
- [ ] Set up proper logging
- [ ] Configure email backend
- [ ] Backup database

---

## 💡 Pro Tips

1. **Bulk create notifications**: Use Django shell for batch operations
2. **Export data**: Use admin export features or Django dumpdata
3. **Monitor performance**: Check response times in Django debug toolbar
4. **User analytics**: Track chatbot usage in ChatbotConversation model
5. **A/B testing**: Test different chatbot responses via admin

---

## 📚 Learning Path

1. **First**: Read `IMPLEMENTATION_SUMMARY.md`
2. **Then**: Try basic chatbot on homepage
3. **Next**: Test advanced search with filters
4. **Later**: Explore admin panel
5. **Finally**: Read `CHATBOT_SEARCH_DOCUMENTATION.md` for deep dive

---

## 🎓 Resources

- Django Docs: https://docs.djangoproject.com/en/6.0/
- Bootstrap Docs: https://getbootstrap.com/docs/5.3/
- JavaScript Fetch API: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
- SQLite Docs: https://www.sqlite.org/docs.html

---

## 📞 Support

For issues:
1. Check `TESTING_GUIDE.md` Troubleshooting section
2. Review Django logs: `python manage.py runserver --verbosity 2`
3. Check browser console for JS errors
4. Verify database: `python manage.py dbshell`

---

## 🎉 Ready to Go!

Your hotel booking system now has:
✅ Intelligent Chatbot
✅ Advanced Search
✅ Notifications
✅ Admin Dashboard
✅ Mobile Support

**Deploy and enjoy! 🚀**

---

*Last Updated: January 15, 2026*
*Version: 1.0*
*Status: Production Ready ✅*
