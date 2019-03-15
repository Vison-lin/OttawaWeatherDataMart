import time

import DataFilter
from DataFilter import read_ottawa_data_from_csv, output_data_from_list_to_new_csv, total_record

num_of_rows_per_csv = 100000

start = time.time()

#
#
#   Process for Ontario_1_1.csv
#
#

print("##### Start to processing Ontario_1_1.csv #####")

valid_weather_list = read_ottawa_data_from_csv('ontario_1_1.csv')

output_data_from_list_to_new_csv("OUTPUT_ontario_1_1_ottawa", valid_weather_list, num_of_rows_per_csv);

valid_weather_list.clear()

print("##### Finished the process for Ontario_1_1.csv #####")

print("Processed total number of "+str(DataFilter.total_record) + " records. :)")
print(str(DataFilter.total_valid_record) + " number of records are valid and were outputted to the file! :)")
#
#
#   Process for Ontario_1_21.csv
#
#

print("##### Start to processing Ontario_1_2.csv #####")

valid_weather_list = read_ottawa_data_from_csv('ontario_1_2.csv')

output_data_from_list_to_new_csv("OUTPUT_ontario_1_2_ottawa", valid_weather_list, num_of_rows_per_csv);

valid_weather_list.clear()

print("##### Finished the process for Ontario_1_2.csv #####")

print("Processed total number of "+str(DataFilter.total_record) + " records. :)")
print(str(DataFilter.total_valid_record) + " number of records are valid and were outputted to the file! :)")

#
#
#   Process for Ontario_2_1.csv
#
#

print("##### Start to processing Ontario_2_1.csv #####")

valid_weather_list = read_ottawa_data_from_csv('ontario_2_1.csv')

output_data_from_list_to_new_csv("OUTPUT_ontario_2_1_ottawa", valid_weather_list, num_of_rows_per_csv);

valid_weather_list.clear()

print("##### Finished the process for Ontario_2_1.csv #####")

print("Processed total number of "+str(DataFilter.total_record) + " records. :)")
print(str(DataFilter.total_valid_record) + " number of records are valid and were outputted to the file! :)")

#
#
#   Process for Ontario_2_2csv
#
#

print("##### Start to processing Ontario_2_2.csv #####")

valid_weather_list = read_ottawa_data_from_csv('ontario_2_2.csv')

output_data_from_list_to_new_csv("OUTPUT_ontario_2_2_ottawa", valid_weather_list, num_of_rows_per_csv);

valid_weather_list.clear()

print("##### Finished the process for Ontario_2_2.csv #####")

print("Processed total number of "+str(DataFilter.total_record) + " records. :)")
print(str(DataFilter.total_valid_record) + " number of records are valid and were outputted to the file! :)")

#
#
#   Process for Ontario_3.csv
#
#

print("##### Start to processing Ontario_3.csv #####")

valid_weather_list = read_ottawa_data_from_csv('ontario_3.csv')

output_data_from_list_to_new_csv("OUTPUT_ontario_3_ottawa", valid_weather_list, num_of_rows_per_csv);

valid_weather_list.clear()

print("##### Finished the process for Ontario_3.csv #####")

print("Processed total number of "+str(DataFilter.total_record) + " records. :)")
print(str(DataFilter.total_valid_record) + " number of records are valid and were outputted to the file! :)")

#
#
#   Process for Ontario_4.csv
#
#

print("##### Start to processing Ontario_4.csv #####")

valid_weather_list = read_ottawa_data_from_csv('ontario_4.csv')

output_data_from_list_to_new_csv("OUTPUT_ontario_4_ottawa", valid_weather_list, num_of_rows_per_csv);

valid_weather_list.clear()

print("##### Finished the process for Ontario_4.csv #####")

print("Processed total number of "+str(DataFilter.total_record) + " records. :)")
print(str(DataFilter.total_valid_record) + " number of records are valid and were outputted to the file! :)")

end = time.time()

hours, rem = divmod(end-start, 3600)

minutes, seconds = divmod(rem, 60)

print("Total time consume is: "+"{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds) + " :(")

print("All processes finished! :) ")
print("Processed total number of "+str(DataFilter.total_record) + " records. :)")
print(str(DataFilter.total_valid_record) + " number of records are valid and were outputted to the file! :)")
