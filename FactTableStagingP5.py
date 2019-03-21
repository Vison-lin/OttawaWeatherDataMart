import csv



delete_index = [1,2,3,4,12]


collision_id =[]

def stagingP5_check_duplicate(filename):
    csvfile = open(filename+'.csv','r')
    collision_table = csv.reader(csvfile)
    final_table = []

    for c in collision_table:
        result =''

        for string in c[1:]:
            result+= str(string)

        if result not in final_table:
            final_table.append(result)
            collision_id.append(c[0])
    csvfile.close()
    # print(len(collision_id))


def stagingP5_create_table(filename,output):
    csvfile = open(filename + '.csv', 'r')
    collision_table = csv.reader(csvfile)
    final_table = []
    title =["Accident-key","ENVIRONMENT",
                         "LIGHT", "SURFACE_CONDITION", "TRAFFIC_CONTROL", "TRAFFIC_CONTROL_CONDITION",
                         "COLLISION_CLASSIFICATION", "IMPACT_TYPE", "Accident_time"]
    final_table.append(title)
    count= 0
    for c in collision_table:
        result = []
        if c[0] in collision_id:
            result.append(count)
            count+=1
            for index in range(1,14):
                if index not in delete_index:
                    result.append(c[index])
            final_table.append(result)

    out_put_new(output,final_table)
    print("stagingP5_create_table finish!!!")






def out_put_new(filename,list_data):
    csvfile = open(filename+'.csv', 'w', newline='')
    writer = csv.writer(csvfile)
    writer.writerows(list_data)
    csvfile.close()

def data_staging_phase_five(input, output):
    stagingP5_check_duplicate(input)
    stagingP5_create_table(input, output)




