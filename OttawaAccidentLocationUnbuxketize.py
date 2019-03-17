import csv
import sys

from Location import Location


def location_string_processor(file_name):
    """
    Retrieve data about the location of the ottawa's collision record from a csv file.
    :param file_name: the file to retrieve data
    """
    global total_record
    global total_valid_record
    locations = []
    total_ctr = 0
    key_ctr = 0
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
                location.location_key = key_ctr
                key_ctr = key_ctr + 1
                location.longitude = row[4]
                if ((int(float(location.longitude)) != -75) and (int(float(location.longitude)) != -76)):
                    raise Exception("Wrong longitude: [" + location.longitude + "], " + row[5])
                location.latitude = row[5]
                if int(float(location.latitude)) != 45 and int(float(location.latitude)) != 44:
                    raise Exception("Wrong latitude: " + row[4] + ", [" + location.latitude + "]")
                locations.append(location)
                location.neighborhood = "CURR:OTTAWA"

    return locations


def output_data_from_list_to_new_csv(file_name, list_to_store):
    """
    This method stores the given list_to_store into the file_name csv file. The file will be created if does not exist.
    :param file_name: the name of the new file. The file name SHOULD NOT CONTAINS .CSV which will be added automatically
    :param list_to_store: the list of content that needs to be stored into the csv file
    :param num_of_row_per_file: the number of row per file. A new file will be created and with sequence number attached to name after automatically.
    """
    with open(file_name + ".csv", 'w', newline='') as csvFile:
        print("Prepare to write the data into the file: " + file_name + ". It might take a while...")
        writer = csv.writer(csvFile)
        writer.writerow(["location_key", "street name", "intersection 1", "intersection 2",
                         "longitude", "latitude", "neighborhood"])
        for location in list_to_store:
            writer.writerow([location.location_key, location.street_name, location.intersection_one, location.intersection_two, location.longitude, location.latitude, location.neighborhood])
    csvFile.close()

    print("Finished the writing!")


list = location_string_processor("2014collisionsfinal.xls.csv")
output_data_from_list_to_new_csv("Hi", list)