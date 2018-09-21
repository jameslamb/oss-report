<template>
<div>
  <section class="section">
    <div class="row">
      <div class="col-lg">

        <div>
          <b>Github username:</b> <br>
          <input type="text" v-model="github_user" class="username_input_form"></input>
          <button v-on:click.prevent="get_events">Get Stats</button>
        </div>
        <p v-if="error" class="error-text">{{ errorText }}</p>
        <br>
        <hr>
      </div>
    </div>

    <div class = "row">
      <div class="col-4">
        <h3>Summary:</h3>

        <ul>
          <li v-for="(activity, index) in activities" :key="index">
            {{ activity.name }} ({{ activity.count }})
          </li>
        </ul>
      </div>

      <div class="col-8">
        <h3>All Contributions:</h3>
        <ul>
          <li v-for="(event, index) in events" :key="index">
            <a :href="event.evidence_url" target="_blank">{{ event.repo_name }} ({{ event.type }})</a>
          </li>
        </ul>
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
      num_events: 0,
      events: [],
      user: "",
      activities: [],
      github_user: "",
      error: null
    }
  },
  computed: {
    errorText() {
      const { status: status_code, statusText } = this.error
      return `${status_code} -- ${statusText}`;
    }
  },
  methods: {
    // get events for a user
    get_events() {
      this.$http.get("/api/events?user=" + this.github_user)
      .then(data => {
        var parsed = JSON.parse(data.bodyText);
        this.events = parsed.events;
        this.user = parsed.user;
        this.num_events = parsed.total;
        this.activities = parsed.activities;
        this.error = null;
      })
      .catch(err => {
        this.error = err;
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
a {
  color: #42b983;
}
.error-text {
  margin-top: 20px;
  color: red;
}
</style>
