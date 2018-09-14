# oss_report

This little app allows you to visualize the activity of a GitHub user. It's that simple.

## From source

Grab the repo

```{bash}
git clone https://github.com/jameslamb/oss_report.git
cd oss_report
```

Kick up the app

```
# Build
docker build -t oss_report:$(cat VERSION) -f Dockerfile-app .

# Run
docker run -p 5090:5090 -d oss_report:$(cat VERSION)
```

## From dockerhub

Pull and run the container from dockerhub.

```{bash}
docker run -p 5090:5090 -d jameslamb/oss_report:0.0.1
```

## Use the service

Navigate to `localhost:5090` in your browser to view the app!

You can hit the `/api/events` endpoint to get JSON data with all the relevant activity a user took in the last 90 days.

```
curl -XGET http://localhost:5090/api/events?user=jameslamb
```

## Pushing to Container Registry

If, for whatever reason, you want to build and push a version of this to your own space in a container registry like Dockerhub, you can use `publish.sh`.

```{bash}
./publish.sh your_repository_name
```

Note that this will tag the container with the version number stored in `VERSION`.

## References

* [Github API - User Details](https://developer.github.com/v3/users/#get-contextual-information-about-a-user)
* [Vue datatable](https://www.npmjs.com/package/vuejs-datatable)
* [collapsables in Vue](https://bootstrap-vue.js.org/docs/components/collapse/)
* [approachable ECS tutorial](https://www.ybrikman.com/writing/2015/11/11/running-docker-aws-ground-up/)
