<template>
<div>
  <section class="section">
    <div class="row">
      <div class="col-lg">
        
        <p>Total activity: {{ num_events}}</p>
      
      </div>
    </div>
  </section>
</div>
</template>

<script>
export default {
  name: 'ActivityStats',
  data () {
    return {
      num_events: 0
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
