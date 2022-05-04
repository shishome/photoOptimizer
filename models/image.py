from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Image(Base):
    __tablename__ = "image"
    id = Column(String(250), primary_key=True)
    name = Column(String(10000))
    def __repr__(self):
        return f"Image(id={self.id!r}"