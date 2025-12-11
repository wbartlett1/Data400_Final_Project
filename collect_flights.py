import os
from amadeus import Client
import pandas as pd
import datetime as dt
from datetime import timedelta
from amadeus import ResponseError
import time
import dropbox
from dropbox.exceptions import ApiError

def collect_cross_country_flights(api_credentials_list, east_coast, west_coast, 
                                  days_ahead=30, airlines=['B6', 'F9', 'AS', 'HA', 'UA', 'AA', 'DL']):
    """
    Simple function to collect cross-country flight data.
    Only searches flights BETWEEN east and west coast (not within same coast).
    Rotates through multiple API credentials to avoid rate limits.
    Automatically skips exhausted API keys.
    
    Args:
        api_credentials_list: List of tuples [(api_key_1, api_secret_1), (api_key_2, api_secret_2), ...]
        east_coast: List of east coast airport codes
        west_coast: List of west coast airport codes
        days_ahead: Number of days ahead to search (default 30)
        airlines: List of airline codes to include. 
                 Defaults to ['B6', 'F9', 'AS', 'HA', 'UA', 'AA', 'DL']
                 Set to None to search all airlines.
    
    Returns: DataFrame with all flight data
    """
    
    all_flights = []
    api_calls = 0
    credential_index = 0
    exhausted_credentials = set()  # Track which credentials have hit limits
    
    # Create cross-country routes only (east-to-west and west-to-east)
    routes = []
    for east in east_coast:
        for west in west_coast:
            routes.append((east, west))  # East to West
            routes.append((west, east))  # West to East
    
    print(f"Starting collection for {len(routes)} cross-country routes...")
    print(f"Using {len(api_credentials_list)} different API credentials for rotation")
    if airlines:
        print(f"Filtering for airlines: {', '.join(airlines)}")
    print(f"This will make {len(routes) * days_ahead} API calls\n")
    
    # Loop through each route
    for route_num, (origin, destination) in enumerate(routes, 1):
        print(f"Route {route_num}/{len(routes)}: {origin} → {destination}")
        
        # Loop through each day
        for day in range(1, days_ahead + 1):
            departure_date = (dt.datetime.now() + timedelta(days=day)).strftime('%Y-%m-%d')
            
            # Try each credential until one works
            success = False
            attempts = 0
            max_attempts = len(api_credentials_list)
            
            while not success and attempts < max_attempts:
                # Find next non-exhausted credential
                while credential_index in exhausted_credentials and len(exhausted_credentials) < len(api_credentials_list):
                    credential_index = (credential_index + 1) % len(api_credentials_list)
                
                # Check if all credentials are exhausted
                if len(exhausted_credentials) >= len(api_credentials_list):
                    print(f"  ⚠️  All API credentials exhausted!")
                    break
                
                api_key, api_secret = api_credentials_list[credential_index]
                current_cred = credential_index + 1  # For display (1-indexed)
                
                # Initialize Amadeus client with current credentials
                amadeus = Client(client_id=api_key, client_secret=api_secret)
                
                api_calls += 1
                attempts += 1
                
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
                    
                    print(f"  Day {day}: Found {len(response.data)} flights (API key #{current_cred})")
                    success = True
                    
                    # Move to next credential for next call
                    credential_index = (credential_index + 1) % len(api_credentials_list)
                    
                except ResponseError as error:
                    # Get detailed error information
                    error_details = error.response.body if hasattr(error, 'response') else str(error)
                    error_code = error.code if hasattr(error, 'code') else 'unknown'
                    
                    # Check if it's a rate limit error
                    if 'rate limit' in str(error_details).lower() or error_code == 429 or 'quota' in str(error_details).lower():
                        print(f"  Day {day}: API key #{current_cred} exhausted (rate limit)")
                        exhausted_credentials.add(credential_index)
                        credential_index = (credential_index + 1) % len(api_credentials_list)
                    else:
                        # Print detailed error for debugging
                        print(f"  Day {day}: API Error [{error_code}] - {error_details}")
                        success = True
                        credential_index = (credential_index + 1) % len(api_credentials_list)
                        
                except Exception as e:
                    print(f"  Day {day}: Error - {e}")
                    success = True  # Don't retry on general errors
                    credential_index = (credential_index + 1) % len(api_credentials_list)
            
            # Small delay between calls
            if success:
                time.sleep(1)
        
        print(f"  ✓ Completed {origin} → {destination}")
        if exhausted_credentials:
            print(f"  📊 Exhausted API keys: {len(exhausted_credentials)}/{len(api_credentials_list)}\n")
        else:
            print()
    
    print(f"\nCollection complete!")
    print(f"Total API calls: {api_calls}")
    print(f"Total flights collected: {len(all_flights)}")
    if exhausted_credentials:
        print(f"⚠️  API keys exhausted: {len(exhausted_credentials)}/{len(api_credentials_list)}")
    
    return pd.DataFrame(all_flights)


def upload_to_dropbox(file_path, app_key, app_secret, refresh_token, dropbox_folder="/flight_data"):
    """
    Upload a file to Dropbox using refresh token (never expires)
    
    Args:
        file_path: Local path to the file
        app_key: Dropbox app key
        app_secret: Dropbox app secret
        refresh_token: Dropbox refresh token
        dropbox_folder: Destination folder in Dropbox (default: /flight_data)
    """
    try:
        # Create Dropbox client with refresh token
        dbx = dropbox.Dropbox(
            app_key=app_key,
            app_secret=app_secret,
            oauth2_refresh_token=refresh_token
        )
        
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
    # Get Dropbox credentials from environment variables
    dropbox_app_key = os.environ.get('DROPBOX_APP_KEY')
    dropbox_app_secret = os.environ.get('DROPBOX_APP_SECRET')
    dropbox_refresh_token = os.environ.get('DROPBOX_REFRESH_TOKEN')
    
    if not all([dropbox_app_key, dropbox_app_secret, dropbox_refresh_token]):
        raise ValueError("Missing Dropbox credentials in environment variables")
    
    # ⚠️ HARDCODED CREDENTIALS
    api_credentials = [
        ("tJXhK2xH0TNcJSYJP67uuv14b9xGUvAb", "z4OPCHJTAsLHQQvu"),
        ("KQThHXQfHxA8YaBIdXCm9cW9ZoJpwwV2", "GqLFKVvWBFoUhyiJ"),
        ("RAoNuXvgY1o9ssOCOUuB15GQm9BXYiJN", "BgFW0IWAHRI9Wnri"),
        ("tJXhK2xH0TNcJSYJP67uuv14b9xGUvAb", "z4OPCHJTAsLHQQvu"),
        ("ZdERRSGVdcQ63vPeog29OVrKcMruuLge", "yATj3fjTXHtGKiCi"),
        ("Yvoh1sbvlyJ9WqmC4UAxW9P7qFxuTc3r", "WYVrP3HsJDGw8yXQ"),
        ("CqrHPey2LwnT9xnT1v1SDb8yt8P8VfnK", "tyfWdsA6Kzi7hwQQ")
    ]
    
    # Define your airports
    east_coast = ['JFK', 'BOS', 'PHL']
    west_coast = ['LAX', 'SFO', 'SEA']
    
    # Collect data
    print("=" * 60)
    print("FLIGHT DATA COLLECTION STARTING")
    print("=" * 60)
    df = collect_cross_country_flights(
        api_credentials,
        east_coast, 
        west_coast, 
        days_ahead=14
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
    upload_to_dropbox(filename, dropbox_app_key, dropbox_app_secret, dropbox_refresh_token)
    
    print("=" * 60)
    print("ALL OPERATIONS COMPLETE")
    print("=" * 60)
