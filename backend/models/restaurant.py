from neomodel import StructuredNode, StringProperty, IntegerProperty, FloatProperty, UniqueIdProperty, RelationshipTo
from .location import City, Country
from .cuisine import Cuisine

class Restaurant(StructuredNode):
    uid = UniqueIdProperty() # unique id for neo4j
    restaurant_id_source = StringProperty(unique_index=True, required=True) # yelp restaurant id
    name = StringProperty(required=True, index=True)
    address = StringProperty()
    location = StringProperty(crs='wgs-84') # user_latitude, user_longitude
    rating = FloatProperty(index=True)
    budget = StringProperty(index=True) # low, middle, high
    reviews_count = IntegerProperty(index=True)

    # relationship
    city = RelationshipTo("City", 'LOCATED_IN_CITY')
    country = RelationshipTo("Country", 'LOCATED_IN_COUNTRY')
    cuisines = RelationshipTo("Cuisine", 'SERVES_CUISINE')

    def __str__(self):
        return self.name