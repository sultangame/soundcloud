from fastapi_users.authentication import AuthenticationBackend, JWTStrategy, CookieTransport


SECRET = "SECRET"
cookie_transport = CookieTransport(cookie_max_age=3600)


def get_jwt_strategy():
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    get_strategy=get_jwt_strategy,
    transport=cookie_transport
)