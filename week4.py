#imports here
import pandas as pd

# Load datasets
listings = pd.read_csv("week3_listings_with_rates.csv.gz", low_memory=False)
sold = pd.read_csv("week3_sold_with_rates.csv.gz", low_memory=False)

sold_before = len(sold)
listings_before = len(listings)
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

#Fill missing values
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

# Date consistency flags
for df in [sold, listings]:

    if (
        "ListingContractDate" in df.columns and
        "CloseDate" in df.columns
    ):
        df["listing_after_close_flag"] = (
            df["ListingContractDate"] >
            df["CloseDate"]
        )

    if (
        "PurchaseContractDate" in df.columns and
        "CloseDate" in df.columns
    ):
        df["purchase_after_close_flag"] = (
            df["PurchaseContractDate"] >
            df["CloseDate"]
        )

    if (
        "ListingContractDate" in df.columns and
        "PurchaseContractDate" in df.columns
    ):
        df["negative_timeline_flag"] = (
            df["PurchaseContractDate"] <
            df["ListingContractDate"]
        )
        
# Geographic quality flags
for df in [sold, listings]:

    if (
        "Latitude" in df.columns and
        "Longitude" in df.columns
    ):

        df["missing_coordinates_flag"] = (
            df["Latitude"].isna() |
            df["Longitude"].isna()
        )

        df["zero_coordinates_flag"] = (
            (df["Latitude"] == 0) |
            (df["Longitude"] == 0)
        )

        df["positive_longitude_flag"] = (
            df["Longitude"] > 0
        )

        df["invalid_coordinate_flag"] = (
            (df["Latitude"] < 32) |
            (df["Latitude"] > 42) |
            (df["Longitude"] < -125) |
            (df["Longitude"] > -114)
        )
        
        
# Final summary
print("\n========== ROW COUNTS ==========")

print("Sold before cleaning:", sold_before)
print("Sold after cleaning :", len(sold))

print("Listings before cleaning:", listings_before)
print("Listings after cleaning :", len(listings))

print("\nDuplicates removed")
print("Sold:", sold_duplicates)
print("Listings:", listing_duplicates)

print("\n========== MISSING VALUES ==========")

print("\nSold")
print(
    sold.isnull()
    .sum()
    .sort_values(ascending=False)
    .head(20)
)

print("\nListings")
print(
    listings.isnull()
    .sum()
    .sort_values(ascending=False)
    .head(20)
)

print("\n-------- DATA TYPES ----------")

print("\nSold")
print(sold.dtypes)

print("\nListings")
print(listings.dtypes)

print("\n--------- DATE CONSISTENCY ----------")

for flag in [
    "listing_after_close_flag",
    "purchase_after_close_flag",
    "negative_timeline_flag"
]:

    if flag in sold.columns:
        print(flag, ":", sold[flag].sum())

print("\n--------- GEOGRAPHIC QUALITY ------------")

for flag in [
    "missing_coordinates_flag",
    "zero_coordinates_flag",
    "positive_longitude_flag",
    "invalid_coordinate_flag"
]:

    if flag in sold.columns:
        print(flag, ":", sold[flag].sum())
        
# Save files
sold.to_csv(
    "week4_sold_cleaned.csv",
    index=False
)

listings.to_csv(
    "week4_listings_cleaned.csv",
    index=False
)