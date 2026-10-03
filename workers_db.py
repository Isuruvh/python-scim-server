workers_db = {
    "hr-worker-2001": {
        "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
        "id": "hr-worker-2001",
        "userName": "j.smith@isurutrader.com",
        "name": {"givenName": "John", "familyName": "Smith"},
        "emails": [{"value": "j.smith@isurutrader.com", "primary": True}],
        "active": True,
        "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User": {
            "employeeNumber": "EMP-2001",
            "costCenter": "AU-FIN-400",
            "department": "Identity & Access Management"
        }
    },
    "hr-worker-2002": {
        "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
        "id": "hr-worker-2002",
        "userName": "a.lee@isurutrader.com",
        "name": {"givenName": "Alice", "familyName": "Lee"},
        "emails": [{"value": "a.lee@isurutrader.com", "primary": True}],
        "active": True,
        "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User": {
            "employeeNumber": "EMP-2002",
            "costCenter": "AU-OPS-200",
            "department": "Cloud Infrastructure"
        }
    },
    "hr-worker-1099": {
        "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
        "id": "hr-worker-1099",
        "userName": "m.wilson@isurutrader.com",
        "name": {"givenName": "Mark", "familyName": "Wilson"},
        "emails": [{"value": "m.wilson@isurutrader.com", "primary": True}],
        "active": False,
        "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User": {
            "employeeNumber": "EMP-1099",
            "costCenter": "AU-HR-100",
            "department": "Human Resources"
        }
    }
}
