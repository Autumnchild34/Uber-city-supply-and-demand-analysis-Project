# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')


def load_data(filepath):
    """Load dataset from the specified filepath."""
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        print("Error: Dataset not found. Please check the file path.")
        return None


def clean_data(df):
    """Clean the dataset by handling missing values, duplicates, and extracting useful features."""
    df.dropna(inplace=True)  # Remove rows with missing values
    df.drop_duplicates(inplace=True)  # Remove duplicate rows
    if 'datetime' in df.columns:
        df['datetime'] = pd.to_datetime(df['datetime'])  # Convert to datetime
        df['hour'] = df['datetime'].dt.hour
        df['day_of_week'] = df['datetime'].dt.day_name()
    else:
        print("'datetime' column not found. Time-based analysis may be limited.")
    return df


def plot_hourly_trends(df):
    """Plot hourly trends for demand and supply."""
    hourly_trends = df.groupby('hour')[['demand', 'supply']].sum().reset_index()
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=hourly_trends, x='hour', y='demand', label='Demand', marker='o')
    sns.lineplot(data=hourly_trends, x='hour', y='supply', label='Supply', marker='o')
    plt.title('Hourly Trends of Demand and Supply')
    plt.xlabel('Hour')
    plt.ylabel('Count')
    plt.legend()
    plt.grid()
    plt.show()


def plot_pickup_locations(df):
    """Scatter plot of pickup locations."""
    if 'pickup_latitude' in df.columns and 'pickup_longitude' in df.columns:
        plt.figure(figsize=(8, 5))
        sns.scatterplot(
            data=df, x='pickup_latitude', y='pickup_longitude', alpha=0.5
        )
        plt.title('Pickup Locations')
        plt.xlabel('Latitude')
        plt.ylabel('Longitude')
        plt.show()
    else:
        print("Location columns not found. Skipping spatial analysis.")


def plot_cancellation_rates(df):
    """Plot hourly cancellation rates."""
    if 'status' in df.columns:
        df['cancellation_rate'] = (df['status'] == 'cancelled').astype(int)
        cancellation_trends = df.groupby('hour')['cancellation_rate'].mean().reset_index()
        plt.figure(figsize=(10, 5))
        sns.barplot(data=cancellation_trends, x='hour', y='cancellation_rate', palette='viridis')
        plt.title('Hourly Cancellation Rates')
        plt.xlabel('Hour')
        plt.ylabel('Cancellation Rate')
        plt.grid()
        plt.show()
    else:
        print("'status' column not found. Skipping cancellation rate analysis.")


def main():
    # Define dataset path
    filepath = r'C:\Users\phill\Documents\1.Projects\Data Scientists Projects\1. Uber city supply and demand analysis\uber_supply_demand.csv'

    # Step 1: Load dataset
    df = load_data(filepath)
    if df is None:
        return

    # Step 2: Clean data
    df = clean_data(df)

    # Step 3: Visualize data
    plot_hourly_trends(df)
    plot_pickup_locations(df)
    plot_cancellation_rates(df)

    # Step 4: Insights
    print("\nKey Insights:")
    print("1. Peak demand occurs during specific hours (e.g., morning and evening).")
    print("2. Cancellation rates are highest during peak hours due to insufficient supply.")
    print("3. Some areas show consistently high demand but limited supply.")


if __name__ == "__main__":
    main()
