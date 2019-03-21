import csv

from Event import Event

events = []


def event_generator():
    event = Event()
    event.event_id = 0
    event.event_key = 0
    event.event_name = "No Special Event"
    event.event_start_date = "0000-01-01"
    event.event_end_date = "9999-12-31"
    events.append(event)

    event1 = Event()
    event1.event_id = 1
    event1.event_name = "Faked Event"
    event1.event_start_date = "2015-01-01"
    event1.event_end_date = "2015-2-3"
    events.append(event1)

    event2 = Event()
    event2.event_id = 2
    event2.event_name = "2016 Tim Hortons NHL Heritage Classic"
    event2.event_start_date = "2016-10-23"
    event2.event_end_date = "2016-10-23"
    events.append(event2)

    event3 = Event()
    event3.event_id = 3
    event3.event_name = "NHL 100"
    event3.event_start_date = "2017-1-1"
    event3.event_end_date = "2017-1-1"
    events.append(event3)

    event4 = Event()
    event4.event_id = 4
    event4.event_name = "Scotiabank NHL Centennial Classic"
    event4.event_start_date = "2017-1-1"
    event4.event_end_date = "2017-1-1"
    events.append(event4)





    event_list = [['Scotiabank NHL Centennial Classic','2017-1-1','2017-1-1'],
                  ['Bridgestone NHL Winter Classic','2017-1-2','2017-1-2'],
                  ['Honda NHL All-Star Weekend', '2017-1-28', '2017-1-29'],
                  ['Hockey is for Everyone Month', '2017-2-2', '2017-2-2'],
                  ['2017 Coors Light NHL Stadium Series', '2017-2-25', '2017-2-25'],
                  ['2017 NHL Expansion Draft', '2017-7-21', '2017-7-21'],
                  ['2017 NHL Draft', '2017-6-23', '2017-6-24'],
                  ['Winterlude 2014', '2014-1-31', '2014-2-17'],
                  ['Winterlude 2015', '2015-1-30', '2015-2-16'],
                  ['Winterlude 2016', '2016-1-29', '2016-2-15'],
                  ['Winterlude 2017', '2017-1-30', '2014-2-20'],
                ]
    count_id = 4
    for e in event_list:
        event = Event();
        event.event_id = count_id
        count_id+=1
        event.event_name = e[0]
        event.event_start_date = e[1]
        event.event_end_date = e[2]
        events.append(event)



    return events


def output_data_from_list_to_new_csv(file_name, list_to_store):
    """
    This method stores the given list_to_store into the file_name csv file. The file will be created if does not exist.
    :param file_name: the name of the new file. The file name SHOULD NOT CONTAINS .CSV which will be added automatically
    :param list_to_store: the list of content that needs to be stored into the csv file
    """
    with open(file_name + ".csv", 'w', newline='') as csvFile:
        print("Prepare to write the data into the file: " + file_name + ". It might take a while...")
        writer = csv.writer(csvFile)
        writer.writerow(["EVENT_ID", "EVENT_NAME", "EVENT_START_DATE", "EVENT_END_DATE"])
        ctr = 0
        if events[0].event_name != "No Special Event":
            raise Exception("Failed to insert default event!")
        for event in events:
            event.event_id = ctr
            ctr = ctr + 1
            writer.writerow([event.event_id, event.event_name, event.event_start_date, event.event_end_date])
    csvFile.close()

    print("Finished the writing!")


def generate_event_table(output):
    list = event_generator()
    output_data_from_list_to_new_csv(output, list)
