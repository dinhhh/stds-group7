import xml.etree.ElementTree as ET
import csv
import os

def parse_stations(state="VIC", xml_file_path="data/weather/metadata/VIC_stations.xml"):
    """
    Parse STATE_stations.xml file to extract station names and IDs,
    then save to CSV with state field set to 'VIC'
    """
    # Path to the XML file    
    # Check if file exists
    if not os.path.exists(xml_file_path):
        print(f"Error: File {xml_file_path} not found")
        return
    
    # Parse the XML file
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
        return
    
    # List to store station data
    stations = []
    
    # Find all div elements with class "option" (both active and inactive)
    for div in root.iter('div'):
        div_class = div.get('class')
        if div_class and 'option' in div_class:
            station_name_elem = div.find('.//span[@class="stationName"]')
            station_id_elem = div.find('.//span[@class="stationId"]')
            
            if station_name_elem is not None and station_id_elem is not None:
                station_name = station_name_elem.text.strip() if station_name_elem.text else ""
                station_id = station_id_elem.text.strip() if station_id_elem.text else ""
                
                # Only add if both name and ID are not empty
                if station_name and station_id:
                    stations.append({
                        'station_name': station_name,
                        'station_id': station_id,
                        'state': state
                    })
    
    # Save to CSV file
    output_file = "data/weather/metadata/stations.csv"
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    try:
        with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['station_name', 'station_id', 'state']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header
            writer.writeheader()
            
            # Write station data
            for station in stations:
                writer.writerow(station)
        
        print(f"Successfully parsed {len(stations)} stations and saved to {output_file}")
        
    except IOError as e:
        print(f"Error writing to CSV file: {e}")

if __name__ == "__main__":
    # Delete the existing stations.csv file if it exists
    stations_csv_path = "data/weather/metadata/stations.csv"
    if os.path.exists(stations_csv_path):
        try:
            os.remove(stations_csv_path)
            print(f"Deleted existing file: {stations_csv_path}")
        except OSError as e:
            print(f"Error deleting file {stations_csv_path}: {e}")
    parse_stations(state="NSW", xml_file_path="data/weather/metadata/NSW_stations.xml")
    parse_stations(state="QLD", xml_file_path="data/weather/metadata/QLD_stations.xml")
    parse_stations(state="VIC", xml_file_path="data/weather/metadata/VIC_stations.xml")
