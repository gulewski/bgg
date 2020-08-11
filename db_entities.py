from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class People(Base):
    __tablename__ = 'people'
    people_id = Column(Integer, primary_key=True)
    people_name = Column(String)