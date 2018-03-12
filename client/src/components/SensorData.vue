<template>
  <div class="sensor-data" v-if="sensorLoaded">
    <h3>{{ sensor.SensorName }}</h3>
    <h4>{{ sensor.City }}, {{ sensor.Country }} : {{ sensor.SensorLatitude }}, {{ sensor.SensorLongitude }} </h4>
    <div>
      <div class="sensor-details">
          <h5>Temperature</h5>
          Current: <span>{{ sensor.Temperature }}</span><br>
          Max: <span>{{ sensor.SensorStats.temperature.max }}</span><br>
          Min: <span>{{ sensor.SensorStats.temperature.min }}</span><br>
          Mean: <span>{{ sensor.SensorStats.temperature.mean }}</span>
      </div>

      <div class="sensor-details">
          <h5>Humidity</h5>
          Current: <span>{{ sensor.Humidity }}</span><br>
          Max: <span>{{ sensor.SensorStats.humidity.max }}</span><br>
          Min: <span>{{ sensor.SensorStats.humidity.min }}</span><br>
          Mean: <span>{{ sensor.SensorStats.humidity.mean }}</span>
      </div>

      <div class="sensor-details">
          <h5>Advanced</h5>
          Covariance between temperature and humidity: <span>{{ sensor.SensorStats.advanced.covariance }}</span><br>
          Correlation between temperature and humidity: <span>{{ sensor.SensorStats.advanced.correlation }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'sensor-data',
  props: {
    sensor: Object,
    sensorLoaded: Boolean
  }
}
</script>

<style scoped>
  span {
    font-weight: bold;
  }

  h5 {
    margin-bottom: 1em;
  }

  .sensor-data>div {
    display: flex;
    flex-direction: column;
  }

  @media screen and (min-width: 800px) {
    .sensor-data>div {
      flex-direction: row;
    }

    .sensor-details {
      flex-basis: 33%;
    }
  }
</style>
