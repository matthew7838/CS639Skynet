# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# class MyspiderItem(scrapy.Item):
#
#     pass

class OrbitalfocusItem(scrapy.Item):
    cat_no = scrapy.Field()
    designation = scrapy.Field()
    name = scrapy.Field()
    date = scrapy.Field()

class ReentrypredictorItem(scrapy.Item):
    object = scrapy.Field()
    #name = scrapy.Field()
    mission = scrapy.Field()
    reentry_type = scrapy.Field()
    launch_date = scrapy.Field()
    predicted_reentry_date = scrapy.Field()
    norad_num = scrapy.Field()
    cospar_num = scrapy.Field()

class Planet4589Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    JCAT = scrapy.Field()
    Satcat = scrapy.Field()
    Piece = scrapy.Field()
    Type = scrapy.Field()
    Name = scrapy.Field()
    PLName = scrapy.Field()
    LDate = scrapy.Field()
    Parent = scrapy.Field()
    SDate = scrapy.Field()
    Primary = scrapy.Field()
    DDate = scrapy.Field()
    Status = scrapy.Field()
    Dest = scrapy.Field()
    Owner = scrapy.Field()
    State = scrapy.Field()
    Manufacturer = scrapy.Field()
    Bus = scrapy.Field()
    Motor = scrapy.Field()
    Mass = scrapy.Field()
    MassFlag = scrapy.Field()
    DryMass = scrapy.Field()
    DryFlag = scrapy.Field()
    TotMass = scrapy.Field()
    TotFlag = scrapy.Field()
    Length = scrapy.Field()
    LFlag = scrapy.Field()
    Diameter = scrapy.Field()
    DFlag = scrapy.Field()
    Span = scrapy.Field()
    SpanFlag = scrapy.Field()
    Shape = scrapy.Field()
    ODate = scrapy.Field()
    Perigee = scrapy.Field()
    PF = scrapy.Field()
    Apogee = scrapy.Field()
    AF = scrapy.Field()
    Inc = scrapy.Field()
    IF = scrapy.Field()
    OpOrbit = scrapy.Field()
    OQUAL = scrapy.Field()
    AltNames = scrapy.Field()
    data_status = scrapy.Field()

class UcsdataItem(scrapy.Item):
    full_name = scrapy.Field()
    official_name = scrapy.Field()
    country = scrapy.Field()
    owner_country = scrapy.Field()
    owner = scrapy.Field()
    users = scrapy.Field()
    purpose = scrapy.Field()
    detail_purpose = scrapy.Field()
    orbit_class = scrapy.Field()
    orbit_type = scrapy.Field()
    in_geo = scrapy.Field()
    perigee = scrapy.Field()
    apogee = scrapy.Field()
    eccentricity = scrapy.Field()
    inclination = scrapy.Field()
    period = scrapy.Field()
    mass = scrapy.Field()
    dry_mass = scrapy.Field()
    power = scrapy.Field()
    launch_date = scrapy.Field()
    expected_lifetime = scrapy.Field()
    contractor = scrapy.Field()
    contractor_country = scrapy.Field()
    launch_site = scrapy.Field()
    launch_vehicle = scrapy.Field()
    cospar = scrapy.Field()
    norad = scrapy.Field()
    source = scrapy.Field()
    additional_source = scrapy.Field()
    data_status = scrapy.Field()

class NtwoYOItem(scrapy.Item):
    NORAD = scrapy.Field()
    Period = scrapy.Field()
