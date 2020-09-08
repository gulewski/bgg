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


# class Artists(Base):
#     __tablename__ = "artists"
#     artist_id = Column(Integer, primary_key=True)
#     artist_name = Column(String)
#     link = Column(String)
#
#     def __init__(self, artist_id, artist_name):
#         self.artist_id = artist_id
#         self.artist_name = artist_name
#         self.link = creds.LINK_REF_TEMPLATE + "boardgameartist/" + str(artist_id)
#
#     def __repr__(self):
#         return f"Artists.\n" \
#                f"ID: {self.artist_id},\n" \
#                f"Name: {self.artist_name},\n" \
#                f"Link: {self.link}"


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


# class Designers(Base):
#     __tablename__ = "designers"
#     designer_id = Column(Integer, primary_key=True)
#     designer_name = Column(String)
#     link = Column(String)
#
#     def __init__(self, designer_id, designer_name):
#         self.designer_id = designer_id
#         self.designer_name = designer_name
#         self.link = creds.LINK_REF_TEMPLATE + "boardgamedesigner/" + str(designer_id)
#
#     def __repr__(self):
#         return f"Designers.\n" \
#                f"ID: {self.designer_id},\n" \
#                f"Name: {self.designer_name},\n" \
#                f"Link: {self.link}"


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


class People(Base):
    __tablename__ = "people"
    person_id = Column(Integer, primary_key=True)
    person_name = Column(String)

    def __init__(self, person_id, person_name):
        self.person_id = person_id
        self.person_name = person_name

    def __repr__(self):
        return f"People.\n" \
               f"ID: {self.person_id},\n" \
               f"Name: {self.person_name}"


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
        return f"Bgames.\n" \
               f"ID: {self.bgame_id},\n" \
               f"title: {self.title},\n" \
               f"year: {self.year},\n" \
               f"min and max players: {self.min_players} {self.max_players},\n" \
               f"playtime, min and max: {self.playtime} {self.min_playtime} {self.max_playtime},\n" \
               f"age: {self.age},\n" \
               f"thumbnail and image: {self.thumbnail} {self.image},\n" \
               f"start of description: {self.description[:25]},\n" \
               f"end of description: {self.description[-25:]},\n" \
               f"rank: {self.rank},\n" \
               f"usersrated: {self.userrated},\n" \
               f"averages: {self.average} {self.bayesaverage}"


class BgamesAccessories(Base):
    __tablename__ = "bgames_accessories"
    bgame_id = Column(Integer, primary_key=True)
    accessory_id = Column(Integer, primary_key=True)

    def __init__(self, bgame_id, accessory_id):
        self.bgame_id = bgame_id
        self.accessory_id = accessory_id

    def __repr__(self):
        return f"BgamesAccessories.\n" \
               f"Bgame ID: {self.bgame_id},\n" \
               f"Accessory ID: {self.accessory_id}"


# class BgamesArtists(Base):
#     __tablename__ = "bgames_artists"
#     bgame_id = Column(Integer, primary_key=True)
#     artist_id = Column(Integer, primary_key=True)
#
#     def __init__(self, bgame_id, artist_id):
#         self.bgame_id = bgame_id
#         self.artist_id = artist_id
#
#     def __repr__(self):
#         return f"BgamesArtists.\n" \
#                f"Bgame ID: {self.bgame_id},\n" \
#                f"Artist ID: {self.artist_id}"


class BgamesCategories(Base):
    __tablename__ = "bgames_categories"
    bgame_id = Column(Integer, primary_key=True)
    category_id = Column(Integer, primary_key=True)

    def __init__(self, bgame_id, category_id):
        self.bgame_id = bgame_id
        self.category_id = category_id

    def __repr__(self):
        return f"BgamesCategories.\n" \
               f"Bgame ID: {self.bgame_id},\n" \
               f"Category ID: {self.category_id}"


# class BgamesDesigners(Base):
#     __tablename__ = "bgames_designers"
#     bgame_id = Column(Integer, primary_key=True)
#     designer_id = Column(Integer, primary_key=True)
#
#     def __init__(self, bgame_id, designer_id):
#         self.bgame_id = bgame_id
#         self.designer_id = designer_id
#
#     def __repr__(self):
#         return f"BgamesDesigners.\n" \
#                f"Bgame ID: {self.bgame_id},\n" \
#                f"Designer ID: {self.designer_id}"


class BgamesExpansions(Base):
    __tablename__ = "bgames_expansions"
    bgame_id = Column(Integer, primary_key=True)
    expansion_id = Column(Integer, primary_key=True)

    def __init__(self, bgame_id, expansion_id):
        self.bgame_id = bgame_id
        self.expansion_id = expansion_id

    def __repr__(self):
        return f"BgamesExpansions.\n" \
               f"Bgame ID: {self.bgame_id},\n" \
               f"Expansion ID: {self.expansion_id}"


class BgamesFamilies(Base):
    __tablename__ = "bgames_families"
    bgame_id = Column(Integer, primary_key=True)
    family_id = Column(Integer, primary_key=True)

    def __init__(self, bgame_id, family_id):
        self.bgame_id = bgame_id
        self.family_id = family_id

    def __repr__(self):
        return f"BgamesFamilies.\n" \
               f"Bgame ID: {self.bgame_id},\n" \
               f"Family ID: {self.family_id}"


class BgamesHonors(Base):
    __tablename__ = "bgames_honors"
    bgame_id = Column(Integer, primary_key=True)
    honor_id = Column(Integer, primary_key=True)

    def __init__(self, bgame_id, honor_id):
        self.bgame_id = bgame_id
        self.honor_id = honor_id

    def __repr__(self):
        return f"BgamesHonors.\n" \
               f"Bgame ID: {self.bgame_id},\n" \
               f"Honor ID: {self.honor_id}"


class BgamesIntegrations(Base):
    __tablename__ = "bgames_integrations"
    bgame_id = Column(Integer, primary_key=True)
    integration_id = Column(Integer, primary_key=True)

    def __init__(self, bgame_id, integration_id):
        self.bgame_id = bgame_id
        self.integration_id = integration_id

    def __repr__(self):
        return f"BgamesIntegrations.\n" \
               f"Bgame ID: {self.bgame_id},\n" \
               f"Integration ID: {self.integration_id}"


class BgamesMechanics(Base):
    __tablename__ = "bgames_mechanics"
    bgame_id = Column(Integer, primary_key=True)
    mechanic_id = Column(Integer, primary_key=True)

    def __init__(self, bgame_id, mechanic_id):
        self.bgame_id = bgame_id
        self.mechanic_id = mechanic_id

    def __repr__(self):
        return f"BgamesMechanics.\n" \
               f"Bgame ID: {self.bgame_id},\n" \
               f"Mechanic ID: {self.mechanic_id}"


class BgamesPeople(Base):
    __tablename__ = "bgames_people"
    bgame_id = Column(Integer, primary_key=True)
    person_id = Column(Integer, primary_key=True)
    person_type = Column(String)
    link = Column(String)

    def __init__(self, bgame_id, person_id, person_type):
        self.bgame_id = bgame_id
        self.person_id = person_id
        self.person_type = person_type
        self.link = creds.LINK_REF_TEMPLATE + person_type + "/" + str(person_id)

    def __repr__(self):
        return f"BgamesPeople.\n" \
               f"Bgame ID: {self.bgame_id},\n" \
               f"Person ID: {self.person_id},\n" \
               f"Person type: {self.person_type},\n" \
               f"Link: {self.link}"


class BgamesPodcasts(Base):
    __tablename__ = "bgames_podcasts"
    bgame_id = Column(Integer, primary_key=True)
    podcast_id = Column(Integer, primary_key=True)

    def __init__(self, bgame_id, podcast_id):
        self.bgame_id = bgame_id
        self.podcast_id = podcast_id

    def __repr__(self):
        return f"BgamesPodcasts.\n" \
               f"Bgame ID: {self.bgame_id},\n" \
               f"Podcast Episode ID: {self.podcast_id}"


class BgamesPublishers(Base):
    __tablename__ = "bgames_publishers"
    bgame_id = Column(Integer, primary_key=True)
    publisher_id = Column(Integer, primary_key=True)

    def __init__(self, bgame_id, publisher_id):
        self.bgame_id = bgame_id
        self.publisher_id = publisher_id

    def __repr__(self):
        return f"BgamesPublishers.\n" \
               f"Bgame ID: {self.bgame_id},\n" \
               f"Publisher ID: {self.publisher_id}"


class BgamesSubdomains(Base):
    __tablename__ = "bgames_subdomains"
    bgame_id = Column(Integer, primary_key=True)
    subdomain_id = Column(Integer, primary_key=True)

    def __init__(self, bgame_id, subdomain_id):
        self.bgame_id = bgame_id
        self.subdomain_id = subdomain_id

    def __repr__(self):
        return f"BgamesSubdomains.\n" \
               f"Bgame ID: {self.bgame_id},\n" \
               f"Subdomain ID: {self.subdomain_id}"


class BgamesVersions(Base):
    __tablename__ = "bgames_versions"
    bgame_id = Column(Integer, primary_key=True)
    version_id = Column(Integer, primary_key=True)

    def __init__(self, bgame_id, version_id):
        self.bgame_id = bgame_id
        self.version_id = version_id

    def __repr__(self):
        return f"BgamesVersions.\n" \
               f"Bgame ID: {self.bgame_id},\n" \
               f"Version ID: {self.version_id}"
