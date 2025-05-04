"""
-Focus on restaurants
-Criteria for recommending restaurants:
    => Similar cuisines
    => Similar price range
    => Nearby location
    => Good rating 
"""

import pandas as pd
import json

# Load Yelp business.json
data = []
with open('yelp_academic_dataset_business.json', 'r', encoding='utf-8') as f:
    for line in f:
        data.append(json.loads(line))

df = pd.DataFrame(data)

# Filter only restaurants
restaurants = df[df['categories'].str.contains('Restaurant', na=False)]

# Extract columns
restaurants_df = restaurants[['business_id', 'name', 'city', 'latitude', 'longitude', 'stars', 'review_count', 'attributes', 'categories']]

# Extract price_range
def get_price(attr):
    if isinstance(attr, dict):
        return attr.get('RestaurantsPriceRange2')
    return None

restaurants_df['price_range'] = restaurants_df['attributes'].apply(get_price)

# Create restaurants.csv
restaurants_final = restaurants_df[['business_id', 'name', 'city', 'latitude', 'longitude', 'price_range', 'stars', 'review_count', 'categories']]
restaurants_final.columns = ['restaurant_id', 'name', 'city', 'latitude', 'longitude', 'price_range', 'rating', 'review_count', 'categories']

# price_range is missing, convert to 0
restaurants_final['price_range'] = pd.to_numeric(restaurants_final['price_range'], errors='coerce').fillna(0).astype(int)
# Convert categories to list
restaurants_final['category_list'] = restaurants_final['categories'].apply(lambda x: [cat.strip() for cat in x.split(',')] if pd.notnull(x) else [])
restaurants_final.drop(columns=['categories'], inplace=True)

restaurants_final.to_csv('restaurants.csv', index=False)
