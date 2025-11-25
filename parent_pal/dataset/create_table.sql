DROP TABLE IF EXISTS public.sleep_track;
DROP TABLE IF EXISTS public.user_info;

CREATE TABLE public.user_info (
    user_id SERIAL PRIMARY KEY,
    fullname VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE public.sleep_track (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL, -- Stores the user's email
    start_date_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_date_time TIMESTAMP WITH TIME ZONE
);