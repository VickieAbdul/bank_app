import streamlit as st

# Initialize session state for accounts and login status
if 'accounts' not in st.session_state:
    st.session_state.accounts = {}  # Store accounts in a dictionary
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False  # Track login status
if 'current_user' not in st.session_state:
    st.session_state.current_user = None  # Track the current logged-in user

# Function to create an account
def create_account(username, pin):
    if username in st.session_state.accounts:
        return False  # Username already exists
    else:
        st.session_state.accounts[username] = {'pin': pin, 'balance': 0}
        return True

# Function to verify login
def login(username, pin):
    if username in st.session_state.accounts and st.session_state.accounts[username]['pin'] == pin:
        st.session_state.logged_in = True
        st.session_state.current_user = username
        return True
    else:
        return False

# Function to reset PIN
def reset_pin(username, new_pin):
    if username in st.session_state.accounts:
        st.session_state.accounts[username]['pin'] = new_pin
        return True
    else:
        return False

# Logout function
def logout():
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.force_rerun = True  # Trigger a rerun after logout
    st.experimental_rerun()

# Streamlit UI
st.title("Online Banking App")

# Check if rerun is needed (for example, after logout)
if 'force_rerun' in st.session_state and st.session_state.force_rerun:
    st.session_state.force_rerun = False
    st.experimental_rerun()

# Check if user is logged in
if not st.session_state.logged_in:
    # Sign in, log in, or reset PIN
    menu = ["Sign In", "Log In", "Reset PIN"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Sign In":
        st.subheader("Create a New Account")
        new_username = st.text_input("Enter a username")
        new_pin = st.text_input("Create a 6-digit PIN", type="password")

        if st.button("Create Account"):
            if new_pin.isdigit() and len(new_pin) == 6:
                if create_account(new_username, new_pin):
                    st.success('Account successfully created! Please log in.')
                else:
                    st.error('Username already exists. Try a different one.')
            else:
                st.error("PIN must be 6 digits and numeric")

    elif choice == "Log In":
        st.subheader("Log In to Your Account")
        username = st.text_input("Username")
        pin = st.text_input("6-digit PIN", type="password")

        if st.button("Log In"):
            if login(username, pin):
                st.success(f"Welcome, {username}")
            else:
                st.error("Incorrect username or PIN")

    elif choice == "Reset PIN":
        st.subheader("Reset Your PIN")
        username = st.text_input("Username")
        new_pin = st.text_input("Enter new 6-digit PIN", type="password")

        if st.button("Reset PIN"):
            if new_pin.isdigit() and len(new_pin) == 6:
                if reset_pin(username, new_pin):
                    st.success("PIN successfully reset! Please log in.")
                else:
                    st.error("Username does not exist. Please create an account first.")
            else:
                st.error("PIN must be 6 digits and numeric")

else:
    # If logged in, show the dashboard and a Logout button at the bottom
    st.subheader(f"Welcome, {st.session_state.current_user}")

    # Dashboard actions (Deposit, Check Balance, etc.)
    action = st.selectbox("Choose an action", ["Deposit", "Check Balance", "Logout", "Exit"])
    
    if action == "Deposit":
        amount = st.number_input("Enter deposit amount", min_value=0)
        if st.button("Deposit"):
            st.session_state.accounts[st.session_state.current_user]['balance'] += amount
            st.success(f"{amount} deposited! New balance: {st.session_state.accounts[st.session_state.current_user]['balance']}")
    
    elif action == "Check Balance":
        current_balance = st.session_state.accounts[st.session_state.current_user]['balance']
        st.info(f"Your current balance is {current_balance}.")
    
    elif action == "Logout":
        st.write("")  # Optional spacing
        st.button("Logout", on_click=logout)

    # Place the Logout button at the bottom
    st.write(" ")  # Adds a blank space to push the button down
    st.write(" ")  # Adds a blank space to push the button down
    st.write(" ")  # Adds a blank space to push the button down
    st.write(" ")  # Adds a blank space to push the button down
    if st.button("Logout", key='bottom_logout'):
        logout()
    
    elif action == "Exit":
        st.write("Thank you for using the app!")
        st.stop()  # This will stop the app entirely
