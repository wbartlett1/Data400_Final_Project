import os
from amadeus import Client
import pandas as pd
import datetime as dt
from datetime import timedelta
from amadeus import ResponseError
import time
import dropbox
from dropbox.exceptions import ApiError

def collect_cross_country_flights(api_key, api_secret, east_coast, west_coast, 
                                  days_ahead=30, airlines=['B6', 'F9', 'AS', 'HA', 'UA', 'AA', 'DL']):
    """
    Simple function to collect cross-country flight data.
    Only searches flights BETWEEN east and west coast (not within same coast).
    
    Args:
        api_key: Amadeus API key
        api_secret: Amadeus API secret
        east_coast: List of east coast airport codes
        west_coast: List of west coast airport codes
        days_ahead: Number of days ahead to search (default 30)
        airlines: List of airline codes to include. 
                 Defaults to ['B6', 'F9', 'AS', 'HA', 'UA', 'AA', 'DL']
                 Set to None to search all airlines.
    
    Returns: DataFrame with all flight data
    """
    
    # Initialize Amadeus client
    amadeus = Client(client_id=api_key, client_secret=api_secret)
    
    all_flights = []
    api_calls = 0
    
    # Create cross-country routes only (east-to-west and west-to-east)
    routes = []
    for east in east_coast:
        for west in west_coast:
            routes.append((east, west))  # East to West
            routes.append((west, east))  # West to East
    
    print(f"Starting collection for {len(routes)} cross-country routes...")
    if airlines:
        print(f"Filtering for airlines: {', '.join(airlines)}")
    print(f"This will make {len(routes) * days_ahead} API calls\n")
    
    # Loop through each route
    for route_num, (origin, destination) in enumerate(routes, 1):
        print(f"Route {route_num}/{len(routes)}: {origin} → {destination}")
        
        # Loop through each day
        for day in range(1, days_ahead + 1):
            departure_date = (dt.datetime.now() + timedelta(days=day)).strftime('%Y-%m-%d')
            api_calls += 1
            
            try:
                # Build API parameters
                params = {
                    'originLocationCode': origin,
                    'destinationLocationCode': destination,
                    'departureDate': departure_date,
                    'adults': 1,
                    'max': 50
                }
                
                # Add airline filter if specified
                if airlines:
                    params['includedAirlineCodes'] = ','.join(airlines)
                
                # Make API call
                response = amadeus.shopping.flight_offers_search.get(**params)
                
                # Capture collection timestamp for this API call
                collection_time = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Process each flight
                for offer in response.data:
                    segments = offer['itineraries'][0]['segments']
                    
                    # Get aircraft types for all segments
                    aircraft_types = [seg.get('aircraft', {}).get('code', 'Unknown') for seg in segments]
                    
                    # Get cabin class (from first traveler's first segment)
                    cabin_class = 'Unknown'
                    try:
                        cabin_class = offer['travelerPricings'][0]['fareDetailsBySegment'][0]['cabin']
                    except (KeyError, IndexError):
                        pass
                    
                    flight_info = {
                        'time_collected': collection_time,
                        'origin': origin,
                        'destination': destination,
                        'departure_date': departure_date,
                        'days_until_departure': day,
                        'price': float(offer['price']['total']),
                        'currency': offer['price']['currency'],
                        'airline': offer['validatingAirlineCodes'][0],
                        'number_of_stops': len(segments) - 1,
                        'departure_time': segments[0]['departure']['at'],
                        'arrival_time': segments[-1]['arrival']['at'],
                        'total_duration': offer['itineraries'][0]['duration'],
                        'aircraft_type': ','.join(aircraft_types),
                        'cabin_class': cabin_class,
                        'bookable_seats': offer.get('numberOfBookableSeats', None)
                    }
                    all_flights.append(flight_info)
                
                print(f"  Day {day}: Found {len(response.data)} flights")
                
            except ResponseError as error:
                print(f"  Day {day}: API Error - {error}")
            except Exception as e:
                print(f"  Day {day}: Error - {e}")
            
            time.sleep(1)  # Wait 1 second between calls
        
        print(f"  ✓ Completed {origin} → {destination}\n")
    
    print(f"\nCollection complete!")
    print(f"Total API calls: {api_calls}")
    print(f"Total flights collected: {len(all_flights)}")
    
    return pd.DataFrame(all_flights)


def upload_to_dropbox(file_path, dropbox_token, dropbox_folder="/flight_data"):
    """
    Upload a file to Dropbox
    
    Args:
        file_path: Local path to the file
        dropbox_token: Dropbox access token
        dropbox_folder: Destination folder in Dropbox (default: /flight_data)
    """
    try:
        dbx = dropbox.Dropbox(dropbox_token)
        
        # Get filename
        filename = os.path.basename(file_path)
        dropbox_path = f"{dropbox_folder}/{filename}"
        
        # Read file and upload
        with open(file_path, 'rb') as f:
            print(f"Uploading {filename} to Dropbox...")
            dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode.overwrite)
            print(f"✓ Successfully uploaded to {dropbox_path}")
            
    except ApiError as e:
        print(f"✗ Dropbox API error: {e}")
        raise
    except Exception as e:
        print(f"✗ Upload error: {e}")
        raise


if __name__ == "__main__":
    # Get Dropbox token from environment variable
    dropbox_token = os.environ.get('DROPBOX_ACCESS_TOKEN')
    
    if not dropbox_token:
        raise ValueError("DROPBOX_ACCESS_TOKEN not found in environment variables")
    
    # ⚠️ HARDCODED CREDENTIALS - Replace with your actual credentials
    api_key = "YOUR_API_KEY_HERE"
    api_secret = "YOUR_API_SECRET_HERE"
    
    # Define your airports
    east_coast = ['JFK', 'BOS', 'EWR', 'DCA', 'PHL']
    west_coast = ['LAX', 'SFO', 'SEA', 'PDX', 'SAN']
    
    # Collect data
    print("=" * 60)
    print("FLIGHT DATA COLLECTION STARTING")
    print("=" * 60)
    df = collect_cross_country_flights(
        api_key, 
        api_secret, 
        east_coast, 
        west_coast, 
        days_ahead=30
    )
    
    # Create temporary data directory
    os.makedirs('data', exist_ok=True)
    
    # Save with timestamp
    timestamp = dt.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'data/flight_data_{timestamp}.csv'
    df.to_csv(filename, index=False)
    
    print("=" * 60)
    print("COLLECTION COMPLETE")
    print("=" * 60)
    print(f"✓ Data saved locally to: {filename}")
    print(f"✓ Total records: {len(df)}")
    print(f"✓ Columns: {', '.join(df.columns.tolist())}")
    
    # Upload to Dropbox
    print("=" * 60)
    print("UPLOADING TO DROPBOX")
    print("=" * 60)
    upload_to_dropbox(filename, dropbox_token)
    
    print("=" * 60)
    print("ALL OPERATIONS COMPLETE")
    print("=" * 60)
