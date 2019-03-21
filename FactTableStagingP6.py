import csv



need_index = [1,2,3,4,10,15]


collision_id =[]

def stagingP6_check_duplicate(filename):
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


def stagingP6_check_fatal(filename,output):
    csvfile = open(filename + '.csv', 'r')
    collision_table = csv.reader(csvfile)
    final_table = []
    title =["Accident-key", "Location-key", "Hour-key", "Weather-key", "Event-key",
                         "IS_FATAL","IS_INTERSECTION"]
    final_table.append(title)
    count = 0
    for c in collision_table:
        result = []
        if c[0] in collision_id:
            result.append(count)
            count+=1
            for index in range(1,15):
                if index in need_index:
                    if index == 10:
                        check =False
                        if c[index]=='Fatal injury':
                            check = True
                        result.append(check)
                        continue
                    result.append(c[index])
            final_table.append(result)

    out_put_new(output,final_table)
    print("stagingP6_check_fatal finish!!!")






def out_put_new(filename,list_data):
    csvfile = open(filename+'.csv', 'w', newline='')
    writer = csv.writer(csvfile)
    writer.writerows(list_data)
    csvfile.close()

def data_staging_phase_six(input, output):
    stagingP6_check_duplicate(input)
    stagingP6_check_fatal(input, output)

