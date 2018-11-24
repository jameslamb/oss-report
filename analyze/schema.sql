
CREATE TABLE IF NOT EXISTS users (
    user_name VARCHAR PRIMARY KEY,
    full_name VARCHAR,
    valid_from BIGINT default 0,
    valid_to BIGINT default 32503696301000
);

CREATE TABLE IF NOT EXISTS events (
    id BIGINT PRIMARY KEY,
    created_at VARCHAR NOT NULL,
    type VARCHAR NOT NULL,
    repo_name VARCHAR NOT NULL,
    evidence_url VARCHAR NOT NULL,
    user_name VARCHAR NOT NULL
);
