import csv

import googlemaps
import polyline
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
import os

import dateutil.relativedelta as REL
from gg506.utils import route
from .models import City, Persona, Route, Da, Hub, InteraRoute


# Create your views here.
def importshp(request):

    cities_shp = os.path.abspath('home/m/605/cities_new.shp')
    from django.contrib.gis.gdal import DataSource
    ds = DataSource(cities_shp)
    lyr=ds[0]
    City.objects.all().delete()
    for feat in lyr:
        print(lyr.geom_type)
        City(name=feat.get('CSDNAME'),geom=feat.geom.wkb,population=feat.get('Population')).save()
        print(feat.get('CSDNAME'), feat.geom.num_points)



def importda(request):
    cities_shp = os.path.abspath('home/m/605/final_das.shp')
    from django.contrib.gis.gdal import DataSource
    ds = DataSource(cities_shp)
    lyr=ds[0]
    Da.objects.all().delete()
    for feat in lyr:
        print(lyr.geom_type)
        cities=City.objects.filter(name__contains=feat.get('CSDNAME'))
        if len(cities) !=1:
            print("error reading feature id",feat.get('DAUID'))
        else:
            Da(id=int(feat.get('DAUID')),city=cities[0], geom=feat.geom.wkb).save()



def importhub(request):
    hubs_shp = os.path.abspath('home/m/605/intercity_transit_hubs.shp')
    from django.contrib.gis.gdal import DataSource
    ds = DataSource(hubs_shp)
    lyr=ds[0]
    Hub.objects.all().delete()
    for feat in lyr:
        print(lyr.geom_type)
        cities=City.objects.filter(name__contains=feat.get('City'))
        if len(cities) !=1:
            print("error reading feature id",feat.get('City'))
        else:
            main_hu=False
            if feat.get('Is_Main_Hu')=="T":
                main_hu=True
            Hub(name=str(feat.get('Name')),city=cities[0],is_main=main_hu, geom=feat.geom.wkb,transit_mode=int(feat.get('Transit_Mo'))).save()



def getcity(oldid):
    if oldid=='"':
        return None
    return City.objects.get(name__contains=oldid.split(" ")[0])
    if oldid==74:
        return 83
    elif oldid==73:
        return 81
    elif oldid==72:
        return 79
    elif oldid==71:
        return 78
    elif oldid==70:
        return 84
    elif oldid==69:
        return 80
    elif oldid==68:
        return 77
    elif oldid==67:
        return 76
    elif oldid==66:
        return 82
    elif oldid==64:
        return 75
    else:
        return 85




def calculatephase2(request):
    from osgeo import ogr

    from django.conf import settings
    # continue

    gmaps = googlemaps.Client(key=getattr(settings, 'GOOGLE_MAPS_API', None))
    cities=City.objects.all()
    for c in cities:
        das=Da.objects.filter(city=c)
        for da in das:
            nearest_hub=Hub.objects.filter()
            from django.contrib.gis.db.models.functions import Distance

            nearest_hub= Hub.objects.annotate(
                distance=Distance('geom', da.geom.centroid)
            ).order_by('distance').first()

#             I have to route from da.centroid to hub
            print(nearest_hub.id,c.name)

            directions_result = gmaps.directions((da.geom.centroid[1],da.geom.centroid[0]),
                                            (nearest_hub.geom.centroid[1],nearest_hub.geom.centroid[0]),
                                                                 mode='driving',
                                                                 # transit_mode='bus|rail',
                                                                 )
            line = ogr.Geometry(ogr.wkbLineString)
            if len(directions_result) == 0:
                print("error")

            main_time=0
            main_distance=0
            for i in directions_result[0]['legs'][0]['steps']:
                main_time += i['duration']['value']
                main_distance += i['distance']['value']
                for point in polyline.decode(i['polyline']['points']):
                    line.AddPoint(point[1], point[0])

            line.SetCoordinateDimension(2)

            r = InteraRoute(da=da,hub=nearest_hub,total_time=main_time,
                            total_distance=main_distance,
                            geom=line.ExportToWkt()).save()




def importprivate(request):
    # Route.objects.all().delete()
    with open('home/m/605/private4.csv', 'rt') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            print(row)
            c_from=getcity((row['city_from']))
            c_to=getcity((row['city_to']))
            tr_mode=int(row['transitmode'])
            persona=int(row['persona'])
            p= Persona.objects.get(id=persona)

            if c_to==None or c_from==None:
                continue



            if row['total distance']=='N/A':
                continue

            dist=int(row['total distance'].replace('km',''))*1000


            # time fixture
            time =float(row['time'])
            # time=row['total time'].split('h')
            # min=int(time[0]*60)
            #
            # if time[1]!=None or time[1]!="":
            #     try:
            #         t2=int(time[1].replace('min',''))
            #         min+=t2
            #     except:
            #         pass

            #
            # cost fixture
            cost=row['total Cost'].replace('$','')
            print(row['start time'])
            print(row['transfertime'])
            print(row['eagres time'])


            print("s1",row['stop 1 long'])
            print(row['stop 1 long'])
            print(row['stop 2 long'])
            print("s2",row['stop 2 lat'])
            # print(row['stop 3 lat'])
            print("s3",row['stop 3 long'])
            print(row['stop 4 lat'])
            print("s4",row['stop 4 long'])
            from osgeo import ogr
            line = ogr.Geometry(ogr.wkbLineString)
            from django.conf import settings
            # continue

            gmaps = googlemaps.Client(key=getattr(settings, 'GOOGLE_MAPS_API', None))
            # from s1 to s2
            directions_result = gmaps.directions((float(row['stop 1 lat']),float(row['stop 1 long'])),
                                                 (float(row['stop 2 lat']),float(row['stop 2 long'])),
                                                 mode='driving',
                                                 # transit_mode='bus|rail',
                                                 )


            if len(directions_result) == 0:
                print("error")

            for i in directions_result[0]['legs'][0]['steps']:
                for point in polyline.decode(i['polyline']['points']):
                    line.AddPoint(point[1], point[0])


            # from s2 to s3
            if row['stop 3 lat']!="" and row['stop 3 long']!="":
                directions_result = gmaps.directions((float(row['stop 2 lat']), float(row['stop 2 long'])),
                                                     (float(row['stop 3 lat']), float(row['stop 3 long'])),
                                                     mode='driving',
                                                     # transit_mode='bus|rail',
                                                     )

                if len(directions_result) == 0:
                    print("error")

                for i in directions_result[0]['legs'][0]['steps']:
                    for point in polyline.decode(i['polyline']['points']):
                        line.AddPoint(point[1], point[0])

            if row['stop 4 lat']!="" and row['stop 4 long']!="" and row['stop 4 lat']!='"' and row['stop 4 long']!='"':
                directions_result = gmaps.directions((float(row['stop 3 lat']), float(row['stop 3 long'])),
                                                     (float(row['stop 4 lat']), float(row['stop 4 long'])),
                                                     mode='driving',
                                                     # transit_mode='bus|rail',
                                                     )

                if len(directions_result) == 0:
                    print("error")

                for i in directions_result[0]['legs'][0]['steps']:
                    for point in polyline.decode(i['polyline']['points']):
                        line.AddPoint(point[1], point[0])



            line.SetCoordinateDimension(2)


            r= Route(city_to_id=c_to.id,city_from_id=c_from.id,persona=p,transit_mode=tr_mode,total_cost=cost,
                  total_time=time,total_distance=dist,geom=line.ExportToWkt()).save()
            # print(r.id)





def generatematrixes(request):



    personas=Persona.objects.all()
    cities1=City.objects.all().order_by('id')
    cities2=City.objects.all().order_by('id')
    for p in personas:
        for mode in range(1,4):


            rows_time=[]
            rows_cost=[]
            rows_distance=[]
            for c1 in cities1:
                row = []
                row.append(c1.name)
                row.append(c1.id)

                row2 = []
                row2.append(c1.name)
                row2.append(c1.id)

                row3 = []
                row3.append(c1.name)
                row3.append(c1.id)
                for c2 in cities2:

                    r=Route.objects.filter(persona=p,city_from=c1,city_to=c2,transit_mode=mode)
                    if len(r)==1:
                        time=r[0].total_time
                        cost=r[0].total_cost
                        distance=r[0].total_distance


                        row.append(time)
                        row2.append(cost)
                        row3.append(distance)
                    else:
                        row.append("")
                        row2.append("")
                        row3.append("")
                        print("[error] Rounte for ",c2.name,c1.name)
                print(row)
                rows_time.append(row)
                rows_cost.append(row2)
                rows_distance.append(row3)

            with open(str(p.id)+'_time_'+str(mode)+'.csv', 'w') as csvfile:
                writer = csv.writer(csvfile, delimiter=' ',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerows(rows_time)
            with open(str(p.id)+'_cost_' + str(mode) + '.csv', 'w') as csvfile:
                writer = csv.writer(csvfile, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerows(rows_cost)
            with open(str(p.id)+'_distance_' + str(mode) + '.csv', 'w') as csvfile:
                writer = csv.writer(csvfile, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerows(rows_distance)
                # spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])


from django.core.serializers import serialize
import json
def get_da(request):
    id= request.GET.get("cityid",None)
    if id!=None:
        city=City.objects.filter(id=id)
        if len(city)==1:


            res=serialize('geojson', Da.objects.filter(city=city[0]),
                      geometry_field='geom'
                      )
            return JsonResponse(json.loads(res),safe=False)

    # FIXME:Send proper error
    return JsonResponse()



def get_route(request):
    id_f = request.GET.get("cityfrom", None)
    id_t = request.GET.get("cityto", None)
    if id_f!=None and id_t!=None:
        routes = Route.objects.filter(city_from_id=id_f, city_to_id=id_t)

        res=serialize('geojson', routes,
                              geometry_field='geom'
                              )
        return JsonResponse(json.loads(res),safe=False)




def update_da_totalcost(request):
    das=Da.objects.all()
    for da in das:
        routs= InteraRoute.objects.filter(da=da)
        total=0
        for r in routs:
            total+=r.total_distance
        da.total_cost=total
        da.save()





def get_city_connections(request):
    id= request.GET.get("cityid",None)
    if id!=None:
        city=City.objects.filter(id=id)
        result=[]
        if len(city)==1:
            res= {
                "c1_lat":city[0].geom.centroid[0],
                "c1_long":city[0].geom.centroid[1],
                "c2_lat":0,
                "c2_long":0,
                "persona":0,
                "transit_mode":0,
                "cost":0,

            }
            citys = City.objects.all()
            for c in citys:
                routes=  Route.objects.filter(city_from=c,city_to=city[0])
                for r in routes:
                    res['c2_lat']=c.geom.centroid[0]
                    res['c2_long']=c.geom.centroid[1]
                    res['persona']=r.persona.id
                    res['transit_mode']=r.transit_mode
                    res['cost']=r.total_cost
                    result.append(res)


    return JsonResponse((result),safe=False)


def get_transit_hubs(requset):
    res = serialize('geojson', Hub.objects.all(),
                    geometry_field='geom'
                    )
    return JsonResponse(json.loads(res), safe=False)


def runmodel(request):

    # Route.objects.filter(transit_mode=1).delete()
    # Route.objects.filter(transit_mode=2).delete()
    cities=City.objects.all()
    personas=Persona.objects.all()
    response=""
    for c1 in cities:
        for c2 in cities:
            if c1.id==c2.id:
                continue


            print('calculation for pairs of ',c1.name," and ",c2.name)
            response+='</br> calculation for pairs of '+c1.name+" and "+c2.name
            # c1=City.objects.get(id=63)
            # c2=City.objects.get(id=55)


            print(c1.geom.centroid[0])

            for persona in personas:
                # persona=Persona.objects.get(id=2)
                print("lets run for persona ",persona.name)
                leave_at=False
                time=None
                if persona.arrive_by!=0:
                    time=persona.arrive_by
                else:
                    time=persona.leave_at
                    leave_at=True

                day=REL.TU
                if persona.day!="TU":
                    day=REL.SA
                for mode in persona.mode.split(','):
                    print("running transit mode for",  str(mode))
                    m = 'driving'
                    if int(mode)==1:
                        m='transit'
                    elif int(mode)==2:
                        m='driving'
                    else:
                    #     TODO: this must be fixed in future for private
                        continue


                    h1= Hub.objects.filter(is_main=True,city=c1)
                    h2= Hub.objects.filter(is_main=True,city=c2)
                    if len(h1)==1 and len(h2)==1:

                    # route((c1.geom.centroid[0],c1.geom.centroid[1]),(c2.geom.centroid[0],c2.geom.centroid[1]),m,leave_at,time,day)
                        start_time, end_time, main_time, end_distance, start_distance, main_distance,coords,line=\
                        route((h1[0].geom.centroid[1],h1[0].geom.centroid[0]),(h2[0].geom.centroid[1],h2[0].geom.centroid[0]),m,leave_at,time,day)
                        # route(c1.name+", ON, Canada",c2.name+", ON, Canada",m,leave_at,time,day)
                        # route((c1.geom.centroid[1],c1.geom.centroid[0]),(c2.geom.centroid[1],c2.geom.centroid[0]),m,leave_at,time,day)
                    # start_time, end_time, main_time, end_distance, start_distance, main_distance,coords,line=route((43.2607249,-80.073231),(45.249814,-76.080432),m,leave_at,time,day)
                        if line != None:
                            Route(city_from=c1, city_to=c2, persona=persona, transit_mode=int(mode),
                                  total_distance=main_distance,
                                  total_time=main_time,
                                  total_cost=0,
                                  start_time=start_time,
                                  transfer_time=0,
                                  eager_time=end_time,
                                  geom=line.ExportToWkt()).save()
                        else:
                            print('[error] no route found for ', c1.name, c2.name)
                            response += '</br> [error] no route found for  ' + c1.name + " and " + c2.name

                    else:
                        response += '</br> [error] no city hub found for  ' + c1.name + " and " + c2.name



    return HttpResponse(response)