import csv

from Collision import Collision
from Event import Event

collisions = []

events = []

new_hours = []


def read_source_file(file_name, hour_file_name):
    with open(file_name, 'r') as readCollision:  # r represent read model
        print("Start to read file: " + file_name + ". This may take a while...")
        file = csv.reader(readCollision)
        for row in file:
            if "COLLISION_ID" not in row[0]:
                collision = Collision()
                collision.collision_id = row[0]
                collision.location_key = row[1]
                collision.hour_key = row[2]
                collision.weather_key = row[3]
                collision.environment = row[4]
                collision.light = row[5]
                collision.surface_condition = row[6]
                collision.traffic_control = row[7]
                collision.traffic_control_condition = row[8]
                collision.collision_classification = row[9]
                collision.impace_type = row[10]
                collision.no_of_pedestrians = row[11]
                collision.date = row[12]
                collision.location = row[13]
                collisions.append(collision)
    readCollision.close()

    with open(hour_file_name, 'r') as readHour:  # r represent read model
        print("Start to read file: " + hour_file_name + ". This may take a while...")
        file = csv.reader(readHour)
        for row in file:
            if "EVENT_ID" not in row[0]:
                event = Event()
                event.event_id = row[0]
                event.event_name = row[1]
                event.event_start_date = row[2]
                event.event_end_date = row[3]
                if int(event.event_start_date.split("-")[0]) > int(event.event_end_date.split("-")[0]):
                    raise Exception("Wrong event time - event starting date must be earlier than event ending date: "
                                    "START:" + event.event_start_date + " compare to END:" + event.event_end_date)
                if int(event.event_start_date.split("-")[1]) > int(event.event_end_date.split("-")[1]):
                    raise Exception("Wrong event time - event starting date must be earlier than event ending date: "
                                    "START:" + event.event_start_date + " compare to END:" + event.event_end_date)
                if int(event.event_start_date.split("-")[2]) > int(event.event_end_date.split("-")[2]):
                    raise Exception("Wrong event time - event starting date must be earlier than event ending date: "
                                    "START:" + event.event_start_date + " compare to END:" + event.event_end_date)
                events.append(event)
    readHour.close()


def generate_surrogate_key_and_remove_duplicate():
    key_ctr = 0
    print("Start to generate surrogate key in event dim table and collision table")
    if events[0].event_name != "No Special Event":
        raise Exception("Missing default event!")
    for event in events:
        event.event_key = key_ctr
        key_ctr = key_ctr + 1
        for collision in collisions:
            time_stemp = collision.date.split(" ")[0]
            y = int(time_stemp.split("-")[0])
            m = int(time_stemp.split("-")[1])
            d = int(time_stemp.split("-")[2])

            ys = int(event.event_start_date.split("-")[0])
            ms = int(event.event_start_date.split("-")[1])
            ds = int(event.event_start_date.split("-")[2])

            ye = int(event.event_end_date.split("-")[0])
            me = int(event.event_end_date.split("-")[1])
            de = int(event.event_end_date.split("-")[2])

            if y <= ye and m <= me and d <= de and y >= ys and m >= ms and d >= ds and event.event_id != 0 and event.event_key != 0:
                collision.event_key = event.event_key
    print("Finished processing in event dim table and collision table. Start to deal with NULL")
    for collision in collisions:
        if collision.event_key == "":
            collision.event_key = 0


def output_collision_data_from_list_to_new_csv(file_name, output_dim_table_name):
    """
    This method stores the given list_to_store into the file_name csv file. The file will be created if does not exist.
    :param file_name: the name of the new file. The file name SHOULD NOT CONTAINS .CSV which will be added automatically
    """
    with open(file_name + ".csv", 'w', newline='') as csvFile:
        print("Prepare to write the data into the file: " + file_name + ". It might take a while...")
        writer = csv.writer(csvFile)
        writer.writerow(["COLLISION_ID", "LOCATION_ID", "HOUR_KEY", "WEATHER_KEY", "EVENT_KEY", "ENVIRONMENT",
                         "LIGHT", "SURFACE_CONDITION", "TRAFFIC_CONTROL", "TRAFFIC_CONTROL_CONDITION",
                         "COLLISION_CLASSIFICATION", "IMPACT_TYPE", "NO_OF_PEDESTRIANS", "TIME_STAMP"])
        for collision in collisions:
            writer.writerow([collision.collision_id, collision.location_key, collision.hour_key,
                             collision.weather_key, collision.event_key, collision.environment, collision.light,
                             collision.surface_condition, collision.traffic_control,
                             collision.traffic_control_condition, collision.collision_classification,
                             collision.impace_type, collision.no_of_pedestrians, collision.date])
    csvFile.close()

    with open(output_dim_table_name + ".csv", 'w', newline='') as csvFile:
        print("Prepare to write the data into the file: " + file_name + ". It might take a while...")
        writer = csv.writer(csvFile)
        writer.writerow(["EVENT_KEY", "EVENT_NAME", "EVENT_START_DATE", "EVENT_END_DATE"])
        for event in events:
            writer.writerow([event.event_key, event.event_name, event.event_start_date, event.event_end_date])
    csvFile.close()

    print("Finished the writing!")


def data_staging_phase_four(input_file_name, dim_table_name, output_file_name, output_dim_table_name):
    read_source_file(input_file_name, dim_table_name)
    print("Finished reading, start sorting")
    temp_collisions = sorted(collisions, key=lambda x: x.hour_id)
    temp_events = sorted(events, key=lambda x: x.event_id)
    print("Finished sorting")
    collisions.clear()
    events.clear()
    collisions.extend(temp_collisions)
    events.extend(temp_events)
    print("Start generate surrogate key and remove duplicate")
    generate_surrogate_key_and_remove_duplicate()
    output_collision_data_from_list_to_new_csv(output_file_name, output_dim_table_name)
