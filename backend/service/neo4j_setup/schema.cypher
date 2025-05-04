CREATE CONSTRAINT constraint_restaurant_id IF NOT EXISTS
FOR (r:Restaurant) REQUIRE r.id IS UNIQUE;

CREATE CONSTRAINT constraint_city_name IF NOT EXISTS
FOR (c:City) REQUIRE c.name IS UNIQUE;

CREATE CONSTRAINT constraint_category_name IF NOT EXISTS
FOR (cat:Category) REQUIRE cat.name IS UNIQUE;