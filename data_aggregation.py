#import here
import pandas as pd
from pathlib import Path

csv_folder = Path("csv")
listing_files = sorted(csv_folder.glob("CRMLSListing*.csv"))
sold_files = sorted(
    f for f in csv_folder.glob("CRMLSSold*.csv")
    if "_filled" not in f.name
)

listing_data = []
for file in listing_files:
    df = pd.read_csv(file, low_memory=False)
    print(file.name, len(df))
    listing_data.append(df)
    
sold_data = []
for file in sold_files:
    df = pd.read_csv(file, low_memory=False)
    print(file.name, len(df))
    sold_data.append(df)
    
listings = pd.concat(
    listing_data,
    ignore_index=True,
    sort=False
)
sold = pd.concat(
    sold_data, 
    ignore_index=True,
    sort=False)

print(f"Combined Listings: {len(listings):,} rows")
print(f"Combined Sold:     {len(sold):,} rows")

listings_before = len(listings)
sold_before = len(sold)

listings = listings[listings["PropertyType"] == "Residential"]
sold = sold[sold["PropertyType"] == "Residential"]

print("Listings before:", listings_before)
print("Listings after:", len(listings))
print()
print(f"Sold Before Filter:     {sold_before:,}")
print(f"Sold After Filter:      {len(sold):,}")

listings.to_csv("combined_listings.csv", index=False)
sold.to_csv("combined_sold.csv", index=False)

print("combined_listings.csv")
print("combined_sold.csv")