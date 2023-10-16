# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# class MyspiderItem(scrapy.Item):
#
#     pass

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
