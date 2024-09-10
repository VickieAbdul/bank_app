import streamlit as st
import math

# Initialize account information (we'll simulate a database with a simple dictionary)
accounts = {}

# Create account function
def create_account(username, pin):
    accounts[username] = {'pin': pin, 'balance': 0}
    st.success(f"Account created for {username}!")

# Login function
def login(username, pin):
    if username in accounts and accounts[username]['pin'] == pin:
        st.session_state['logged_in'] = True
        st.session_state['username'] = username
        st.success(f"Login successful for {username}!")
        return True
    else:
        st.error("Invalid username or pin")
        return False

# Logout function
def logout():
    st.session_state['logged_in'] = False
    st.session_state['username'] = None
    st.info("You have been logged out.")

# Deposit function
def deposit(username, amount):
    accounts[username]['balance'] += amount
    st.success(f"{amount} deposited! New balance: {accounts[username]['balance']}")

# Check balance function
def check_balance(username):
    current_balance = accounts[username]['balance']
    st.info(f"Your current balance is {current_balance}.")

# Compound interest calculator
def calculate_compound_interest(p, r, t):
    a = p * math.exp(r * t)
    st.info(f"The future value is: {a}")

# Initialize session state for login if not present
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None

# Streamlit UI
st.title("Online Banking App")

# Check if user is logged in
if not st.session_state['logged_in']:
    # Sign in or log in
    menu = ["Sign In", "Log In"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Sign In":
        st.subheader("Create a New Account")
        new_username = st.text_input("Enter a username")
        new_pin = st.text_input("Create a 6-digit PIN", type="password")

        if st.button("Create Account"):
            if len(new_pin) == 6:
                create_account(new_username, new_pin)
            else:
                st.error("PIN must be 6 digits")

    elif choice == "Log In":
        st.subheader("Log In to Your Account")
        username = st.text_input("Username")
        pin = st.text_input("6-digit PIN", type="password")

        if st.button("Log In"):
            login(username, pin)

else:
    # If logged in, show actions and a Logout button
    st.subheader(f"Welcome, {st.session_state['username']}")

    action = st.selectbox("Choose an action", ["Deposit", "Check Balance", "Calculate Interest", "Logout", "Exit"])
    
    if action == "Deposit":
        amount = st.number_input("Enter deposit amount", min_value=0)
        if st.button("Deposit"):
            deposit(st.session_state['username'], amount)
    
    elif action == "Check Balance":
        check_balance(st.session_state['username'])
    
    elif action == "Calculate Interest":
        principal = st.number_input("Enter initial amount", min_value=0.0)
        rate = st.number_input("Enter interest rate (e.g., 0.05 for 5%)", min_value=0.0, max_value=1.0)
        time = st.number_input("Enter the number of years", min_value=0)
        
        if st.button("Calculate Interest"):
            calculate_compound_interest(principal, rate, time)
    
    elif action == "Logout":
        logout()

    elif action == "Exit":
        st.write("Thank you for using the app!")
        st.stop()  # This will stop the app entirely
