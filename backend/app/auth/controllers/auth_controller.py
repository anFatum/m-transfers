from http import HTTPStatus

from flask import current_app, request
from flask_restplus import Resource

from backend.app.auth.utils.dto import AuthDto
from backend.app.core.utils.logger import get_logger
from backend.app.auth.utils.auth_provider import get_auth_provider

api = AuthDto.api
logger = get_logger("app")


@api.route("/sign-in")
class SignInResource(Resource):

    @api.doc("sign-in", responses={
        HTTPStatus.OK: "Sign in successful",
        HTTPStatus.UNAUTHORIZED: "Wrong credentials"
    }, body=AuthDto.auth_model_input)
    @api.expect(AuthDto.auth_model_input, validate=True)
    @api.marshal_with(AuthDto.auth_model_response)
    def post(self):
        """
        Sign In endpoint, redirects to Auth provider login page
        """
        auth_provider = get_auth_provider(current_app.config['AUTH_TYPE'])
        user_token = auth_provider.retrieve_token(email=request.json.get('email'),
                                                  password=request.json.get('password'))
        return {"token": user_token}, HTTPStatus.OK
