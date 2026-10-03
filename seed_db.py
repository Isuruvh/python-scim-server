import json
import http.client

# Configuration matching your local SCIM server
SERVER_HOST = "localhost:8000"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer test-token-12345"
}

def seed_scim_server():
    # Load your JSON sample data file
    try:
        with open("scim_sample_users.json", "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        print("Error: 'scim_sample_users.json' file not found.")
        return

    # Connect to your local server running on port 8000
    conn = http.client.HTTPConnection(SERVER_HOST)
    
    print(f"Starting database seed: Uploading {len(users)} records...")
    
    for index, user in enumerate(users, start=1):
        payload = json.dumps(user)
        
        # POST directly to your local endpoint
        conn.request("POST", "/scim/v2/Users", body=payload, headers=HEADERS)
        response = conn.getresponse()
        response.read()  # Clear response buffer
        
        if response.status == 201:
            print(f"[{index}/{len(users)}] Successfully provisioned: {user.get('userName')}")
        else:
            print(f"[{index}/{len(users)}] Failed to upload {user.get('userName')} (Status: {response.status})")
            
    conn.close()
    print("Seeding complete! You can now run a full import pull from your Okta tenant dashboard.")

if __name__ == "__main__":
    seed_scim_server()
