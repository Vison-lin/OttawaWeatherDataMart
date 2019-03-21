import csv
import sys

total_record = 0

total_valid_record = 0


def generate_weather_station_list():
    ottawaWeatherStationList = []  # global list for storing all the weather stations name that are in Ottawa

    with open('Station Inventory EN.csv', 'r') as readStations:  # r represent read model
        print("Start to read the stations...")
        reader = csv.reader(readStations)
        lines = list(reader)
        for line in lines:
            if ("OTTAWA" in line[0] or "RIDEAU" in line[0]) and "ONTARIO" in line[1]:
                # if is in Ontario and the station name contains OTTAWA or RIDEAU
                if "NOTTAWASAGA ISLAND" != line[0]:  # exclude the exception
                    ottawaWeatherStationList.append(line)
    readStations.close()
    print("Finished station reading.")
    return ottawaWeatherStationList


def read_ottawa_data_from_csv(file_name):
    """
    Retrieve data about the ottawa's weather record from a csv file.
    :param file_name: the file to retrieve data
    """
    global total_record
    global total_valid_record
    result_list = []
    total_ctr = 0
    valid_ctr = 0
    ottawaWeatherStationList = generate_weather_station_list()
    ottawaWeatherStationNameList = []
    for station in ottawaWeatherStationList:
        ottawaWeatherStationNameList.append(station[0])
    with open(file_name, 'r') as readData:  # r represent read model
        print("Start to read file: " + file_name + ". This may take a while...")
        file = csv.reader(readData)
        for row in file:
            total_ctr = total_ctr + 1
            sys.stdout.write("\r" + str(total_ctr) + " records have been processed!")
            sys.stdout.flush()
            if "Year" in row[1] and "Month" in row[2]:
                result_list.append(row)
            if "ONTARIO" in row[25]:  # if is Ontario's station
                if row[24] in ottawaWeatherStationNameList:  # if is Ottawa's station
                    result_list.append(row)
                    valid_ctr = valid_ctr + 1
    print("\nFinished loading data. Total of " + str(valid_ctr) + " data records retrieved!")
    total_record = total_record + total_ctr
    total_valid_record = total_valid_record + valid_ctr
    return result_list


def output_data_from_list_to_new_csv(file_name, list_to_store, num_of_row_per_file):
    """
    This method stores the given list_to_store into the file_name csv file. The file will be created if does not exist.
    :param file_name: the name of the new file. The file name SHOULD NOT CONTAINS .CSV which will be added automatically
    :param list_to_store: the list of content that needs to be stored into the csv file
    :param num_of_row_per_file: the number of row per file. A new file will be created and with sequence number attached to name after automatically.
    """

    def output_data_from_list_to_new_csv_helper(sub_file_name, sub_list_to_store):
        with open(sub_file_name + ".csv", 'w', newline='') as csvFile:
            print("Prepare to write the data into the file: " + sub_file_name + ". It might take a while...")
            writer = csv.writer(csvFile)
            writer.writerows(sub_list_to_store)
        csvFile.close()

    if len(list_to_store) > num_of_row_per_file:
        print("Start dividing files...")

        def chunk():
            for i in range(0, len(list_to_store), num_of_row_per_file):
                yield list_to_store[i: i + num_of_row_per_file]

        name_ctr = 0

        for sublist in chunk():
            if name_ctr == 0:
                print("start dividing the first sle")
            if name_ctr == 1:
                print("start dividing the second file")
            if name_ctr == 2:
                print("start dividing the third file")
            if name_ctr > 2:
                print("start dividing the " + str(name_ctr + 1) + "th file")
            if name_ctr != 0:
                output_data_from_list_to_new_csv_helper(file_name + "_" + str(name_ctr), sublist)
            else:
                output_data_from_list_to_new_csv_helper(file_name, sublist)
            name_ctr = name_ctr + 1

    else:
        output_data_from_list_to_new_csv_helper(file_name, list_to_store)

    print("Finished the writing!")
