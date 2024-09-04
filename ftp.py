import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# Define the FTP server's root directory
FTP_ROOT = "/srv/ftp"

# Create the FTP root directory if it doesn't exist
os.makedirs(FTP_ROOT, exist_ok=True)

# Create an authorizer for managing 'virtual' users
authorizer = DummyAuthorizer()

# Define permissions
super_user_perm = "elradfmwMT" # Full permissions for super user
normal_user_perm = "elr" # Read and list permissions for normal users

# Set to store existing usernames
existing_usernames = set()

# Function to register a user
def register_user():
    while True:
        username = input("Enter a new username: ")
        if username in existing_usernames:
            print("Username already taken. Please choose a different username.")
        else:
            existing_usernames.add(username)
            password = input(f"Enter password for user '{username}': ")
            if username == "superuser":
                authorizer.add_user(username, password, FTP_ROOT, perm=super_user_perm)
            else:
                authorizer.add_user(username, password, FTP_ROOT, perm=normal_user_perm)
            print(f"User '{username}' registered successfully.")
            break

# Allow registration of multiple users
num_users = int(input("How many users do you want to register? "))
for _ in range(num_users):
    register_user()

# Create the FTP handler and assign the authorizer
handler = FTPHandler
handler.authorizer = authorizer

# Define the server address and port
server_address = ("0.0.0.0", 2100) # Listen on all interfaces on port 21

# Create and start the FTP server
ftp_server = FTPServer(server_address, handler)

print(f"Starting FTP server on {server_address[0]}:{server_address[1]}...")
ftp_server.serve_forever()