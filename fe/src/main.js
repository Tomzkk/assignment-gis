import Vue from 'vue'
import App from './App.vue'
import vueResource from 'vue-resource'
import BootstrapVue from 'bootstrap-vue'

Vue.use(vueResource)
Vue.use(BootstrapVue)


delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
    iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
    iconUrl: require('leaflet/dist/images/marker-icon.png'),
    shadowUrl: require('leaflet/dist/images/marker-shadow.png')
});

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
