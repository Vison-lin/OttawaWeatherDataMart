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
