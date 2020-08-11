from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Additionals(Base):
    __tablename__ = 'additionals'
    additional_id = Column(Integer, primary_key=True)
    additional_name = Column(String)


class Bgames(Base):
    __tablename__ = 'bgames'
    bgame_id = Column(Integer, primary_key=True)
    title = Column(String)
    year = Column(Integer)
    min_players = Column(Integer)
    max_players = Column(Integer)
    playtime = Column(Integer)
    min_playtime = Column(Integer)
    max_playtime = Column(Integer)
    age = Column(Integer)
    thumbnail = Column(String)
    image = Column(String)
    description = Column(String)
    rank = Column(Integer)
    userrated = Column(Integer)
    average = Column(Numeric)
    bayesaverage = Column(Numeric)


class BgamesAdditionals(Base):
    __tablename__ = 'bgames_additionals'
    bgame_id = Column(Integer, primary_key=True)
    additional_id = Column(Integer, primary_key=True)
    additional_type = Column(String, primary_key=True)
    link_ref = Column(String)


class BgamesPeople(Base):
    __tablename__ = 'bgames_people'
    bgame_id = Column(Integer, primary_key=True)
    person_id = Column(Integer, primary_key=True)
    person_type = Column(String, primary_key=True)
    link_ref = Column(String)


class BgamesRelatedGames(Base):
    __tablename__ = 'bgames_related_games'
    bgame_id = Column(Integer, primary_key=True)
    related_game_id = Column(Integer, primary_key=True)
    related_game_type = Column(String, primary_key=True)
    link_ref = Column(String)


class BgameTags(Base):
    __tablename__ = 'bgames_tags'
    bgame_id = Column(Integer, primary_key=True)
    tag_id = Column(Integer, primary_key=True)
    tag_type = Column(String, primary_key=True)
    link_ref = Column(String)


class People(Base):
    __tablename__ = 'people'
    person_id = Column(Integer, primary_key=True)
    person_name = Column(String)


class RelatedGames(Base):
    __tablename__ = 'related_games'
    related_game_id = Column(Integer, primary_key=True)
    related_game_name = Column(String)


class Tags(Base):
    __tablename__ = 'tags'
    tag_id = Column(Integer, primary_key=True)
    tag_name = Column(String)
