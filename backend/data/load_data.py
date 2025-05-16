import csv
import os
import traceback
from shapely.geometry import Point

from backend.models import Restaurant, City, Country, Cuisine
from neomodel import db, UniqueProperty


def clear_database_content():
    """Deletes all nodes and relationships in the database. Use with caution!"""
    print("Clearing existing database content...")
    db.cypher_query("MATCH (n) DETACH DELETE n")
    print("Database cleared.")


def install_all_model_labels():
    """Ensures all labels and indexes are created in the DB."""
    print("Installing labels and indexes for all models...")
    for model_cls in [Restaurant, City, Country, Cuisine]:
        try:
            print(f"Installing labels/indexes for {model_cls.__name__}...")
           # model_cls.install_labels()
        except Exception as e:
            print(f"Error installing labels for {model_cls.__name__}: {e}")
    print("Labels and indexes should now be installed.")


def load_restaurants_from_csv(filepath: str):
    """Loads restaurant data from a CSV file into the Neo4j database."""
    print(f"Starting data load from: {filepath}")
    install_all_model_labels()

    processed_count = 0
    error_count = 0
    try:
        with open(filepath, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row_number, row in enumerate(reader, 1):
                try:
                    with db.transaction:
                        source_country_id = int(row['country_id'])
                        country_node, _ = Country.nodes.get_or_create(source_country_id=source_country_id)

                        city_name = row['city'].strip()
                        city_node, city_created = City.nodes.get_or_create(name=city_name)
                        if city_created or not city_node.country.is_connected(country_node):
                            city_node.country.connect(country_node)

                        source_restaurant_id = row['restaurant_id']
                        restaurant_node, _ = Restaurant.nodes.get_or_create(
                            source_restaurant_id=source_restaurant_id
                        )

                        restaurant_node.name = row['restaurant_name']
                        restaurant_node.address = row.get('user_address', '')

                        try:
                            lon = float(row['user_longitude'])
                            lat = float(row['user_latitude'])
                            restaurant_node.coordinates = Point(lon, lat)
                        except (ValueError, TypeError, KeyError):
                            restaurant_node.coordinates = None

                        try:
                            restaurant_node.rating = float(row['user_rating'])
                        except (ValueError, TypeError, KeyError):
                            restaurant_node.rating = None

                        restaurant_node.budget = row.get('user_budget', '')  # e.g., 'low', 'medium', 'high'

                        try:
                            restaurant_node.reviews_count = int(row['user_reviews'])
                        except (ValueError, TypeError, KeyError):
                            restaurant_node.reviews_count = None

                        restaurant_node.save()  # Important to persist changes

                        if not restaurant_node.city.is_connected(city_node):
                            restaurant_node.city.connect(city_node)
                        if not restaurant_node.country.is_connected(country_node):
                            restaurant_node.country.connect(country_node)

                        cuisine_names_str = row.get('user_cuisine', '')
                        if cuisine_names_str:
                            cuisine_names = [c.strip() for c in cuisine_names_str.split(',') if c.strip()]
                            for cuisine_name in cuisine_names:
                                cuisine_node, _ = Cuisine.nodes.get_or_create(name=cuisine_name)
                                if not restaurant_node.cuisines.is_connected(cuisine_node):
                                    restaurant_node.cuisines.connect(cuisine_node)

                    processed_count += 1
                    if processed_count % 100 == 0:  # Log progress every 100 rows
                        print(f"{processed_count} restaurants processed...")

                except UniqueProperty as e:
                    error_count += 1
                    print(
                        f"Error (UniqueProperty) in CSV row {row_number} (Restaurant ID: {row.get('restaurant_id', 'N/A')}): {e}")
                except Exception as e_row:
                    error_count += 1
                    print(
                        f"General error in CSV row {row_number} (Restaurant ID: {row.get('restaurant_id', 'N/A')}): {e_row}")
                    traceback.print_exc()

        print(f"\nData loading finished.")
        print(f"  Successfully processed restaurants: {processed_count}")
        print(f"  Rows with errors: {error_count}")

    except FileNotFoundError:
        print(f"ERROR: CSV file not found at {filepath}")
    except Exception as e_global:
        print(f"Global error during data loading: {e_global}")
        traceback.print_exc()


def print_some_data_examples():
    """Prints some example data from the database."""
    print("\n--- Example Data from Neo4j Database ---")

    try:
        print(f"\nTotal Restaurants: {len(Restaurant.nodes.all())}")
        print(f"Total Cities: {len(City.nodes.all())}")
        print(f"Total Countries: {len(Country.nodes.all())}")
        print(f"Total Cuisines: {len(Cuisine.nodes.all())}")

        print("\nSome Restaurants (max 5):")
        for restaurant in Restaurant.nodes.all()[:5]:
            city_name = restaurant.city.single().name if restaurant.city.single() else "N/A"
            country_display = "N/A"
            country_node_single = restaurant.country.single()
            if country_node_single:
                country_display = country_node_single.name or f"ID: {country_node_single.source_country_id}"

            cuisines_list = [c.name for c in restaurant.cuisines.all()]

            print(f"- {restaurant.name} (Source ID: {restaurant.source_restaurant_id})")
            print(f"  City: {city_name}, Country: {country_display}")
            print(f"  Rating: {restaurant.rating}, Budget: {restaurant.budget}, Reviews: {restaurant.reviews_count}")
            print(f"  Cuisines: {', '.join(cuisines_list) if cuisines_list else 'Not specified'}")
            if restaurant.coordinates:
                print(f"  Coordinates: (Lon: {restaurant.coordinates.x}, Lat: {restaurant.coordinates.y})")
            print("-" * 20)

        print("\nCities with Restaurant Counts (max 5 cities):")
        for city in City.nodes.all()[:5]:
            print(f"- {city.name}: {len(city.restaurants.all())} restaurant(s)")

        print("\nCuisines with Restaurant Counts (max 5 cuisines):")
        for cuisine in Cuisine.nodes.all()[:5]:
            print(f"- {cuisine.name}: {len(cuisine.restaurants.all())} restaurant(s)")

    except Exception as e:
        print(f"Error fetching example data: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    csv_file_path = os.path.join("../data/", 'restaurants.csv')

    if not os.path.exists(csv_file_path):
        print(f"ERROR: CSV file not found at {csv_file_path}")
        print("Please ensure 'restaurants.csv' exists in the project root directory.")
    else:
        SHOULD_CLEAR_DATABASE = False
        if SHOULD_CLEAR_DATABASE:
            clear_database_content()

        load_restaurants_from_csv(csv_file_path)

        print_some_data_examples()

    print("\nScript finished.")