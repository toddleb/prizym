--
-- PostgreSQL database dump
--

-- Dumped from database version 17.3 (Homebrew)
-- Dumped by pg_dump version 17.3 (Homebrew)

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

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: pg_database_owner
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO pg_database_owner;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: pg_database_owner
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- Name: update_timestamp(); Type: FUNCTION; Schema: public; Owner: todd
--

CREATE FUNCTION public.update_timestamp() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$;


ALTER FUNCTION public.update_timestamp() OWNER TO todd;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: agencies; Type: TABLE; Schema: public; Owner: todd
--

CREATE TABLE public.agencies (
    user_id integer NOT NULL,
    company_name character varying(255),
    industry character varying(255),
    services_offered text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.agencies OWNER TO todd;

--
-- Name: ai_assignments; Type: TABLE; Schema: public; Owner: todd
--

CREATE TABLE public.ai_assignments (
    id integer NOT NULL,
    model_id integer,
    area character varying(50) NOT NULL,
    assigned_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.ai_assignments OWNER TO todd;

--
-- Name: ai_assignments_id_seq; Type: SEQUENCE; Schema: public; Owner: todd
--

CREATE SEQUENCE public.ai_assignments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ai_assignments_id_seq OWNER TO todd;

--
-- Name: ai_assignments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: todd
--

ALTER SEQUENCE public.ai_assignments_id_seq OWNED BY public.ai_assignments.id;


--
-- Name: ai_models; Type: TABLE; Schema: public; Owner: todd
--

CREATE TABLE public.ai_models (
    id integer NOT NULL,
    model_name character varying(100) NOT NULL,
    provider character varying(50) NOT NULL,
    api_url text,
    model_type character varying(50),
    is_active boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT now(),
    api_key text
);


ALTER TABLE public.ai_models OWNER TO todd;

--
-- Name: ai_models_id_seq; Type: SEQUENCE; Schema: public; Owner: todd
--

CREATE SEQUENCE public.ai_models_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ai_models_id_seq OWNER TO todd;

--
-- Name: ai_models_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: todd
--

ALTER SEQUENCE public.ai_models_id_seq OWNED BY public.ai_models.id;


--
-- Name: ai_requests; Type: TABLE; Schema: public; Owner: todd
--

CREATE TABLE public.ai_requests (
    id integer NOT NULL,
    model_id integer,
    area character varying(50) NOT NULL,
    request_text text NOT NULL,
    requested_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.ai_requests OWNER TO todd;

--
-- Name: ai_requests_id_seq; Type: SEQUENCE; Schema: public; Owner: todd
--

CREATE SEQUENCE public.ai_requests_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ai_requests_id_seq OWNER TO todd;

--
-- Name: ai_requests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: todd
--

ALTER SEQUENCE public.ai_requests_id_seq OWNED BY public.ai_requests.id;


--
-- Name: ai_responses; Type: TABLE; Schema: public; Owner: todd
--

CREATE TABLE public.ai_responses (
    id integer NOT NULL,
    request_id integer,
    model_id integer,
    response_text text NOT NULL,
    execution_time double precision,
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.ai_responses OWNER TO todd;

--
-- Name: ai_responses_id_seq; Type: SEQUENCE; Schema: public; Owner: todd
--

CREATE SEQUENCE public.ai_responses_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ai_responses_id_seq OWNER TO todd;

--
-- Name: ai_responses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: todd
--

ALTER SEQUENCE public.ai_responses_id_seq OWNED BY public.ai_responses.id;


--
-- Name: categories; Type: TABLE; Schema: public; Owner: todd
--

CREATE TABLE public.categories (
    category_id integer NOT NULL,
    category_name character varying(255) NOT NULL,
    parent_category_id integer
);


ALTER TABLE public.categories OWNER TO todd;

--
-- Name: categories_category_id_seq; Type: SEQUENCE; Schema: public; Owner: todd
--

CREATE SEQUENCE public.categories_category_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.categories_category_id_seq OWNER TO todd;

--
-- Name: categories_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: todd
--

ALTER SEQUENCE public.categories_category_id_seq OWNED BY public.categories.category_id;


--
-- Name: dashboard_config; Type: TABLE; Schema: public; Owner: todd
--

CREATE TABLE public.dashboard_config (
    id integer NOT NULL,
    user_type character varying(50) NOT NULL,
    dashboard_name character varying(255) NOT NULL,
    elements jsonb NOT NULL
);


ALTER TABLE public.dashboard_config OWNER TO todd;

--
-- Name: dashboard_config_id_seq; Type: SEQUENCE; Schema: public; Owner: todd
--

CREATE SEQUENCE public.dashboard_config_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.dashboard_config_id_seq OWNER TO todd;

--
-- Name: dashboard_config_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: todd
--

ALTER SEQUENCE public.dashboard_config_id_seq OWNED BY public.dashboard_config.id;


--
-- Name: discovery; Type: TABLE; Schema: public; Owner: todd
--

CREATE TABLE public.discovery (
    id integer NOT NULL,
    nextie_id integer NOT NULL,
    stage integer DEFAULT 1 NOT NULL,
    responses jsonb,
    scores jsonb,
    recommended_path character varying(50),
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.discovery OWNER TO todd;

--
-- Name: discovery_id_seq; Type: SEQUENCE; Schema: public; Owner: todd
--

CREATE SEQUENCE public.discovery_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.discovery_id_seq OWNER TO todd;

--
-- Name: discovery_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: todd
--

ALTER SEQUENCE public.discovery_id_seq OWNED BY public.discovery.id;


--
-- Name: discovery_library; Type: TABLE; Schema: public; Owner: todd
--

CREATE TABLE public.discovery_library (
    id integer NOT NULL,
    category_id integer NOT NULL,
    question_text text NOT NULL,
    question_type character varying(50) NOT NULL,
    options jsonb,
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.discovery_library OWNER TO todd;

--
-- Name: discovery_library_id_seq; Type: SEQUENCE; Schema: public; Owner: todd
--

CREATE SEQUENCE public.discovery_library_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.discovery_library_id_seq OWNER TO todd;

--
-- Name: discovery_library_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: todd
--

ALTER SEQUENCE public.discovery_library_id_seq OWNED BY public.discovery_library.id;


--
-- Name: match_results; Type: TABLE; Schema: public; Owner: todd
--

CREATE TABLE public.match_results (
    id integer NOT NULL,
    nextie_id integer,
    program_id integer,
    overall_score double precision NOT NULL,
    criteria_data jsonb NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.match_results OWNER TO todd;

--
-- Name: match_results_id_seq; Type: SEQUENCE; Schema: public; Owner: todd
--

CREATE SEQUENCE public.match_results_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.match_results_id_seq OWNER TO todd;

--
-- Name: match_results_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: todd
--

ALTER SEQUENCE public.match_results_id_seq OWNED BY public.match_results.id;


--
-- Name: mybrand; Type: TABLE; Schema: public; Owner: toddlebaron
--

CREATE TABLE public.mybrand (
    id integer NOT NULL,
    nextie_id integer,
    headline character varying(255),
    skills text[],
    interests text[],
    experience jsonb,
    education jsonb,
    bio text,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.mybrand OWNER TO toddlebaron;

--
-- Name: mybrand_id_seq; Type: SEQUENCE; Schema: public; Owner: toddlebaron
--

CREATE SEQUENCE public.mybrand_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.mybrand_id_seq OWNER TO toddlebaron;

--
-- Name: mybrand_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: toddlebaron
--

ALTER SEQUENCE public.mybrand_id_seq OWNED BY public.mybrand.id;


--
-- Name: myexploration; Type: TABLE; Schema: public; Owner: toddlebaron
--

CREATE TABLE public.myexploration (
    id integer NOT NULL,
    nextie_id integer,
    category character varying(50) NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    engagement_level character varying(50),
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.myexploration OWNER TO toddlebaron;

--
-- Name: myexploration_id_seq; Type: SEQUENCE; Schema: public; Owner: toddlebaron
--

CREATE SEQUENCE public.myexploration_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.myexploration_id_seq OWNER TO toddlebaron;

--
-- Name: myexploration_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: toddlebaron
--

ALTER SEQUENCE public.myexploration_id_seq OWNED BY public.myexploration.id;


--
-- Name: mygrowth; Type: TABLE; Schema: public; Owner: toddlebaron
--

CREATE TABLE public.mygrowth (
    id integer NOT NULL,
    nextie_id integer,
    milestone character varying(255),
    target_date date,
    progress_percentage integer,
    additional_courses jsonb,
    score integer,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now(),
    CONSTRAINT mygrowth_progress_percentage_check CHECK (((progress_percentage >= 0) AND (progress_percentage <= 100))),
    CONSTRAINT mygrowth_score_check CHECK (((score >= 0) AND (score <= 100)))
);


ALTER TABLE public.mygrowth OWNER TO toddlebaron;

--
-- Name: mygrowth_id_seq; Type: SEQUENCE; Schema: public; Owner: toddlebaron
--

CREATE SEQUENCE public.mygrowth_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.mygrowth_id_seq OWNER TO toddlebaron;

--
-- Name: mygrowth_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: toddlebaron
--

ALTER SEQUENCE public.mygrowth_id_seq OWNED BY public.mygrowth.id;


--
-- Name: myinsights; Type: TABLE; Schema: public; Owner: toddlebaron
--

CREATE TABLE public.myinsights (
    id integer NOT NULL,
    nextie_id integer,
    life_score double precision,
    education_score double precision,
    work_score double precision,
    overall_score double precision,
    updated_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.myinsights OWNER TO toddlebaron;

--
-- Name: myinsights_id_seq; Type: SEQUENCE; Schema: public; Owner: toddlebaron
--

CREATE SEQUENCE public.myinsights_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.myinsights_id_seq OWNER TO toddlebaron;

--
-- Name: myinsights_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: toddlebaron
--

ALTER SEQUENCE public.myinsights_id_seq OWNED BY public.myinsights.id;


--
-- Name: mypaths; Type: TABLE; Schema: public; Owner: todd
--

CREATE TABLE public.mypaths (
    id integer NOT NULL,
    nextie_id integer,
    path_type_id integer,
    recommended_path text NOT NULL,
    explanation text,
    created_at timestamp without time zone DEFAULT now(),
    confidence_score double precision DEFAULT 0.0,
    recommended_industry text DEFAULT 'General'::text,
    suggested_jobs text DEFAULT 'General Roles'::text
);


ALTER TABLE public.mypaths OWNER TO todd;

--
-- Name: mypaths_id_seq; Type: SEQUENCE; Schema: public; Owner: todd
--

CREATE SEQUENCE public.mypaths_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.mypaths_id_seq OWNER TO todd;

--
-- Name: mypaths_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: todd
--

ALTER SEQUENCE public.mypaths_id_seq OWNED BY public.mypaths.id;


--
-- Name: myplan; Type: TABLE; Schema: public; Owner: toddlebaron
--

CREATE TABLE public.myplan (
    id integer NOT NULL,
    nextie_id integer,
    goal_title character varying(255),
    goal_description text,
    plan_steps jsonb,
    status character varying(50) DEFAULT 'In Progress'::character varying,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.myplan OWNER TO toddlebaron;

--
-- Name: myscoring; Type: TABLE; Schema: public; Owner: toddlebaron
--

CREATE TABLE public.myscoring (
    id integer NOT NULL,
    scoring_type_id integer,
    entity_id integer NOT NULL,
    match_score double precision,
    demand_score double precision,
    final_score double precision,
    updated_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.myscoring OWNER TO toddlebaron;

--
-- Name: mysettings; Type: TABLE; Schema: public; Owner: toddlebaron
--

CREATE TABLE public.mysettings (
    id integer NOT NULL,
    user_id integer,
    theme character varying(50) DEFAULT 'default'::character varying,
    layout jsonb,
    notifications jsonb,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.mysettings OWNER TO toddlebaron;

--
-- Name: mysettings_id_seq; Type: SEQUENCE; Schema: public; Owner: toddlebaron
--

CREATE SEQUENCE public.mysettings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.mysettings_id_seq OWNER TO toddlebaron;

--
-- Name: mysettings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: toddlebaron
--

ALTER SEQUENCE public.mysettings_id_seq OWNED BY public.mysettings.id;


--
-- Name: nextie_interactions; Type: TABLE; Schema: public; Owner: todd
--

CREATE TABLE public.nextie_interactions (
    id integer NOT NULL,
    nextie_id integer NOT NULL,
    interaction_type character varying(50) NOT NULL,
    question_id integer NOT NULL,
    response jsonb,
    "timestamp" timestamp without time zone DEFAULT now()
);


ALTER TABLE public.nextie_interactions OWNER TO todd;

--
-- Name: nextie_interactions_id_seq; Type: SEQUENCE; Schema: public; Owner: todd
--

CREATE SEQUENCE public.nextie_interactions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.nextie_interactions_id_seq OWNER TO todd;

--
-- Name: nextie_interactions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: todd
--

ALTER SEQUENCE public.nextie_interactions_id_seq OWNED BY public.nextie_interactions.id;


--
-- Name: nextie_responses; Type: TABLE; Schema: public; Owner: todd
--

CREATE TABLE public.nextie_responses (
    id integer NOT NULL,
    nextie_id integer NOT NULL,
    interaction_type character varying(50) NOT NULL,
    question_id integer NOT NULL,
    response jsonb,
    "timestamp" timestamp without time zone DEFAULT now()
);


ALTER TABLE public.nextie_responses OWNER TO todd;

--
-- Name: nextie_responses_id_seq; Type: SEQUENCE; Schema: public; Owner: todd
--

CREATE SEQUENCE public.nextie_responses_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.nextie_responses_id_seq OWNER TO todd;

--
-- Name: nextie_responses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: todd
--

ALTER SEQUENCE public.nextie_responses_id_seq OWNED BY public.nextie_responses.id;


--
-- Name: nexties; Type: TABLE; Schema: public; Owner: todd
--

CREATE TABLE public.nexties (
    user_id integer NOT NULL,
    city character varying(255),
    state character varying(255),
    lat character varying(255),
    lon character varying(255),
    interests text,
    wants text,
    extracurriculars text,
    skills text,
    careers text,
    paths text,
    interest_level character varying(255),
    start_data character varying(255),
    acceptance_chance double precision,
    next_score double precision,
    spark_score double precision,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.nexties OWNER TO todd;

--
-- Name: path_types; Type: TABLE; Schema: public; Owner: todd
--

CREATE TABLE public.path_types (
    id integer NOT NULL,
    path_type character varying(50) NOT NULL
);


ALTER TABLE public.path_types OWNER TO todd;

--
-- Name: path_types_id_seq; Type: SEQUENCE; Schema: public; Owner: todd
--

CREATE SEQUENCE public.path_types_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.path_types_id_seq OWNER TO todd;

--
-- Name: path_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: todd
--

ALTER SEQUENCE public.path_types_id_seq OWNED BY public.path_types.id;


--
-- Name: planning_id_seq; Type: SEQUENCE; Schema: public; Owner: toddlebaron
--

CREATE SEQUENCE public.planning_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.planning_id_seq OWNER TO toddlebaron;

--
-- Name: planning_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: toddlebaron
--

ALTER SEQUENCE public.planning_id_seq OWNED BY public.myplan.id;


--
-- Name: programs; Type: TABLE; Schema: public; Owner: todd
--

CREATE TABLE public.programs (
    user_id integer,
    institution_name character varying(255),
    program_description text,
    requirements text,
    available_slots integer,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    accrediting_agency text,
    website text,
    net_price_calculator text,
    avg_student_loan double precision,
    median_sat_score double precision,
    median_act_score double precision,
    city character varying(255),
    state character varying(50),
    id integer NOT NULL
);


ALTER TABLE public.programs OWNER TO todd;

--
-- Name: programs_id_seq; Type: SEQUENCE; Schema: public; Owner: todd
--

CREATE SEQUENCE public.programs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.programs_id_seq OWNER TO todd;

--
-- Name: programs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: todd
--

ALTER SEQUENCE public.programs_id_seq OWNED BY public.programs.id;


--
-- Name: scoring_id_seq; Type: SEQUENCE; Schema: public; Owner: toddlebaron
--

CREATE SEQUENCE public.scoring_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.scoring_id_seq OWNER TO toddlebaron;

--
-- Name: scoring_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: toddlebaron
--

ALTER SEQUENCE public.scoring_id_seq OWNED BY public.myscoring.id;


--
-- Name: scoring_types; Type: TABLE; Schema: public; Owner: toddlebaron
--

CREATE TABLE public.scoring_types (
    id integer NOT NULL,
    scoring_type character varying(50) NOT NULL
);


ALTER TABLE public.scoring_types OWNER TO toddlebaron;

--
-- Name: scoring_types_id_seq; Type: SEQUENCE; Schema: public; Owner: toddlebaron
--

CREATE SEQUENCE public.scoring_types_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.scoring_types_id_seq OWNER TO toddlebaron;

--
-- Name: scoring_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: toddlebaron
--

ALTER SEQUENCE public.scoring_types_id_seq OWNED BY public.scoring_types.id;


--
-- Name: sidebar_config; Type: TABLE; Schema: public; Owner: todd
--

CREATE TABLE public.sidebar_config (
    id integer NOT NULL,
    user_type character varying(50) NOT NULL,
    sidebar_name character varying(255) DEFAULT ''::character varying NOT NULL,
    sidebar_color character varying(50) DEFAULT ''::character varying NOT NULL,
    show_logo boolean DEFAULT true,
    logo text DEFAULT ''::text,
    sections jsonb NOT NULL,
    signout_button jsonb DEFAULT '{"icon": "/icons/signout.svg", "link": "/logout", "name": "Sign Out"}'::jsonb NOT NULL,
    location character varying(10) DEFAULT 'left'::character varying NOT NULL
);


ALTER TABLE public.sidebar_config OWNER TO todd;

--
-- Name: sidebar_config_id_seq; Type: SEQUENCE; Schema: public; Owner: todd
--

CREATE SEQUENCE public.sidebar_config_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sidebar_config_id_seq OWNER TO todd;

--
-- Name: sidebar_config_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: todd
--

ALTER SEQUENCE public.sidebar_config_id_seq OWNED BY public.sidebar_config.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: todd
--

CREATE TABLE public.users (
    id integer NOT NULL,
    uuid text NOT NULL,
    user_type character varying(50),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    is_opted_in boolean DEFAULT false,
    parental_approval boolean DEFAULT false,
    CONSTRAINT users_user_type_check CHECK (((user_type)::text = ANY ((ARRAY['nextie'::character varying, 'program'::character varying, 'third_party'::character varying])::text[])))
);


ALTER TABLE public.users OWNER TO todd;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: todd
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO todd;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: todd
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: ai_assignments id; Type: DEFAULT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.ai_assignments ALTER COLUMN id SET DEFAULT nextval('public.ai_assignments_id_seq'::regclass);


--
-- Name: ai_models id; Type: DEFAULT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.ai_models ALTER COLUMN id SET DEFAULT nextval('public.ai_models_id_seq'::regclass);


--
-- Name: ai_requests id; Type: DEFAULT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.ai_requests ALTER COLUMN id SET DEFAULT nextval('public.ai_requests_id_seq'::regclass);


--
-- Name: ai_responses id; Type: DEFAULT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.ai_responses ALTER COLUMN id SET DEFAULT nextval('public.ai_responses_id_seq'::regclass);


--
-- Name: categories category_id; Type: DEFAULT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.categories ALTER COLUMN category_id SET DEFAULT nextval('public.categories_category_id_seq'::regclass);


--
-- Name: dashboard_config id; Type: DEFAULT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.dashboard_config ALTER COLUMN id SET DEFAULT nextval('public.dashboard_config_id_seq'::regclass);


--
-- Name: discovery id; Type: DEFAULT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.discovery ALTER COLUMN id SET DEFAULT nextval('public.discovery_id_seq'::regclass);


--
-- Name: discovery_library id; Type: DEFAULT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.discovery_library ALTER COLUMN id SET DEFAULT nextval('public.discovery_library_id_seq'::regclass);


--
-- Name: match_results id; Type: DEFAULT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.match_results ALTER COLUMN id SET DEFAULT nextval('public.match_results_id_seq'::regclass);


--
-- Name: mybrand id; Type: DEFAULT; Schema: public; Owner: toddlebaron
--

ALTER TABLE ONLY public.mybrand ALTER COLUMN id SET DEFAULT nextval('public.mybrand_id_seq'::regclass);


--
-- Name: myexploration id; Type: DEFAULT; Schema: public; Owner: toddlebaron
--

ALTER TABLE ONLY public.myexploration ALTER COLUMN id SET DEFAULT nextval('public.myexploration_id_seq'::regclass);


--
-- Name: mygrowth id; Type: DEFAULT; Schema: public; Owner: toddlebaron
--

ALTER TABLE ONLY public.mygrowth ALTER COLUMN id SET DEFAULT nextval('public.mygrowth_id_seq'::regclass);


--
-- Name: myinsights id; Type: DEFAULT; Schema: public; Owner: toddlebaron
--

ALTER TABLE ONLY public.myinsights ALTER COLUMN id SET DEFAULT nextval('public.myinsights_id_seq'::regclass);


--
-- Name: mypaths id; Type: DEFAULT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.mypaths ALTER COLUMN id SET DEFAULT nextval('public.mypaths_id_seq'::regclass);


--
-- Name: myplan id; Type: DEFAULT; Schema: public; Owner: toddlebaron
--

ALTER TABLE ONLY public.myplan ALTER COLUMN id SET DEFAULT nextval('public.planning_id_seq'::regclass);


--
-- Name: myscoring id; Type: DEFAULT; Schema: public; Owner: toddlebaron
--

ALTER TABLE ONLY public.myscoring ALTER COLUMN id SET DEFAULT nextval('public.scoring_id_seq'::regclass);


--
-- Name: mysettings id; Type: DEFAULT; Schema: public; Owner: toddlebaron
--

ALTER TABLE ONLY public.mysettings ALTER COLUMN id SET DEFAULT nextval('public.mysettings_id_seq'::regclass);


--
-- Name: nextie_interactions id; Type: DEFAULT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.nextie_interactions ALTER COLUMN id SET DEFAULT nextval('public.nextie_interactions_id_seq'::regclass);


--
-- Name: nextie_responses id; Type: DEFAULT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.nextie_responses ALTER COLUMN id SET DEFAULT nextval('public.nextie_responses_id_seq'::regclass);


--
-- Name: path_types id; Type: DEFAULT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.path_types ALTER COLUMN id SET DEFAULT nextval('public.path_types_id_seq'::regclass);


--
-- Name: programs id; Type: DEFAULT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.programs ALTER COLUMN id SET DEFAULT nextval('public.programs_id_seq'::regclass);


--
-- Name: scoring_types id; Type: DEFAULT; Schema: public; Owner: toddlebaron
--

ALTER TABLE ONLY public.scoring_types ALTER COLUMN id SET DEFAULT nextval('public.scoring_types_id_seq'::regclass);


--
-- Name: sidebar_config id; Type: DEFAULT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.sidebar_config ALTER COLUMN id SET DEFAULT nextval('public.sidebar_config_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: ai_assignments ai_assignments_area_key; Type: CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.ai_assignments
    ADD CONSTRAINT ai_assignments_area_key UNIQUE (area);


--
-- Name: ai_assignments ai_assignments_pkey; Type: CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.ai_assignments
    ADD CONSTRAINT ai_assignments_pkey PRIMARY KEY (id);


--
-- Name: ai_models ai_models_model_name_key; Type: CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.ai_models
    ADD CONSTRAINT ai_models_model_name_key UNIQUE (model_name);


--
-- Name: ai_models ai_models_pkey; Type: CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.ai_models
    ADD CONSTRAINT ai_models_pkey PRIMARY KEY (id);


--
-- Name: ai_requests ai_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.ai_requests
    ADD CONSTRAINT ai_requests_pkey PRIMARY KEY (id);


--
-- Name: ai_responses ai_responses_pkey; Type: CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.ai_responses
    ADD CONSTRAINT ai_responses_pkey PRIMARY KEY (id);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (category_id);


--
-- Name: dashboard_config dashboard_config_pkey; Type: CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.dashboard_config
    ADD CONSTRAINT dashboard_config_pkey PRIMARY KEY (id);


--
-- Name: dashboard_config dashboard_config_user_type_key; Type: CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.dashboard_config
    ADD CONSTRAINT dashboard_config_user_type_key UNIQUE (user_type);


--
-- Name: discovery_library discovery_library_pkey; Type: CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.discovery_library
    ADD CONSTRAINT discovery_library_pkey PRIMARY KEY (id);


--
-- Name: discovery discovery_pkey; Type: CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.discovery
    ADD CONSTRAINT discovery_pkey PRIMARY KEY (id);


--
-- Name: match_results match_results_pkey; Type: CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.match_results
    ADD CONSTRAINT match_results_pkey PRIMARY KEY (id);


--
-- Name: mybrand mybrand_pkey; Type: CONSTRAINT; Schema: public; Owner: toddlebaron
--

ALTER TABLE ONLY public.mybrand
    ADD CONSTRAINT mybrand_pkey PRIMARY KEY (id);


--
-- Name: myexploration myexploration_pkey; Type: CONSTRAINT; Schema: public; Owner: toddlebaron
--

ALTER TABLE ONLY public.myexploration
    ADD CONSTRAINT myexploration_pkey PRIMARY KEY (id);


--
-- Name: mygrowth mygrowth_pkey; Type: CONSTRAINT; Schema: public; Owner: toddlebaron
--

ALTER TABLE ONLY public.mygrowth
    ADD CONSTRAINT mygrowth_pkey PRIMARY KEY (id);


--
-- Name: myinsights myinsights_pkey; Type: CONSTRAINT; Schema: public; Owner: toddlebaron
--

ALTER TABLE ONLY public.myinsights
    ADD CONSTRAINT myinsights_pkey PRIMARY KEY (id);


--
-- Name: mypaths mypaths_pkey; Type: CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.mypaths
    ADD CONSTRAINT mypaths_pkey PRIMARY KEY (id);


--
-- Name: mysettings mysettings_pkey; Type: CONSTRAINT; Schema: public; Owner: toddlebaron
--

ALTER TABLE ONLY public.mysettings
    ADD CONSTRAINT mysettings_pkey PRIMARY KEY (id);


--
-- Name: nextie_interactions nextie_interactions_pkey; Type: CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.nextie_interactions
    ADD CONSTRAINT nextie_interactions_pkey PRIMARY KEY (id);


--
-- Name: nextie_responses nextie_responses_pkey; Type: CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.nextie_responses
    ADD CONSTRAINT nextie_responses_pkey PRIMARY KEY (id);


--
-- Name: nexties nexties_pkey; Type: CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.nexties
    ADD CONSTRAINT nexties_pkey PRIMARY KEY (user_id);


--
-- Name: path_types path_types_path_type_key; Type: CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.path_types
    ADD CONSTRAINT path_types_path_type_key UNIQUE (path_type);


--
-- Name: path_types path_types_pkey; Type: CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.path_types
    ADD CONSTRAINT path_types_pkey PRIMARY KEY (id);


--
-- Name: myplan planning_pkey; Type: CONSTRAINT; Schema: public; Owner: toddlebaron
--

ALTER TABLE ONLY public.myplan
    ADD CONSTRAINT planning_pkey PRIMARY KEY (id);


--
-- Name: programs programs_pkey; Type: CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.programs
    ADD CONSTRAINT programs_pkey PRIMARY KEY (id);


--
-- Name: myscoring scoring_pkey; Type: CONSTRAINT; Schema: public; Owner: toddlebaron
--

ALTER TABLE ONLY public.myscoring
    ADD CONSTRAINT scoring_pkey PRIMARY KEY (id);


--
-- Name: scoring_types scoring_types_pkey; Type: CONSTRAINT; Schema: public; Owner: toddlebaron
--

ALTER TABLE ONLY public.scoring_types
    ADD CONSTRAINT scoring_types_pkey PRIMARY KEY (id);


--
-- Name: scoring_types scoring_types_scoring_type_key; Type: CONSTRAINT; Schema: public; Owner: toddlebaron
--

ALTER TABLE ONLY public.scoring_types
    ADD CONSTRAINT scoring_types_scoring_type_key UNIQUE (scoring_type);


--
-- Name: sidebar_config sidebar_config_pkey; Type: CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.sidebar_config
    ADD CONSTRAINT sidebar_config_pkey PRIMARY KEY (id);


--
-- Name: sidebar_config sidebar_config_user_type_location_key; Type: CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.sidebar_config
    ADD CONSTRAINT sidebar_config_user_type_location_key UNIQUE (user_type, location);


--
-- Name: agencies third_party_pkey; Type: CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.agencies
    ADD CONSTRAINT third_party_pkey PRIMARY KEY (user_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_uuid_key; Type: CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_uuid_key UNIQUE (uuid);


--
-- Name: idx_discovery_category_id; Type: INDEX; Schema: public; Owner: todd
--

CREATE INDEX idx_discovery_category_id ON public.discovery_library USING btree (category_id);


--
-- Name: idx_match_results_nextie; Type: INDEX; Schema: public; Owner: todd
--

CREATE INDEX idx_match_results_nextie ON public.match_results USING btree (nextie_id);


--
-- Name: idx_match_results_program; Type: INDEX; Schema: public; Owner: todd
--

CREATE INDEX idx_match_results_program ON public.match_results USING btree (program_id);


--
-- Name: ai_assignments ai_assignments_model_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.ai_assignments
    ADD CONSTRAINT ai_assignments_model_id_fkey FOREIGN KEY (model_id) REFERENCES public.ai_models(id) ON DELETE CASCADE;


--
-- Name: ai_requests ai_requests_model_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.ai_requests
    ADD CONSTRAINT ai_requests_model_id_fkey FOREIGN KEY (model_id) REFERENCES public.ai_models(id) ON DELETE CASCADE;


--
-- Name: ai_responses ai_responses_model_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.ai_responses
    ADD CONSTRAINT ai_responses_model_id_fkey FOREIGN KEY (model_id) REFERENCES public.ai_models(id) ON DELETE CASCADE;


--
-- Name: ai_responses ai_responses_request_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.ai_responses
    ADD CONSTRAINT ai_responses_request_id_fkey FOREIGN KEY (request_id) REFERENCES public.ai_requests(id) ON DELETE CASCADE;


--
-- Name: categories categories_parent_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_parent_category_id_fkey FOREIGN KEY (parent_category_id) REFERENCES public.categories(category_id) ON DELETE SET NULL;


--
-- Name: discovery_library discovery_library_category_fk; Type: FK CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.discovery_library
    ADD CONSTRAINT discovery_library_category_fk FOREIGN KEY (category_id) REFERENCES public.categories(category_id) ON DELETE CASCADE;


--
-- Name: discovery discovery_nextie_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.discovery
    ADD CONSTRAINT discovery_nextie_id_fkey FOREIGN KEY (nextie_id) REFERENCES public.nexties(user_id) ON DELETE CASCADE;


--
-- Name: agencies fk_agency_user; Type: FK CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.agencies
    ADD CONSTRAINT fk_agency_user FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: mybrand fk_mybrand_nextie; Type: FK CONSTRAINT; Schema: public; Owner: toddlebaron
--

ALTER TABLE ONLY public.mybrand
    ADD CONSTRAINT fk_mybrand_nextie FOREIGN KEY (nextie_id) REFERENCES public.nexties(user_id) ON DELETE CASCADE;


--
-- Name: myexploration fk_myexploration_nextie; Type: FK CONSTRAINT; Schema: public; Owner: toddlebaron
--

ALTER TABLE ONLY public.myexploration
    ADD CONSTRAINT fk_myexploration_nextie FOREIGN KEY (nextie_id) REFERENCES public.nexties(user_id) ON DELETE CASCADE;


--
-- Name: mygrowth fk_mygrowth_nextie; Type: FK CONSTRAINT; Schema: public; Owner: toddlebaron
--

ALTER TABLE ONLY public.mygrowth
    ADD CONSTRAINT fk_mygrowth_nextie FOREIGN KEY (nextie_id) REFERENCES public.nexties(user_id) ON DELETE CASCADE;


--
-- Name: myinsights fk_myinsights_nextie; Type: FK CONSTRAINT; Schema: public; Owner: toddlebaron
--

ALTER TABLE ONLY public.myinsights
    ADD CONSTRAINT fk_myinsights_nextie FOREIGN KEY (nextie_id) REFERENCES public.nexties(user_id) ON DELETE CASCADE;


--
-- Name: myplan fk_myplan_nextie; Type: FK CONSTRAINT; Schema: public; Owner: toddlebaron
--

ALTER TABLE ONLY public.myplan
    ADD CONSTRAINT fk_myplan_nextie FOREIGN KEY (nextie_id) REFERENCES public.nexties(user_id) ON DELETE CASCADE;


--
-- Name: mysettings fk_mysettings_user; Type: FK CONSTRAINT; Schema: public; Owner: toddlebaron
--

ALTER TABLE ONLY public.mysettings
    ADD CONSTRAINT fk_mysettings_user FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: nexties fk_nextie_user; Type: FK CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.nexties
    ADD CONSTRAINT fk_nextie_user FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: programs fk_program_user; Type: FK CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.programs
    ADD CONSTRAINT fk_program_user FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: myscoring fk_scoring_type; Type: FK CONSTRAINT; Schema: public; Owner: toddlebaron
--

ALTER TABLE ONLY public.myscoring
    ADD CONSTRAINT fk_scoring_type FOREIGN KEY (scoring_type_id) REFERENCES public.scoring_types(id) ON DELETE CASCADE;


--
-- Name: match_results match_results_nextie_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.match_results
    ADD CONSTRAINT match_results_nextie_id_fkey FOREIGN KEY (nextie_id) REFERENCES public.nexties(user_id) ON DELETE CASCADE;


--
-- Name: match_results match_results_program_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.match_results
    ADD CONSTRAINT match_results_program_id_fkey FOREIGN KEY (program_id) REFERENCES public.programs(id) ON DELETE CASCADE;


--
-- Name: mybrand mybrand_nextie_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: toddlebaron
--

ALTER TABLE ONLY public.mybrand
    ADD CONSTRAINT mybrand_nextie_id_fkey FOREIGN KEY (nextie_id) REFERENCES public.nexties(user_id) ON DELETE CASCADE;


--
-- Name: myexploration myexploration_nextie_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: toddlebaron
--

ALTER TABLE ONLY public.myexploration
    ADD CONSTRAINT myexploration_nextie_id_fkey FOREIGN KEY (nextie_id) REFERENCES public.nexties(user_id) ON DELETE CASCADE;


--
-- Name: mygrowth mygrowth_nextie_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: toddlebaron
--

ALTER TABLE ONLY public.mygrowth
    ADD CONSTRAINT mygrowth_nextie_id_fkey FOREIGN KEY (nextie_id) REFERENCES public.nexties(user_id) ON DELETE CASCADE;


--
-- Name: myinsights myinsights_nextie_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: toddlebaron
--

ALTER TABLE ONLY public.myinsights
    ADD CONSTRAINT myinsights_nextie_id_fkey FOREIGN KEY (nextie_id) REFERENCES public.nexties(user_id) ON DELETE CASCADE;


--
-- Name: mypaths mypaths_nextie_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.mypaths
    ADD CONSTRAINT mypaths_nextie_id_fkey FOREIGN KEY (nextie_id) REFERENCES public.nexties(user_id) ON DELETE CASCADE;


--
-- Name: mypaths mypaths_path_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.mypaths
    ADD CONSTRAINT mypaths_path_type_id_fkey FOREIGN KEY (path_type_id) REFERENCES public.path_types(id) ON DELETE CASCADE;


--
-- Name: mysettings mysettings_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: toddlebaron
--

ALTER TABLE ONLY public.mysettings
    ADD CONSTRAINT mysettings_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: nextie_interactions nextie_interactions_nextie_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.nextie_interactions
    ADD CONSTRAINT nextie_interactions_nextie_id_fkey FOREIGN KEY (nextie_id) REFERENCES public.nexties(user_id) ON DELETE CASCADE;


--
-- Name: nextie_interactions nextie_interactions_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.nextie_interactions
    ADD CONSTRAINT nextie_interactions_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.discovery_library(id) ON DELETE CASCADE;


--
-- Name: nextie_responses nextie_responses_nextie_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.nextie_responses
    ADD CONSTRAINT nextie_responses_nextie_id_fkey FOREIGN KEY (nextie_id) REFERENCES public.nexties(user_id) ON DELETE CASCADE;


--
-- Name: nextie_responses nextie_responses_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.nextie_responses
    ADD CONSTRAINT nextie_responses_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.discovery_library(id) ON DELETE CASCADE;


--
-- Name: nexties nexties_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.nexties
    ADD CONSTRAINT nexties_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: myplan planning_nextie_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: toddlebaron
--

ALTER TABLE ONLY public.myplan
    ADD CONSTRAINT planning_nextie_id_fkey FOREIGN KEY (nextie_id) REFERENCES public.nexties(user_id) ON DELETE CASCADE;


--
-- Name: programs programs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.programs
    ADD CONSTRAINT programs_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: myscoring scoring_scoring_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: toddlebaron
--

ALTER TABLE ONLY public.myscoring
    ADD CONSTRAINT scoring_scoring_type_id_fkey FOREIGN KEY (scoring_type_id) REFERENCES public.scoring_types(id) ON DELETE CASCADE;


--
-- Name: agencies third_party_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.agencies
    ADD CONSTRAINT third_party_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

