--
-- PostgreSQL database dump
--

-- Dumped from database version 13.4
-- Dumped by pg_dump version 13.4

-- Started on 2022-01-04 22:20:43

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 203 (class 1259 OID 17479)
-- Name: actor; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.actor (
    id integer NOT NULL,
    name character varying NOT NULL,
    birthdate date,
    gender character varying(1)
);


ALTER TABLE public.actor OWNER TO postgres;

--
-- TOC entry 202 (class 1259 OID 17477)
-- Name: actor_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.actor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.actor_id_seq OWNER TO postgres;

--
-- TOC entry 3016 (class 0 OID 0)
-- Dependencies: 202
-- Name: actor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.actor_id_seq OWNED BY public.actor.id;


--
-- TOC entry 204 (class 1259 OID 17490)
-- Name: actorsinmovies; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.actorsinmovies (
    actor_id integer NOT NULL,
    movie_id integer NOT NULL
);


ALTER TABLE public.actorsinmovies OWNER TO postgres;

--
-- TOC entry 201 (class 1259 OID 17466)
-- Name: movie; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.movie (
    id integer NOT NULL,
    title character varying NOT NULL,
    year integer
);


ALTER TABLE public.movie OWNER TO postgres;

--
-- TOC entry 200 (class 1259 OID 17464)
-- Name: movie_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.movie_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.movie_id_seq OWNER TO postgres;

--
-- TOC entry 3017 (class 0 OID 0)
-- Dependencies: 200
-- Name: movie_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.movie_id_seq OWNED BY public.movie.id;


--
-- TOC entry 2863 (class 2604 OID 17482)
-- Name: actor id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.actor ALTER COLUMN id SET DEFAULT nextval('public.actor_id_seq'::regclass);


--
-- TOC entry 2862 (class 2604 OID 17469)
-- Name: movie id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movie ALTER COLUMN id SET DEFAULT nextval('public.movie_id_seq'::regclass);


--
-- TOC entry 3009 (class 0 OID 17479)
-- Dependencies: 203
-- Data for Name: actor; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.actor (id, name, birthdate, gender) FROM stdin;
2	Keanu Reeves	1964-09-02	m
1	Morgan Freeman	1937-06-01	m
6	Tim Robbins	1958-10-16	m
8	Sandra Bullock	1964-07-26	f
9	Carrie-Anne Moss	1967-08-21	f
10	Al Pacino	1940-04-25	m
11	John Travolta	1954-02-18	m
12	Uma Thurman	1970-04-29	f
\.


--
-- TOC entry 3010 (class 0 OID 17490)
-- Dependencies: 204
-- Data for Name: actorsinmovies; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.actorsinmovies (actor_id, movie_id) FROM stdin;
1	1
2	3
6	1
8	3
2	4
9	4
10	6
11	7
12	7
\.


--
-- TOC entry 3007 (class 0 OID 17466)
-- Dependencies: 201
-- Data for Name: movie; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.movie (id, title, year) FROM stdin;
1	The Shawshank Redemption	1994
3	Speed	1994
4	The Matrix	1999
6	The Godfather	1972
7	Pulp Fiction	1994
\.


--
-- TOC entry 3018 (class 0 OID 0)
-- Dependencies: 202
-- Name: actor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.actor_id_seq', 12, true);


--
-- TOC entry 3019 (class 0 OID 0)
-- Dependencies: 200
-- Name: movie_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.movie_id_seq', 7, true);


--
-- TOC entry 2869 (class 2606 OID 17489)
-- Name: actor actor_name_birthdate_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.actor
    ADD CONSTRAINT actor_name_birthdate_key UNIQUE (name, birthdate);


--
-- TOC entry 2871 (class 2606 OID 17487)
-- Name: actor actor_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.actor
    ADD CONSTRAINT actor_pkey PRIMARY KEY (id);


--
-- TOC entry 2873 (class 2606 OID 17494)
-- Name: actorsinmovies actorsinmovies_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.actorsinmovies
    ADD CONSTRAINT actorsinmovies_pkey PRIMARY KEY (actor_id, movie_id);


--
-- TOC entry 2865 (class 2606 OID 17474)
-- Name: movie movie_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movie
    ADD CONSTRAINT movie_pkey PRIMARY KEY (id);


--
-- TOC entry 2867 (class 2606 OID 17476)
-- Name: movie movie_title_year_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movie
    ADD CONSTRAINT movie_title_year_key UNIQUE (title, year);


--
-- TOC entry 2874 (class 2606 OID 17495)
-- Name: actorsinmovies actorsinmovies_actor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.actorsinmovies
    ADD CONSTRAINT actorsinmovies_actor_id_fkey FOREIGN KEY (actor_id) REFERENCES public.actor(id);


--
-- TOC entry 2875 (class 2606 OID 17500)
-- Name: actorsinmovies actorsinmovies_movie_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.actorsinmovies
    ADD CONSTRAINT actorsinmovies_movie_id_fkey FOREIGN KEY (movie_id) REFERENCES public.movie(id);


-- Completed on 2022-01-04 22:20:44

--
-- PostgreSQL database dump complete
--

