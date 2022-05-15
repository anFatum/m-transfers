from flask_restplus import Namespace, fields


class AuthDto:
    api = Namespace("Authentication", path="/", description="Authentication related "
                                                            "operations")
    auth_model_input = api.model("AuthInput", {
        "email": fields.String(required=True),
        "password": fields.String(required=True)
    })

    auth_model_response = api.model("AuthResponse", {
        "token": fields.String(readonly=True)
    })


class UserDto:
    api = Namespace("User API", path="/user", description="User related operations")
    user_model = api.model("User", {
        "id": fields.String(readonly=True),
        "email": fields.String(required=True),
        "name": fields.String(required=True),
        "password": fields.String(required=True, skip_none=True),
        "roles": fields.List(fields.String(), required=True),
        "accounts": fields.List(fields.Raw(), skip_none=True, readonly=True)
    })
