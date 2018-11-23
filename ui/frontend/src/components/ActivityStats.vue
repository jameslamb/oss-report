<template>
<div>
  <section class="section">
    <div class="row">
      <div class="col-lg">

        <div>
          <b>Github username:</b> <br>
          <input type="text" v-model="github_user" class="username_input_form"></input>
          <button v-on:click.prevent="getEvents">Get Stats</button>
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

      <div class="col-4">
        <h3>Repos:</h3>
        <ul>
          <li v-for="(repoEvents, repoName) in repos" :key="repoName">
            <a target="_blank" :href="`https://github.com/${repoName}`">{{ repoName }}</a>
            <ul>
              <li v-for="(events, eventName) in repoEvents" :key="eventName">
                {{ eventName }} ({{ events.length }})
              </li>
            </ul>
          </li>
        </ul>
      </div>

    </div>

  </section>
</div>
</template>

<script>
import userTransformer from '../transformers/user';
import repoTransformer from '../transformers/repo';

export default {
  name: 'ActivityStats',
  data () {
    return {
      activities: [],
      repos: [],
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
    async getEvents() {
      const data = await this.$http.get("/api/events?user=" + this.github_user).catch(err => {
        this.error = err;
        console.error(err);
      });

      const userData = userTransformer(data.bodyText);
      const repos = repoTransformer(userData.events);
      this.user = userData.user;
      this.activities = userData.activities;
      this.repos = repos;
      this.error = null;
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
