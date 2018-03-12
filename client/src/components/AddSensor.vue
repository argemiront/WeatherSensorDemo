<template>
  <div>
    <div class="controls">
      <button type="button" name="button" v-on:click="cancelAdd">Cancel</button>
      <button type="button" name="button" v-on:click="addSensor">Add</button>
    </div>
    <div class="form">
      <label for="s-name">
            Name: <input type="text" id="s-name" v-model="sensorName">
      </label>
      <br>
      <label for="s-lat">
            Latitude: <input type="number" id="s-lat" v-model="sensorLat">
      </label>
      <br>
      <label for="s-lng">
            Longitude: <input type="number" id="s-lng" v-model="sensorLng">
      </label>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'add-sensor',
  data: function () {
    return {
      sensorName: '',
      sensorLat: NaN,
      sensorLng: NaN
    }
  },
  methods: {
    addSensor: function () {
      if (this.sensorName === '' || isNaN(this.sensorLat) || isNaN(this.sensorLng)) {
        alert('Please, fill the appropriate sensor data.')
        return
      }

      const aSensor = {
        name: this.sensorName,
        lat: Number(this.sensorLat),
        lng: Number(this.sensorLng)
      }

      axios
        .post(
          'https://0l2rwk8v23.execute-api.us-west-2.amazonaws.com/dev/add-sensor',
          aSensor
        )
        .then(response => {
          this.$router.go(-1)
        })
        .catch(error => {
          console.log(error)
        })
    },
    cancelAdd: function () {
      this.$router.go(-1)
    }
  }
}
</script>

<style scoped>
button {
  margin-bottom: 3em;
}
</style>
