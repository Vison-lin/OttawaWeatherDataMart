import csv
from datetime import date

import holidays as holidays

from Hour import Hour


def hour_string_processor(file_name):
    """
    Retrieve data about the time, in hour, of the ottawa's collision record from a csv file.
    :param file_name: the file to retrieve data
    """
    global total_record
    global total_valid_record
    times = []
    key_ctr = 0
    with open(file_name, 'r') as readData:  # r represent read model
        print("Start to read file: " + file_name + ". This may take a while...")
        file = csv.reader(readData)
        canada_holiday = holidays.CA();
        for row in file:
            if "COLLISION_ID" not in row[0]:
                hour = Hour()
                readDate = row[4]
                time = row[5]
                splited_date = readDate.split("-", 2)
                if len(splited_date) != 3:
                    raise Exception("Invalid date format: " + row[6])
                year = splited_date[0]
                month = splited_date[1]
                day = splited_date[2]
                day_of_week = date(int(year), int(month), int(day)).isoweekday()
                hour.day_of_week = day_of_week
                is_weekend = day_of_week == 6 or day_of_week == 7
                hour.hour_key = key_ctr
                key_ctr = key_ctr + 1
                time_period = time.split(" ", 1)[1]
                h = time.split(":", 1)[0]
                if "AM" in time_period:
                    hour.hour_start = h + ":00:00"
                    hour.hour_end = h + ":59:59"
                elif "PM" in time_period:
                    hour.hour_start = str((int(h) + 12)) + ":00:00"
                    hour.hour_end = str((int(h) + 12)) + ":59:59"
                else:
                    raise Exception("Wrong time format: " + time)
                hour.date = readDate
                hour.day = day
                hour.month = month
                hour.year = year
                hour.weekend = is_weekend
                if readDate in canada_holiday:
                    hour.holiday = True
                    hour.holiday_name = canada_holiday.get(readDate)
                else:
                    hour.holiday = False
                    hour.holiday_name = "N/A"
                hour.hour_id = hour.date + hour.hour_start
                times.append(hour)

    return times


def output_data_from_list_to_new_csv(file_name, list_to_store):
    """
    This method stores the given list_to_store into the file_name csv file. The file will be created if does not exist.
    :param file_name: the name of the new file. The file name SHOULD NOT CONTAINS .CSV which will be added automatically
    :param list_to_store: the list of content that needs to be stored into the csv file
    """
    with open(file_name + ".csv", 'w', newline='') as csvFile:
        print("Prepare to write the data into the file: " + file_name + ". It might take a while...")
        writer = csv.writer(csvFile)
        writer.writerow(["HOUR_KEY", "HOUR_ID", "HOUR_START", "HOUR_END", "DATE",
                         "DAY_OF_WEEK", "DAY", "MONTH", "YEAR", "WEEKEND", "HOLIDAY", "HOLIDAY_NAME"])
        for hour in list_to_store:
            writer.writerow([hour.hour_key, hour.hour_id, hour.hour_start, hour.hour_end, hour.date, hour.day_of_week,
                             hour.day, hour.month, hour.year, hour.weekend, hour.holiday, hour.holiday_name])
    csvFile.close()

    print("Finished the writing!")


list = hour_string_processor("processed2014Collision.csv")
output_data_from_list_to_new_csv("2014ProcessedCollisionHourList", list)
