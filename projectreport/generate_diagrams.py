"""Generate ER Diagram and DFD images using matplotlib (no graphviz binary needed)."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch
import os

OUTPUT_DIR = '/home/nikhil/roombookings3/roombookings/Hoteliers_Myproject/projectreport'

# Colors
HEADER_BG = '#4A90D9'
ENTITY_BG = '#E8F0FE'
REL_BG = '#FFF3CD'
STORE_BG = '#E2E3E5'
PROC_BG = '#CCE5FF'
EXT_BG = '#F8D7DA'
TEXT_COLOR = '#333333'

# ============================
# 1. ER DIAGRAM
# ============================
fig, ax = plt.subplots(1, 1, figsize=(20, 14))
ax.set_xlim(0, 20)
ax.set_ylim(0, 14)
ax.axis('off')
ax.set_title('Entity Relationship Diagram - Hotel Room Booking System', fontsize=16, fontweight='bold', pad=20)

def draw_entity(ax, x, y, w, h, name, attrs, color=ENTITY_BG):
    """Draw an entity box with attributes."""
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05", 
                          facecolor=color, edgecolor='#333', linewidth=1.5)
    ax.add_patch(box)
    # Header
    ax.text(x + w/2, y + h - 0.35, name, ha='center', va='center', fontsize=9, fontweight='bold', color='white',
            bbox=dict(boxstyle='round,pad=0.15', facecolor=HEADER_BG, edgecolor='none'))
    for i, attr in enumerate(attrs):
        ax.text(x + 0.15, y + h - 0.9 - i*0.35, attr, fontsize=7.5, color=TEXT_COLOR, va='top')

def draw_arrow(ax, x1, y1, x2, y2, label, style='arc3,rad=0.1'):
    """Draw a relationship arrow with label."""
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color='#555', lw=1.5, connectionstyle=style))
    mx, my = (x1 + x2)/2, (y1 + y2)/2 + 0.3
    ax.text(mx, my, label, ha='center', va='bottom', fontsize=7.5, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.1', facecolor='white', edgecolor='#ccc', alpha=0.8))

# Draw entities
draw_entity(ax, 1, 9.5, 3.5, 2.5, 'roomtypedb\n(Room Category)',
    ['id (PK)', 'ROOMTYPE', 'ROOMTYPEIMAGE', 'DESCRIPTION'])

draw_entity(ax, 1, 5.5, 4, 3.3, 'roomnamedb\n(Room)',
    ['id (PK)', 'ROOMTYPE (FK → roomtypedb)', 'ROOMNAME', 'ROOMIMAGE', 'ROOMPRICE', 'ROOMDESCRIPTION'])

draw_entity(ax, 6.5, 1, 3.5, 3.5, 'bookingdb\n(Booking)',
    ['id (PK)', 'CUSTOMER (FK→Registerdb)', 'CUSTOMERNAME', 'CONTACTEMAIL', 'CHECKIN', 'CHECKOUT',
     'TOTALADULTS', 'TOTALCHILDS', 'SELECTROOM (FK→roomnamedb)', 'SPECIALREQUEST', 'TOTALPRICE'], ENTITY_BG)

draw_entity(ax, 11, 2.5, 3.2, 2.5, 'Totaldb\n(Payment)',
    ['id (PK)', 'BOOKING (FK→bookingdb)', 'CUSTOMERNAME', 'MOBILE', 'TOTALPRICE'], ENTITY_BG)

draw_entity(ax, 6.5, 5.5, 3.5, 2, 'Registerdb\n(Customer)',
    ['id (PK)', 'USERNAME', 'PASSWORD', 'EMAIL'], ENTITY_BG)

draw_entity(ax, 6.5, 8.5, 3.5, 2.2, 'staffdb\n(Staff Profile)',
    ['id (PK)', 'STAFFNAME', 'DESIGNATION', 'FACEBOOKURL', 'INSTAGRAMURL', 'STAFFIMAGE'], ENTITY_BG)

draw_entity(ax, 15, 8.5, 3.5, 2, 'customercontactdb\n(Contact Enquiry)',
    ['id (PK)', 'CONTACTNAME', 'CONTACTNUMBER', 'CONTACTEMAIL', 'CONTACTSUBJECT', 'CONTACTMESSAGE'], ENTITY_BG)

draw_entity(ax, 11, 5.5, 3.5, 2, 'ChatbotResponse\n(Training Data)',
    ['id (PK)', 'keywords', 'response', 'query_type'], ENTITY_BG)

draw_entity(ax, 15, 5.5, 3.5, 2, 'ChatbotConversation\n(Conv. Log)',
    ['id (PK)', 'username', 'user_message', 'bot_response', 'query_type', 'created_at'], ENTITY_BG)

draw_entity(ax, 15, 2.5, 3.2, 2, 'Notification',
    ['id (PK)', 'username', 'message', 'is_read', 'created_at'], ENTITY_BG)

# Relationships - CORRECTED COORDINATES
# Arrow 1: roomtypedb (right edge x=4.5, y≈10.75) → roomnamedb (right edge x=5, y≈7.15)
draw_arrow(ax, 4.5, 10.75, 5, 7.15, '1:N', 'arc3,rad=0.2')
ax.text(5.8, 9.2, 'One Room Type\nhas many Rooms', ha='center', fontsize=7, color='#555')

# Arrow 2: Registerdb (right edge x=10, y≈6.5) → bookingdb (right edge x=10, y≈3.5)
draw_arrow(ax, 10, 6.5, 10, 3.5, '1:N')
ax.text(11.2, 5.2, 'One Customer makes\nmany Bookings (SET_NULL)', ha='left', fontsize=7, color='#555')

# Arrow 3: roomnamedb (right edge x=5, y≈7) → bookingdb (left edge x=6.5, y≈3.5)
draw_arrow(ax, 5, 7, 6.5, 3.5, '1:N', 'arc3,rad=0.15')
ax.text(4.8, 5.0, 'One Room appears in\nmany Bookings (CASCADE)', ha='center', fontsize=7, color='#555')

# Arrow 4: bookingdb (right edge x=10, y≈3.5) → Totaldb (left edge x=11, y≈4)
draw_arrow(ax, 10, 3.5, 11, 4, '1:1', 'arc3,rad=0.1')
ax.text(10.5, 4.5, 'One Booking has\none Payment (CASCADE)', ha='left', fontsize=7, color='#555')

plt.tight_layout()
er_path = os.path.join(OUTPUT_DIR, 'er_diagram.png')
plt.savefig(er_path, dpi=200, bbox_inches='tight')
plt.close()
print(f"ER Diagram saved: {er_path}")


# ============================
# 2. DFD - Context Diagram (Level 0)
# ============================
fig, ax = plt.subplots(1, 1, figsize=(14, 8))
ax.set_xlim(0, 14)
ax.set_ylim(0, 8)
ax.axis('off')
ax.set_title('Context Diagram (Level 0 DFD) - Hotel Room Booking System', fontsize=14, fontweight='bold', pad=15)

# Customer entity
box_cust = FancyBboxPatch((0.3, 3), 2.5, 2, boxstyle="round,pad=0.1", facecolor='#FFF3CD', edgecolor='#333', lw=2)
ax.add_patch(box_cust)
ax.text(1.55, 4, 'CUSTOMER', ha='center', va='center', fontsize=11, fontweight='bold')
ax.text(1.55, 3.5, '(External Entity)', ha='center', fontsize=8, color='#666')

# System box
box_sys = FancyBboxPatch((5, 2.5), 4, 3, boxstyle="round,pad=0.15", facecolor='#D1E7DD', edgecolor='#333', lw=2.5)
ax.add_patch(box_sys)
ax.text(7, 4.3, 'HOTEL ROOM', ha='center', va='center', fontsize=13, fontweight='bold')
ax.text(7, 3.8, 'BOOKING SYSTEM', ha='center', va='center', fontsize=13, fontweight='bold')
ax.text(7, 3.2, '(The System)', ha='center', fontsize=9, color='#555')

# Admin entity
box_adm = FancyBboxPatch((11.2, 3), 2.5, 2, boxstyle="round,pad=0.1", facecolor='#FFF3CD', edgecolor='#333', lw=2)
ax.add_patch(box_adm)
ax.text(12.45, 4, 'ADMINISTRATOR', ha='center', va='center', fontsize=10, fontweight='bold')
ax.text(12.45, 3.5, '(External Entity)', ha='center', fontsize=8, color='#666')

# Arrows - Customer to System
ax.annotate('', xy=(5, 4.5), xytext=(2.8, 4.5),
            arrowprops=dict(arrowstyle='->', color='#c0392b', lw=1.5))
ax.text(3.5, 5.2, 'Registration, Login,\nSearch, Booking, Payment,\nContact, Chatbot', ha='center', fontsize=7, color='#c0392b')

ax.annotate('', xy=(2.8, 3.5), xytext=(5, 3.5),
            arrowprops=dict(arrowstyle='->', color='#2980b9', lw=1.5))
ax.text(3.5, 2.3, 'Room Listings, Booking\nConfirmation, Payment Status,\nSearch Results, Chatbot\nResponses, Emails, PDF', ha='center', fontsize=7, color='#2980b9')

# Arrows - Admin to System
ax.annotate('', xy=(11.2, 4.5), xytext=(9, 4.5),
            arrowprops=dict(arrowstyle='->', color='#c0392b', lw=1.5))
ax.text(10.5, 5.2, 'Login, Room Type,\nRoom, Staff Data', ha='center', fontsize=7, color='#c0392b')

ax.annotate('', xy=(9, 3.5), xytext=(11.2, 3.5),
            arrowprops=dict(arrowstyle='->', color='#2980b9', lw=1.5))
ax.text(10.5, 2.3, 'Booking Records,\nPayment Records,\nContacts, Dashboard', ha='center', fontsize=7, color='#2980b9')

plt.tight_layout()
dfd0_path = os.path.join(OUTPUT_DIR, 'dfd_context.png')
plt.savefig(dfd0_path, dpi=200, bbox_inches='tight')
plt.close()
print(f"DFD Context Diagram saved: {dfd0_path}")


# ============================
# 3. DFD - Level 1
# ============================
fig, ax = plt.subplots(1, 1, figsize=(18, 12))
ax.set_xlim(0, 18)
ax.set_ylim(0, 12)
ax.axis('off')
ax.set_title('Level 1 Data Flow Diagram - Hotel Room Booking System', fontsize=14, fontweight='bold', pad=15)

def draw_process(ax, x, y, num, name, color=PROC_BG):
    circle = plt.Circle((x, y), 0.75, facecolor=color, edgecolor='#333', lw=1.5)
    ax.add_patch(circle)
    ax.text(x, y + 0.3, num, ha='center', va='center', fontsize=10, fontweight='bold')
    ax.text(x, y - 0.1, name, ha='center', va='center', fontsize=7.5)

def draw_store(ax, x, y, name, color=STORE_BG):
    cyl = FancyBboxPatch((x-0.8, y-0.5), 1.6, 1, boxstyle="round,pad=0.1",
                          facecolor=color, edgecolor='#333', lw=1.2)
    ax.add_patch(cyl)
    ax.text(x, y, name, ha='center', va='center', fontsize=7, fontweight='bold')

def draw_external(ax, x, y, name, color=EXT_BG):
    box = FancyBboxPatch((x-1.2, y-0.5), 2.4, 1.2, boxstyle="round,pad=0.05",
                          facecolor=color, edgecolor='#333', lw=1.5)
    ax.add_patch(box)
    ax.text(x, y, name, ha='center', va='center', fontsize=8, fontweight='bold')

def draw_flow(ax, x1, y1, x2, y2, label='', color='#555'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=1, connectionstyle='arc3,rad=0.15'))
    mx, my = (x1 + x2)/2, (y1 + y2)/2
    ax.text(mx, my + 0.15, label, ha='center', va='bottom', fontsize=6.5, color=color)

# External entities
draw_external(ax, 1, 10, 'CUSTOMER', '#FFF3CD')
draw_external(ax, 1, 2, 'ADMIN', '#FFF3CD')
draw_external(ax, 16, 8, 'Razorpay\nPayment Gateway', '#F8D7DA')
draw_external(ax, 16, 3, 'Gmail SMTP\nServer', '#F8D7DA')

# Processes (8 circles in a grid)
procs = [
    (4, 10, 'P1', 'User\nManagement'),
    (8, 10, 'P2', 'Room\nManagement'),
    (4, 7, 'P3', 'Search &\nFiltering'),
    (8, 7, 'P4', 'Booking\nEngine'),
    (6, 4, 'P5', 'Payment\nProcessing'),
    (10, 4, 'P6', 'Notification\nSystem'),
    (4, 4, 'P7', 'Chatbot\nEngine'),
    (8, 4, 'P8', 'Admin\nDashboard'),
]
for x, y, num, name in procs:
    draw_process(ax, x, y, num, name)

# Data stores (row at bottom)
stores = [
    (2, 1.5, 'D1\nroomtypedb'),
    (4, 1.5, 'D2\nroomnamedb'),
    (6, 1.5, 'D3\nstaffdb'),
    (8, 1.5, 'D4\nRegisterdb'),
    (10, 1.5, 'D5\nbookingdb'),
    (12, 1.5, 'D6\nTotaldb'),
    (2, 0.3, 'D7\ncontactdb'),
    (4, 0.3, 'D8\nChatbot\nResponse'),
    (6, 0.3, 'D9\nChatbot\nConv'),
    (8, 0.3, 'D10\nNotif'),
]
for x, y, name in stores:
    draw_store(ax, x, y, name)

# Flows from Customer
draw_flow(ax, 2.2, 9.5, 3.3, 9.5, 'Credentials')
draw_flow(ax, 2.2, 7.5, 3.3, 7.5, 'Search criteria')
draw_flow(ax, 2.2, 4.5, 3.3, 4.5, 'Chat queries')
draw_flow(ax, 1, 8.5, 4.5, 8.5, '')
ax.text(2.5, 8.3, 'Booking request', ha='center', fontsize=6.5)

# Flows to Customer
draw_flow(ax, 4.7, 9, 2.2, 9, 'Auth status', '#2980b9')
draw_flow(ax, 4.7, 6.5, 2.2, 6.5, 'Results', '#2980b9')
draw_flow(ax, 4.7, 3.5, 2.2, 3.5, 'Response', '#2980b9')
draw_flow(ax, 9.5, 5.5, 2.5, 8, '')
ax.text(6, 6.5, 'Confirmation/Email', ha='center', fontsize=6.5, color='#2980b9')

# Flows from Admin
draw_flow(ax, 2.2, 2.5, 7.3, 3.5, 'CRUD operations')
draw_flow(ax, 1, 1, 9, 1.5, '')
ax.text(5, 0.8, 'View Dashboard', ha='center', fontsize=6.5)

# To Admin
draw_flow(ax, 8.7, 3.5, 2.2, 2.5, 'Summary', '#2980b9')

# P1-P8 connections to stores
store_connections = [
    (3.5, 3.5, 2, 2, 'Read/Write'),
    (7.5, 3.5, 4, 2, 'Read/Write'),
    (7.5, 3.5, 6, 2, 'Read/Write'),
    (3.5, 8.5, 8, 2, 'Read/Write'),
    (5.5, 6.5, 10, 2, 'Write'),
    (5.5, 3.5, 12, 2, 'Write'),
    (9.5, 6.5, 10, 2, 'Read/Write'),
    (3.5, 4.5, 4, 1.5, 'Read'),
    (3.5, 4.5, 6, 1.5, 'Write'),
    (9.5, 4.5, 8, 1.5, 'Read'),
]
for sx, sy, dx, dy, label in store_connections:
    c = '#8B4513'
    ax.annotate('', xy=(dx, dy), xytext=(sx, sy),
                arrowprops=dict(arrowstyle='->', color=c, lw=0.8, connectionstyle='arc3,rad=0.1'))
    ax.text((sx+dx)/2, (sy+dy)/2 + 0.1, label, ha='center', fontsize=6, color=c)

# P5 to Razorpay
draw_flow(ax, 6.8, 4, 15, 7.5, 'Order/Payment')
draw_flow(ax, 15, 8.5, 6.8, 4.5, 'Verification', '#2980b9')

# P6 to SMTP
draw_flow(ax, 10.7, 4, 15, 3.5, 'Send email')

plt.tight_layout()
dfd1_path = os.path.join(OUTPUT_DIR, 'dfd_level1.png')
plt.savefig(dfd1_path, dpi=200, bbox_inches='tight')
plt.close()
print(f"DFD Level 1 Diagram saved: {dfd1_path}")

print("\nAll diagrams generated successfully!")
