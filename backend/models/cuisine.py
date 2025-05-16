from neomodel import StructuredNode, StringProperty, UniqueIdProperty, RelationshipFrom

class Cuisine(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)

    restaurants = RelationshipFrom('recsys_kg.models.restaurant.Restaurant', 'SERVES_CUISINE')

    def __str__(self):
        return self.name