from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Accessories(Base):
    __tablename__ = "accessories"
    accessory_id = Column(Integer, primary_key=True)
    accessory_name = Column(String)
    link_ref = Column(String)

    def __repr__(self):
        return f"Accessories. " \
               f"ID: {self.accessory_id}, " \
               f"name: {self.accessory_name}" \
               f"link ref: {self.link_ref}"


class Artists(Base):
    __tablename__ = "artists"
    artist_id = Column(Integer, primary_key=True)
    artist_name = Column(String)
    link_ref = Column(String)

    def __repr__(self):
        return f"Artists. " \
               f"ID: {self.artist_id}, " \
               f"name: {self.artist_name}" \
               f"link ref: {self.link_ref}"


class Bgames(Base):
    __tablename__ = "bgames"
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
    usersrated = Column(Integer)
    average = Column(Numeric)
    bayesaverage = Column(Numeric)

    def __repr__(self):
        return f"Bgames. " \
               f"ID: {self.bgame_id}, " \
               f"title: {self.title}, " \
               f"year: {self.year}, " \
               f"min and max players: {self.min_players} {self.max_players}, " \
               f"playtime, min and max: {self.playtime} {self.min_playtime} {self.max_playtime}, " \
               f"age: {self.age}, " \
               f"thumbnail and image: {self.thumbnail} {self.image}, " \
               f"start of description: {self.description[:25]}, " \
               f"end of description: {self.description[-25:]}, " \
               f"rank: {self.rank}, " \
               f"usersrated: {self.userrated}, " \
               f"averages: {self.average} {self.bayesaverage}"


class BgamesAccessories(Base):
    __tablename__ = "bgames_accessories"
    bgame_id = Column(Integer, primary_key=True)
    accessory_id = Column(Integer, primary_key=True)

    def __repr__(self):
        return f"BgamesAccessories. " \
               f"Bgame ID: {self.bgame_id}, " \
               f"Accessory ID: {self.accessory_id}"


class BgamesArtists(Base):
    __tablename__ = "bgames_artists"
    bgame_id = Column(Integer, primary_key=True)
    artist_id = Column(Integer, primary_key=True)

    def __repr__(self):
        return f"BgamesArtists. " \
               f"Bgame ID: {self.bgame_id}, " \
               f"Artist ID: {self.artist_id}"


class BgamesCategories(Base):
    __tablename__ = "bgames_categories"
    bgame_id = Column(Integer, primary_key=True)
    category_id = Column(Integer, primary_key=True)

    def __repr__(self):
        return f"BgamesCategories. " \
               f"Bgame ID: {self.bgame_id}, " \
               f"Category ID: {self.category_id}"


class BgamesDesigners(Base):
    __tablename__ = "bgames_designers"
    bgame_id = Column(Integer, primary_key=True)
    designer_id = Column(Integer, primary_key=True)

    def __repr__(self):
        return f"BgamesDesigners. " \
               f"Bgame ID: {self.bgame_id}, " \
               f"Designer ID: {self.designer_id}"


class BgamesExpansions(Base):
    __tablename__ = "bgames_expansions"
    bgame_id = Column(Integer, primary_key=True)
    expansion_id = Column(Integer, primary_key=True)

    def __repr__(self):
        return f"BgamesExpansions. " \
               f"Bgame ID: {self.bgame_id}, " \
               f"Expansion ID: {self.expansion_id}"


class BgamesFamilies(Base):
    __tablename__ = "bgames_families"
    bgame_id = Column(Integer, primary_key=True)
    family_id = Column(Integer, primary_key=True)

    def __repr__(self):
        return f"BgamesFamilies. " \
               f"Bgame ID: {self.bgame_id}, " \
               f"Family ID: {self.family_id}"


class BgamesHonors(Base):
    __tablename__ = "bgames_honors"
    bgame_id = Column(Integer, primary_key=True)
    honor_id = Column(Integer, primary_key=True)

    def __repr__(self):
        return f"BgamesHonors. " \
               f"Bgame ID: {self.bgame_id}, " \
               f"Honor ID: {self.honor_id}"


class BgamesIntegrations(Base):
    __tablename__ = "bgames_integrations"
    bgame_id = Column(Integer, primary_key=True)
    integration_id = Column(Integer, primary_key=True)

    def __repr__(self):
        return f"BgamesIntegrations. " \
               f"Bgame ID: {self.bgame_id}, " \
               f"Integration ID: {self.integration_id}"


class BgamesMechanics(Base):
    __tablename__ = "bgames_mechanics"
    bgame_id = Column(Integer, primary_key=True)
    mechanic_id = Column(Integer, primary_key=True)

    def __repr__(self):
        return f"BgamesMechanics. " \
               f"Bgame ID: {self.bgame_id}, " \
               f"Mechanic ID: {self.mechanic_id}"


class BgamesPodcasts(Base):
    __tablename__ = "bgames_podcasts"
    bgame_id = Column(Integer, primary_key=True)
    podcast_id = Column(Integer, primary_key=True)

    def __repr__(self):
        return f"BgamesPodcasts. " \
               f"Bgame ID: {self.bgame_id}, " \
               f"Podcast ID: {self.podcast_id}"


class BgamesPublishers(Base):
    __tablename__ = "bgames_publishers"
    bgame_id = Column(Integer, primary_key=True)
    publisher_id = Column(Integer, primary_key=True)

    def __repr__(self):
        return f"BgamesPublishers. " \
               f"Bgame ID: {self.bgame_id}, " \
               f"Publisher ID: {self.publisher_id}"


class BgamesSubdomains(Base):
    __tablename__ = "bgames_subdomains"
    bgame_id = Column(Integer, primary_key=True)
    subdomain_id = Column(Integer, primary_key=True)

    def __repr__(self):
        return f"BgamesSubdomains. " \
               f"Bgame ID: {self.bgame_id}, " \
               f"Subdomain ID: {self.subdomain_id}"


class BgamesVersions(Base):
    __tablename__ = "bgames_versions"
    bgame_id = Column(Integer, primary_key=True)
    version_id = Column(Integer, primary_key=True)

    def __repr__(self):
        return f"BgamesVersions. " \
               f"Bgame ID: {self.bgame_id}, " \
               f"Version ID: {self.version_id}"


class Categories(Base):
    __tablename__ = "categories"
    category_id = Column(Integer, primary_key=True)
    category_name = Column(String)
    link_ref = Column(String)

    def __repr__(self):
        return f"Categories. " \
               f"ID: {self.category_id}, " \
               f"name: {self.category_name}" \
               f"link ref: {self.link_ref}"


class Designers(Base):
    __tablename__ = "designers"
    designer_id = Column(Integer, primary_key=True)
    designer_name = Column(String)
    link_ref = Column(String)

    def __repr__(self):
        return f"Designers. " \
               f"ID: {self.designer_id}, " \
               f"name: {self.designer_name}" \
               f"link ref: {self.link_ref}"


class Expansions(Base):
    __tablename__ = "expansions"
    expansion_id = Column(Integer, primary_key=True)
    expansion_name = Column(String)
    link_ref = Column(String)

    def __repr__(self):
        return f"Expansions. " \
               f"ID: {self.expansion_id}, " \
               f"name: {self.expansion_name}" \
               f"link ref: {self.link_ref}"


class Families(Base):
    __tablename__ = "families"
    family_id = Column(Integer, primary_key=True)
    family_name = Column(String)
    link_ref = Column(String)

    def __repr__(self):
        return f"Families. " \
               f"ID: {self.family_id}, " \
               f"name: {self.family_name}" \
               f"link ref: {self.link_ref}"


class Honors(Base):
    __tablename__ = "honors"
    honor_id = Column(Integer, primary_key=True)
    honor_name = Column(String)
    link_ref = Column(String)

    def __repr__(self):
        return f"Honors. " \
               f"ID: {self.honor_id}, " \
               f"name: {self.honor_name}" \
               f"link ref: {self.link_ref}"


class Integrations(Base):
    __tablename__ = "integrations"
    integration_id = Column(Integer, primary_key=True)
    integration_name = Column(String)
    link_ref = Column(String)

    def __repr__(self):
        return f"Integrations. " \
               f"ID: {self.integration_id}, " \
               f"name: {self.integration_name}" \
               f"link ref: {self.link_ref}"


class Mechanics(Base):
    __tablename__ = "mechanics"
    mechanic_id = Column(Integer, primary_key=True)
    mechanic_name = Column(String)
    link_ref = Column(String)

    def __repr__(self):
        return f"Mechanics. " \
               f"ID: {self.mechanic_id}, " \
               f"name: {self.mechanic_name}" \
               f"link ref: {self.link_ref}"


class Podcasts(Base):
    __tablename__ = "podcasts"
    podcast_id = Column(Integer, primary_key=True)
    podcast_name = Column(String)
    link_ref = Column(String)

    def __repr__(self):
        return f"Podcasts. " \
               f"ID: {self.podcast_id}, " \
               f"name: {self.podcast_name}" \
               f"link ref: {self.link_ref}"


class Publishers(Base):
    __tablename__ = "publishers"
    publisher_id = Column(Integer, primary_key=True)
    publisher_name = Column(String)
    link_ref = Column(String)

    def __repr__(self):
        return f"Publishers. " \
               f"ID: {self.publisher_id}, " \
               f"name: {self.publisher_name}" \
               f"link ref: {self.link_ref}"


class Subdomains(Base):
    __tablename__ = "subdomains"
    subdomain_id = Column(Integer, primary_key=True)
    subdomain_name = Column(String)
    link_ref = Column(String)

    def __repr__(self):
        return f"Subdomains. " \
               f"ID: {self.subdomain_id}, " \
               f"name: {self.subdomain_name}" \
               f"link ref: {self.link_ref}"


class Versions(Base):
    __tablename__ = "versions"
    version_id = Column(Integer, primary_key=True)
    version_name = Column(String)
    link_ref = Column(String)

    def __repr__(self):
        return f"Versions. " \
               f"ID: {self.version_id}, " \
               f"name: {self.version_name}" \
               f"link ref: {self.link_ref}"
