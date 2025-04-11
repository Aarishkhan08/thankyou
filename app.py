import streamlit as st
import time
import datetime
import json
import os
import random
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Messages for Mrs. Corio",
    page_icon="💌",
    layout="wide"
)

# Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #ff6b6b;
        text-align: center;
        margin-bottom: 1rem;
    }
    .message-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    .message-card:hover {
        transform: translateY(-5px);
    }
    .message-sender {
        font-weight: bold;
        color: #4e73df;
        margin-bottom: 5px;
    }
    .message-timestamp {
        font-size: 0.8rem;
        color: #6c757d;
        text-align: right;
    }
    .message-content {
        font-size: 1.1rem;
        color: #343a40;
        line-height: 1.5;
    }
    .sidebar-card {
        background-color: #fff3cd;
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        animation: fadeIn 0.5s ease-in;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .sidebar-quote {
        font-style: italic;
        color: #5a5a5a;
    }
    .sidebar-author {
        font-weight: bold;
        text-align: right;
        color: #6c757d;
        margin-top: 10px;
    }
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 30px;
        background-color: #f8f9fa;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    .login-header {
        text-align: center;
        margin-bottom: 20px;
        color: #4e73df;
    }
    .stButton > button {
        background-color: #4e73df;
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 5px;
        cursor: pointer;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #3a56a5;
    }
    .category-tag {
        display: inline-block;
        background-color: #e9ecef;
        border-radius: 15px;
        padding: 5px 10px;
        margin-right: 5px;
        font-size: 0.8rem;
        color: #495057;
    }
    .reaction-button {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 20px;
        padding: 5px 12px;
        margin-right: 8px;
        font-size: 0.9rem;
        cursor: pointer;
    }
    .reaction-button:hover {
        background-color: #e9ecef;
    }
    .featured-message {
        border-left: 4px solid #ffc107;
        background-color: #fff9db;
    }
    .background-ribbon {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 10px;
        background: linear-gradient(90deg, #ff6b6b, #6b8fff, #6bffac);
        z-index: 1000;
    }
</style>
""", unsafe_allow_html=True)

# Create data files if they don't exist
if not os.path.exists("messages.json"):
    with open("messages.json", "w") as f:
        json.dump([], f)

if not os.path.exists("reactions.json"):
    with open("reactions.json", "w") as f:
        json.dump({}, f)

# Function to load messages
def load_messages():
    try:
        with open("messages.json", "r") as f:
            messages = json.load(f)
            # Ensure all messages have required fields
            for msg in messages:
                if "category" not in msg:
                    msg["category"] = "General"
                if "featured" not in msg:
                    msg["featured"] = False
                if "id" not in msg:
                    msg["id"] = f"legacy_msg_{int(time.time())}_{random.randint(1000, 9999)}"
            return messages
    except:
        return []

# Function to save messages
def save_message(name, message, category="General"):
    messages = load_messages()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message_id = f"msg_{int(time.time())}_{len(messages)}"
    messages.append({
        "id": message_id,
        "name": name,
        "message": message,
        "timestamp": timestamp,
        "category": category,
        "featured": False
    })
    with open("messages.json", "w") as f:
        json.dump(messages, f)
    return message_id

# Function to load reactions
def load_reactions():
    try:
        with open("reactions.json", "r") as f:
            return json.load(f)
    except:
        return {}

# Function to save reaction
def save_reaction(message_id, reaction_type):
    reactions = load_reactions()
    if message_id not in reactions:
        reactions[message_id] = {"❤️": 0, "👍": 0, "🌟": 0}
    reactions[message_id][reaction_type] += 1
    with open("reactions.json", "w") as f:
        json.dump(reactions, f)

# Function to toggle featured status
def toggle_featured(message_id):
    messages = load_messages()
    for msg in messages:
        if msg["id"] == message_id:
            msg["featured"] = not msg["featured"]
            break
    with open("messages.json", "w") as f:
        json.dump(messages, f)

# Secret password - in a real app, this would be securely stored
SECRET_PASSWORD = "GetWellSoonMrsCorio2025"  # This is the secret password

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = ""
if "sidebar_message_index" not in st.session_state:
    st.session_state.sidebar_message_index = 0
if "last_update" not in st.session_state:
    st.session_state.last_update = time.time()
if "view" not in st.session_state:
    st.session_state.view = "all"
if "search_query" not in st.session_state:
    st.session_state.search_query = ""
if "filter_category" not in st.session_state:
    st.session_state.filter_category = "All"
if "refresh_counter" not in st.session_state:
    st.session_state.refresh_counter = 0

# Login page
def show_login():
    st.markdown("<div class='background-ribbon'></div>", unsafe_allow_html=True)
    st.markdown("<h1 class='login-header'>Messages for Mrs. Corio</h1>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        st.subheader("Please Log In")
        
        username = st.text_input("Your Name (will be displayed with your message)")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if password == SECRET_PASSWORD:
                st.session_state.logged_in = True
                st.session_state.current_user = username if username else "Anonymous"
                st.rerun()
            else:
                st.error("Invalid password. Please try again.")
        
        st.markdown("<p style='text-align: center; margin-top: 20px;'>Enter the class password to post messages of support</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# Main app page
def show_main_app():
    st.markdown("<div class='background-ribbon'></div>", unsafe_allow_html=True)
    
    # Auto-refresh functionality without using the external package
    refresh_interval = 5  # seconds
    
    # Implement our own auto-refresh mechanism
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = time.time()
    
    current_time = time.time()
    time_diff = current_time - st.session_state.last_refresh
    
    if time_diff > refresh_interval:
        st.session_state.refresh_counter += 1
        st.session_state.last_refresh = current_time
        
        # Update sidebar message index for rotating messages
        messages = load_messages()
        if messages:
            st.session_state.sidebar_message_index = (st.session_state.sidebar_message_index + 1) % len(messages)
    
    # Hidden element to force periodic refresh
    st.empty().markdown(f"<div style='display:none'>{st.session_state.refresh_counter}</div>", unsafe_allow_html=True)
    
    # Add a manual refresh button in the sidebar
    if st.sidebar.button("↻ Refresh"):
        st.rerun()
    
    # Use columns for layout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("<h1 class='main-header'>Wall of Letters for Mrs. Corio</h1>", unsafe_allow_html=True)
        
        # Message input form
        with st.expander("Post a New Message", expanded=True):
            st.subheader(f"Post a Message as {st.session_state.current_user}")
            message = st.text_area("Your message for Mrs. Corio", height=100)
            
            # Add category selection
            categories = ["General", "Memory", "Appreciation", "Well Wishes", "Inspiration", "Thank You"]
            category = st.selectbox("Category", categories)
            
            if st.button("Post Message"):
                if message:
                    message_id = save_message(st.session_state.current_user, message, category)
                    st.success("Message posted successfully!")
                    st.session_state.last_update = time.time()
                    time.sleep(1)
                    st.rerun()
                else:
                    st.warning("Please enter a message.")
        
        # Filtering and search tools
        with st.container():
            col_search, col_filter, col_view = st.columns(3)
            
            with col_search:
                st.session_state.search_query = st.text_input("🔍 Search messages", value=st.session_state.search_query)
            
            with col_filter:
                all_categories = ["All"] + ["General", "Memory", "Appreciation", "Well Wishes", "Inspiration", "Thank You"]
                st.session_state.filter_category = st.selectbox("Category Filter", all_categories, index=all_categories.index(st.session_state.filter_category) if st.session_state.filter_category in all_categories else 0)
            
            with col_view:
                view_options = {"all": "All Messages", "featured": "Featured Messages"}
                st.session_state.view = st.radio("View", options=list(view_options.keys()), format_func=lambda x: view_options[x], horizontal=True)
        
        # Display messages
        messages = load_messages()
        reactions = load_reactions()
        
        # Apply filters
        if st.session_state.filter_category != "All":
            messages = [msg for msg in messages if msg.get("category", "General") == st.session_state.filter_category]
        
        if st.session_state.search_query:
            search_query = st.session_state.search_query.lower()
            messages = [msg for msg in messages if search_query in msg.get("message", "").lower() or search_query in msg.get("name", "").lower()]
        
        if st.session_state.view == "featured":
            messages = [msg for msg in messages if msg.get("featured", False)]
        
        # Display filtered messages
        st.subheader(f"Messages ({len(messages)})")
        if not messages:
            st.info("No messages found matching your criteria.")
        else:
            for idx, msg in enumerate(reversed(messages)):
                message_id = msg.get("id", f"legacy_msg_{idx}")
                
                # Get reactions for this message
                msg_reactions = reactions.get(message_id, {"❤️": 0, "👍": 0, "🌟": 0})
                
                # Determine if this is a featured message
                is_featured = msg.get("featured", False)
                card_class = "message-card featured-message" if is_featured else "message-card"
                category = msg.get("category", "General")
                
                # Display the full message with attribution
                st.markdown(f"""
                <div class="{card_class}">
                    <div class="message-sender">{msg.get('name', 'Anonymous')}</div>
                    <span class="category-tag">{category}</span>
                    {"<span class='category-tag' style='background-color: #ffd700; color: #000;'>✨ Featured</span>" if is_featured else ""}
                    <div class="message-content">{msg.get('message', '')}</div>
                    <div class="message-timestamp">{msg.get('timestamp', '')}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Reaction buttons
                col_r1, col_r2, col_r3, col_r4 = st.columns([1, 1, 1, 3])
                with col_r1:
                    if st.button(f"❤️ {msg_reactions['❤️']}", key=f"heart_{message_id}"):
                        save_reaction(message_id, "❤️")
                        st.rerun()
                with col_r2:
                    if st.button(f"👍 {msg_reactions['👍']}", key=f"like_{message_id}"):
                        save_reaction(message_id, "👍")
                        st.rerun()
                with col_r3:
                    if st.button(f"🌟 {msg_reactions['🌟']}", key=f"star_{message_id}"):
                        save_reaction(message_id, "🌟")
                        st.rerun()
                with col_r4:
                    if st.session_state.current_user.lower() == "admin":
                        featured_text = "Unfeature" if is_featured else "Feature"
                        if st.button(f"{featured_text}", key=f"feature_{message_id}"):
                            toggle_featured(message_id)
                            st.rerun()

    # Sidebar with rotating messages and stats
    with col2:
        st.sidebar.markdown("<h2>Message Spotlight</h2>", unsafe_allow_html=True)
        
        # Display current message in spotlight
        if messages:
            # Find featured messages first
            featured_messages = [msg for msg in messages if msg.get("featured", False)]
            
            # If there are featured messages, prioritize them in the rotation
            if featured_messages and random.random() > 0.3:  # 70% chance to show featured message
                spotlight_msg = random.choice(featured_messages)
            elif messages:
                # Otherwise choose from all messages
                spotlight_index = min(st.session_state.sidebar_message_index, len(messages) - 1)
                spotlight_msg = messages[spotlight_index]
            else:
                spotlight_msg = None
            
            if spotlight_msg:
                message_id = spotlight_msg.get("id", "unknown")
                msg_reactions = reactions.get(message_id, {"❤️": 0, "👍": 0, "🌟": 0})
                
                st.sidebar.markdown(f"""
                <div class="sidebar-card">
                    <div class="sidebar-quote">"{spotlight_msg.get('message', '')}"</div>
                    <div class="sidebar-author">- {spotlight_msg.get('name', 'Anonymous')}</div>
                    <div style="margin-top: 5px;">
                        <span style="margin-right: 10px;">❤️ {msg_reactions['❤️']}</span>
                        <span style="margin-right: 10px;">👍 {msg_reactions['👍']}</span>
                        <span>🌟 {msg_reactions['🌟']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.sidebar.info("Messages will appear here once posted.")
        
        # Display stats
        st.sidebar.subheader("Message Wall Stats")
        
        all_messages = load_messages()
        reactions_data = load_reactions()
        
        total_messages = len(all_messages)
        total_reactions = sum([sum(r.values()) for r in reactions_data.values()])
        categories_count = {}
        for msg in all_messages:
            cat = msg.get("category", "General")
            if cat in categories_count:
                categories_count[cat] += 1
            else:
                categories_count[cat] = 1
        
        st.sidebar.metric("Total Messages", total_messages)
        st.sidebar.metric("Total Reactions", total_reactions)
        
        # Show analytics
        st.sidebar.subheader("Message Categories")
        
        # Prepare data for chart
        if categories_count:
            categories_df = pd.DataFrame({
                'Category': list(categories_count.keys()),
                'Count': list(categories_count.values())
            })
            st.sidebar.bar_chart(categories_df.set_index('Category'))
        
        # Most active contributors
        st.sidebar.subheader("Top Contributors")
        name_counts = {}
        for msg in all_messages:
            name = msg.get("name", "Anonymous")
            if name in name_counts:
                name_counts[name] += 1
            else:
                name_counts[name] = 1
        
        # Sort by number of messages
        sorted_contributors = sorted(name_counts.items(), key=lambda x: x[1], reverse=True)
        for name, count in sorted_contributors[:5]:  # Show top 5
            st.sidebar.text(f"• {name}: {count} messages")
        
        st.sidebar.write(f"Last updated: {datetime.datetime.now().strftime('%H:%M:%S')}")
    
    # Add logout button at the bottom of sidebar
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = ""
        st.rerun()

# Main app logic
def main():
    if st.session_state.logged_in:
        show_main_app()
    else:
        show_login()

if __name__ == "__main__":
    main()
