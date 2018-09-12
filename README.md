# user_report

This little app allows you to visualize the activity of a GitHub user. It's that simple.

Kick up the app

```
cd app && docker-compose up -d
```

Hit it

```
curl -XGET http://localhost:5090/api/events?user=jameslamb
```

## References

* [Github API - User Details](https://developer.github.com/v3/users/#get-contextual-information-about-a-user)
* [Vue datatable](https://www.npmjs.com/package/vuejs-datatable)
* [collapsables in Vue](https://bootstrap-vue.js.org/docs/components/collapse/)
