"""
Update a record of all events, given a file full
of users.
"""

import csv
import json
import requests
import sqlite3
import click


@click.command()
@click.option(
    '--csv-file',
    help="Full path to the CSV file to use"
)
@click.option(
    '--db-file',
    help="Full path to the SQLite (.db) file to use"
)
@click.option(
    '--api-url',
    help="URL for the oss_report API. On local, this might be " +
         "'http://localhost:5090'"
)
def main(csv_file, db_file, api_url):
    """
    Update a database of Github user activity.
    """

    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    with open(csv_file) as f:
        x = csv.reader(f, delimiter=',')
        csv_rows = [r for r in x]

    headers = csv_rows.pop(0)

    user_insert_sql = "INSERT INTO users({}) VALUES({})".format(
        ",".join(headers),
        ",".join(['?'] * len(headers))
    )

    for user in csv_rows:
        try:
            cur.execute(user_insert_sql, user)
            conn.commit()
            print("[INFO] Created user '{}'".format(user[0]))
        except sqlite3.IntegrityError:
            print("[WARN] User '{}'' already exists".format(user[0]))

    # Grab users from the database
    cur.execute('SELECT user_name FROM users')
    user_names = [x[0] for x in cur.fetchall()]
    conn.commit()

    # Get events for each user, then write them to the DB
    event_fields = [
        "id",
        "created_at",
        "type",
        "repo_name",
        "evidence_url"
    ]

    event_insert_sql = "INSERT INTO events({},user_name) VALUES({},?)".format(
        ",".join(event_fields),
        ",".join(['?'] * len(event_fields))
    )

    for user_name in user_names:
        print("Updating events for '{}'".format(user_name))
        res = requests.get("{}/api/events?user={}".format(api_url, user_name))
        events = res.json()['events']
        duplicates = 0
        inserts = 0
        for event in events:
            try:
                cur.execute(
                    event_insert_sql,
                    [event[k] for k in event_fields] + [user_name]
                )
                conn.commit()
                inserts += 1
            except sqlite3.IntegrityError:
                duplicates += 1

        msg = "Done updating events for user '{}' ({} inserts, {} dupes)"
        msg = msg.format(user_name, inserts, duplicates)
        print(msg)

    print("Done updating events")


if __name__ == "__main__":
    main()
