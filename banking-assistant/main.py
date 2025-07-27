import requests
from assistant.input_handler import get_user_input, validate_input
from assistant.dialogue_manager import DialogueManager

API_URL = "http://127.0.0.1:5000"

def register():
    print("--- Register ---")
    username = validate_input("Username: ")
    password = validate_input("Password: ", is_password=True)
    email = validate_input("Email: ")
    resp = requests.post(f"{API_URL}/register", json={"username": username, "password": password, "email": email})
    print(resp.json().get('msg'))

def login():
    print("--- Login ---")
    username = validate_input("Username: ")
    password = validate_input("Password: ", is_password=True)
    resp = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
    if resp.status_code == 200:
        print("Login successful!")
        return resp.json()['access_token']
    print(resp.json().get('msg'))
    return None

def main():
    print("Welcome to the Banking Assistant!")
    while True:
        choice = input("Do you want to (l)ogin, (r)egister, or (q)uit? ").strip().lower()
        if choice == 'r':
            register()
        elif choice == 'l':
            token = login()
            if token:
                run_session(token)
        elif choice == 'q':
            print("Goodbye!")
            break

def run_session(token):
    dm = DialogueManager(token)
    headers = {"Authorization": f"Bearer {token}"}
    while True:
        user_input = get_user_input()
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        response = dm.handle_message(user_input)
        print(f"Assistant: {response}")
        # Save conversation to backend
        requests.post(f"{API_URL}/conversation", json={"message": user_input, "response": response}, headers=headers)

if __name__ == "__main__":
    main()
