from sqlalchemy import Column, Integer, String, Text, DateTime
from .database import Base
from datetime import datetime
from flask_login import UserMixin


class Post(UserMixin, Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    intro = Column(String(100), nullable=False)
    text = Column(Text, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Post {self.id}>'