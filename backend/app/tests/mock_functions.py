from faker import Faker


AZURE_TOKEN = None
fake = Faker()


def mock_tokens(mocker, user):
    mocker.patch(
        'app.auth.services.user_service.get_or_create_user',
        return_value=user
    )

