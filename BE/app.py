from flask import Flask
from flask import jsonify, g
from flask import request
from db import get_db_conn
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object('config')
CORS(app, support_credentials=True)


@app.route('/heatmapInCounty', methods=['GET'])
def get_heatmap_of_county():
    cur = get_db_conn().cursor()
    county_id = request.args.get('county_id')
    print(county_id)
    cur.execute("""WITH bbx AS (SELECT ST_Transform(ST_SetSRID(way, 900913), 4326) AS bx FROM planet_osm_polygon WHERE osm_id = %s)
                    SELECT json_build_object(
                    'type', 'Feature',
                    'geometry', ST_AsGeoJSON(hm.pnt)::json,
                    'properties', json_build_object(
                        'accCount', count(hm.pnt)
                    ))
                    FROM
                    (SELECT ST_SetSRID(ST_MakePoint(x,y), 4326) as pnt, county.bx as county FROM
                    (SELECT generate_series(floor(ST_Ymin(bbx.bx))::int, ceiling(ST_Ymax(bbx.bx))::int, 0.05) as y FROM bbx) ys
                    CROSS JOIN 
                    (SELECT generate_series(floor(ST_Xmin(bbx.bx))::int, ceiling(ST_Xmax(bbx.bx))::int, 0.05) as x FROM bbx) xs
                    CROSS JOIN 
                    (SELECT bx from bbx) as county) as hm
                    JOIN accidents_texas a ON ST_DWithin(ST_SetSRID(a.way, 4326)::geography, hm.pnt::geography, 6000)
                    WHERE ST_Contains(hm.county, hm.pnt)
                    GROUP BY hm.pnt""", (county_id,))

    rows = cur.fetchall()

    rows = [rows[i][0] for i in range(len(rows))]
    if rows == None:
        return jsonify({})
    return jsonify(rows)


@app.route('/accidentsInCounty', methods=['GET'])
def get_accidents_by_county():
    cur = get_db_conn().cursor()
    county_id = request.args.get('county_id')

    cur.execute("""SELECT json_build_object(
                    'type', 'Feature',
                    'geometry', ST_AsGeoJson(a.way)::json,
                    'properties', json_build_object (
                        'persons', a.persons
                    )) FROM accident a
                    JOIN planet_osm_polygon p ON p.osm_id = %s 
                    WHERE ST_Contains(ST_Transform(ST_SetSRID(p.way::geometry, 900913), 4326), ST_SetSRID(a.way::geometry, 4326))""",
                (county_id,))
    rows = cur.fetchall()

    rows = [rows[i][0] for i in range(len(rows))]
    if rows == None:
        return jsonify({})
    return jsonify(rows)


@app.route('/allCounties', methods=['GET'])
def get_counties():
    cur = get_db_conn().cursor()
    cur.execute("""SELECT json_build_object(
                        'type', 'Feature',
                        'geometry', ST_AsGeoJson(ST_Transform(way,4326))::json,
                        'properties', json_build_object(
                            'county_id', osm_id)) FROM planet_osm_polygon
                        WHERE boundary='administrative' AND admin_level='6'""")
    rows = cur.fetchall()

    if rows == None:
        return jsonify({})
    rows = [rows[i][0] for i in range(len(rows))]
    return jsonify(rows)


@app.route('/accidentsOnRoad', methods=[
    'GET'])  # CASE ref is null ... ELSE select vsetky kde ref = ref
def get_accidents_on_road():
    cur = get_db_conn().cursor()
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    distance = request.args.get('distance')

    cur.execute("""WITH closest_road AS 
                    (SELECT CASE 
                        WHEN road.ref is null THEN road.way
                        ELSE (SELECT ST_Union(l1.way) as way FROM planet_osm_line l1 WHERE l1.ref = road.ref)
                        END
                        FROM(
                        WITH pnt AS (SELECT ST_SetSRID(ST_MakePoint(%s, %s)::geography, 4326) as way)
                        SELECT l.way, l.ref, l.name FROM planet_osm_line l 
                        CROSS JOIN (SELECT way FROM pnt) as pw
                        WHERE l.highway is not null and l.highway != 'footway' and ST_DWithin(pw.way, l.way::geography, %s)
                        ORDER BY ST_Distance(pw.way, l.way::geography) ASC
                        LIMIT 1) as road)
                    SELECT json_build_object(
                        'type', 'Feature',
                        'geometry', ST_AsGeoJSON(a.way)::json,
                        'properties', json_build_object(

                        )
                    ) FROM accidents_texas a
                    CROSS JOIN (SELECT way FROM closest_road) as cr
                    WHERE ST_DWithin(ST_SetSRID(a.way::geography, 4326), cr.way::geography, 100)
                    UNION ALL
                    SELECT json_build_object(
                            'type', 'Feature',
                            'geometry', ST_AsGeoJSON(way)::json,
                            'properties', json_build_object(

                            )
                        ) FROM closest_road""", (lng, lat, distance))

    rows = cur.fetchall()

    if rows == None:
        return jsonify({})
    rows = [rows[i][0] for i in range(len(rows))]
    return jsonify(rows)


@app.route('/accidentsProximity', methods=['GET'])
def get_accidents_proximity():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    dist = request.args.get('distance')

    cur = get_db_conn().cursor()
    cur.execute("""SELECT ST_AsGeoJson(way) FROM accident 
                    WHERE ST_DWithin(ST_SetSRID(ST_MakePoint(%s,%s)::geography, 4326), way::geography, %s)""",
                (lng, lat, dist))
    row = cur.fetchall()

    if row == None:
        return jsonify({})
    return jsonify(row)


@app.route('/')
def main():
    return "W"


if __name__ == "__main__":
    app.run(host='0.0.0.0')
