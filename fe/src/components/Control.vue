<template>
    <div>
        <b-form-group class="group">
            <b-card>
                <b-form-row>
                    Search distance
                    <div class="slidecontainer">
                        <input v-model="distance" type="range" min="10" max="25000" value="10" class="slider" id="myRange"/>
                    </div>
                <b-form-input v-model="distance"
                        type="number"
                        placeholder="Search distance"></b-form-input>
                </b-form-row>
                <b-form-row>
                    <b-button
                        @click="accidentsInProximity">
                        Proximity
                    </b-button>
                </b-form-row>
                <b-form-row>
                    <b-button
                        @click="accidentsOnRoad">
                        Road
                    </b-button>
                </b-form-row>
            </b-card>
        </b-form-group>
        <b-form-group>
            <b-card>
                <b-button :pressed.sync="showingCounties" variant="primary">Show all counties</b-button>
                <b-form-radio-group class="radio-group" v-model="selectedMode">
                    <b-form-radio value="Accidents">Accidents in county</b-form-radio>
                    <b-form-radio value="Heatmap">County heatmap</b-form-radio>
                </b-form-radio-group>
            </b-card>
        </b-form-group>
    </div>
</template>

<script>
    //import {  } from "module";
    export default {
        name: "Control",
        components: {
            
            },
            data () {
                return {
                    distance: 1000,
                    showingCounties: false,
                    selectedMode: "Accidents",
                };
            },
            props: {

            },
            watch: {
                distance: function (val) {
                    this.$parent.updateDistance(val)
                },
                showingCounties: function (val) {
                    if (val == true){
                        this.$parent.showAllCounties()
                    }
                    else {
                        this.$parent.hideCounties()
                    }
                },
                selectedMode: function (val) {
                    this.$parent.setPolygonFunction(val)
                }
            },
            methods: {
                editDistance: function () {
                    this.distance = 10000
                },
                showCounties: function () {
                    this.$parent.showAllCounties()
                },
                accidentsInProximity: function () {
                    this.$parent.getAccidentsInProximity(this.distance)
                },
                accidentsOnRoad: function () {
                    this.$parent.getAccidentsOnRoad()
                }
            }
    }
</script>

<style>
.slidecontainer {
    width: 100%; /* Width of the outside container */
}

/* The slider itself */
.slider {
    -webkit-appearance: none;  /* Override default CSS styles */
    appearance: none;
    width: 100%; /* Full-width */
    height: 25px; /* Specified height */
    background: #d3d3d3; /* Grey background */
    outline: none; /* Remove outline */
    opacity: 0.7; /* Set transparency (for mouse-over effects on hover) */
    -webkit-transition: .2s; /* 0.2 seconds transition on hover */
    transition: opacity .2s;
}

/* Mouse-over effects */
.slider {
    -webkit-appearance: none;
    width: 100%;
    height: 10px;
    border-radius: 5px;   
    background: #d3d3d3;
    outline: none;
    opacity: 0.7;
    -webkit-transition: .2s;
    transition: opacity .2s;
}

.slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 15px;
    height: 15px;
    border-radius: 50%; 
    background: #39383a;
    cursor: pointer;
}

.slider::-moz-range-thumb {
    width: 15px;
    height: 15px;
    border-radius: 50%;
    background: #39383a;
    cursor: pointer;
}
button {
    margin: 5px 0 !important;
    width:100%;
}

.card {
    text-align: left;
}

.group {
    margin-top: 10px;
}


.radio-group {
    margin-top:20px !important;
}
</style>
