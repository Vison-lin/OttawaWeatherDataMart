import csv
import sys

from Collision import Collision

collisions = []

weathers = []

weathers_in_month = {}

new_weathers = []


def read_source_file(file_name, weather_file_name):
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
                collision.location = row[12]
                collisions.append(collision)
    readCollision.close()

    with open(weather_file_name, 'r') as readWeather:  # r represent read model
        print("Start to read file: " + weather_file_name + ". This may take a while...")
        file = csv.reader(readWeather)
        key_ctr = 0
        for row in file:
            weathers.append(row)
            # print(row[0]+" @ "+row[24])
    readWeather.close()


def grouping_weather_data_by_year():
    weather_index = []
    print("Start indexing weather records")
    for weather in weathers:
        date = str(int(weather[1])) + "-" + str(int(weather[2]))
        if len(date.split("-")) != 2:
            raise Exception("Wrong data format: " + date)
        # new_date = "-".join(date.split(" ", 1)[0].split("-", 2)[:2])
        if date not in weather_index:
            weather_index.append(date)
            # print(date)
    print("Finished indexing, start to group weather records")
    ctr = 0
    l = len(weather_index)
    for index in weather_index:
        sys.stdout.write(
            "\r" + str(ctr) + "/" + str(l) + " index have been processed! Current processing index is: " + index)
        sys.stdout.flush()
        ctr = ctr + 1
        temp_list = []
        for weather in weathers:
            date = str(int(weather[1])) + "-" + str(int(weather[2]))
            if index == date:
                # print(index)
                temp_list.append(weather)
        weathers_in_month[index] = temp_list
    print("Finished grouping")


def generate_surrogate_key_and_remove_duplicate():
    grouping_weather_data_by_year()

    weather_key_ctr = 0

    ctr = 0
    l = len(collisions)
    for collision in collisions:
        founded = False
        ctr = ctr + 1
        weather_station = collision.location
        sys.stdout.write("\r" + str(ctr) + "/" + str(l) + " collision records have been processed!")
        sys.stdout.flush()
        date = collision.date
        date = "-".join(date.split(" ", 1)[0].split("-", 2)[:2])
        curr_weathers = weathers_in_month[date]
        temp_date = " ".join(collision.date.split(":")[0].split(" ", 2)) + ":00"
        for weather in curr_weathers:
            temp_h = str(int(weather[4].split(":")[0])) + ":" + "00"
            exact_date = str(int(weather[1])) + "-" + str(int(weather[2])) + "-" + str(int(weather[3])) + " " + temp_h
            # print("|"+temp_date + "| - - |" + exact_date+"|"+weather_station)
            if temp_date == exact_date and weather[24] == weather_station:
                if founded:
                    raise Exception("Duplicated weather data")
                founded = True
                collision.weather_key = weather_key_ctr
                row_id = [weather_key_ctr]  # generate the id for weather table
                row = row_id + weather  # add the generated id to the first row
                weather = row
                new_weathers.append(weather)
        if not founded:
            raise Exception("Missing weather data for: " + collision.date + "@ " + collision.location)
    print("Finished grouping!")

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
                         "WEATHER_STATION_STAMP"])
        for collision in collisions:
            writer.writerow([collision.collision_id, collision.location_key, collision.hour_key,
                             collision.environment, collision.light,
                             collision.surface_condition, collision.traffic_control,
                             collision.traffic_control_condition, collision.collision_classification,
                             collision.impace_type, collision.no_of_pedestrians, collision.date, collision.location])
    csvFile.close()

    with open(output_dim_table_name + ".csv", 'w', newline='') as dimCsvFile:
        print("Prepare to write the data into the file: " + output_dim_table_name + ". It might take a while...")
        writer = csv.writer(dimCsvFile)
        writer.writerow(["WEATHER_ID", "DATE", "YEAR", "MONTH", "DAY", "TIME", "TEMPERATURE_C", "TEMPERATURE_FLAG"
                                                                                                "DEW_POINT_TEMP_C",
                         "DEW_POINT_TEMP_FLAG", "REL_HUM", "REL_HUM_FLAG", "WIND_DIR",
                         "WIND_DIR_FLAG", "WIND_SPEED", "WIND_SPEED_FLAG", "VISIBILITY", "VISIBILITY_FLAG",
                         "STN_PRESS_KPA", "STN.PRESS.FLAG", "HMDX", "HMDX_FLAG", "WIND_CHILL", "WIND_CHILL_FLAG",
                         "WEATHER", "STATION_NAME", "STATION_PROVINCE"])
        writer.writerows(new_weathers)
    dimCsvFile.close()

    print("Finished the writing!")


def data_staging_phase_two(input_file_name, dim_table_name, output_file_name, output_dim_table_name):
    read_source_file(input_file_name, dim_table_name)
    # print("Finished reading, start sorting")
    # temp_collisions = sorted(collisions, key=lambda x: x.hour_id)
    # temp_locations = sorted(locations, key=lambda x: x.location_id)
    # print("Finished sorting")
    # collisions.clear()
    # locations.clear()
    # collisions.extend(temp_collisions)
    # locations.extend(temp_locations)
    print("Start generate surrogate key and remove duplicate")
    generate_surrogate_key_and_remove_duplicate()
    output_collision_data_from_list_to_new_csv(output_file_name, output_dim_table_name)


data_staging_phase_two("Staging_2_Main.csv", "copy_weather_data_season_same.csv", "Staging_3_Main",
                       "Staging_3_WEATHER")
