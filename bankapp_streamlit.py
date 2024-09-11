import streamlit as st
import math

# Initialize session state
if 'accounts' not in st.session_state:
    st.session_state.accounts = {}
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Functions
def create_account(username, pin):
    if username in st.session_state.accounts:
        return False
    st.session_state.accounts[username] = {'pin': pin, 'balance': 0}
    return True

def login(username, pin):
    if username in st.session_state.accounts and st.session_state.accounts[username]['pin'] == pin:
        st.session_state.logged_in = True
        st.session_state.current_user = username
        return True
    return False

def reset_pin(username, new_pin):
    if username in st.session_state.accounts:
        st.session_state.accounts[username]['pin'] = new_pin
        return True
    return False

def logout():
    st.session_state.logged_in = False
    st.session_state.current_user = None

def deposit(username, amount):
    st.session_state.accounts[username]['balance'] += amount

def withdraw(username, amount):
    if st.session_state.accounts[username]['balance'] >= amount:
        st.session_state.accounts[username]['balance'] -= amount
        return True
    return False

def calculate_compound_interest(principal, rate, time):
    return principal * math.exp(rate * time)

# Streamlit UI
st.title("Online Banking App")

if not st.session_state.logged_in:
    menu = ["Sign In", "Log In", "Reset PIN", "Exit"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Sign In":
        st.subheader("Create a New Account")
        new_username = st.text_input("Enter a username")
        new_pin = st.text_input("Create a 6-digit PIN", type="password")

        if st.button("Create Account"):
            if new_pin.isdigit() and len(new_pin) == 6:  # Key Change: Ensured PIN is numeric and 6 digits
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
                st.success("Logged in successfully!")
            else:
                st.error("Incorrect username or PIN")

    elif choice == "Reset PIN":
        st.subheader("Reset Your PIN")
        username = st.text_input("Username")
        new_pin = st.text_input("Enter new 6-digit PIN", type="password")

        if st.button("Reset PIN"):
            if new_pin.isdigit() and len(new_pin) == 6:  # Key Change: Ensured new PIN is numeric and 6 digits
                if reset_pin(username, new_pin):
                    st.success("PIN successfully reset! Please log in.")
                else:
                    st.error("Username does not exist. Please create an account first.")
            else:
                st.error("PIN must be 6 digits and numeric")

    elif choice == "Exit":
        st.write("Thank you for using the app!")
        st.stop()  # Key Change: Exit the app

else:
    st.subheader(f"Welcome, {st.session_state.current_user}")

    action = st.selectbox("Choose an action", ["Deposit", "Withdraw", "Check Balance", "Calculate Interest", "Logout", "Exit"])
    
    if action == "Deposit":
        amount = st.number_input("Enter deposit amount", min_value=0.0)
        if st.button("Deposit"):
            deposit(st.session_state.current_user, amount)
            st.success(f"Deposited {amount}. New balance: {st.session_state.accounts[st.session_state.current_user]['balance']}")
    
    elif action == "Withdraw":
        amount = st.number_input("Enter withdrawal amount", min_value=0.0)
        if st.button("Withdraw"):
            if withdraw(st.session_state.current_user, amount):
                st.success(f"Withdrew {amount}. New balance: {st.session_state.accounts[st.session_state.current_user]['balance']}")
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
            st.write("You have been logged out.")
    
    if st.button("Exit"):
        st.write("Thank you for using the app!")
        st.stop()  # Key Change: Exit the app
