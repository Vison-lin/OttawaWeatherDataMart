import csv



need_index = [1,2,3,4,10]


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


def stagingP6_create_table(filename,output):
    csvfile = open(filename + '.csv', 'r')
    collision_table = csv.reader(csvfile)
    final_table = []
    title =["Accident-key", "Location-key", "Hour-key", "Weather-key", "Event-key",
                         "IMPACT_TYPE"]
    final_table.append(title)
    count = 0
    for c in collision_table:
        result = []
        if c[0] in collision_id:
            result.append(count)
            count+=1
            for index in range(1,14):
                if index in need_index:
                    result.append(c[index])
            final_table.append(result)

    out_put_new(output,final_table)
    print("stagingP6_create_table finish!!!")






def out_put_new(filename,list_data):
    csvfile = open(filename+'.csv', 'w', newline='')
    writer = csv.writer(csvfile)
    writer.writerows(list_data)
    csvfile.close()

def main():
    stagingP6_check_duplicate('Determine/Staging_4_Integrity_Checked')
    stagingP6_create_table('Determine/Staging_4_Integrity_Checked','Determine/Fact table')


main()

