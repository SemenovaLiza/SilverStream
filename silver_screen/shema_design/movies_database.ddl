CREATE SCHEMA IF NOT EXISTS content; 


CREATE TABLE "content"."filmwork" 
(
    "id" uuid NOT NULL PRIMARY KEY,       
    "title" varchar(255) NOT NULL,
    "description" text NULL, 
    "creation_date" date NULL, 
    "file_path" varchar(100) NULL, 
    "rating" double precision NULL, 
    "type" varchar(25) NOT NULL,
    "created_at" timestamp with time zone NOT NULL,
    "updated_at" timestamp with time zone NOT NULL
);

CREATE TABLE "content"."genre" 
(
    "id" uuid NOT NULL PRIMARY KEY,       
    "name" varchar(255) NOT NULL,
    "description" text NULL,
    "created_at" timestamp with time zone NOT NULL,
    "updated_at" timestamp with time zone NOT NULL
);

CREATE TABLE "content"."person" 
(
    "id" uuid NOT NULL PRIMARY KEY,
    "full_name" varchar(255) NOT NULL,
    "created_at" timestamp with time zone NOT NULL,
    "updated_at" timestamp with time zone NOT NULL    
);

CREATE TABLE "content"."filmwork_person" 
(
    "id" uuid NOT NULL PRIMARY KEY,
    "filmwork_id" uuid NOT NULL,
    "person_id" uuid NOT NULL,
    "created_at" timestamp with time zone NOT NULL,
    "role" text NULL   
    
);

CREATE TABLE "content"."filmwork_genre" 
(
    "id" uuid NOT NULL PRIMARY KEY, 
    "filmwork_id" uuid NOT NULL,
    "genre_id" uuid NOT NULL,
    "created_at" timestamp with time zone NOT NULL   
);


CREATE UNIQUE INDEX filmwork_person_role ON "content"."filmwork_person" (filmwork_id, person_id, role);