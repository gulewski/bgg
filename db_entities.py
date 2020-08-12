from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Additionals(Base):
    __tablename__ = 'additionals'
    additional_id = Column(Integer, primary_key=True)
    additional_name = Column(String)

    def __repr__(self):
        return f'Additionals. ' \
               f'ID: {self.additional_id}, ' \
               f'name: {self.additional_name}'


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

    def __repr__(self):
        return f'Bgames. ' \
               f'ID: {self.bgame_id}, ' \
               f'title: {self.title}, ' \
               f'year: {self.year}, ' \
               f'min and max players: {self.min_players} {self.max_players}, ' \
               f'playtime, min and max: {self.playtime} {self.min_playtime} {self.max_playtime}, ' \
               f'age: {self.age}, ' \
               f'thumbnail and image: {self.thumbnail} {self.image}, ' \
               f'start of description: {self.description[:25]}, ' \
               f'end of description: {self.description[-25:]}, ' \
               f'rank: {self.rank}, ' \
               f'userrated: {self.userrated}, ' \
               f'averages: {self.average} {self.bayesaverage}'


class BgamesAdditionals(Base):
    __tablename__ = 'bgames_additionals'
    bgame_id = Column(Integer, primary_key=True)
    additional_id = Column(Integer, primary_key=True)
    additional_type = Column(String, primary_key=True)
    link_ref = Column(String)

    def __repr__(self):
        return f'BgamesAdditionals. ' \
               f'Bgame ID: {self.bgame_id}, ' \
               f'Additional ID: {self.additional_id}, ' \
               f'Additional type: {self.additional_type}, ' \
               f'link ref: {self.link_ref}'


class BgamesPeople(Base):
    __tablename__ = 'bgames_people'
    bgame_id = Column(Integer, primary_key=True)
    person_id = Column(Integer, primary_key=True)
    person_type = Column(String, primary_key=True)
    link_ref = Column(String)

    def __repr__(self):
        return f'BgamesPeople. ' \
               f'Bgame ID: {self.bgame_id}, ' \
               f'Person ID: {self.person_id}, ' \
               f'Person type: {self.person_type}, ' \
               f'link ref: {self.link_ref}'


class BgamesRelatedGames(Base):
    __tablename__ = 'bgames_related_games'
    bgame_id = Column(Integer, primary_key=True)
    related_game_id = Column(Integer, primary_key=True)
    related_game_type = Column(String, primary_key=True)
    link_ref = Column(String)

    def __repr__(self):
        return f'BgamesRelatedGames. ' \
               f'Bgame ID: {self.bgame_id}, ' \
               f'Related game ID: {self.related_game_id}, ' \
               f'Related game type: {self.related_game_type}, ' \
               f'link ref: {self.link_ref}'


class BgamesTags(Base):
    __tablename__ = 'bgames_tags'
    bgame_id = Column(Integer, primary_key=True)
    tag_id = Column(Integer, primary_key=True)
    tag_type = Column(String, primary_key=True)
    link_ref = Column(String)

    def __repr__(self):
        return f'BgamesTags. ' \
               f'Bgame ID: {self.bgame_id}, ' \
               f'Tag ID: {self.tag_id}, ' \
               f'Tag type: {self.tag_type}, ' \
               f'link ref: {self.link_ref}'


class People(Base):
    __tablename__ = 'people'
    person_id = Column(Integer, primary_key=True)
    person_name = Column(String)

    def __repr__(self):
        return f'People. ' \
               f'Person ID: {self.person_id}, ' \
               f'Person name: {self.person_name}'


class RelatedGames(Base):
    __tablename__ = 'related_games'
    related_game_id = Column(Integer, primary_key=True)
    related_game_name = Column(String)

    def __repr__(self):
        return f'RelatedGames. ' \
               f'Related Game ID: {self.related_game_id}, ' \
               f'Related Game name: {self.related_game_name}, '


class Tags(Base):
    __tablename__ = 'tags'
    tag_id = Column(Integer, primary_key=True)
    tag_name = Column(String)

    def __repr__(self):
        return f'Tags. ' \
               f'Tag ID: {self.tag_id}, ' \
               f'Tag name: {self.tag_name}, '
