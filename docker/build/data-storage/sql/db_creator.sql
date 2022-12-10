--
-- PostgreSQL database dump
--

-- Dumped from database version 11.18
-- Dumped by pg_dump version 11.18

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

SET default_with_oids = false;

--
-- Name: action_configs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.action_configs (
    id smallint NOT NULL,
    is_continuous boolean NOT NULL
);


ALTER TABLE public.action_configs OWNER TO postgres;

--
-- Name: continuous_action_spaces; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.continuous_action_spaces (
    id smallint NOT NULL,
    speed_min smallint NOT NULL,
    speed_max smallint NOT NULL,
    steering_left_max smallint NOT NULL,
    steering_right_max character varying NOT NULL
);


ALTER TABLE public.continuous_action_spaces OWNER TO postgres;

--
-- Name: discreate_action_spaces; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.discreate_action_spaces (
    id smallint NOT NULL,
    steering_angle smallint NOT NULL,
    speed smallint NOT NULL
);


ALTER TABLE public.discreate_action_spaces OWNER TO postgres;

--
-- Name: hyperparameters; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.hyperparameters (
    id smallint NOT NULL,
    batch_size smallint NOT NULL,
    beta_entropy numeric NOT NULL,
    discount_factor numeric NOT NULL,
    e_greedy_value numeric NOT NULL,
    epsilon_steps smallint NOT NULL,
    exploration_type character varying(20) NOT NULL,
    loss_type character varying(20) NOT NULL,
    lr numeric NOT NULL,
    num_episodes_between_training smallint NOT NULL,
    num_epochs smallint NOT NULL,
    stack_size integer NOT NULL,
    term_cond_avg_score numeric NOT NULL,
    term_cond_max_episodes smallint NOT NULL,
    sac_alpha numeric NOT NULL
);


ALTER TABLE public.hyperparameters OWNER TO postgres;

--
-- Name: COLUMN hyperparameters.lr; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.hyperparameters.lr IS 'The learning rate';


--
-- Name: machine; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.machine (
    id smallint NOT NULL,
    name character varying NOT NULL
);


ALTER TABLE public.machine OWNER TO postgres;

--
-- Name: training_runs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.training_runs (
    id smallint NOT NULL,
    model_name character varying(30) NOT NULL,
    model_cloned_from character varying(30),
    start_time timestamp without time zone NOT NULL,
    stop_time timestamp without time zone,
    worker_amount smallint NOT NULL,
    reward_function text NOT NULL,
    hyperparameters_id smallint NOT NULL,
    action_space_id smallint NOT NULL,
    training_remark character varying NOT NULL,
    machine_id smallint NOT NULL,
    best_lap_time interval NOT NULL,
    average_lap_time interval NOT NULL,
    end_training_completion_rate_percent smallint NOT NULL,
    end_eval_completion_percent smallint NOT NULL
);


ALTER TABLE public.training_runs OWNER TO postgres;

--
-- Name: COLUMN training_runs.model_cloned_from; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.training_runs.model_cloned_from IS 'Can be null if it has not been pretrained';


--
-- Name: COLUMN training_runs.stop_time; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.training_runs.stop_time IS 'Is null while training is running';


--
-- Data for Name: action_configs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.action_configs (id, is_continuous) FROM stdin;
\.


--
-- Data for Name: continuous_action_spaces; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.continuous_action_spaces (id, speed_min, speed_max, steering_left_max, steering_right_max) FROM stdin;
\.


--
-- Data for Name: discreate_action_spaces; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.discreate_action_spaces (id, steering_angle, speed) FROM stdin;
\.


--
-- Data for Name: hyperparameters; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.hyperparameters (id, batch_size, beta_entropy, discount_factor, e_greedy_value, epsilon_steps, exploration_type, loss_type, lr, num_episodes_between_training, num_epochs, stack_size, term_cond_avg_score, term_cond_max_episodes, sac_alpha) FROM stdin;
\.


--
-- Data for Name: machine; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.machine (id, name) FROM stdin;
\.


--
-- Data for Name: training_runs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.training_runs (id, model_name, model_cloned_from, start_time, stop_time, worker_amount, reward_function, hyperparameters_id, action_space_id, training_remark, machine_id, best_lap_time, average_lap_time, end_training_completion_rate_percent, end_eval_completion_percent) FROM stdin;
\.


--
-- Name: action_configs action_configs_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.action_configs
    ADD CONSTRAINT action_configs_pk PRIMARY KEY (id);


--
-- Name: continuous_action_spaces continuous_action_spaces_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.continuous_action_spaces
    ADD CONSTRAINT continuous_action_spaces_pk PRIMARY KEY (id);


--
-- Name: discreate_action_spaces discreate_action_spaces_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.discreate_action_spaces
    ADD CONSTRAINT discreate_action_spaces_pk PRIMARY KEY (id);


--
-- Name: hyperparameters hyper_parameters_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hyperparameters
    ADD CONSTRAINT hyper_parameters_pk PRIMARY KEY (id);


--
-- Name: machine machine_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.machine
    ADD CONSTRAINT machine_pk PRIMARY KEY (id);


--
-- Name: training_runs training_runs_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.training_runs
    ADD CONSTRAINT training_runs_pk PRIMARY KEY (id);


--
-- Name: training_runs fk_hyperparameters; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.training_runs
    ADD CONSTRAINT fk_hyperparameters FOREIGN KEY (hyperparameters_id) REFERENCES public.hyperparameters(id);


--
-- Name: training_runs fk_machine; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.training_runs
    ADD CONSTRAINT fk_machine FOREIGN KEY (machine_id) REFERENCES public.machine(id);


--
-- PostgreSQL database dump complete
--

