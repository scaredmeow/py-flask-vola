from flask import Flask, current_app
from supabase import create_client, Client, ClientOptions

supabase: Client = None


def init_app(app: Flask) -> None:
    global supabase
    with app.app_context():
        supabase = create_client(
            supabase_url=current_app.config["SUPABASE_URL"],
            supabase_key=current_app.config["SUPABASE_KEY"],
            options=ClientOptions(auto_refresh_token=False),
        )
        supabase.auth.sign_in_with_password(  # noqa
            {
                "email": current_app.config["SUPABASE_EMAIL"],
                "password": current_app.config["SUPABASE_PASSWORD"],
            }
        )
