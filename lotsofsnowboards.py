#!/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Brand, Base, Snowboard, User

engine = create_engine('sqlite:///brandsnowboard.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543' +
             '/18debd694829ed78203a5a36dd364160_400x400.png', id="1")
session.add(User1)
session.commit()

# Snowboards for RIDE
brand1 = Brand(name="Ride")

session.add(brand1)
session.commit()

snowboard1 = Snowboard(name="Machete", style="Freestyle", brand=brand1, user=User1)

session.add(snowboard1)
session.commit()

snowboard2 = Snowboard(name="Berzerker", style="Freestyle", brand=brand1, user=User1)

session.add(snowboard2)
session.commit()

snowboard3 = Snowboard(name="Alter Ego", style="Freeride", brand=brand1, user=User1)

session.add(snowboard3)
session.commit()

snowboard4 = Snowboard(name="Rapture", style="All-Mountain", brand=brand1, user=User1)

session.add(snowboard4)
session.commit()

snowboard5 = Snowboard(name="Promise", style="All-Mountain", brand=brand1, user=User1)

session.add(snowboard5)
session.commit()

snowboard6 = Snowboard(name="OMG", style="Freestyle", brand=brand1, user=User1)

session.add(snowboard6)
session.commit()

snowboard7 = Snowboard(name="Timeless", style="Powder", brand=brand1, user=User1)

session.add(snowboard7)
session.commit()

snowboard8 = Snowboard(name="Helix", style="Park", brand=brand1, user=User1)

session.add(snowboard8)
session.commit()


# Snowboards for Arbor
brand2 = Brand(name="Arbor")

session.add(brand1)
session.commit()

snowboard1 = Snowboard(name="Cask", style="Powder", brand=brand2)

session.add(snowboard1)
session.commit()

snowboard2 = Snowboard(name="Clovis", style="Powder", brand=brand2)

session.add(snowboard2)
session.commit()

snowboard3 = Snowboard(name="Swoon Rocker", style="All-Mountain", brand=brand2)

session.add(snowboard3)
session.commit()

snowboard4 = Snowboard(name="Poparazzi", style="All-Mountain", brand=brand2)

session.add(snowboard4)
session.commit()

snowboard5 = Snowboard(name="Whiskey", style="All-Mountain", brand=brand2)

session.add(snowboard5)
session.commit()

snowboard6 = Snowboard(name="Westmark Camber", style="Park", brand=brand2)

session.add(snowboard6)
session.commit()


# Snowboards for Burton
brand3 = Brand(name="Burton")

session.add(brand1)
session.commit()

snowboard1 = Snowboard(name="Talent Scout", style="Park", brand=brand3)

session.add(snowboard1)
session.commit()

snowboard2 = Snowboard(name="Day Trader", style="Powder", brand=brand3)

session.add(snowboard2)
session.commit()

snowboard3 = Snowboard(name="Rewind", style="Park", brand=brand3)

session.add(snowboard3)
session.commit()

snowboard4 = Snowboard(name="Stick Shift", style="Powder", brand=brand3)

session.add(snowboard4)
session.commit()

snowboard5 = Snowboard(name="Hideaway", style="All-Mountain", brand=brand3)

session.add(snowboard5)
session.commit()

snowboard6 = Snowboard(name="Stylus", style="All-Mountain", brand=brand3)

session.add(snowboard6)
session.commit()

snowboard7 = Snowboard(name="Flight Attendant", style="Freeride", brand=brand3)

session.add(snowboard7)
session.commit()

snowboard8 = Snowboard(name="Process Off-Axis",
                       style="Freestyle", brand=brand3)

session.add(snowboard8)
session.commit()

# Snowboards for Salomon
brand4 = Brand(name="Salomon")

session.add(brand1)
session.commit()

snowboard1 = Snowboard(name="Villain", style="Freestyle", brand=brand4)

session.add(snowboard1)
session.commit()

snowboard2 = Snowboard(name="Gypsy", style="Freestyle", brand=brand4)

session.add(snowboard2)
session.commit()

snowboard3 = Snowboard(name="Pulse", style="Freestyle", brand=brand4)

session.add(snowboard3)
session.commit()

snowboard4 = Snowboard(name="Ace", style="All-Mountain", brand=brand4)

session.add(snowboard4)
session.commit()

snowboard5 = Snowboard(name="Titan", style="All-Mountain", brand=brand4)

session.add(snowboard5)
session.commit()

snowboard6 = Snowboard(name="Oh Yeah", style="Freestyle", brand=brand4)

session.add(snowboard6)
session.commit()

snowboard7 = Snowboard(name="Speedway", style="Powder", brand=brand4)

session.add(snowboard7)
session.commit()

# Snowboards for K2
brand5 = Brand(name="K2")

session.add(brand1)
session.commit()

snowboard1 = Snowboard(name="Standard", style="Freestyle", brand=brand5)

session.add(snowboard1)
session.commit()

snowboard2 = Snowboard(name="Raygun", style="Freestyle", brand=brand5)

session.add(snowboard2)
session.commit()

snowboard3 = Snowboard(name="Carveair", style="Freeride", brand=brand5)

session.add(snowboard3)
session.commit()

snowboard4 = Snowboard(name="Vandal", style="All-Mountain", brand=brand5)

session.add(snowboard4)
session.commit()

snowboard5 = Snowboard(name="Happy Hour", style="All-Mountain", brand=brand5)

session.add(snowboard5)
session.commit()

snowboard6 = Snowboard(name="Manifest", style="Freestyle", brand=brand5)

session.add(snowboard6)
session.commit()

snowboard7 = Snowboard(name="Joydriver", style="Powder", brand=brand5)

session.add(snowboard7)
session.commit()

snowboard8 = Snowboard(name="Afterblack", style="Park", brand=brand5)

session.add(snowboard8)
session.commit()

print "Done!"
