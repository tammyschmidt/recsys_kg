from neomodel import StructuredNode, StringProperty, IntegerProperty, UniqueIdProperty, RelationshipTo, RelationshipFrom

class Country(StructuredNode):
    uid = UniqueIdProperty()
    country_id_source = IntegerProperty(unique_index=True, required=True)
    name = StringProperty(index=True)

    cities = RelationshipFrom('City', 'LOCATED_IN_COUNTRY')
    restaurants = RelationshipFrom('recsys_kg.models.restaurant.Restaurant', 'LOCATED_IN_COUNTRY')

    def __str__(self):
        return self.name or f"Country ID: {self.country_id_source}"

class City(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)

    country = RelationshipTo("Country", 'LOCATED_IN_COUNTRY')
    restaurants = RelationshipFrom('recsys_kg.models.restaurant.Restaurant', 'LOCATED_IN_CITY')

    def __str__(self):
        return self.name