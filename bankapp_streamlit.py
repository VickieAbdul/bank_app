import streamlit as st
import math

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

# Function to deposit money
def deposit(username, amount):
    st.session_state.accounts[username]['balance'] += amount
    return st.session_state.accounts[username]['balance']

# Function to withdraw money
def withdraw(username, amount):
    if st.session_state.accounts[username]['balance'] >= amount:
        st.session_state.accounts[username]['balance'] -= amount
        return True
    else:
        return False  # Insufficient balance

# Compound interest calculator
def calculate_compound_interest(principal, rate, time):
    return principal * math.exp(rate * time)

# Streamlit UI
st.title("Online Banking App")

# Check if user is logged in
if not st.session_state.logged_in:
    # Sign in, log in, or reset PIN
    menu = ["Sign In", "Log In", "Reset PIN", "Exit"]
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

    elif choice == "Exit":
        st.write("Thank you for using the app!")
        st.stop()  # This will stop the app entirely

else:
    # If logged in, show the dashboard and a Logout button at the bottom
    st.subheader(f"Welcome, {st.session_state.current_user}")

    # Dashboard actions (Deposit, Withdraw, Check Balance, Calculate Interest, etc.)
    action = st.selectbox("Choose an action", ["Deposit", "Withdraw", "Check Balance", "Calculate Interest"])
    
    if action == "Deposit":
        amount = st.number_input("Enter deposit amount", min_value=0)
        if st.button("Deposit"):
            new_balance = deposit(st.session_state.current_user, amount)
            st.success(f"{amount} deposited! New balance: {new_balance}")
    
    elif action == "Withdraw":
        amount = st.number_input("Enter withdrawal amount", min_value=0)
        if st.button("Withdraw"):
            if withdraw(st.session_state.current_user, amount):
                st.success(f"{amount} withdrawn! New balance: {st.session_state.accounts[st.session_state.current_user]['balance']}")
            else:
                st.error("Insufficient balance")

    elif action == "Check Balance":
        current_balance = st.session_state.accounts[st.session_state.current_user]['balance']
        st.info(f"Your current balance is {current_balance}.")
    
    elif action == "Calculate Interest":
        principal = st.number_input("Enter initial amount", min_value=0.0)
        rate = st.number_input("Enter interest rate (e.g., 0.05 for 5%)", min_value=0.0, max_value=1.0)
        time = st.number_input("Enter the number of years", min_value=0)
        
        if st.button("Calculate Interest"):
            future_value = calculate_compound_interest(principal, rate, time)
            st.success(f"The future value is: {future_value}")
    
    elif action == "Logout":
        if st.button("Logout"):
            logout()
    
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

