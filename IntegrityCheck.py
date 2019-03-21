import csv
import sys


def out_put_new(filename, list_data):
    csvfile = open(filename + '.csv', 'w', newline='')
    writer = csv.writer(csvfile)
    writer.writerows(list_data)
    csvfile.close()


collision_table = []
weather_table = []

list_index = [collision_table, weather_table]


def read_data(collisionName, weatherName):
    name = [collisionName, weatherName]
    count = 0
    for n in name:
        csvfile = open(n + '.csv', 'r')
        file = csv.reader(csvfile)
        for i in file:
            list_index[count].append(i)
        count += 1


# def check_duplicate():
#     count = 0
#     weatherdata =''
#     data = []
#     same= 0
#     unknown_w=0
#     different =0
#     unknown_c=0
#     result = []
#     for c in collision_table[1:]:
#         w = weather_table[int(c[3])+1]
#
#         if c[5] != w[24]:
#             different+=1
#
#         if w[24] =='Unknown':
#            unknown_w+=1
#
#         if c[5] == w[24] and w[24]!='Unknown':
#             same+=1
#
#         if c[5]=='Unknown' and w[24]!='Unknown':
#             unknown_c+=1
#
#
#     #         if(weatherdata==''):
#     #             weatherdata = w[24]
#     #
#     #         if(weatherdata!=w[24]):
#     #             data.append([weatherdata,count])
#     #             count = 1
#     #             weatherdata = w[24]
#     #             continue
#     #
#     #         count+1
#     # data.append([weatherdata, count])
#
#     result = 'Same:'+str(same)+'\n'+'Unknown_Weather: '+str(unknown_w)+'\n'+'Unknown_Collision: '+str(unknown_c)+'\n'+'Different: '+str(different)+'\n'
#     return result

def translate_CtoW():

    for c in collision_table[1:]:
        if(c[5]!='Unknown'):
            weather_table[int(c[3]) + 1][24]=c[5]


def deleteBlankColumn(filename):

    final_data = []
    result = []
    ctr = 1
    l = len(weather_table[1:])
    for s in weather_table[1:]:
        sys.stdout.write("\r" + str(ctr) + "/" + str(l) + " records have been processed!")
        sys.stdout.flush()
        ctr = ctr + 1
        continueCheck = True
        for c in final_collision:
            # print(s)
            if int(c[3]) == int(s[0]):
                continueCheck = False
                break
        if continueCheck:
            continue
        result = s
        for i in s[:-1]:
            if i == '':
                continue
            result.append(i)
        final_data.append(result)
    out_put_new(filename,final_data)
    print('deleteBlankColumn() finish!!!')






# def weather_surface():
#     weather = []
#     surface = []
#     weather_surface = []
#
#     for c in collision_table[1:]:
#         if c[5] not in weather:
#             weather.append(c[5])
#         if c[7] not in surface:
#             surface.append(c[7])
#         data = [c[5],c[7]]
#         if data not in weather_surface:
#             weather_surface.append(data)
#
#
#
#     print("weather: "+str(weather))
#     print('surface: '+str(surface))
#     weather_surface.sort()
#     out_put_new('Weather_Surface','Determine',weather_surface)

final_collision = []
def determine(filename):

    result = []
    for c in collision_table[1:]:
        result = c
        w = weather_table[int(c[3]) + 1]

        if c[5] == 'Unknown':
            if w[24] == 'Unknown':
                continue
            else:
                result[5] = w[24]

        final_collision.append(result)

    out_put_new(filename, final_collision)
    print("determine() finish!!!")


def integrity_check(collisioinName, weatherName, outputCollisionName, outputWeatherNaeme):
    read_data(collisioinName, weatherName)
    determine(outputCollisionName)
    print("Dtermine finished")
    translate_CtoW()
    print("Translate CTOW finished")
    deleteBlankColumn(outputWeatherNaeme)












