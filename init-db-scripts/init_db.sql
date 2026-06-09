--
-- PostgreSQL database dump
--

\restrict 7li6Z2mfkcOlPie7uI02IH9tdBxlRXybmQWHJr20sCIsubziSr235NE64hnKFyn

-- Dumped from database version 18.4
-- Dumped by pg_dump version 18.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: job_applications; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.job_applications (
    id integer NOT NULL,
    position_name character varying(30) NOT NULL,
    applicant_id integer NOT NULL
);


ALTER TABLE public.job_applications OWNER TO postgres;

--
-- Name: job_applications_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.job_applications_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.job_applications_id_seq OWNER TO postgres;

--
-- Name: job_applications_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.job_applications_id_seq OWNED BY public.job_applications.id;


--
-- Name: service_appointments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.service_appointments (
    id integer NOT NULL,
    service_name character varying(30) NOT NULL,
    date date NOT NULL,
    "time" time without time zone NOT NULL,
    client_id integer NOT NULL
);


ALTER TABLE public.service_appointments OWNER TO postgres;

--
-- Name: service_appointments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.service_appointments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.service_appointments_id_seq OWNER TO postgres;

--
-- Name: service_appointments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.service_appointments_id_seq OWNED BY public.service_appointments.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    phone_number character varying(11),
    email character varying(30),
    password character varying(60),
    is_user boolean DEFAULT true NOT NULL,
    is_admin boolean DEFAULT false NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: job_applications id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_applications ALTER COLUMN id SET DEFAULT nextval('public.job_applications_id_seq'::regclass);


--
-- Name: service_appointments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.service_appointments ALTER COLUMN id SET DEFAULT nextval('public.service_appointments_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
de8630cc6411
\.


--
-- Data for Name: job_applications; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.job_applications (id, position_name, applicant_id) FROM stdin;
1	administrator	1
\.


--
-- Data for Name: service_appointments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.service_appointments (id, service_name, date, "time", client_id) FROM stdin;
1	Осмотр автомобиля	2026-06-10	16:30:00	1
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, first_name, last_name, phone_number, email, password, is_user, is_admin) FROM stdin;
1	Тимур	Батрудинов	81098745918	batruda@mail.ru	$2b$12$XR5Tp21JJ5ov.jvEjkOJYO4u8Ta7cMfRSEYuP17tAQEWX9sWQQH0q	t	f
\.


--
-- Name: job_applications_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.job_applications_id_seq', 1, true);


--
-- Name: service_appointments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.service_appointments_id_seq', 1, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 1, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: job_applications job_applications_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_applications
    ADD CONSTRAINT job_applications_pkey PRIMARY KEY (id);


--
-- Name: service_appointments service_appointments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.service_appointments
    ADD CONSTRAINT service_appointments_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: job_applications job_applications_applicant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_applications
    ADD CONSTRAINT job_applications_applicant_id_fkey FOREIGN KEY (applicant_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: service_appointments service_appointments_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.service_appointments
    ADD CONSTRAINT service_appointments_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict 7li6Z2mfkcOlPie7uI02IH9tdBxlRXybmQWHJr20sCIsubziSr235NE64hnKFyn

