from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# Hardcoded token for Okta API credential validation
BEARER_TOKEN = "test-token-12345"

# In-memory "HRIS Worker" database pre-populated with a sample user
workers_db = {
    "hr-worker-101": {
        "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
        "id": "hr-worker-101",
        "userName": "bross@example.com",
        "name": {"givenName": "Bob", "familyName": "Ross"},
        "emails": [{"value": "bross@example.com", "primary": True}],
        "active": True,
        "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User": {
            "employeeNumber": "EMP-001",
            "costCenter": "AU-9900",
            "organization": "Identity Engineering",
            "division": "Operations"
        }
    }
}

def check_auth():
    auth_header = request.headers.get("Authorization")
    if not auth_header or auth_header != f"Bearer {BEARER_TOKEN}":
        return False
    return True

# --- SCIM 2.0 Users Endpoints ---

@app.route("/scim/v2/Users", methods=["GET"])
def get_users():
    if not check_auth():
        return jsonify({"error": "Unauthorized"}), 401
        
    print(f"\n[GET /Users] Okta checking directory list. Query string: {request.args}")
    
    # Return list format expected by Okta / SCIM specification
    resources = list(workers_db.values())
    response = {
        "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
        "totalResults": len(resources),
        "startIndex": 1,
        "itemsPerPage": len(resources),
        "Resources": resources
    }
    return jsonify(response), 200

@app.route("/scim/v2/Users/<user_id>", methods=["GET"])
def get_user_by_id(user_id):
    if not check_auth():
        return jsonify({"error": "Unauthorized"}), 401

    print(f"\n[GET /Users/{user_id}] Okta validating user specific record.")
    user = workers_db.get(user_id)
    if not user:
        return jsonify({"schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"], "detail": "User not found", "status": "404"}), 404
        
    return jsonify(user), 200

@app.route("/scim/v2/Users", methods=["POST"])
def create_user():
    if not check_auth():
        return jsonify({"error": "Unauthorized"}), 401

    payload = request.json
    print(f"\n[POST /Users] Inbound provisioning trigger received!\nPayload: {payload}")
    
    # Generate unique ID mimicking an external HR system sequence
    new_id = f"hr-worker-{int(time.time())}"
    payload["id"] = new_id
    
    workers_db[new_id] = payload
    return jsonify(payload), 201

@app.route("/scim/v2/Users/<user_id>", methods=["PUT", "PATCH"])
def update_user(user_id):
    if not check_auth():
        return jsonify({"error": "Unauthorized"}), 401

    print(f"\n[{request.method} /Users/{user_id}] Update / Lifecycle state alteration requested.")
    if user_id not in workers_db:
        return jsonify({"detail": "User not found"}), 404

    if request.method == "PUT":
        payload = request.json
        payload["id"] = user_id
        workers_db[user_id] = payload
    elif request.method == "PATCH":
        # Basic patch handling for active state adjustments
        payload = request.json
        for op in payload.get("Operations", []):
            if op.get("op") == "replace" or op.get("op") == "Replace":
                value = op.get("value")
                if isinstance(value, dict):
                    for k, v in value.items():
                        if k == "active":
                            workers_db[user_id]["active"] = v
                elif "active" in op.get("path", ""):
                    workers_db[user_id]["active"] = value

    return jsonify(workers_db[user_id]), 200
@app.route("/scim/v2/Groups", methods=["GET"])
def get_groups():
    if not check_auth():
        return jsonify({"error": "Unauthorized"}), 401
        
    print("\n[GET /Groups] Okta checking for structural groups. Returning empty list.")
    
    # Standard empty SCIM ListResponse payload
    response = {
        "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
        "totalResults": 0,
        "startIndex": 1,
        "itemsPerPage": 0,
        "Resources": []
    }
    return jsonify(response), 200

if __name__ == "__main__":
    # Runs locally on port 8000
    app.run(host="0.0.0.0", port=8000, debug=True)
