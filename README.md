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

## Authentication with the Github API

Note that this service hits the Github API. This API's [rate limit policy](https://developer.github.com/v3/#rate-limiting) states that unauthenticated requests are limited (by IP address) to 60 requests per hour. Authenticated requests are limited to 5000 an hour.

If you want to run this app authenticated as your Github user, set the `GITHUB_PAT` environment variable to an OAUTH2 token generated from https://github.com/settings/tokens.

I recommend setting up a `.env` file with something like this:

```
GITHUB_PAT="my_github_key"
```

And then reading it into the container at run time.

```
docker run -p 5090:5090 --env-file creds.env -d jameslamb/oss_report:0.0.1
```

## Case Study: Analyzing an Organizational Open Source Program

The UI and supporting server code in this project mainly support an interactive one user at a time workflow. However, they can be used to support another workflow: tracking the open source participation of a group of users, such as all members of a meetup group or participants in a company's open source initiatives.

### Running this analysis for the first time

1. Kick up an instance of the app running on `localhost`:

```
docker run -p 5090:5090 -d oss_report:$(cat VERSION)
```

2. Generate a [SQLite](https://docs.python.org/2/library/sqlite3.html) database file in the `analyze/` folder.

```
cat analyze/schema.sql | sqlite3 thing.db
```

3. Populate a CSV with your users.

* `user_name`: Github user name (e.g. `jameslamb`)
* `full_name`: full first and last name (`James Lamb`)

For example:

```
echo "user_name,full_name" > thing.csv
echo "jameslamb,James Lamb" >> thing.csv
echo "bburns632,Brian Burns" >> thing.csv
echo "jayqi,Jay Qi" >> thing.csv
```

4. Run the update script that will seed the database with users and pull events for each of them

```
python analyze/update_db.py \
    --csv-file $(pwd)/thing.csv \
    --db-file $(pwd)/thing.db \
    --api-url http://localhost:5090
```

5. You can now query `thing.db` to build any reports you want!

For example, you can run this to get an overview of activity by user.

```
sqlite3 \
    -column \
    -header \
    thing.db \
    'SELECT user_name, COUNT(*) AS total_contributions, COUNT(DISTINCT(repo_name)) AS num_unique_repos FROM events GROUP BY user_name;'
```

### Updating an existing DB

The Github API only allows you to get the last 90 days of activity, so you may want to run this process regularly to build up a longer history over time. 

If you already have the CSV and DB files generated, just kick up the service and run the update script! 

```
docker run -p 5090:5090 -d oss_report:$(cat VERSION)
cd analyze/
python update_db.py
```

## References

* [Github API - User Details](https://developer.github.com/v3/users/#get-contextual-information-about-a-user)
* [Vue datatable](https://www.npmjs.com/package/vuejs-datatable)
* [collapsables in Vue](https://bootstrap-vue.js.org/docs/components/collapse/)
* [approachable ECS tutorial](https://www.ybrikman.com/writing/2015/11/11/running-docker-aws-ground-up/)
* [docker-compose on Travis](http://elliot.land/post/using-docker-compose-on-travis-ci)
* [docker in Travis builds](https://docs.travis-ci.com/user/docker/)
