<template>
  <div>
    <button type="button" name="button" v-on:click="addSensor">Add Sensor</button>
    <gmap-map
    class='gmap-container'
    :center="center"
    :zoom="12">
      <gmap-marker
        :key="index"
        v-for="(m, index) in markers"
        :position="m.position"
        :clickable="true"
        :title="m.title"
        @click="getSensorData(m.title)">
      </gmap-marker>
    </gmap-map>
    <sensor-data :sensor="sensorData" :sensorLoaded="sensorLoaded"/>
  </div>
</template>

<script>
// Google maps register
import * as VueGoogleMaps from 'vue2-google-maps'
import Vue from 'vue'
import axios from 'axios'
import sensor from './SensorData'

Vue.use(VueGoogleMaps, {
  load: {
    key: 'AIzaSyAoFX_Zugbcuu_WUHsjpVeIX6Zf_nLbLN4',
    libraries: 'places'
  }
})

export default {
  data () {
    return {
      center: { lat: 49.230225, lng: -123.011357 },
      markers: [],
      sensorData: {},
      sensorList: [],
      sensorLoaded: false
    }
  },
  methods: {
    getSensorData: function (sensorID) {
      this.sensorList.forEach(element => {
        if (element.id === sensorID) {
          this.sensorData = element
          this.sensorLoaded = true
        }
      })
    },
    addSensor: function () {
      this.$router.push('/add')
    }
  },
  components: {
    'sensor-data': sensor
  },
  created: function () {
    axios.get('https://0l2rwk8v23.execute-api.us-west-2.amazonaws.com/dev/list-sensors')
      .then(response => {
        response.data.forEach(element => {
          this.sensorList.push(element)

          const aSensor = {
            position: {lat: element.SensorLatitude, lng: element.SensorLongitude},
            title: element.id,
            label: element.SensorName
          }
          this.markers.push(aSensor)
        })
      })
      .catch(error => {
        console.log(error)
      })
  }
}
</script>

<style scoped>

.gmap-container {
  width: 100%;
  height: 60vh;
}

button {
  margin-bottom: 3em;
}

</style>
