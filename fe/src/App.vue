<template>
  <div id="app">
    <div class="container-fluid h-100">
      <div class="row justify-content-center h-100">
        <div class="col-2">
          <control/>
        </div>
        <div class="col-10">
          <mapa ref="mapa"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import Control from './components/Control.vue'
  import Mapa from './components/LeafletMap.vue'

  export default {
    name: 'app',
    components: {
      Control,
      Mapa
    },
    methods: {
      showAllCounties: function () {
        this.$refs.mapa.allCounties()
      },
      hideCounties: function () {
        this.$refs.mapa.hideCounties()
      },
      updateDistance: function (val) {
        this.$refs.mapa.updateDistance(parseInt(val))
      },
      getAccidentsInProximity: function (distance) {
        this.$refs.mapa.accidentsProximity(distance)
      },
      getAccidentsOnRoad: function () {
        this.$refs.mapa.accidentsOnRoad()
      },
      setPolygonFunction: function (val) {
        this.$refs.mapa.setMode(val)
      }
    }
  }
</script>

<style>
@import '~bootstrap/dist/css/bootstrap.css';
@import '~bootstrap-vue/dist/bootstrap-vue.css';

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

</style>
