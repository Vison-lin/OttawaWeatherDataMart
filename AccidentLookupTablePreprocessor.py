import csv

import holidays as holidays

from Collision import Collision


def collision_processor(file_name):
    """
    Retrieve data about the time, in hour, of the ottawa's collision record from a csv file.
    :param file_name: the file to retrieve data
    """
    global total_record
    global total_valid_record
    collisions = []
    key_ctr = 0
    with open(file_name, 'r') as readData:  # r represent read model
        print("Start to read file: " + file_name + ". This may take a while...")
        file = csv.reader(readData)
        canada_holiday = holidays.CA();
        for row in file:
            if "COLLISION_ID" not in row[0]:
                collision = Collision()
                collision.collision_id = key_ctr
                key_ctr = key_ctr + 1
                collision.location = row[1]
                collision.longtitude = row[4]
                collision.latitude = row[5]
                collision.date = row[6]
                collision.time = row[7]
                environment = row[8]
                if row[8] == "":
                    environment = "Unknown"
                collision.environment = remove_prefix(environment, "Unknown")
                light = row[9]
                if row[9] == "":
                    light = "Unknown"
                collision.light = remove_prefix(light, "Unknown")
                surface_condition = row[10]
                if row[10] == "":
                    surface_condition = "Unknown"
                collision.surface_condition = remove_prefix(surface_condition, "Unknown")
                traffic_control = row[11]
                if row[11] == "":
                    traffic_control = "Unknown"
                collision.traffic_control = remove_prefix(traffic_control, "Unknown")
                traffic_control_condition = row[12]
                if row[12] == "":
                    if collision.traffic_control == "No control":
                        traffic_control_condition = "N/A"
                        collision.traffic_control_condition = traffic_control_condition
                    else:
                        traffic_control_condition = "Unknown"
                        collision.traffic_control_condition = traffic_control_condition
                else:
                    collision.traffic_control_condition = remove_prefix(traffic_control_condition, "Unknown")
                collision_classification = row[13]
                if row[13] == "":
                    collision_classification = "Unknown"
                collision.collision_classification = remove_prefix(collision_classification, "Unknown")
                impact_type = row[14]
                if row[14] == "":
                    impact_type = "Unknown"
                collision.impace_type = remove_prefix(impact_type, "Unknown")
                no_of_pedestrians = row[15]
                if row[14] == "":
                    no_of_pedestrians = -1
                collision.no_of_pedestrians = no_of_pedestrians
                collisions.append(collision)
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
        writer.writerow(["COLLISION_ID", "LOCATION", "LONGITUDE", "LATITUDE", "DATE", "TIME", "ENVIRONMENT",
                         "LIGHT", "SURFACE_CONDITION", "TRAFFIC_CONTROL", "TRAFFIC_CONTROL_CONDITION",
                         "COLLISION_CLASSIFICATION", "IMPACT_TYPE", "NO_OF_PEDESTRIANS"])
        for collision in list_to_store:
            writer.writerow([collision.collision_id, collision.location, collision.longtitude, collision.latitude,
                             collision.date, collision.time, collision.environment, collision.light,
                             collision.surface_condition, collision.traffic_control,
                             collision.traffic_control_condition, collision.collision_classification,
                             collision.impace_type, collision.no_of_pedestrians])
    csvFile.close()

    print("Finished the writing!")


def remove_prefix(string, replacement):
    string_list = string.split(" - ", 1)
    if len(string_list) != 2 and string != replacement:
        raise Exception("Wrong format: " + string)
    if string != replacement:
        string = string_list[1]
    else:
        string = replacement
    return string


list = collision_processor("2014collisionsfinal.xls.csv")
output_collision_data_from_list_to_new_csv("processed2014Collision", list)
