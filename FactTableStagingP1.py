import csv

from Collision import Collision
from Hour import Hour

collisions = []

hours = []

new_hours = []


def read_source_file(file_name, hour_file_name):
    with open(file_name, 'r') as readCollision:  # r represent read model
        print("Start to read file: " + file_name + ". This may take a while...")
        file = csv.reader(readCollision)
        for row in file:
            if "COLLISION_ID" not in row[0]:
                collision = Collision()
                collision.collision_id = row[0]
                collision.location_id = row[1]
                collision.hour_id = row[2]
                collision.environment = row[3]
                collision.light = row[4]
                collision.surface_condition = row[5]
                collision.traffic_control = row[6]
                collision.traffic_control_condition = row[7]
                collision.collision_classification = row[8]
                collision.impace_type = row[9]
                collision.no_of_pedestrians = row[10]
                collisions.append(collision)
    readCollision.close()

    with open(hour_file_name, 'r') as readHour:  # r represent read model
        print("Start to read file: " + hour_file_name + ". This may take a while...")
        file = csv.reader(readHour)
        for row in file:
            if "HOUR_ID" not in row[0]:
                hour = Hour()
                hour.hour_id = row[0]
                hour.hour_start = row[1]
                hour.hour_end = row[2]
                hour.date = row[3]
                hour.day_of_week = row[4]
                hour.day = row[5]
                hour.month = row[6]
                hour.year = row[7]
                hour.weekend = row[8]
                hour.holiday = row[9]
                hour.holiday_name = row[10]
                hours.append(hour)
    readHour.close()


def generate_surrogate_key_and_remove_duplicate():
    prev_value = ""
    key_ctr = -1
    print("Start to remove duplicate in hour dim table")
    for hour in hours:
        curr_value = hour.hour_id
        if prev_value != curr_value:  # if not the same
            prev_value = curr_value
            key_ctr = key_ctr + 1
            hour.hour_key = key_ctr
            new_hours.append(hour)
        else:  # if the same
            hour.hour_key = key_ctr
    print("Finished processing in hour dim table, start to processing collision table")
    for collision in collisions:
        for hour in new_hours:
            if collision.hour_id == hour.hour_id:
                collision.hour_key = hour.hour_key  # replace the id with key
                if len(hour.month) == 1:
                    hour.month = "0" + hour.month
                if len(hour.month) > 2:
                    raise Exception("Invalid hour month format" + hour.month)
                if len(hour.day) == 1:
                    hour.day = "0" + hour.day
                if len(hour.day) > 2:
                    raise Exception("Invalid hour day format" + hour.day)
                collision.date = str(hour.year) + "-" + str(int(hour.month)) + "-" + str(int(hour.day)) + " " + str(
                    hour.hour_start)
    print("Finished processing collision table")


def output_collision_data_from_list_to_new_csv(file_name, output_dim_table_name):
    """
    This method stores the given list_to_store into the file_name csv file. The file will be created if does not exist.
    :param file_name: the name of the new file. The file name SHOULD NOT CONTAINS .CSV which will be added automatically
    """
    with open(file_name + ".csv", 'w', newline='') as csvFile:
        print("Prepare to write the data into the file: " + file_name + ". It might take a while...")
        writer = csv.writer(csvFile)
        writer.writerow(["COLLISION_ID", "LOCATION_ID", "HOUR_KEY", "ENVIRONMENT",
                         "LIGHT", "SURFACE_CONDITION", "TRAFFIC_CONTROL", "TRAFFIC_CONTROL_CONDITION",
                         "COLLISION_CLASSIFICATION", "IMPACT_TYPE", "NO_OF_PEDESTRIANS", "TIME_STAMP"])
        for collision in collisions:
            writer.writerow([collision.collision_id, collision.location_id, collision.hour_key,
                             collision.environment, collision.light,
                             collision.surface_condition, collision.traffic_control,
                             collision.traffic_control_condition, collision.collision_classification,
                             collision.impace_type, collision.no_of_pedestrians, collision.date])
    csvFile.close()

    with open(output_dim_table_name + ".csv", 'w', newline='') as dimCsvFile:
        print("Prepare to write the data into the file: " + output_dim_table_name + ". It might take a while...")
        writer = csv.writer(dimCsvFile)
        writer.writerow(["HOUR_KEY", "HOUR_START", "HOUR_END", "DATE",
                         "DAY_OF_WEEK", "DAY", "MONTH", "YEAR", "WEEKEND", "HOLIDAY", "HOLIDAY_NAME"])
        for hour in new_hours:
            writer.writerow([hour.hour_key, hour.hour_start, hour.hour_end, hour.date, hour.day_of_week,
                             hour.day, hour.month, hour.year, hour.weekend, hour.holiday, hour.holiday_name])
    dimCsvFile.close()

    print("Finished the writing!")


def data_staging_phase_one(input_file_name, dim_table_name, output_file_name, output_dim_table_name):
    read_source_file(input_file_name, dim_table_name)
    print("Finished reading, start sorting")
    temp_collisions = sorted(collisions, key=lambda x: x.hour_id)
    temp_hours = sorted(hours, key=lambda x: x.hour_id)
    print("Finished sorting")
    collisions.clear()
    hours.clear()
    collisions.extend(temp_collisions)
    hours.extend(temp_hours)
    print("Start generate surrogate key and remove duplicate")
    generate_surrogate_key_and_remove_duplicate()
    output_collision_data_from_list_to_new_csv(output_file_name, output_dim_table_name)

# data_staging_phase_one("LOOKUP_TABLE_2014.csv", "2014ProcessedCollisionHourList.csv", "Staging_1_Main",
#                        "Staging_1_Hour")
