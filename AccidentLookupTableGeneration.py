import csv

from Collision import Collision


def accident_processor(collision_file_name, hour_file_name, location_file_name):
    """
    Retrieve data about the time, in hour, of the ottawa's collision record from a csv file.
    :param collision_file_name: The name of the collision file, which has been generated from preprocessor
    :param hour_file_name: The processed hour table file
    :param location_file_name: the processed location table file
    """
    global total_record
    global total_valid_record
    hours = []
    locations = []
    collisions = []
    with open(hour_file_name, 'r') as readHour:  # r represent read model
        print("Start to read file: " + hour_file_name + ". This may take a while...")
        file = csv.reader(readHour)
        for row in file:
            if "HOUR_ID" not in row[0]:
                hour_id = row[0]
                hours.append(hour_id)
    readHour.close()

    print("Finished reading data from hour table")

    with open(location_file_name, 'r') as readLocation:  # r represent read model
        print("Start to read file: " + location_file_name + ". This may take a while...")
        file = csv.reader(readLocation)
        for row in file:
            if "LOCATION_ID" not in row[0]:
                location_id = row[0]
                locations.append(location_id)
    readLocation.close()

    print("Finished reading data from location table")

    with open(collision_file_name, 'r') as readCollision:  # r represent read model
        print("Start to read file: " + collision_file_name + ". This may take a while...")
        file = csv.reader(readCollision)
        ptr = 0
        for row in file:
            if "COLLISION_ID" not in row[0]:
                collision = Collision()
                collision.collision_id = row[0]
                collision.location_id = locations[ptr]  # append corresponding id
                collision.hour_id = hours[ptr]  # append corresponding id
                collision.environment = row[6]
                collision.light = row[7]
                collision.surface_condition = row[8]
                collision.traffic_control = row[9]
                collision.traffic_control_condition = row[10]
                collision.collision_classification = row[11]
                collision.impace_type = row[12]
                collision.no_of_pedestrians = row[13]
                ptr = ptr + 1
                collisions.append(collision)
    readCollision.close()

    print("Finished processing collision table")

    return collisions


def output_collision_data_from_list_to_new_csv(file_name, list_to_store):
    """
    This method stores the given list_to_store into the file_name csv file. The file will be created if does not exist.
    :param file_name: the name of the new file. The file name SHOULD NOT CONTAINS .CSV which will be added automatically
    :param list_to_store: the list of content that needs to be stored into the csv file
    """
    with open(file_name + ".csv", 'w', newline='') as csvFile:
        print("Prepare to write the data into the file: " + file_name + ". It might take a while...")
        writer = csv.writer(csvFile)
        writer.writerow(["COLLISION_ID", "LOCATION_ID", "HOUR_ID", "ENVIRONMENT",
                         "LIGHT", "SURFACE_CONDITION", "TRAFFIC_CONTROL", "TRAFFIC_CONTROL_CONDITION",
                         "COLLISION_CLASSIFICATION", "IMPACT_TYPE", "NO_OF_PEDESTRIANS"])
        for collision in list_to_store:
            writer.writerow([collision.collision_id, collision.location_id, collision.hour_id,
                             collision.environment, collision.light,
                             collision.surface_condition, collision.traffic_control,
                             collision.traffic_control_condition, collision.collision_classification,
                             collision.impace_type, collision.no_of_pedestrians])
    csvFile.close()

    print("Finished the writing!")


def lookup_table_generation(collision, hour, location, output):
    list = accident_processor(collision, hour, location)
    output_collision_data_from_list_to_new_csv(output, list)
