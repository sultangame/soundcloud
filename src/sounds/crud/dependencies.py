from src.config.crud import Service
from .repository import SoundRepository


def sound_service():
    return Service(SoundRepository)
