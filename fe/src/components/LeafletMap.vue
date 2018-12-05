<template>
    <div class="map">
        <l-map :zoom="zoom"
               :center="center"
               @click="setMarker">
            <l-marker v-if="marker"
                        :latLng="marker">
                <l-icon
                    :iconUrl="marker_icon_custom"
                    :shadowUrl="marker_shadow_custom"/>
            </l-marker>
            <l-circle v-if="marker"
                        :latLng="marker"
                        :radius="distance"
                        color="#a637ba"
                        fillColor="#a637ba"
                        :fillOpacity="0.15"/>
            <l-tile-layer 
                        :url="url"/>
            <l-geo-json v-for="(item, index) in geostuff"
                        :key="index"
                        :geojson="item"
                        layer-type="overlay"/>
            <l-geo-json v-for="(item, index) in counties"
                        :key="index+'c'"
                        :geojson="item"
                        layer-type="overlay"
                        @click="performPolygonAction($event, index)"/>
            <LeafletHeatmap v-if="hm_points"
                            :lat-lng="hm_points"
                            :radius="30"
                            :max-zoom="9"
                            :minOpacity="0.2"
                            :blur="25"
                            :gradient="{.0:'blue',.2:'cyan',.4:'lime',.5:'yellow', 7: 'orange', 1:'red'}"/>            
        </l-map>
    </div>
</template>

<script>
    import {
        L,
        LMap,
        LTileLayer,
        LGeoJson,
        LMarker,
        LIcon,
        LCircle,
    } from 'vue2-leaflet';
    import LeafletHeatmap from 'vue2-leaflet-heatmap'

    export default {
        name: "Map",
        components: {
            LMap,
            LTileLayer,
            LGeoJson,
            LMarker,
            LIcon,
            LCircle,
            LeafletHeatmap
        },
        data () {
            return {
                marker: null,
                marker_icon_custom: "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-violet.png",
                marker_shadow_custom: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
                counties: [],
                geostuff: [],
                distance: 1000,
                hm_points: null,
                selectedMode: "Accidents",
            };
        },
        props: {
            zoom: {
                type: Number,
                default: 6
            },
            center: {
                type: Array,
                default: () => [31.647, -97.699]
            },
            url: {
                type: String,
                default: 'https://api.mapbox.com/styles/v1/tomzkk/cjovk4feh146c2so52ry4a4cr/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoidG9temtrIiwiYSI6ImNqbzhnYnlpeTA4djEza3AwaGQxNDdudmoifQ.sKCNHTCVysDMvnpoheoMZw'
            },
            attribution: {
                type: String,
                default: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attribution">CARTO</a>'
            }
        },
        methods: {
            setMarker: function (event) {
                console.log(event.latlng.lng + ', ' + event.latlng.lat)
                this.marker = event.latlng
            },
            updateDistance: function (val) {
                this.distance = val
            },
            accidentsProximity: function (distance) {
                if(this.marker == null){
                    return null
                }
                this.geostuff.splice(0, this.geostuff.length)
                this.$http.get("http://127.0.0.1:5000/accidentsProximity", {
                    params: {
                        lat : this.marker.lat,
                        lng : this.marker.lng,
                        distance : distance
                    }
                }).then(function(response){
                    for (var i = 0; i < response.data.length; i++){
                        var geojs = JSON.parse(response.data[i])
                        this.geostuff.push(geojs)
                    }
                })
            },
            accidentsOnRoad: function () {
                if(this.marker == null){
                    return null
                }
                this.geostuff.splice(0, this.geostuff.length)
                this.$http.get("http://127.0.0.1:5000/accidentsOnRoad", {
                    params: {
                        lat : this.marker.lat,
                        lng : this.marker.lng,
                        distance : this.distance
                    }
                }).then(function(response){
                    for (var i = 0; i < response.data.length; i++){
                        var geojs = response.data[i]
                        this.geostuff.push(geojs)
                        console.log(geojs['geometry']['coordinates'])
                    }
                })
            },
            allCounties: function () {
                this.counties.splice(0, this.counties.length)
                this.geostuff.splice(0, this.geostuff.length)
                this.marker = null
                
                this.$http.get("http://127.0.0.1:5000/allCounties").then(function(response){
                    for (var i = 0; i < response.data.length; i++){
                        var geojs = response.data[i]
                        this.counties.push(geojs)
                    }
                })
            },
            hideCounties: function () {
                this.counties.splice(0, this.counties.length)
                this.geostuff.splice(0, this.geostuff.length)
            },
            accidentsInCounty: function (event, index) {
                L.DomEvent.stopPropagation(event)
                this.geostuff.splice(0, this.geostuff.length)
                this.$http.get("http://127.0.0.1:5000/accidentsInCounty", {
                    params: {
                        county_id : this.counties[index]['properties']['county_id']
                    }
                }).then(function(response){
                    for (var i = 0; i < response.data.length; i++){
                        var geojs = response.data[i]
                        this.geostuff.push(geojs)
                    }
                })
            },
            heatmapCounty: function (event, index) {
                L.DomEvent.stopPropagation(event)
                if(this.hm_points != null){
                    this.hm_points = null
                }
                this.geostuff.splice(0, this.geostuff.length)
                var points = []
                this.$http.get("http://127.0.0.1:5000/heatmapInCounty", {
                    params: {
                        county_id : this.counties[index]['properties']['county_id']
                    }
                }).then(function(response){
                    var min = Infinity
                    var max = -Infinity
                    for (var i = 0; i < response.data.length; i++){
                        var cur = response.data[i]['properties']['accCount']
                        if(cur < min){
                            min = cur
                        }
                        if(cur > max){
                            max = cur
                        }
                    }
                    console.log(min)
                    console.log(max)
                    for (i = 0; i < response.data.length; i++){
                        var pnt = response.data[i]['geometry']['coordinates']
                        pnt.reverse()
                        var val = (response.data[i]['properties']['accCount'] - min) / (max - min)
                        pnt.push(val)
                        points.push(pnt)
                    }
                console.log(points)
                this.hm_points = points
                })
            },
            setMode: function (val) {
                console.log(val)
                this.selectedMode = val
            },
            performPolygonAction: function (event, index) {
                if (this.selectedMode == "Accidents") {
                    this.accidentsInCounty(event, index)
                }
                if (this.selectedMode == "Heatmap") {
                    this.heatmapCounty(event, index)
                }
            },
        }
    }
</script>

<style scoped>
@import '~leaflet/dist/leaflet.css';

    .map {
        height: 100vh;
    }
</style>