import csv
import requests
import os
import time

# Directory listing for verification
directory = r'C:\Users\Yoni\Desktop\add_targets'
print(os.listdir(directory))

# Path to your CSV file
csv_file_path = r'C:\Users\Yoni\Desktop\add_targets\monitoring-client.csv'

# URL of the API endpoint
api_url = 'API_ADDRESS'

# Credentials for basic authentication
auth_credentials = ('admin', 'admin12')  # Replace with actual username and password

# Headers to ensure proper request format
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': '*/*'
}

# Read the CSV file and make POST requests
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    
    for row in csv_reader:
        ip_address = row['ip_address'].strip()  # Strip whitespace from IP addresses
        
        # Payload using 'hostname' as observed in the browser
        payload = {'hostname': ip_address}
        print("Payload sent:", payload)  # Debugging print statement
        
        try:
            # Send POST request with form data, headers, and basic authentication
            response = requests.post(api_url, data=payload, auth=auth_credentials, headers=headers)
            
            # Print the full response details for debugging
            print(f"Response for IP {ip_address}:")
            print(f"Status Code: {response.status_code}")
            print("Response Text:", response.text)  # Full response content
            
            # Check if the request was actually successful or duplicate
            if response.status_code == 200:
                if "Duplicate entry" in response.text:
                    print(f"{ip_address} is already configured, skipping.")
                elif "Invalid hostname or IP address" in response.text:
                    print(f"Failed to add {ip_address}: Invalid hostname or IP address")
                else:
                    print(f"Successfully added {ip_address}")
            else:
                print(f"Failed to add {ip_address}. Status Code: {response.status_code}, Response: {response.text}")
                
            # Optional delay to avoid rapid requests
            time.sleep(1)
            
        except requests.RequestException as e:
            print(f"An error occurred for IP {ip_address}: {e}")
