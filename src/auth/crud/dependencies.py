from .repository import UserRepository, LinksRepository, ProfilesRepository
from .service import UserService
from src.config.crud import Service


def user_service():
    return UserService(UserRepository)


def profiles_service():
    return Service(ProfilesRepository)


def links_service():
    return Service(LinksRepository)
