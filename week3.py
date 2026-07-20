#imports here
import pandas as pd

# Load datasets
listings = pd.read_csv("week2_listings_cleaned.csv", low_memory=False)
sold = pd.read_csv("week2_sold_cleaned.csv", low_memory=False)

# Download Data
url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"

mortgage = pd.read_csv(url)

# Convert date column
mortgage["observation_date"] = pd.to_datetime(
    mortgage["observation_date"]
)

# Rename columns
mortgage.rename(
    columns={
        "observation_date": "date",
        "MORTGAGE30US": "rate_30yr_fixed"
    },
    inplace=True
)

# Create year-month
mortgage["year_month"] = mortgage["date"].dt.to_period("M")

# Monthly average
mortgage_monthly = (
    mortgage.groupby("year_month")["rate_30yr_fixed"]
    .mean()
    .reset_index()
)

mortgage_monthly = (
    mortgage.groupby("year_month")["rate_30yr_fixed"]
    .mean()
    .reset_index()
)

#merge keys
sold["CloseDate"] = pd.to_datetime(sold["CloseDate"])
listings["ListingContractDate"] = pd.to_datetime(
    listings["ListingContractDate"]
)

sold["year_month"] = sold["CloseDate"].dt.to_period("M")
listings["year_month"] = listings["ListingContractDate"].dt.to_period("M")

# Merge
sold = sold.merge(
    mortgage_monthly,
    on="year_month",
    how="left"
)

listings = listings.merge(
    mortgage_monthly,
    on="year_month",
    how="left"
)

# Validation
print("Missing mortgage rates (sold):")
print(sold["rate_30yr_fixed"].isnull().sum())

print("Missing mortgage rates (listings):")
print(listings["rate_30yr_fixed"].isnull().sum())

print(
    sold[
        [
            "CloseDate",
            "ClosePrice",
            "rate_30yr_fixed"
        ]
    ].head()
)

print(sold.memory_usage(deep=True).sum() / 1024**2, "MB")
print(listings.memory_usage(deep=True).sum() / 1024**2, "MB")
# Save files
sold.to_csv(
    "week3_sold_with_rates.csv.gz",
    index=False,
    compression="gzip"
)

listings.to_csv(
    "week3_listings_with_rates.csv.gz",
    index=False,
    compression="gzip"
)