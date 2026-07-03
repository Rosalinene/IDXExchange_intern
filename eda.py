#imports here
import pandas as pd

# Load datasets
listings = pd.read_csv("combined_listings.csv", low_memory=False)
sold = pd.read_csv("combined_sold.csv", low_memory=False)

# Initial structure check
print("Listings shape:", listings.shape)
print("Sold shape:", sold.shape)

print(listings.columns)
print(sold.columns)

print(listings.head())
print(sold.head())

# Property type validation
print("Listings types:", listings["PropertyType"].unique())
print("Sold types:", sold["PropertyType"].unique())

# Filter Residential
listings_before = len(listings)
sold_before = len(sold)

listings = listings[listings["PropertyType"] == "Residential"]
sold = sold[sold["PropertyType"] == "Residential"]

print("Listings before:", listings_before)
print("Listings after:", len(listings))

print("Sold before:", sold_before)
print("Sold after:", len(sold))

# Missing value
missing_listings = listings.isnull().sum().sort_values(ascending=False)
missing_sold = sold.isnull().sum().sort_values(ascending=False)

print("\nListings missing values:")
print(missing_listings.head(20))

print("\nSold missing values:")
print(missing_sold.head(20))

print(missing_listings.head(20))
print(missing_sold.head(20))

#missing percent top 20%
missing_pct = (listings.isnull().mean() * 100).sort_values(ascending=False)

print("\nMissing top 20")
print(missing_pct.head(20))

#bad columns >90% missing
bad_cols = missing_pct[missing_pct > 90]

print("\nHigh missing column >90%")
print(bad_cols)

#stat sumary
print("\nStat Sumary")
cols = [
    "ClosePrice",
    "ListPrice",
    "LivingArea",
    "LotSizeAcres",
    "BedroomsTotal",
    "BathroomsTotalInteger",
    "DaysOnMarket",
    "YearBuilt"
]

print(listings[cols].describe())

#median and percentiles
print("Median Close Price:", listings["ClosePrice"].median())

print("\nPercentiles:")
print(listings["ClosePrice"].quantile([0.25, 0.5, 0.75, 0.95]))

#business analysis
# Residential share
print("\nResidential Share:")
print(listings["PropertyType"].value_counts(normalize=True))

# Days on market
print("\nDays on Market Summary:")
print(listings["DaysOnMarket"].describe())

# Above vs below list price
sold["above_list"] = sold["ClosePrice"] > sold["ListPrice"]

print("\nAbove vs Below List Price:")
print(sold["above_list"].value_counts(normalize=True))

#save files
listings.to_csv("week2_listings_cleaned.csv", index=False)
sold.to_csv("week2_sold_cleaned.csv", index=False)
