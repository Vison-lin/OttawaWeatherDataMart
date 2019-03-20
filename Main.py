import csv

from AccidentLookupTableGeneration import lookup_table_generation
from AccidentLookupTablePreprocessor import collision_processor, remove_prefix, \
    output_collision_data_from_list_to_new_csv
from Collision import Collision
from FactTableStagingP1 import data_staging_phase_one
from FactTableStagingP2 import data_staging_phase_two
from FactTableStagingP3 import data_staging_phase_three
from OttawaAccidentHourTableUnbucketize import unbucketizeHourTable
from OttawaAccidentLocationUnbucketize import unbucketizeLocationTable


def process_collision_table():
    list = collision_processor("2014collisionsfinal.xls.csv")
    list1 = collision_processor("2016collisionsfinal.xls.csv")
    list2 = collision_processor("2015collisionsfinal.xls.csv")

    collisions = []

    with open("h2017collisionsfinal.csv", 'r') as readData:  # r represent read model
        print("Start to read file: h2017collisionsfinal.csv. This may take a while...")
        file = csv.reader(readData)
        key_ctr = 0
        for row in file:
            if "Record" not in row[0]:
                collision = Collision()
                collision.collision_id = key_ctr
                key_ctr = key_ctr + 1
                collision.location = row[1]
                collision.longtitude = row[4]
                collision.latitude = row[5]
                collision.date = row[7]
                collision.time = row[8]
                environment = row[9]
                if row[9] == "":
                    environment = "Unknown"
                collision.environment = remove_prefix(environment, "Unknown")
                light = row[13]
                if row[13] == "":
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
                collision.traffic_control_condition = "N/A"
                collision_classification = row[14]
                if row[14] == "":
                    collision_classification = "Unknown"
                collision.collision_classification = remove_prefix(collision_classification, "Unknown")
                impact_type = row[15]
                if row[15] == "":
                    impact_type = "Unknown"
                collision.impace_type = remove_prefix(impact_type, "Unknown")
                collision.no_of_pedestrians = "N/A"
                collisions.append(collision)
    readData.close()

    # with open("2017collisionsfinal.xls.csv", 'w', newline='') as csvFile:
    #     print("Prepare to write the data into the file: h2017collisionsfinal.csv. It might take a while...")
    #     writer = csv.writer(csvFile)
    #     writer.writerow(["COLLISION_ID", "LOCATION", "LONGITUDE", "LATITUDE", "DATE", "TIME", "ENVIRONMENT",
    #                      "LIGHT", "SURFACE_CONDITION", "TRAFFIC_CONTROL", "TRAFFIC_CONTROL_CONDITION",
    #                      "COLLISION_CLASSIFICATION", "IMPACT_TYPE", "NO_OF_PEDESTRIANS"])
    #     for collision in collisions:
    #         writer.writerow([collision.collision_id, collision.location, collision.longtitude, collision.latitude,
    #                          collision.date, collision.time, collision.environment, collision.light,
    #                          collision.surface_condition, collision.traffic_control,
    #                          collision.traffic_control_condition, collision.collision_classification,
    #                          collision.impace_type, collision.no_of_pedestrians])
    # csvFile.close()

    list.extend(list1)
    list.extend(list2)
    list.extend(collisions)
    output_collision_data_from_list_to_new_csv("Collision_Table", list)

print("##### Prefiltering Weather Data #####")
# prefilteringWeatherData()
print("##### Finished prefiltering #####")
print("##### Processing collision table #####")

# process_collision_table()

print("##### Finished processing collision table #####")
print("##### Unbucketizing Hour table #####")

# unbucketizeHourTable("Collision_Table.csv", "Hour_Table")

print("##### Finished unbucketizing hour table #####")
print("##### Unbucketizing Location table #####")

# unbucketizeLocationTable("Collision_Table.csv", "Location_Table")

print("##### Finished unbucketizing location table #####")
print("##### Generating look_up table for FACT #####")

# lookup_table_generation("Collision_Table.csv", "Hour_Table.csv", "Location_Table.csv", "LOOKUP_TABLE")

print("##### Staging 1 #####")

# data_staging_phase_one("LOOKUP_TABLE.csv", "Hour_Table.csv", "Staging_1_Main", "Final_Hour")

print("##### Finished Staging 1 #####")
print("##### Staging 2 #####")

# data_staging_phase_two("Staging_1_Main.csv", "Location_Table.csv", "Staging_2_Main", "Final_Location")

print("##### Finished Staging 2 #####")
print("##### Staging 3 #####")

data_staging_phase_three("Staging_2_Main.csv", "weather_data_final_finish.csv", "Staging_3_Main",
                       "Final_Weather")

print("##### Finished Staging 3 #####")