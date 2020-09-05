from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base
import creds

Base = declarative_base()


class Accessories(Base):
    __tablename__ = "accessories"
    accessory_id = Column(Integer, primary_key=True)
    accessory_name = Column(String)
    link = Column(String)

    def __init__(self, accessory_id, accessory_name):
        self.accessory_id = accessory_id
        self.accessory_name = accessory_name
        self.link = creds.LINK_REF_TEMPLATE + "boardgameaccessory/" + str(accessory_id)

    def __repr__(self):
        return f"Accessories.\n" \
               f"ID: {self.accessory_id},\n" \
               f"Name: {self.accessory_name},\n" \
               f"Link: {self.link}"


class Artists(Base):
    __tablename__ = "artists"
    artist_id = Column(Integer, primary_key=True)
    artist_name = Column(String)
    link = Column(String)

    def __init__(self, artist_id, artist_name):
        self.artist_id = artist_id
        self.artist_name = artist_name
        self.link = creds.LINK_REF_TEMPLATE + "boardgameartist/" + str(artist_id)

    def __repr__(self):
        return f"Artists.\n" \
               f"ID: {self.artist_id},\n" \
               f"Name: {self.artist_name},\n" \
               f"Link: {self.link}"


class Bgames(Base):
    __tablename__ = "bgames"
    bgame_id = Column(Integer, primary_key=True)
    title = Column(String)
    yearpublished = Column(Integer)
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
    link = Column(String)

    def __init__(self, category_id, category_name):
        self.category_id = category_id
        self.category_name = category_name
        self.link = creds.LINK_REF_TEMPLATE + "boardgamecategory/" + str(category_id)

    def __repr__(self):
        return f"Categories.\n" \
               f"ID: {self.category_id},\n" \
               f"Name: {self.category_name},\n" \
               f"Link: {self.link}"


class Designers(Base):
    __tablename__ = "designers"
    designer_id = Column(Integer, primary_key=True)
    designer_name = Column(String)
    link = Column(String)

    def __init__(self, designer_id, designer_name):
        self.designer_id = designer_id
        self.designer_name = designer_name
        self.link = creds.LINK_REF_TEMPLATE + "boardgamedesigner/" + str(designer_id)

    def __repr__(self):
        return f"Designers.\n" \
               f"ID: {self.designer_id},\n" \
               f"Name: {self.designer_name},\n" \
               f"Link: {self.link}"


class Expansions(Base):
    __tablename__ = "expansions"
    expansion_id = Column(Integer, primary_key=True)
    expansion_name = Column(String)
    link = Column(String)

    def __init__(self, expansion_id, expansion_name):
        self.expansion_id = expansion_id
        self.expansion_name = expansion_name
        self.link = creds.LINK_REF_TEMPLATE + "boardgameexpansion/" + str(expansion_id)

    def __repr__(self):
        return f"Expansions.\n" \
               f"ID: {self.expansion_id},\n" \
               f"Name: {self.expansion_name},\n" \
               f"Link: {self.link}"


class Families(Base):
    __tablename__ = "families"
    family_id = Column(Integer, primary_key=True)
    family_name = Column(String)
    link = Column(String)

    def __init__(self, family_id, family_name):
        self.family_id = family_id
        self.family_name = family_name
        self.link = creds.LINK_REF_TEMPLATE + "boardgamefamily/" + str(family_id)

    def __repr__(self):
        return f"Families.\n" \
               f"ID: {self.family_id},\n" \
               f"Name: {self.family_name},\n" \
               f"Link: {self.link}"


class Honors(Base):
    __tablename__ = "honors"
    honor_id = Column(Integer, primary_key=True)
    honor_name = Column(String)
    link = Column(String)

    def __init__(self, honor_id, honor_name):
        self.honor_id = honor_id
        self.honor_name = honor_name
        self.link = creds.LINK_REF_TEMPLATE + "boardgamehonor/" + str(honor_id)

    def __repr__(self):
        return f"Honors.\n" \
               f"ID: {self.honor_id},\n" \
               f"Name: {self.honor_name},\n" \
               f"Link: {self.link}"


class Integrations(Base):
    __tablename__ = "integrations"
    integration_id = Column(Integer, primary_key=True)
    integration_name = Column(String)
    link = Column(String)

    def __init__(self, integration_id, integration_name):
        self.integration_id = integration_id
        self.integration_name = integration_name
        self.link = creds.LINK_REF_TEMPLATE + "boardgame/" + str(integration_id)

    def __repr__(self):
        return f"Integrations.\n" \
               f"ID: {self.integration_id},\n" \
               f"Name: {self.integration_name},\n" \
               f"Link: {self.link}"


class Mechanics(Base):
    __tablename__ = "mechanics"
    mechanic_id = Column(Integer, primary_key=True)
    mechanic_name = Column(String)
    link = Column(String)

    def __init__(self, mechanic_id, mechanic_name):
        self.mechanic_id = mechanic_id
        self.mechanic_name = mechanic_name
        self.link = creds.LINK_REF_TEMPLATE + "boardgamemechanic/" + str(mechanic_id)

    def __repr__(self):
        return f"Mechanics.\n" \
               f"ID: {self.mechanic_id},\n" \
               f"Name: {self.mechanic_name},\n" \
               f"Link: {self.link}"


class Podcasts(Base):
    __tablename__ = "podcasts"
    podcast_id = Column(Integer, primary_key=True)
    podcast_name = Column(String)
    link = Column(String)

    def __init__(self, podcast_id, podcast_name):
        self.podcast_id = podcast_id
        self.podcast_name = podcast_name
        self.link = creds.LINK_REF_TEMPLATE + "boardgamepodcastepisode/" + str(podcast_id)

    def __repr__(self):
        return f"Podcasts.\n" \
               f"ID: {self.podcast_id},\n" \
               f"Name: {self.podcast_name},\n" \
               f"Link: {self.link}"


class Publishers(Base):
    __tablename__ = "publishers"
    publisher_id = Column(Integer, primary_key=True)
    publisher_name = Column(String)
    link = Column(String)

    def __init__(self, publisher_id, publisher_name):
        self.publisher_id = publisher_id
        self.publisher_name = publisher_name
        self.link = creds.LINK_REF_TEMPLATE + "boardgamepublisher/" + str(publisher_id)

    def __repr__(self):
        return f"Publishers.\n" \
               f"ID: {self.publisher_id},\n" \
               f"Name: {self.publisher_name},\n" \
               f"Link: {self.link}"


class Subdomains(Base):
    __tablename__ = "subdomains"
    subdomain_id = Column(Integer, primary_key=True)
    subdomain_name = Column(String)
    link = Column(String)

    def __init__(self, subdomain_id, subdomain_name):
        self.subdomain_id = subdomain_id
        self.subdomain_name = subdomain_name
        self.link = creds.LINK_REF_TEMPLATE + "boardgamesubdomain/" + str(subdomain_id)

    def __repr__(self):
        return f"Subdomains.\n" \
               f"ID: {self.subdomain_id},\n" \
               f"Name: {self.subdomain_name},\n" \
               f"Link: {self.link}"


class Versions(Base):
    __tablename__ = "versions"
    version_id = Column(Integer, primary_key=True)
    version_name = Column(String)
    link = Column(String)

    def __init__(self, version_id, version_name):
        self.version_id = version_id
        self.version_name = version_name
        self.link = creds.LINK_REF_TEMPLATE + "boardgameversion/" + str(version_id)

    def __repr__(self):
        return f"Versions.\n" \
               f"ID: {self.version_id},\n" \
               f"Name: {self.version_name},\n" \
               f"Link: {self.link}"
