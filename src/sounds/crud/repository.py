from src.config.crud import SQLAlchemyRepository
from src.sounds import Sound


class SoundRepository(SQLAlchemyRepository):
    model = Sound
