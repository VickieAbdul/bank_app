import streamlit as st
import math

# Initialize session state for storing accounts, balances, and login status
if 'accounts' not in st.session_state:
    st.session_state.accounts = {}  # Store accounts in a dictionary
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False  # Track login status
if 'current_user' not in st.session_state:
    st.session_state.current_user = None  # Track the current logged-in user
if 'balances' not in st.session_state:
    st.session_state.balances = {}  # Store balances for each user

# Function to create an account
def create_account(username, pin):
    if username in st.session_state.accounts:
        st.error("Username already exists. Please choose another one.")
        return False
    else:
        st.session_state.accounts[username] = pin
        st.session_state.balances[username] = 0  # Initialize balance to 0
        st.success(f"Account for {username} created successfully!")
        return True

# Function to verify login
def login(username, pin):
    if username in st.session_state.accounts and st.session_state.accounts[username] == pin:
        st.session_state.logged_in = True
        st.session_state.current_user = username
        st.success(f"Login successful! Welcome, {username}.")
    else:
        st.error("Invalid username or PIN.")
        return False

# Forgot PIN function
def forgot_pin(username, new_pin):
    if username in st.session_state.accounts:
        st.session_state.accounts[username] = new_pin
        st.success(f"PIN for {username} reset successfully!")
    else:
        st.error("Username not found.")

# Logout function
def logout():
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.info("You have been logged out.")
    st.write("Redirecting to login page...")

# Deposit function
def deposit(username, amount):
    st.session_state.balances[username] += amount
    st.success(f"{amount} deposited! New balance: {st.session_state.balances[username]}")

# Withdrawal function
def withdrawal(username, amount):
    if st.session_state.balances[username] >= amount:
        st.session_state.balances[username] -= amount
        st.success(f"{amount} withdrawn! New balance: {st.session_state.balances[username]}")
    else:
        st.error("Insufficient funds.")

# Check balance function
def check_balance(username):
    current_balance = st.session_state.balances[username]
    st.info(f"Your current balance is {current_balance}.")

# Compound interest calculator
def calculate_compound_interest(p, r, t):
    a = p * math.exp(r * t)
    st.info(f"The future value is: {a:.2f}")

# Streamlit UI
st.title("Online Banking App")

# Check if user is logged in
if not st.session_state.logged_in:
    # Sign in, log in, or reset PIN
    menu = ["Sign In", "Log In", "Forgot PIN"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Sign In":
        st.subheader("Create a New Account")
        new_username = st.text_input("Enter a username")
        new_pin = st.text_input("Create a 6-digit PIN", type="password")

        if st.button("Create Account"):
            if len(new_pin) == 6 and new_pin.isdigit():  # Check that PIN is 6 digits and numeric
                if create_account(new_username, new_pin):
                    st.success('Please log in from the menu.')

    elif choice == "Log In":
        st.subheader("Log In to Your Account")
        username = st.text_input("Username")
        pin = st.text_input("6-digit PIN", type="password")

        if st.button("Log In"):
            login(username, pin)

    elif choice == "Forgot PIN":
        st.subheader("Reset Your PIN")
        username = st.text_input("Enter your username")
        new_pin = st.text_input("Enter a new 6-digit PIN", type="password")

        if st.button("Reset PIN"):
            if len(new_pin) == 6 and new_pin.isdigit():  # Check that PIN is 6 digits and numeric
                forgot_pin(username, new_pin)
                st.success('PIN reset successful, please log in.')

else:
    # If logged in, show actions and a Logout button
    st.subheader(f"Welcome, {st.session_state.current_user}")

    action = st.selectbox("Choose an action", ["Deposit", "Withdrawal", "Check Balance", "Calculate Interest", "Logout", "Exit"])

    if action == "Deposit":
        amount = st.number_input("Enter deposit amount", min_value=0.0)
        if st.button("Deposit"):
            deposit(st.session_state.current_user, amount)

    elif action == "Withdrawal":
        amount = st.number_input("Enter withdrawal amount", min_value=0.0)
        if st.button("Withdraw"):
            withdrawal(st.session_state.current_user, amount)

    elif action == "Check Balance":
        check_balance(st.session_state.current_user)

    elif action == "Calculate Interest":
        principal = st.number_input("Enter initial amount", min_value=0.0)
        rate = st.number_input("Enter interest rate (e.g., 0.05 for 5%)", min_value=0.0, max_value=1.0)
        time = st.number_input("Enter the number of years", min_value=0)

        if st.button("Calculate Interest"):
            calculate_compound_interest(principal, rate, time)

    elif action == "Logout":
        logout()
        if st.button("Calculate Interest"):
            calculate_compound_interest(principal, rate, time)

    elif action == "Logout":
        logout()
