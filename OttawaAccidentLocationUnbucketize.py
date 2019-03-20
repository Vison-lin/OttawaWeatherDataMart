import csv
import math
import sys

from DataFilter import generate_weather_station_list
from Location import Location
from NeighborhoodLookupTable import generate_neighborhood_lookup_table


def location_string_processor(file_name):
    """
    Retrieve data about the location of the ottawa's collision record from a csv file.
    :param file_name: the file to retrieve data
    """
    global total_record
    global total_valid_record
    locations = []
    total_ctr = 0
    neighborhoods = generate_neighborhood_lookup_table()
    weather_stations = generate_weather_station_list()
    with open(file_name, 'r') as readData:  # r represent read model
        print("Start to read file: " + file_name + ". This may take a while...")
        file = csv.reader(readData)
        for row in file:
            if "COLLISION_ID" not in row[0]:
                location = Location()
                total_ctr = total_ctr + 1
                sys.stdout.write("\r" + str(total_ctr) + " records have been processed!")
                sys.stdout.flush()
                location_str = row[1]
                is_at = False
                is_btwn = False;
                if "@" in location_str:
                    is_at = True
                if "btwn" in location_str:
                    is_btwn = True
                if is_at and is_btwn:
                    raise Exception("Unexpected format: have both btwn and @: " + location_str)

                if is_at:
                    substring = location_str.split("@", 1)
                    location.street_name = substring[0]
                    substring = substring[1]
                    if "@" in substring:
                        raise Exception("Contains more than one @ in location string: " + location_str)
                    substring = substring.split("/", 1)
                    if len(substring) == 2:
                        location.intersection_one = substring[0]
                        location.intersection_two = substring[1]
                    elif len(substring) == 1:
                        location.intersection_one = substring[0]
                        location.intersection_two = "N/A"
                    else:
                        raise Exception("Wrong format location address: " + location_str)
                if is_btwn:
                    substring = location_str.split("btwn", 1)
                    location.street_name = substring[0]
                    substring = substring[1]
                    if "@" in substring:
                        raise Exception("Contains more than one btwn in location string: " + location_str)
                    substring = substring.split("&", 1)
                    if len(substring) == 2:
                        location.intersection_one = substring[0]
                        location.intersection_two = substring[1]
                    elif len(substring) == 1:
                        location.intersection_one = substring[0]
                        location.intersection_two = "N/A"
                    else:
                        raise Exception("Wrong format location address: " + location_str)
                location.longitude = row[2]
                if ((int(float(location.longitude)) != -75) and (int(float(location.longitude)) != -76)):
                    raise Exception("Wrong longitude: [" + location.longitude + "], " + row[2])
                location.latitude = row[3]
                if int(float(location.latitude)) != 45 and int(float(location.latitude)) != 44:
                    raise Exception("Wrong latitude: " + row[3] + ", [" + location.latitude + "]")
                location.location_id = str(location.longitude) + str(location.latitude)
                shortest_dist = float("inf")
                for neighborhood in neighborhoods:
                    difflong = float(location.longitude) - neighborhood.longitude
                    difflati = float(location.latitude) - neighborhood.latitude
                    distance = math.sqrt(pow(difflong, 2) + pow(difflati, 2))
                    if distance < shortest_dist:
                        shortest_dist = distance
                        location.neighborhood = neighborhood.neighborhood
                shortest_dist = float("inf")
                for station in weather_stations:
                    difflong = float(location.longitude) - float(station[7])  # long
                    difflati = float(location.latitude) - float(station[6])  # lati
                    distance = math.sqrt(pow(difflong, 2) + pow(difflati, 2))
                    if distance < shortest_dist:
                        shortest_dist = distance
                        location.closest_weather_station = station[0]  # name
                locations.append(location)
    return locations


def output_data_from_list_to_new_csv(file_name, list_to_store):
    """
    This method stores the given list_to_store into the file_name csv file. The file will be created if does not exist.
    :param file_name: the name of the new file. The file name SHOULD NOT CONTAINS .CSV which will be added automatically
    :param list_to_store: the list of content that needs to be stored into the csv file
    """
    with open(file_name + ".csv", 'w', newline='') as csvFile:
        print("Prepare to write the data into the file: " + file_name + ". It might take a while...")
        writer = csv.writer(csvFile)
        writer.writerow(["LOCATION_ID", "STREET_NAME", "INTERSECTION_1", "INTERSECTION_2",
                         "LONGITUDE", "LATITUDE", "NEIGHBORHOOD", "CLOSEST_WEATHER_STATION_NAME"])
        for location in list_to_store:
            writer.writerow([location.location_id, location.street_name,
                             location.intersection_one, location.intersection_two, location.longitude,
                             location.latitude, location.neighborhood,
                             location.closest_weather_station])
    csvFile.close()

    print("Finished the writing!")


def unbucketizeLocationTable(file_name, output):
    list = location_string_processor(file_name)
    output_data_from_list_to_new_csv(output, list)
