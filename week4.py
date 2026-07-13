#imports here
import pandas as pd

# Load datasets
listings = pd.read_csv("week3_listings_with_rates.csv", low_memory=False)
sold = pd.read_csv("week3_sold_with_rates.csv", low_memory=False)

# Convert date columns
date_columns = [
    "CloseDate",
    "PurchaseContractDate",
    "ListingContractDate",
    "ContractStatusChangeDate"
]

for col in date_columns:

    if col in sold.columns:
        sold[col] = pd.to_datetime(
            sold[col],
            errors="coerce"
        )

    if col in listings.columns:
        listings[col] = pd.to_datetime(
            listings[col],
            errors="coerce"
        )

# Convert numeric columns
numeric_columns = [
    "ClosePrice",
    "ListPrice",
    "OriginalListPrice",
    "LivingArea",
    "LotSizeAcres",
    "BedroomsTotal",
    "BathroomsTotalInteger",
    "DaysOnMarket",
    "YearBuilt",
    "Latitude",
    "Longitude"
]

for col in numeric_columns:

    if col in sold.columns:
        sold[col] = pd.to_numeric(
            sold[col],
            errors="coerce"
        )

    if col in listings.columns:
        listings[col] = pd.to_numeric(
            listings[col],
            errors="coerce"
        )

# Remove invalid values
sold_before = len(sold)

sold = sold[
    (sold["ClosePrice"] > 0) &
    (sold["LivingArea"] > 0) &
    (sold["DaysOnMarket"] >= 0) &
    (sold["BedroomsTotal"] >= 0) &
    (sold["BathroomsTotalInteger"] >= 0)
]

print("\nInvalid sold rows removed:",
      sold_before - len(sold))

listings_before = len(listings)

listings = listings[
    (listings["ListPrice"] > 0) &
    (listings["LivingArea"] > 0) &
    (listings["DaysOnMarket"] >= 0) &
    (listings["BedroomsTotal"] >= 0) &
    (listings["BathroomsTotalInteger"] >= 0)
]

print("Invalid listing rows removed:",
      listings_before - len(listings))

# Fill missing values
fill_columns = [
    "LivingArea",
    "LotSizeAcres",
    "BedroomsTotal",
    "BathroomsTotalInteger",
    "DaysOnMarket",
    "YearBuilt"
]

for col in fill_columns:

    if col in sold.columns:
        sold[col] = sold[col].fillna(
            sold[col].median()
        )

    if col in listings.columns:
        listings[col] = listings[col].fillna(
            listings[col].median()
        )

# Remove duplicate rows

sold_duplicates = sold.duplicated().sum()
listing_duplicates = listings.duplicated().sum()

print("\nDuplicate sold rows:", sold_duplicates)
print("Duplicate listing rows:", listing_duplicates)

sold = sold.drop_duplicates()
listings = listings.drop_duplicates()

# Remove unnecessary columns
drop_columns = [
    "year_month"
]

sold.drop(
    columns=[c for c in drop_columns if c in sold.columns],
    inplace=True
)

listings.drop(
    columns=[c for c in drop_columns if c in listings.columns],
    inplace=True
)

# Final summary
print("Data after cleaning")

print("Listings rows:", len(listings))
print("Sold rows:", len(sold))

print("\nRemaining Missing Values (Top 20)")

print(
    sold.isnull()
    .sum()
    .sort_values(ascending=False)
    .head(20)
)

print("\nFinal Data Types")

print(sold.dtypes)
# Save files
sold.to_csv(
    "week4_sold_cleaned.csv",
    index=False
)

listings.to_csv(
    "week4_listings_cleaned.csv",
    index=False
)