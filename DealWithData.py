# encoding:utf-8
import csv
import time
import sys

noChange = [6,8,10,12,14,15,16,18,19,20,22]  # the index of column will do not process

total_data = [] # to save all the weather data


yearlist= []
yearindex = []


'''
This method is used to find stations which have weather data.
'''

station_has_data = []
station_has_name = []


def find_Station_With_Data(filename):
    print('finding_data')
    csvfile = open(filename, 'r')
    weather_file = csv.reader(csvfile)
    for s in weather_file:
        for i in range(5,24):
            if(s[i]!=''):
                if(s[24] not in station_has_name):
                    station_has_name.append(s[24])
                    station_has_data.append(s)
                else:
                    station_has_data.append(s)
                break
        total_data.append(s)

    def takeDate(elem):
        return elem[1]
    station_has_data.sort(key=takeDate)
    total_data.sort(key=takeDate)
    csvfile.close()


def separate_data():
    print('separating_data')
    yearindex.clear()
    yearlist.clear()
    year = ''
    data = []
    for s in station_has_data:
        if(year==''):
            year = s[1]
            continue
        if(s[1]!=year):
            yearlist.append(data)
            yearindex.append(int(year))
            out_put_new('year_'+year,'temporary table',data)
            year = s[1]
            data = []
        data.append(s)

    yearlist.append(data)
    yearindex.append(int(year))
    out_put_new('year_' + year, 'temporary table', data)



yearmonthlist = []
def separate_data_month():
    print('separating_data_month')
    spring = [3, 4, 5]
    summer = [6, 7, 8]
    fall = [9, 10, 11]
    winter = [12, 1, 2]
    season = [winter,spring,summer,fall]
    year = ''
    data = []
    data2 = []
    for s in yearlist:
        for sea in season:
            data = []
            countSeason = 1
            currentMonth = 0
            month = sea[0]
            breakCheck = False
            for x in s:
                if(year==''):
                    year = x[1]
                    currentMonth = x[2]
                if int(x[2]) not in sea:
                    if countSeason == 3:
                        breakCheck =True
                        break
                    else:
                        continue
                else:
                    if (currentMonth != x[2]):
                        countSeason += 1
                        currentMonth = x[2]
                data.append(x)
                if breakCheck:
                    break
            data2.append(data)
            out_put_new('year_'+str(year)+'_month_'+str(month),'temporary table',data)
        year = ''
        yearmonthlist.append(data2)







'''
This method is used to create the Ontario weather station list . e.g [Name,Latitude,Longitude]
'''
ontario_weather_station_name = []
ontario_weather_station_coordinate = []

def find_Ontario_Station():
    csvfile = open('Station.csv', 'r')
    station_file = csv.reader(csvfile)
    for s in station_file:
        if (s[1] != 'ONTARIO'):
            continue
        name = s[0]
        coordinate = [s[6],s[7]]
        ontario_weather_station_name.append(name)
        ontario_weather_station_coordinate.append(coordinate)

    csvfile.close()

'''
This method is used to find the closest station by giving a station name.
'''

def find_closest_station(stationName):
    minDistance = ''
    result= ''
    for s in station_has_name:
        if(s==stationName):
            continue
        x = float(ontario_weather_station_coordinate[ontario_weather_station_name.index(s)][0])-\
            float(ontario_weather_station_coordinate[ontario_weather_station_name.index(stationName)][1])
        y = float(ontario_weather_station_coordinate[ontario_weather_station_name.index(s)][0])-\
            float(ontario_weather_station_coordinate[ontario_weather_station_name.index(stationName)][1])
        if(minDistance==''):
            minDistance = (x-y)**2
            result = s
        if((x-y)**2<minDistance):
            minDistance = (x-y)**2
            result = s
    return result





'''
first step to fill missing data
'''


copy_weather_data_complete_same = []

def copy_weather_data_complete_same_method():
    a=0
    for s in total_data:

        print(a)
        a+=1
        if(s[24] in station_has_name):
            station_copy = s[24]
        else:
            station_copy = find_closest_station(s[24])
        result = s

        try:
            dataProcess = yearlist[yearindex.index(int(s[1]))]

        except:
            copy_weather_data_complete_same.append(result)
            continue

        for index in range(5,24):
            if(index in noChange):
                continue
            if(result[index]==''):
                sum = 0
                count = 0
                for infor in dataProcess:
                    if( result[0]==infor[0] and station_copy == infor[24]):
                        result[index] = infor[index]
                        break
                    if (result[0] == infor[0]):
                        if (infor[index] == ''):
                            continue
                        try:
                            sum += float(infor[index])
                            count += 1
                        except ValueError:
                            continue
                if(result[index]==''):
                    if(index==23):
                        result[index]='NA'
                        break
                    if (sum != 0):
                        if (count == 0):
                            count = 1
                        result[index] = str(sum / count)



        copy_weather_data_complete_same.append(result)
    out_put_new('copy_weather_data_complete_same','temporary table',copy_weather_data_complete_same)
    print("finish copy_weather_data_complete_same !!")



'''
second step to fill missing data
'''


copy_weather_data_season_same = []

def copy_weather_data_season_same_method():
    spring = [3,4,5]
    summer = [6,7,8]
    fall = [9,10,11]
    winter = [12,1,2]
    season = [spring,summer,fall,winter]
    seasonindex = [winter, spring, summer, fall]
    seasonstring = ['WINTER','SPRING','SUMMER','FALL']
    station_has_data.clear()
    station_has_name.clear()
    total_data.clear()
    find_Station_With_Data('temporary table/copy_weather_data_complete_same.csv')
    # print(len(total_data))
    separate_data()
    separate_data_month()
    missdata = 0
    processdata = 0

    a= 0
    for s in total_data:

        a += 1
        if a==1000:
            break
        sys.stdout.write("\r" + str(a) + " records have been processed!")
        sys.stdout.flush()

        checkSeason = []
        for sea in season:
            if int(s[2]) in sea:
                checkSeason = sea
                break

        result = s

        seasonnumber = seasonindex.index(checkSeason)

        result.append(seasonstring[seasonnumber])

        try:
            dataProcess = yearmonthlist[yearindex.index(int(s[1]))][seasonnumber]
        except ValueError:
            copy_weather_data_season_same.append(result)
            continue

        if(result[23]=='' or result[23]=='NA'):
            result[23] = 'N/A'
        for index in range(5,23):
            if (index in noChange):
                continue
            if(result[index]==''):
                sum = 0
                count = 0
                sum2 = 0
                count2 =0
                currentSeason = checkSeason
                countSeason = 1
                currentMonth = 0
                currentData = ''
                for infor in dataProcess:

                    # if (s[1] != infor[1]):
                    #     continue
                    # if currentMonth == 0:
                    #     currentMonth = infor[2]
                    # if int(infor[2]) not in currentSeason:
                    #     if countSeason == 3:
                    #         break
                    #     else:
                    #         continue
                    # else:
                    #     if (currentMonth != infor[2]):
                    #         countSeason += 1
                    #         currentMonth = infor[2]




                    if (infor[index] == ''):
                        continue

                    if(currentData==''):
                        currentData= infor[index]
                    else:
                        if(currentData==infor[index]):
                            continue


                    if(int(s[3])==int(infor[3])and  int(s[4].split(":")[0])==int(infor[4].split(":")[0]) ):
                        if (s[24] == infor[24]):
                            try:
                                sum += float(infor[index])
                                count += 1
                            except ValueError:

                                continue


                        try:
                            sum2 += float(infor[index])
                            count2 += 1

                        except ValueError:


                            continue


                if (sum2 != 0):
                    if (count2 == 0):
                        count2 = 1
                    result[index] = str(sum2 / count2)

                if (sum != 0):
                    if (count == 0):
                        count = 1
                    result[index] = str(sum / count)
                if(result[index]==''):
                    missdata += 1
                    continue
                processdata +=1




        copy_weather_data_season_same.append(result)
    out_put_new('copy_weather_data_season_same', 'temporary table', copy_weather_data_season_same)
    print("finish copy_weather_data_season_same !!")
    return str(missdata)+' | '+str(processdata)






def out_put_new(filename,output,list_data):
    csvfile = open(output+'/'+filename+'.csv', 'w', newline='')
    writer = csv.writer(csvfile)
    writer.writerows(list_data)
    csvfile.close()





def main():
    start = time.time()
    # find_Ontario_Station()

    # '''read csv file: from OUTPUT_ontario_2_1_ottawa_0 to OUTPUT_ontario_2_1_ottawa_17 '''
    # for i in range(18):
    #     find_Station_With_Data('Weather data/OUTPUT_ontario_2_1_ottawa_'+str(i)+'.csv')
    # '''read csv file: from OUTPUT_ontario_2_2_ottawa_0 to OUTPUT_ontario_2_2_ottawa_16 '''
    # for i in range(17):
    #     find_Station_With_Data('Weather data/OUTPUT_ontario_2_2_ottawa_' + str(i) + '.csv')
    # out_put_new('hasData','temporary table',station_has_data)
    # separate_data()
    # copy_weather_data_complete_same_method()
    print("Finally, missing data|processing data : "+copy_weather_data_season_same_method())

    end = time.time()
    hours, rem = divmod(end - start, 3600)
    minutes, seconds = divmod(rem, 60)
    print("Total time consume is: " + "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds) + " :(")
    print("All processes finished! :) ")








main()
