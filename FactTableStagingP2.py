import csv

from Collision import Collision
from Location import Location

collisions = []

locations = []

new_locations = []


def read_source_file(file_name, locoation_file_name):
    with open(file_name, 'r') as readCollision:  # r represent read model
        print("Start to read file: " + file_name + ". This may take a while...")
        file = csv.reader(readCollision)
        for row in file:
            if "COLLISION_ID" not in row[0]:
                collision = Collision()
                collision.collision_id = row[0]
                collision.location_id = row[1]
                collision.hour_key = row[2]
                collision.environment = row[3]
                collision.light = row[4]
                collision.surface_condition = row[5]
                collision.traffic_control = row[6]
                collision.traffic_control_condition = row[7]
                collision.collision_classification = row[8]
                collision.impace_type = row[9]
                collision.no_of_pedestrians = row[10]
                collision.date = row[11]
                collisions.append(collision)
    readCollision.close()

    with open(locoation_file_name, 'r') as readLocation:  # r represent read model
        print("Start to read file: " + locoation_file_name + ". This may take a while...")
        file = csv.reader(readLocation)
        for row in file:
            if "LOCATION_ID" not in row[0]:
                location = Location()
                location.location_id = row[0]
                location.street_name = row[1]
                location.intersection_one = row[2]
                location.intersection_two = row[3]
                location.longitude = row[4]
                location.latitude = row[5]
                location.neighborhood = row[6]
                location.closest_weather_station = row[7]
                locations.append(location)
    readLocation.close()


def generate_surrogate_key_and_remove_duplicate():
    prev_value = ""
    key_ctr = -1
    print("Start to remove duplicate in hour dim table")
    for location in locations:
        curr_value = location.location_id
        if prev_value != curr_value:  # if not the same
            prev_value = curr_value
            key_ctr = key_ctr + 1
            location.location_key = key_ctr
            new_locations.append(location)
        else:  # if the same
            location.location_key = key_ctr
    print("Finished processing in hour dim table, start to processing collision table")
    for collision in collisions:
        for location in new_locations:
            if collision.location_id == location.location_id:
                collision.location_key = location.location_key  # replace the id with key
                collision.location = location.closest_weather_station  # temp use collision location to store closest weather station
                if location.intersection_one == "N/A" and location.intersection_two == "N/A":
                    collision.is_intersection = True
                else:
                    collision.is_intersection = False
    print("Finished processing collision table")


def output_collision_data_from_list_to_new_csv(file_name, output_dim_table_name):
    """
    This method stores the given list_to_store into the file_name csv file. The file will be created if does not exist.
    :param file_name: the name of the new file. The file name SHOULD NOT CONTAINS .CSV which will be added automatically
    """
    with open(file_name + ".csv", 'w', newline='') as csvFile:
        print("Prepare to write the data into the file: " + file_name + ". It might take a while...")
        writer = csv.writer(csvFile)
        writer.writerow(["COLLISION_ID", "LOCATION_KEY", "HOUR_KEY", "ENVIRONMENT",
                         "LIGHT", "SURFACE_CONDITION", "TRAFFIC_CONTROL", "TRAFFIC_CONTROL_CONDITION",
                         "COLLISION_CLASSIFICATION", "IMPACT_TYPE", "NO_OF_PEDESTRIANS", "TIME_STAMP",
                         "WEATHER_STATION_STAMP", "IS_INTERSECTION"])
        for collision in collisions:
            writer.writerow([collision.collision_id, collision.location_key, collision.hour_key,
                             collision.environment, collision.light,
                             collision.surface_condition, collision.traffic_control,
                             collision.traffic_control_condition, collision.collision_classification,
                             collision.impace_type, collision.no_of_pedestrians, collision.date, collision.location, collision.is_intersection])
    csvFile.close()

    with open(output_dim_table_name + ".csv", 'w', newline='') as dimCsvFile:
        print("Prepare to write the data into the file: " + output_dim_table_name + ". It might take a while...")
        writer = csv.writer(dimCsvFile)
        writer.writerow(["LOCATION_KEY", "STREET_NAME", "INTERSECTION_1", "INTERSECTION_2",
                         "LONGITUDE", "LATITUDE", "NEIGHBORHOOD", "CLOSEST_WEATHER_STATION_NAME"])
        for location in new_locations:
            writer.writerow([location.location_key, location.street_name,
                             location.intersection_one, location.intersection_two, location.longitude,
                             location.latitude, location.neighborhood,
                             location.closest_weather_station])
    dimCsvFile.close()

    print("Finished the writing!")


def data_staging_phase_two(input_file_name, dim_table_name, output_file_name, output_dim_table_name):
    read_source_file(input_file_name, dim_table_name)
    print("Finished reading, start sorting")
    temp_collisions = sorted(collisions, key=lambda x: x.hour_id)
    temp_locations = sorted(locations, key=lambda x: x.location_id)
    print("Finished sorting")
    collisions.clear()
    locations.clear()
    collisions.extend(temp_collisions)
    locations.extend(temp_locations)
    print("Start generate surrogate key and remove duplicate")
    generate_surrogate_key_and_remove_duplicate()
    output_collision_data_from_list_to_new_csv(output_file_name, output_dim_table_name)

# data_staging_phase_two("Staging_1_Main.csv", "2014ProcessedCollisionLocationList.csv", "Staging_2_Main",
#                        "Staging_2_Location")
