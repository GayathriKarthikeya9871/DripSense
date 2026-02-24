import streamlit as st
import pandas as pd
import time
import datetime
import random
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# Set page configuration
st.set_page_config(
    page_title="Water Leakage Detection System",
    page_icon="💧",
    layout="wide"
)

# Define custom CSS for the water theme
def apply_custom_css():
    st.markdown("""
    <style>
        .main {
            background: linear-gradient(135deg, #001a33, #000000);
            color: white;
        }
        .stButton>button {
            background-color: #0066cc;
            color: white;
            border-radius: 5px;
            padding: 8px 16px;
            border: none;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            background-color: #004c99;
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .flat-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
            gap: 10px;
            padding: 10px;
        }
        .flat-card {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 80px;
            border-radius: 5px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .flat-card:hover {
            transform: scale(1.05);
        }
        .flat-green {
            background-color: #28a745;
            color: white;
        }
        .flat-red {
            background-color: #dc3545;
            color: white;
            animation: pulse 1.5s infinite;
        }
        .flat-yellow {
            background-color: #ffc107;
            color: black;
        }
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.7; }
            100% { opacity: 1; }
        }
        .login-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 20px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            backdrop-filter: blur(5px);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        }
        .notification {
            padding: 10px 15px;
            border-radius: 5px;
            margin-bottom: 10px;
            background-color: #004080;
            color: white;
            animation: fadeIn 0.5s;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .history-item {
            background: rgba(255, 255, 255, 0.1);
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 5px;
        }
        .logout-btn {
            position: absolute;
            top: 10px;
            right: 10px;
        }
        .section-title {
            color: #4da6ff;
            border-bottom: 1px solid #4da6ff;
            padding-bottom: 5px;
            margin-bottom: 15px;
        }
        .tabs-custom .stTabs [data-baseweb=tab-list] {
            background-color: rgba(0, 25, 50, 0.3);
            border-radius: 5px;
        }
        .tabs-custom .stTabs [data-baseweb=tab] {
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state variables
def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'flats_status' not in st.session_state:
        # Initialize all flats as green (normal)
        blocks = ['A', 'B', 'C']
        floors = [1, 2, 3, 4, 5]
        units = list(range(1, 21))
        
        st.session_state.flats_status = {}
        for block in blocks:
            for floor in floors:
                for unit in units:
                    flat_id = f"{block}{floor}{unit:02d}" if unit < 10 else f"{block}{floor}{unit}"
                    st.session_state.flats_status[flat_id] = {
                        'status': 'green',  # green, red, yellow
                        'room': None,
                        'timestamp': None,
                        'maintenance_start': None,
                        'maintenance_end': None,
                        'flow_data': generate_normal_flow_data(),
                        'room_data': {
                            'hall': generate_normal_flow_data(),
                            'kitchen': generate_normal_flow_data(),
                            'balcony': generate_normal_flow_data(),
                            'bedroom': generate_normal_flow_data(),
                            'bathroom': generate_normal_flow_data()
                        }
                    }
    
    if 'notifications' not in st.session_state:
        st.session_state.notifications = []
        
    if 'maintenance_history' not in st.session_state:
        st.session_state.maintenance_history = []
        
    if 'selected_flat' not in st.session_state:
        st.session_state.selected_flat = None
        
    if 'selected_room' not in st.session_state:
        st.session_state.selected_room = None
        
    if 'show_popup' not in st.session_state:
        st.session_state.show_popup = False
        
    if 'popup_message' not in st.session_state:
        st.session_state.popup_message = ""
        
    if 'last_leak_time' not in st.session_state:
        st.session_state.last_leak_time = datetime.now() - timedelta(minutes=5)
        
    if 'app_start_time' not in st.session_state:
        st.session_state.app_start_time = datetime.now()
        
    if 'leak_simulation_active' not in st.session_state:
        st.session_state.leak_simulation_active = True
    
    if 'last_graph_update' not in st.session_state:
        st.session_state.last_graph_update = datetime.now()

# Generate user data - Residents are flat numbers
def get_user_data():
    user_data = {
        'maintenance': {
            'maintenance1': 'pass1',
            'maintenance2': 'pass2',
            'maintenance3': 'pass3'
        },
        'resident': {},
        'admin': {
            'admin': 'admin123'
        }
    }
    
    # Generate resident users - flat numbers as usernames
    blocks = ['A', 'B', 'C']
    floors = [1, 2, 3, 4, 5]
    units = list(range(1, 21))
    
    for block in blocks:
        for floor in floors:
            for unit in units:
                flat_id = f"{block}{floor}{unit:02d}" if unit < 10 else f"{block}{floor}{unit}"
                user_data['resident'][flat_id] = f"pass{flat_id}"
    
    return user_data

# Generate sample flow data for graphs
def generate_normal_flow_data():
    now = datetime.now()
    timestamps = [(now - timedelta(minutes=i*2)).strftime('%H:%M:%S') for i in range(30, 0, -1)]
    flow_values = [random.uniform(40, 50) for _ in range(30)]
    return {'timestamps': timestamps, 'values': flow_values}

def generate_leak_flow_data():
    now = datetime.now()
    timestamps = [(now - timedelta(minutes=i*2)).strftime('%H:%M:%S') for i in range(30, 0, -1)]
    # Normal flow initially, then sudden increase for leak
    flow_values = [random.uniform(40, 50) for _ in range(15)] + [random.uniform(70, 85) for _ in range(15)]
    return {'timestamps': timestamps, 'values': flow_values}

def generate_decreasing_flow_data():
    now = datetime.now()
    timestamps = [(now - timedelta(minutes=i*2)).strftime('%H:%M:%S') for i in range(30, 0, -1)]
    # High values for leak then decreasing
    flow_values = [random.uniform(70, 85) for _ in range(10)] + \
                 [random.uniform(60, 70) for _ in range(10)] + \
                 [random.uniform(40, 50) for _ in range(10)]
    return {'timestamps': timestamps, 'values': flow_values}

# Update flow data for all flats
def update_flow_data():
    now = datetime.now()
    
    # Update every 15 seconds
    if (now - st.session_state.last_graph_update).total_seconds() >= 15:
        st.session_state.last_graph_update = now
        
        # Update all flats
        for flat_id, flat_data in st.session_state.flats_status.items():
            status = flat_data['status']
            
            # Update main flow data
            timestamps = flat_data['flow_data']['timestamps']
            values = flat_data['flow_data']['values']
            
            # Add new data point
            new_time = now.strftime('%H:%M:%S')
            
            if status == 'green':
                new_value = random.uniform(40, 50)
            elif status == 'red':
                new_value = random.uniform(70, 85)
            else:  # yellow (maintenance)
                new_value = random.uniform(50, 60)
            
            # Add new data and remove oldest
            timestamps.append(new_time)
            timestamps.pop(0)
            values.append(new_value)
            values.pop(0)
            
            # Update room data
            for room, room_data in flat_data['room_data'].items():
                room_status = 'red' if room == flat_data['room'] and status != 'green' else 'green'
                
                room_timestamps = room_data['timestamps']
                room_values = room_data['values']
                
                # Add new data point for room
                if room_status == 'green':
                    room_new_value = random.uniform(40, 50)
                elif room_status == 'red':
                    room_new_value = random.uniform(70, 85)
                else:  # maintenance
                    room_new_value = random.uniform(50, 60)
                
                # Add new data and remove oldest
                room_timestamps.append(new_time)
                room_timestamps.pop(0)
                room_values.append(room_new_value)
                room_values.pop(0)

# Function to login
def login(username, password, role):
    user_data = get_user_data()
    if role in user_data and username in user_data[role]:
        if user_data[role][username] == password:
            st.session_state.logged_in = True
            st.session_state.user_role = role
            st.session_state.username = username
            # Reset logout clicked state when a new user logs in
            st.session_state.logout_clicked = False
            return True
    return False
    
# Function to logout
def logout():
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.username = None
    st.session_state.selected_flat = None
    st.session_state.selected_room = None
    # Reset logout clicked state when user logs out
    st.session_state.logout_clicked = False

# Function to simulate leak for n random flats
def simulate_leak(n=2):
    blocks = ['A', 'B', 'C']
    floors = [1, 2, 3, 4, 5]
    units = list(range(1, 21))
    rooms = ['hall', 'kitchen', 'balcony', 'bedroom', 'bathroom']
    
    # Get all green flats
    green_flats = []
    for flat_id, data in st.session_state.flats_status.items():
        if data['status'] == 'green':
            green_flats.append(flat_id)
    
    # Randomly select n flats (or fewer if not enough green flats)
    n = min(n, len(green_flats))
    if n == 0:
        return  # No green flats available
    
    selected_flats = random.sample(green_flats, n)
    
    for flat_id in selected_flats:
        affected_room = random.choice(rooms)
        st.session_state.flats_status[flat_id]['status'] = 'red'
        st.session_state.flats_status[flat_id]['room'] = affected_room
        st.session_state.flats_status[flat_id]['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.flats_status[flat_id]['flow_data'] = generate_leak_flow_data()
        st.session_state.flats_status[flat_id]['room_data'][affected_room] = generate_leak_flow_data()
        
        # Add notification
        notification = f"🚨 ALERT: Water leakage detected in flat {flat_id}, {affected_room} at {st.session_state.flats_status[flat_id]['timestamp']}"
        st.session_state.notifications.insert(0, notification)
    
    # Update last leak time
    st.session_state.last_leak_time = datetime.now()
    
    # Show popup for the first leak
    if selected_flats:
        first_flat = selected_flats[0]
        first_room = st.session_state.flats_status[first_flat]['room']
        st.session_state.show_popup = True
        st.session_state.popup_message = f"🚨 ALERT: Water leakage detected in flat {first_flat}, {first_room} at {st.session_state.flats_status[first_flat]['timestamp']}"

# Function to check if it's time to simulate leaks
def check_leak_simulation():
    now = datetime.now()
    
    # Wait 20 seconds after app start before first leak
    if (now - st.session_state.app_start_time).total_seconds() < 20:
        return
    
    # Check if it's been 3 minutes since last leak
    if (now - st.session_state.last_leak_time).total_seconds() >= 180:  # 3 minutes
        # Simulate leak for 1-3 random flats
        n = random.randint(1, 3)
        simulate_leak(n)
        st.rerun()

# Function to start maintenance
def start_maintenance(flat_id):
    if st.session_state.flats_status[flat_id]['status'] == 'red':
        st.session_state.flats_status[flat_id]['status'] = 'yellow'
        st.session_state.flats_status[flat_id]['maintenance_start'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Add notification
        room = st.session_state.flats_status[flat_id]['room']
        notification = f"🔧 MAINTENANCE: Work started in flat {flat_id}, {room} at {st.session_state.flats_status[flat_id]['maintenance_start']}"
        st.session_state.notifications.insert(0, notification)
        st.session_state.show_popup = True
        st.session_state.popup_message = notification

# Function to complete maintenance
def complete_maintenance(flat_id):
    if st.session_state.flats_status[flat_id]['status'] == 'yellow':
        st.session_state.flats_status[flat_id]['status'] = 'green'
        st.session_state.flats_status[flat_id]['maintenance_end'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Update flow data
        st.session_state.flats_status[flat_id]['flow_data'] = generate_decreasing_flow_data()
        room = st.session_state.flats_status[flat_id]['room']
        st.session_state.flats_status[flat_id]['room_data'][room] = generate_decreasing_flow_data()
        
        # Add to history
        history_entry = {
            'flat_id': flat_id,
            'room': st.session_state.flats_status[flat_id]['room'],
            'detected': st.session_state.flats_status[flat_id]['timestamp'],
            'started': st.session_state.flats_status[flat_id]['maintenance_start'],
            'completed': st.session_state.flats_status[flat_id]['maintenance_end']
        }
        st.session_state.maintenance_history.insert(0, history_entry)
        
        # Add notification
        notification = f"✅ COMPLETED: Maintenance work completed in flat {flat_id}, {room} at {st.session_state.flats_status[flat_id]['maintenance_end']}"
        st.session_state.notifications.insert(0, notification)
        st.session_state.show_popup = True
        st.session_state.popup_message = notification
        
        # Reset room info
        st.session_state.flats_status[flat_id]['room'] = None

# Display flow graph
def display_flow_graph(flow_data, title):
    fig = px.line(
        x=flow_data['timestamps'], 
        y=flow_data['values'],
        labels={'x': 'Time', 'y': 'Water Flow Rate (L/min)'},
        title=title
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    )
    
    # Add threshold lines
    fig.add_hline(y=60, line_dash="dash", line_color="yellow", annotation_text="Warning Level", annotation_position="top right")
    fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Leak Level", annotation_position="top right")
    
    st.plotly_chart(fig, use_container_width=True)

# Display flat grid for a specific block
def display_block_grid(block):
    st.markdown(f"<h3 class='section-title'>Block {block}</h3>", unsafe_allow_html=True)
    
    # For residents, only show their flat
    user_flat = None
    if st.session_state.user_role == 'resident':
        user_flat = st.session_state.username
    
    # Create grid layout for floors
    for floor in range(5, 0, -1):
        cols = st.columns(20)
        for unit in range(1, 21):
            flat_id = f"{block}{floor}{unit:02d}" if unit < 10 else f"{block}{floor}{unit}"
            
            # Skip if resident and not their flat
            if user_flat and flat_id != user_flat:
                continue
                
            status = st.session_state.flats_status[flat_id]['status']
            
            with cols[unit-1]:
                status_class = f"flat-card flat-{status}"
                st.markdown(
                    f"""
                    <div class='{status_class}' onclick='handleFlatClick("{flat_id}")'>
                        {flat_id}
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
                # Since the onclick in HTML won't work directly with Streamlit,
                # we'll use a button as a workaround
                if st.button(f"View {flat_id}", key=f"btn_{flat_id}", help=f"View details for {flat_id}"):
                    st.session_state.selected_flat = flat_id
                    st.session_state.selected_room = None
                    # Rerun to refresh UI
                    st.rerun()

# Display notifications panel
def display_notifications():
    st.markdown("<h3 class='section-title'>Notifications</h3>", unsafe_allow_html=True)
    
    for notification in st.session_state.notifications[:10]:  # Show only the latest 10 notifications
        st.markdown(f"<div class='notification'>{notification}</div>", unsafe_allow_html=True)

# Display maintenance history
def display_maintenance_history():
    st.markdown("<h3 class='section-title'>Maintenance History</h3>", unsafe_allow_html=True)
    
    # Filter history to show only the past month
    one_month_ago = datetime.now() - timedelta(days=30)
    
    if not st.session_state.maintenance_history:
        st.info("No maintenance history available")
    else:
        for entry in st.session_state.maintenance_history:
            if entry['completed']:
                completed_date = datetime.strptime(entry['completed'], "%Y-%m-%d %H:%M:%S")
                
                # Only show entries from the past month
                if completed_date > one_month_ago:
                    st.markdown(
                        f"""
                        <div class='history-item'>
                            <strong>Flat:</strong> {entry['flat_id']} | 
                            <strong>Room:</strong> {entry['room']} | 
                            <strong>Detected:</strong> {entry['detected']} | 
                            <strong>Started:</strong> {entry['started']} | 
                            <strong>Completed:</strong> {entry['completed']}
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )

# Display flat details
def display_flat_details(flat_id):
    st.markdown(f"<h2 class='section-title'>Flat {flat_id} Details</h2>", unsafe_allow_html=True)
    
    flat_data = st.session_state.flats_status[flat_id]
    status = flat_data['status']
    
    # Status information
    status_text = {
        'green': "Normal - No Issues",
        'red': "ALERT - Leak Detected",
        'yellow': "Under Maintenance"
    }
    
    status_color = {
        'green': "green",
        'red': "red",
        'yellow': "yellow"
    }
    
    # Display status
    st.markdown(f"<h3>Status: <span style='color:{status_color[status]}'>{status_text[status]}</span></h3>", unsafe_allow_html=True)
    
    # Show room info if there's an issue
    if flat_data['room']:
        st.markdown(f"<h4>Affected Room: {flat_data['room'].title()}</h4>", unsafe_allow_html=True)
    
    # Show timestamps if available
    if flat_data['timestamp']:
        st.markdown(f"<p>Leak Detected: {flat_data['timestamp']}</p>", unsafe_allow_html=True)
    
    if flat_data['maintenance_start']:
        st.markdown(f"<p>Maintenance Started: {flat_data['maintenance_start']}</p>", unsafe_allow_html=True)
    
    # Show action buttons for maintenance team
    if st.session_state.user_role == 'maintenance':
        col1, col2 = st.columns(2)
        
        with col1:
            if status == 'red':
                if st.button("Start Maintenance", key="start_maint"):
                    start_maintenance(flat_id)
                    st.rerun()
        
        with col2:
            if status == 'yellow':
                if st.button("Complete Maintenance", key="complete_maint"):
                    complete_maintenance(flat_id)
                    st.rerun()
    
    # Water flow graph for the flat
    st.markdown("### Water Flow Data")
    display_flow_graph(flat_data['flow_data'], f"Water Flow for Flat {flat_id}")
    
    # Show rooms data
    if st.session_state.selected_room is None:
        st.markdown("### Rooms")
        room_cols = st.columns(5)
        rooms = ['hall', 'kitchen', 'balcony', 'bedroom', 'bathroom']
        
        for i, room in enumerate(rooms):
            with room_cols[i]:
                if st.button(room.title(), key=f"room_{room}"):
                    st.session_state.selected_room = room
                    st.rerun()
    else:
        st.markdown(f"### {st.session_state.selected_room.title()} Flow Data")
        display_flow_graph(flat_data['room_data'][st.session_state.selected_room], 
                          f"Water Flow in {st.session_state.selected_room.title()}")
        
        if st.button("Back to All Rooms", key="back_to_rooms"):
            st.session_state.selected_room = None
            st.rerun()

# Display popup notification
def display_popup():
    if st.session_state.show_popup:
        # Create a placeholder for the popup
        popup_placeholder = st.empty()
        
        # Display the popup
        with popup_placeholder.container():
            st.markdown(
                f"""
                <div style="
                    position: fixed;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    background-color: rgba(0, 64, 128, 0.9);
                    padding: 20px;
                    border-radius: 10px;
                    z-index: 1000;
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
                    width: 80%;
                    max-width: 500px;
                    text-align: center;
                    animation: fadeIn 0.5s;
                ">
                    <h3>Notification</h3>
                    <p>{st.session_state.popup_message}</p>
                    <button onclick="this.parentElement.style.display='none';" style="
                        background-color: #0066cc;
                        color: white;
                        border: none;
                        padding: 8px 16px;
                        border-radius: 5px;
                        cursor: pointer;
                        margin-top: 10px;
                    ">
                        Close
                    </button>
                </div>
                """, 
                unsafe_allow_html=True
            )
        
        # Since the HTML/JS button won't work directly with Streamlit,
        # auto-close the popup after 3 seconds
        time.sleep(3)
        st.session_state.show_popup = False
        popup_placeholder.empty()

# Function to toggle leak simulation
def toggle_leak_simulation():
    st.session_state.leak_simulation_active = not st.session_state.leak_simulation_active
    
    if st.session_state.leak_simulation_active:
        st.success("Automatic leak simulation activated")
    else:
        st.warning("Automatic leak simulation deactivated")

# Main app function
def main():
    apply_custom_css()
    init_session_state()
    
    # Check if we should simulate leaks (if logged in and simulation is active)
    if st.session_state.logged_in and st.session_state.leak_simulation_active:
        check_leak_simulation()
    
    # Update flow data every 15 seconds
    update_flow_data()
    
    # Display popup if needed
    display_popup()
    
    # Login screen
    # Original login screen code to replace
    # Login screen
    if not st.session_state.logged_in:
        st.markdown("<h1 style='text-align: center; color: #4da6ff;'>💧 Water Leakage Detection System</h1>", unsafe_allow_html=True)
        
        # Centered login container
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        
        st.markdown("<h2 style='text-align: center;'>Login</h2>", unsafe_allow_html=True)
        
        # Role selection
        role = st.selectbox("Select Role", ['resident', 'maintenance', 'admin'])
        
        # Get usernames for the selected role
        user_data = get_user_data()
        usernames = list(user_data[role].keys())
        
        # Username and password fields
        username = st.selectbox("Username", usernames)
        
        # Handle form submission with Enter key
        with st.form(key="login_form", clear_on_submit=False):
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Login")
            
            # This will be triggered when the form is submitted (either by button or Enter key)
            if submit_button:
                if login(username, password, role):
                    st.success("Login successful!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Invalid username or password")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    else:  # User is logged in
        # Logout button in top-right corner
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"<h1 style='color: #4da6ff;'>💧 Water Leakage Detection System</h1>", unsafe_allow_html=True)
            st.markdown(f"<p>Logged in as <b>{st.session_state.username}</b> ({st.session_state.user_role})</p>", unsafe_allow_html=True)
        
        with col2:
            # if st.button("Logout", key="logout_btn"):
            #     confirm_logout = st.button("Are you sure you want to logout?", key="logout_confirm")
            #     if confirm_logout:
            #         logout()
            #         st.rerun()
            if 'logout_clicked' not in st.session_state:
                st.session_state.logout_clicked = False
    
            if st.session_state.logout_clicked:
                st.write("Are you sure you want to logout?")
                col_yes, col_no = st.columns(2)
                with col_yes:
                    if st.button("Yes", key="confirm_logout_yes"):
                        logout()
                        st.rerun()
                with col_no:
                    if st.button("No", key="confirm_logout_no"):
                        st.session_state.logout_clicked = False
                        st.rerun()
            else:
                if st.button("Logout", key="logout_btn"):
                    st.session_state.logout_clicked = True
                    st.rerun()
                
        # Admin controls
        if st.session_state.user_role == 'admin':
            st.sidebar.markdown("## Admin Controls")
            
            # Manual leak simulation
            if st.sidebar.button("Simulate Leak Now"):
                n = random.randint(1, 3)  # Random number of flats between 1 and 3
                simulate_leak(n)
                st.rerun()
            
            # Toggle automatic leak simulation
            if st.sidebar.button("Toggle Auto Leak Simulation"):
                toggle_leak_simulation()
            
            # Show auto leak status
            status_text = "Active" if st.session_state.leak_simulation_active else "Inactive"
            status_color = "green" if st.session_state.leak_simulation_active else "red"
            st.sidebar.markdown(f"Auto Leak Simulation: <span style='color:{status_color};'>{status_text}</span>", unsafe_allow_html=True)
            
           # Show next leak time
            if st.session_state.leak_simulation_active:
                next_leak_time = st.session_state.last_leak_time + timedelta(minutes=3)
                time_remaining = next_leak_time - datetime.now()
                seconds_remaining = max(0, int(time_remaining.total_seconds()))
                minutes = seconds_remaining // 60
                seconds = seconds_remaining % 60
                st.sidebar.markdown(f"Next simulated leak in: **{minutes}m {seconds}s**")
        
        # Display selected flat details or dashboard
        if st.session_state.selected_flat:
            display_flat_details(st.session_state.selected_flat)
            
            # Back button
            if st.button("Back to Dashboard", key="back_btn"):
                st.session_state.selected_flat = None
                st.session_state.selected_room = None
                st.rerun()
        else:
            # Setup tabs for different views
            st.markdown('<div class="tabs-custom">', unsafe_allow_html=True)
            tabs = st.tabs(["Dashboard", "Notifications", "Maintenance History"])
            
            with tabs[0]:  # Dashboard
                # Show building blocks
                blocks = ['A', 'B', 'C']
                
                # For residents, only show their block
                if st.session_state.user_role == 'resident':
                    user_flat = st.session_state.username
                    user_block = user_flat[0]  # First character of flat ID is the block
                    blocks = [user_block]  # Only show the user's block
                
                # Display blocks
                for block in blocks:
                    display_block_grid(block)
                
                # Show status summary
                st.markdown("<h3 class='section-title'>Status Summary</h3>", unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                # Count statuses
                green_count = sum(1 for status in st.session_state.flats_status.values() if status['status'] == 'green')
                red_count = sum(1 for status in st.session_state.flats_status.values() if status['status'] == 'red')
                yellow_count = sum(1 for status in st.session_state.flats_status.values() if status['status'] == 'yellow')
                
                with col1:
                    st.metric("Normal", green_count)
                
                with col2:
                    st.metric("Leaks Detected", red_count, delta="+0" if red_count == 0 else f"+{red_count}")
                
                with col3:
                    st.metric("Under Maintenance", yellow_count)
                
                # Display a gauge chart showing system health
                total_flats = len(st.session_state.flats_status)
                health_percentage = (green_count / total_flats) * 100
                
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=health_percentage,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "System Health"},
                    gauge={
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "rgba(0, 150, 255, 0.8)"},
                        'steps': [
                            {'range': [0, 60], 'color': "red"},
                            {'range': [60, 85], 'color': "yellow"},
                            {'range': [85, 100], 'color': "green"}
                        ],
                        'threshold': {
                            'line': {'color': "white", 'width': 4},
                            'thickness': 0.75,
                            'value': health_percentage
                        }
                    }
                ))
                
                fig.update_layout(
                    height=250, 
                    margin=dict(l=20, r=20, t=50, b=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with tabs[1]:  # Notifications
                display_notifications()
            
            with tabs[2]:  # Maintenance History
                display_maintenance_history()
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # For admin and maintenance, add a footer with extra stats
            if st.session_state.user_role in ['admin', 'maintenance']:
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("<h3 class='section-title'>System Statistics</h3>", unsafe_allow_html=True)
                
                # Calculate statistics
                now = datetime.now()
                system_uptime = now - st.session_state.app_start_time
                uptime_hours = int(system_uptime.total_seconds() // 3600)
                uptime_minutes = int((system_uptime.total_seconds() % 3600) // 60)
                
                total_leaks = len([n for n in st.session_state.notifications if "ALERT" in n])
                completed_maintenance = len(st.session_state.maintenance_history)
                
                # Display stats in columns
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("System Uptime", f"{uptime_hours}h {uptime_minutes}m")
                
                with col2:
                    st.metric("Total Leaks Detected", total_leaks)
                
                with col3:
                    st.metric("Completed Maintenance", completed_maintenance)
                
                with col4:
                    response_rate = completed_maintenance / total_leaks * 100 if total_leaks > 0 else 0
                    st.metric("Response Rate", f"{response_rate:.1f}%")

# Run the app
if __name__ == "__main__":
    main()