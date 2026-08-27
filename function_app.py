import azure.functions as func
import json

app = func.FunctionApp()


# --------------------------------------------------
# 1. Hello Function
# URL: GET /api/hello
# --------------------------------------------------
@app.route(
    route="hello",
    methods=["GET"],
    auth_level=func.AuthLevel.ANONYMOUS
)
def hello(req: func.HttpRequest) -> func.HttpResponse:

    name = req.params.get("name")

    if name:
        message = f"Hello {name}! Azure Function is working."
    else:
        message = "Hello! Azure Function is working."

    return func.HttpResponse(
        message,
        status_code=200
    )


# --------------------------------------------------
# 2. Get All Users
# URL: GET /api/users
# --------------------------------------------------
@app.route(
    route="users",
    methods=["GET"],
    auth_level=func.AuthLevel.ANONYMOUS
)
def get_users(req: func.HttpRequest) -> func.HttpResponse:

    users = [
        {
            "id": 1,
            "name": "Veera",
            "email": "veera@example.com",
            "role": "DevOps Engineer"
        },
        {
            "id": 2,
            "name": "Ravi",
            "email": "ravi@example.com",
            "role": "Python Developer"
        },
        {
            "id": 3,
            "name": "Kiran",
            "email": "kiran@example.com",
            "role": "Cloud Engineer"
        }
    ]

    return func.HttpResponse(
        json.dumps(users),
        status_code=200,
        mimetype="application/json"
    )


# --------------------------------------------------
# 3. Get User By ID
# URL: GET /api/users/1
# --------------------------------------------------
@app.route(
    route="users/{user_id}",
    methods=["GET"],
    auth_level=func.AuthLevel.ANONYMOUS
)
def get_user(req: func.HttpRequest) -> func.HttpResponse:

    user_id = req.route_params.get("user_id")

    users = {
        "1": {
            "id": 1,
            "name": "Veera",
            "email": "veera@example.com",
            "role": "DevOps Engineer"
        },
        "2": {
            "id": 2,
            "name": "Ravi",
            "email": "ravi@example.com",
            "role": "Python Developer"
        }
    }

    user = users.get(user_id)

    if user is None:
        return func.HttpResponse(
            json.dumps({
                "error": "User not found",
                "user_id": user_id
            }),
            status_code=404,
            mimetype="application/json"
        )

    return func.HttpResponse(
        json.dumps(user),
        status_code=200,
        mimetype="application/json"
    )


# --------------------------------------------------
# 4. Create User
# URL: POST /api/users
# --------------------------------------------------
@app.route(
    route="users",
    methods=["POST"],
    auth_level=func.AuthLevel.ANONYMOUS
)
def create_user(req: func.HttpRequest) -> func.HttpResponse:

    try:
        data = req.get_json()
    except ValueError:
        return func.HttpResponse(
            json.dumps({
                "error": "Invalid JSON"
            }),
            status_code=400,
            mimetype="application/json"
        )

    name = data.get("name")
    email = data.get("email")
    role = data.get("role")

    if not name or not email or not role:
        return func.HttpResponse(
            json.dumps({
                "error": "name, email and role are required"
            }),
            status_code=400,
            mimetype="application/json"
        )

    new_user = {
        "id": 4,
        "name": name,
        "email": email,
        "role": role
    }

    return func.HttpResponse(
        json.dumps({
            "message": "User created successfully",
            "user": new_user
        }),
        status_code=201,
        mimetype="application/json"
    )
