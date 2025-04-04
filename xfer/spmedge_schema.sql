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
-- Name: cleaning_patterns; Type: TABLE; Schema: public; Owner: todd
--

CREATE TABLE public.cleaning_patterns (
    id integer NOT NULL,
    pattern text NOT NULL,
    replacement text DEFAULT ''::text,
    pattern_type character varying(50) NOT NULL,
    active boolean DEFAULT true,
    description text,
    sort_order integer DEFAULT 0
);


ALTER TABLE public.cleaning_patterns OWNER TO todd;

--
-- Name: cleaning_patterns_id_seq; Type: SEQUENCE; Schema: public; Owner: todd
--

CREATE SEQUENCE public.cleaning_patterns_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cleaning_patterns_id_seq OWNER TO todd;

--
-- Name: cleaning_patterns_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: todd
--

ALTER SEQUENCE public.cleaning_patterns_id_seq OWNED BY public.cleaning_patterns.id;


--
-- Name: comp_components; Type: TABLE; Schema: public; Owner: todd
--

CREATE TABLE public.comp_components (
    id integer NOT NULL,
    plan_id integer NOT NULL,
    name text NOT NULL,
    type text,
    weight text,
    target_amount text,
    frequency text,
    metrics jsonb,
    structure jsonb,
    special_features jsonb
);


ALTER TABLE public.comp_components OWNER TO todd;

--
-- Name: comp_components_id_seq; Type: SEQUENCE; Schema: public; Owner: todd
--

CREATE SEQUENCE public.comp_components_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.comp_components_id_seq OWNER TO todd;

--
-- Name: comp_components_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: todd
--

ALTER SEQUENCE public.comp_components_id_seq OWNED BY public.comp_components.id;


--
-- Name: comp_plans; Type: TABLE; Schema: public; Owner: todd
--

CREATE TABLE public.comp_plans (
    id integer NOT NULL,
    title text NOT NULL,
    effective_dates text,
    total_target text,
    source_file text,
    summary text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.comp_plans OWNER TO todd;

--
-- Name: comp_plans_id_seq; Type: SEQUENCE; Schema: public; Owner: todd
--

CREATE SEQUENCE public.comp_plans_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.comp_plans_id_seq OWNER TO todd;

--
-- Name: comp_plans_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: todd
--

ALTER SEQUENCE public.comp_plans_id_seq OWNED BY public.comp_plans.id;


--
-- Name: comp_provisions; Type: TABLE; Schema: public; Owner: todd
--

CREATE TABLE public.comp_provisions (
    id integer NOT NULL,
    plan_id integer NOT NULL,
    provision text NOT NULL
);


ALTER TABLE public.comp_provisions OWNER TO todd;

--
-- Name: comp_provisions_id_seq; Type: SEQUENCE; Schema: public; Owner: todd
--

CREATE SEQUENCE public.comp_provisions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.comp_provisions_id_seq OWNER TO todd;

--
-- Name: comp_provisions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: todd
--

ALTER SEQUENCE public.comp_provisions_id_seq OWNED BY public.comp_provisions.id;


--
-- Name: comp_tags; Type: TABLE; Schema: public; Owner: todd
--

CREATE TABLE public.comp_tags (
    id integer NOT NULL,
    component_id integer NOT NULL,
    tag text NOT NULL
);


ALTER TABLE public.comp_tags OWNER TO todd;

--
-- Name: comp_tags_id_seq; Type: SEQUENCE; Schema: public; Owner: todd
--

CREATE SEQUENCE public.comp_tags_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.comp_tags_id_seq OWNER TO todd;

--
-- Name: comp_tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: todd
--

ALTER SEQUENCE public.comp_tags_id_seq OWNED BY public.comp_tags.id;


--
-- Name: processing_status; Type: TABLE; Schema: public; Owner: todd
--

CREATE TABLE public.processing_status (
    id integer NOT NULL,
    file_path text NOT NULL,
    status text NOT NULL,
    error_message text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.processing_status OWNER TO todd;

--
-- Name: processing_status_id_seq; Type: SEQUENCE; Schema: public; Owner: todd
--

CREATE SEQUENCE public.processing_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.processing_status_id_seq OWNER TO todd;

--
-- Name: processing_status_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: todd
--

ALTER SEQUENCE public.processing_status_id_seq OWNED BY public.processing_status.id;


--
-- Name: spm_component_breakdown; Type: VIEW; Schema: public; Owner: todd
--

CREATE VIEW public.spm_component_breakdown AS
 SELECT cc.id,
    cc.name,
    cc.type,
    cc.weight,
    cc.target_amount,
    cc.frequency,
    cp.title AS plan_title,
        CASE
            WHEN ((cc.name ~~* '%revenue%'::text) OR (cc.type ~~* '%revenue%'::text)) THEN 'revenue'::text
            WHEN ((cc.name ~~* '%implant%'::text) OR (cc.type ~~* '%implant%'::text)) THEN 'implant'::text
            WHEN ((cc.name ~~* '%margin%'::text) OR (cc.name ~~* '%sgm%'::text)) THEN 'margin'::text
            WHEN ((cc.name ~~* '%expense%'::text) OR (cc.name ~~* '%cost%'::text)) THEN 'expense'::text
            WHEN ((cc.name ~~* '%mbo%'::text) OR (cc.name ~~* '%objective%'::text)) THEN 'mbo'::text
            ELSE 'other'::text
        END AS component_category
   FROM (public.comp_components cc
     JOIN public.comp_plans cp ON ((cc.plan_id = cp.id)));


ALTER VIEW public.spm_component_breakdown OWNER TO todd;

--
-- Name: spm_component_counts; Type: VIEW; Schema: public; Owner: todd
--

CREATE VIEW public.spm_component_counts AS
 SELECT count(*) AS total_components,
    sum(
        CASE
            WHEN ((name ~~* '%revenue%'::text) OR (type ~~* '%revenue%'::text)) THEN 1
            ELSE 0
        END) AS revenue_components,
    sum(
        CASE
            WHEN ((name ~~* '%implant%'::text) OR (type ~~* '%implant%'::text)) THEN 1
            ELSE 0
        END) AS implant_components,
    sum(
        CASE
            WHEN ((name ~~* '%margin%'::text) OR (name ~~* '%sgm%'::text)) THEN 1
            ELSE 0
        END) AS margin_components,
    sum(
        CASE
            WHEN ((name ~~* '%expense%'::text) OR (name ~~* '%cost%'::text)) THEN 1
            ELSE 0
        END) AS expense_components,
    sum(
        CASE
            WHEN ((name ~~* '%mbo%'::text) OR (name ~~* '%objective%'::text)) THEN 1
            ELSE 0
        END) AS mbo_components
   FROM public.comp_components;


ALTER VIEW public.spm_component_counts OWNER TO todd;

--
-- Name: spm_plan_overview; Type: VIEW; Schema: public; Owner: todd
--

CREATE VIEW public.spm_plan_overview AS
 SELECT cp.id AS plan_id,
    cp.title,
    cp.effective_dates,
    cp.summary,
    count(cc.id) AS component_count,
    ( SELECT count(*) AS count
           FROM public.comp_components
          WHERE ((comp_components.plan_id = cp.id) AND (comp_components.name ~~* '%revenue%'::text))) AS revenue_components,
    ( SELECT count(*) AS count
           FROM public.comp_components
          WHERE ((comp_components.plan_id = cp.id) AND (comp_components.name ~~* '%implant%'::text))) AS implant_components,
    ( SELECT count(*) AS count
           FROM public.comp_components
          WHERE (((comp_components.plan_id = cp.id) AND (comp_components.name ~~* '%margin%'::text)) OR (comp_components.name ~~* '%sgm%'::text))) AS margin_components,
    ( SELECT count(*) AS count
           FROM public.comp_components
          WHERE ((comp_components.plan_id = cp.id) AND (comp_components.name ~~* '%expense%'::text))) AS expense_components
   FROM (public.comp_plans cp
     LEFT JOIN public.comp_components cc ON ((cp.id = cc.plan_id)))
  GROUP BY cp.id, cp.title, cp.effective_dates, cp.summary;


ALTER VIEW public.spm_plan_overview OWNER TO todd;

--
-- Name: spm_role_coverage; Type: VIEW; Schema: public; Owner: todd
--

CREATE VIEW public.spm_role_coverage AS
 SELECT count(*) AS total_plans,
    sum(
        CASE
            WHEN ((title ~~* '%sales%'::text) OR (title ~~* '%representative%'::text)) THEN 1
            ELSE 0
        END) AS sales_roles,
    sum(
        CASE
            WHEN ((title ~~* '%service%'::text) OR (title ~~* '%specialist%'::text) OR (title ~~* '%clinical%'::text)) THEN 1
            ELSE 0
        END) AS service_roles,
    sum(
        CASE
            WHEN ((title ~~* '%manager%'::text) OR (title ~~* '%director%'::text) OR (title ~~* '%vp%'::text)) THEN 1
            ELSE 0
        END) AS leadership_roles
   FROM public.comp_plans;


ALTER VIEW public.spm_role_coverage OWNER TO todd;

--
-- Name: cleaning_patterns id; Type: DEFAULT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.cleaning_patterns ALTER COLUMN id SET DEFAULT nextval('public.cleaning_patterns_id_seq'::regclass);


--
-- Name: comp_components id; Type: DEFAULT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.comp_components ALTER COLUMN id SET DEFAULT nextval('public.comp_components_id_seq'::regclass);


--
-- Name: comp_plans id; Type: DEFAULT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.comp_plans ALTER COLUMN id SET DEFAULT nextval('public.comp_plans_id_seq'::regclass);


--
-- Name: comp_provisions id; Type: DEFAULT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.comp_provisions ALTER COLUMN id SET DEFAULT nextval('public.comp_provisions_id_seq'::regclass);


--
-- Name: comp_tags id; Type: DEFAULT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.comp_tags ALTER COLUMN id SET DEFAULT nextval('public.comp_tags_id_seq'::regclass);


--
-- Name: processing_status id; Type: DEFAULT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.processing_status ALTER COLUMN id SET DEFAULT nextval('public.processing_status_id_seq'::regclass);


--
-- Name: cleaning_patterns cleaning_patterns_pkey; Type: CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.cleaning_patterns
    ADD CONSTRAINT cleaning_patterns_pkey PRIMARY KEY (id);


--
-- Name: comp_components comp_components_pkey; Type: CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.comp_components
    ADD CONSTRAINT comp_components_pkey PRIMARY KEY (id);


--
-- Name: comp_plans comp_plans_pkey; Type: CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.comp_plans
    ADD CONSTRAINT comp_plans_pkey PRIMARY KEY (id);


--
-- Name: comp_provisions comp_provisions_pkey; Type: CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.comp_provisions
    ADD CONSTRAINT comp_provisions_pkey PRIMARY KEY (id);


--
-- Name: comp_tags comp_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.comp_tags
    ADD CONSTRAINT comp_tags_pkey PRIMARY KEY (id);


--
-- Name: processing_status processing_status_pkey; Type: CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.processing_status
    ADD CONSTRAINT processing_status_pkey PRIMARY KEY (id);


--
-- Name: processing_status unique_file_path; Type: CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.processing_status
    ADD CONSTRAINT unique_file_path UNIQUE (file_path);


--
-- Name: idx_components_plan_id; Type: INDEX; Schema: public; Owner: todd
--

CREATE INDEX idx_components_plan_id ON public.comp_components USING btree (plan_id);


--
-- Name: idx_processing_status_file_path; Type: INDEX; Schema: public; Owner: todd
--

CREATE INDEX idx_processing_status_file_path ON public.processing_status USING btree (file_path);


--
-- Name: idx_provisions_plan_id; Type: INDEX; Schema: public; Owner: todd
--

CREATE INDEX idx_provisions_plan_id ON public.comp_provisions USING btree (plan_id);


--
-- Name: idx_tags_component_id; Type: INDEX; Schema: public; Owner: todd
--

CREATE INDEX idx_tags_component_id ON public.comp_tags USING btree (component_id);


--
-- Name: comp_plans update_comp_plans_timestamp; Type: TRIGGER; Schema: public; Owner: todd
--

CREATE TRIGGER update_comp_plans_timestamp BEFORE UPDATE ON public.comp_plans FOR EACH ROW EXECUTE FUNCTION public.update_timestamp();


--
-- Name: processing_status update_processing_status_timestamp; Type: TRIGGER; Schema: public; Owner: todd
--

CREATE TRIGGER update_processing_status_timestamp BEFORE UPDATE ON public.processing_status FOR EACH ROW EXECUTE FUNCTION public.update_timestamp();


--
-- Name: comp_components comp_components_plan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.comp_components
    ADD CONSTRAINT comp_components_plan_id_fkey FOREIGN KEY (plan_id) REFERENCES public.comp_plans(id) ON DELETE CASCADE;


--
-- Name: comp_provisions comp_provisions_plan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.comp_provisions
    ADD CONSTRAINT comp_provisions_plan_id_fkey FOREIGN KEY (plan_id) REFERENCES public.comp_plans(id) ON DELETE CASCADE;


--
-- Name: comp_tags comp_tags_component_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: todd
--

ALTER TABLE ONLY public.comp_tags
    ADD CONSTRAINT comp_tags_component_id_fkey FOREIGN KEY (component_id) REFERENCES public.comp_components(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

