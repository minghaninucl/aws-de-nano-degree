
CREATE TABLE public.staging_events (
    artist varchar(512),
    auth varchar(256),
    firstName varchar(256),
    gender varchar(256),
    itemInSession int4,
    lastName varchar(256),
    length float8,
    "level" varchar(256),
    location varchar(512),
    "method" varchar(256),
    page varchar(256),
    registration float8,
    sessionId int4,
    song varchar(512),
    status int4,
    ts int8,
    userAgent varchar(1024), 
    userId int4
);

CREATE TABLE public.staging_songs (
    num_songs int4,
    artist_id varchar(256),
    artist_latitude float8,
    artist_longitude float8,
    artist_location varchar(512),
    artist_name varchar(512), 
    song_id varchar(256),
    title varchar(512),  
    duration float8,
    "year" int4
);

CREATE TABLE public.songplays (
    playid varchar(32) NOT NULL, 
    start_time timestamp NOT NULL,
    userid int4 NOT NULL,
    "level" varchar(256),
    song_id varchar(256),
    artist_id varchar(256),
    session_id int4,
    location varchar(512),
    user_agent varchar(1024),
    CONSTRAINT songplays_pkey PRIMARY KEY (playid)
);


CREATE TABLE public.users (
    userid int4 NOT NULL,
    first_name varchar(256),
    last_name varchar(256),
    gender varchar(256),
    "level" varchar(256),
    CONSTRAINT users_pkey PRIMARY KEY (userid)
);


CREATE TABLE public.songs (
    song_id varchar(256) NOT NULL,
    title varchar(512), 
    artist_id varchar(256),
    "year" int4,
    duration float8,
    CONSTRAINT songs_pkey PRIMARY KEY (song_id)
);


CREATE TABLE public.artists (
    artist_id varchar(256) NOT NULL,
    artist_name varchar(512),     
    artist_location varchar(512),
    artist_latitude float8,
    artist_longitude float8,
    CONSTRAINT artists_pkey PRIMARY KEY (artist_id)
);


CREATE TABLE public."time" (
    start_time timestamp NOT NULL,
    "hour" int4,
    "day" int4,
    week int4,
    "month" varchar(256),
    "year" int4,
    weekday varchar(256),
    CONSTRAINT time_pkey PRIMARY KEY (start_time)
);