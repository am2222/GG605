import googlemaps
from datetime import datetime

from django.conf import settings
import polyline

def route(source,dist,transit_mode,leave_at,time,day):



    gmaps = googlemaps.Client(key=getattr(settings,'GOOGLE_MAPS_API',None))

    # Geocoding an address
    # geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

    # Look up an address with reverse geocoding
    # reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

    # Request directions via public transit

    # find next WED,SAT
    import datetime as DT
    import dateutil.relativedelta as REL
    today = DT.date.today()
    print(today)
    # 2012-01-10
    # FIXME:this line is just for test, comment it
    # day=REL.FR
    rd = REL.relativedelta(days=1, weekday=day)
    next_day = today + rd
    next_day=datetime.combine(next_day, datetime.min.time())
    print(int(time))
    next_day=next_day.replace(hour=int(time))
    if leave_at==True:
        directions_result = gmaps.directions(source,
                                         dist,
                                         mode=transit_mode,
                                         transit_mode='bus|rail',
                                         departure_time=next_day)
    else:
        directions_result = gmaps.directions(source,
                                             dist,
                                             mode=transit_mode,
                                             transit_mode='bus|rail',
                                             arrival_time=next_day)

    print(source,dist,transit_mode,next_day,leave_at)
    start_time = 0
    end_time= 0
    main_time= 0
    end_distance= 0
    start_distance= 0
    main_distance = 0
    coords=[]



    from osgeo import ogr
    line = ogr.Geometry(ogr.wkbLineString)

    if len(directions_result) == 0:
        return start_time, end_time, main_time, end_distance, start_distance, main_distance, coords, None

#
#     if transit_mode=="transit":
#         max_distance_step=None
#         max_step_id=0
#         current_step_id=1
#
#
#
#         for step in directions_result[0]['legs'][0]['steps']:
#             coords.append(polyline.decode(step['polyline']['points']))
#
#             for point in polyline.decode(step['polyline']['points']):
#                 line.AddPoint(point[1], point[0])
#
#
#             current_step_id+=1
#             if max_distance_step==None:
#                 max_distance_step=step
#
#             if max_distance_step['distance']['value']<step['distance']['value']:
#                 max_distance_step=step
#                 max_step_id=current_step_id
#
#         #     to get start_time and eager time.
#
#         start = directions_result[0]['legs'][0]['steps'][0:max_step_id]
#         end = directions_result[0]['legs'][0]['steps'][max_step_id:]
#
#         for i in start:
#             start_time+=i['duration']['value']
#             start_distance+=i['distance']['value']
#         for i in end:
#             end_time+=i['duration']['value']
#             end_distance+=i['distance']['value']
#         # here max_distance_step is the main step
#
#         main_time += max_distance_step['duration']['value']
#         main_distance += max_distance_step['distance']['value']
#     elif transit_mode=="driving":
# #         we do not have any start time or eagers time

    for i in directions_result[0]['legs'][0]['steps']:
        main_time+=i['duration']['value']
        main_distance+=i['distance']['value']
        coords.append(polyline.decode(i['polyline']['points']))
        for point in polyline.decode(i['polyline']['points']):
            line.AddPoint(point[1], point[0])

    print(start_time, end_time, main_time, end_distance, start_distance, main_distance)
    line.SetCoordinateDimension(2)
    return start_time, end_time, main_time, end_distance, start_distance, main_distance,coords,line


