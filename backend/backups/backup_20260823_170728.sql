--
-- PostgreSQL database dump
--

\restrict nCEgyN68D9RYFCfHRhhlFpM0JR85zyr7kXeVqrRVWib5ogC83q1l4o71Q6EXNgV

-- Dumped from database version 15.18
-- Dumped by pg_dump version 17.11 (Debian 17.11-0+deb13u1)

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
-- Name: frequencytype; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.frequencytype AS ENUM (
    'fixed',
    'variable'
);


--
-- Name: transactiontype; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.transactiontype AS ENUM (
    'income',
    'expense',
    'invest'
);


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: backup_settings; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.backup_settings (
    id integer NOT NULL,
    frequency_days integer NOT NULL,
    updated_at timestamp with time zone DEFAULT now()
);


--
-- Name: backup_settings_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.backup_settings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: backup_settings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.backup_settings_id_seq OWNED BY public.backup_settings.id;


--
-- Name: categories; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.categories (
    id integer NOT NULL,
    name character varying NOT NULL,
    description character varying,
    transaction_type public.transactiontype NOT NULL,
    parent_id integer,
    user_id integer,
    is_predefined boolean,
    icon character varying,
    created_at timestamp with time zone DEFAULT now()
);


--
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;


--
-- Name: monthly_budgets; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.monthly_budgets (
    id integer NOT NULL,
    user_id integer,
    year integer,
    month integer,
    amount double precision
);


--
-- Name: monthly_budgets_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.monthly_budgets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: monthly_budgets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.monthly_budgets_id_seq OWNED BY public.monthly_budgets.id;


--
-- Name: transactions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.transactions (
    id integer NOT NULL,
    type public.transactiontype NOT NULL,
    amount numeric(12,2) NOT NULL,
    date timestamp with time zone DEFAULT now(),
    category_id integer NOT NULL,
    description character varying,
    notes text,
    is_paid boolean NOT NULL,
    frequency public.frequencytype,
    user_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


--
-- Name: transactions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.transactions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: transactions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.transactions_id_seq OWNED BY public.transactions.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id integer NOT NULL,
    email character varying,
    hashed_password character varying,
    created_at timestamp with time zone DEFAULT now()
);


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: backup_settings id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.backup_settings ALTER COLUMN id SET DEFAULT nextval('public.backup_settings_id_seq'::regclass);


--
-- Name: categories id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);


--
-- Name: monthly_budgets id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.monthly_budgets ALTER COLUMN id SET DEFAULT nextval('public.monthly_budgets_id_seq'::regclass);


--
-- Name: transactions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.transactions ALTER COLUMN id SET DEFAULT nextval('public.transactions_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: backup_settings; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.backup_settings (id, frequency_days, updated_at) FROM stdin;
1	5	2026-08-23 17:07:26.817271+00
\.


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.categories (id, name, description, transaction_type, parent_id, user_id, is_predefined, icon, created_at) FROM stdin;
56	Supermercado	\N	expense	49	1	t	shopping-bag	2026-04-22 22:36:31.056917+00
1	Transporte	Categoría padre para gastos de transporte	expense	\N	\N	t	car	2026-04-21 16:02:37.472945+00
2	Coche	Gastos del automóvil	expense	1	\N	t	car	2026-04-21 16:02:37.472945+00
3	Moto	Gastos de moto	expense	1	\N	t	bike	2026-04-21 16:02:37.472945+00
5	Gasolina	Combustible	expense	1	\N	t	fuel	2026-04-21 16:02:37.472945+00
8	Restaurante	Comidas fuera de casa	expense	6	\N	t	utensils	2026-04-21 16:02:37.472945+00
7	Supermercado	Compras de supermercado	expense	6	\N	t	shopping-cart	2026-04-21 16:02:37.472945+00
6	Alimentación	Categoría padre para gastos de comida	expense	\N	\N	t	apple	2026-04-21 16:02:37.472945+00
9	Vivienda	Categoría padre para gastos de casa	expense	\N	\N	t	home	2026-04-21 16:02:37.472945+00
10	Alquiler	Pago de alquiler	expense	9	\N	t	key	2026-04-21 16:02:37.472945+00
11	Servicios	Agua, luz, internet	expense	9	\N	t	zap	2026-04-21 16:02:37.472945+00
12	Mantenimiento	Reparaciones y limpieza	expense	9	\N	t	wrench	2026-04-21 16:02:37.472945+00
13	Ocio	Entretenimiento y diversión	expense	\N	\N	t	film	2026-04-21 16:02:37.472945+00
14	Cine	Películas y entretenimiento	expense	13	\N	t	ticket	2026-04-21 16:02:37.472945+00
15	Suscripciones	Netflix, Spotify, etc	expense	13	\N	t	music	2026-04-21 16:02:37.472945+00
58	Comida fuera	\N	expense	49	1	t	utensils	2026-04-22 22:36:31.056917+00
59	Restaurantes	\N	expense	50	1	t	utensils-crossed	2026-04-22 22:36:31.079877+00
19	Inversiones	Dinero invertido	invest	\N	\N	t	trending-up	2026-04-21 16:02:37.472945+00
20	Bolsa	Inversión en acciones	invest	19	\N	t	line-chart	2026-04-21 16:02:37.472945+00
21	Criptomonedas	Inversión en cripto	invest	19	\N	t	bitcoin	2026-04-21 16:02:37.472945+00
16	Salario	Ingresos laborales	income	\N	\N	t	wallet	2026-04-21 16:02:37.472945+00
17	Freelance	Trabajos puntuales	income	\N	\N	t	briefcase	2026-04-21 16:02:37.472945+00
18	Otros Ingresos	Ingresos diversos	income	\N	\N	t	plus-circle	2026-04-21 16:02:37.472945+00
4	Recambios	Repuestos y accesorios	expense	1	\N	t	wrench	2026-04-21 16:02:37.472945+00
108	Gato	\N	expense	\N	1	f	cat	2026-04-30 08:49:15.738848+00
41	Trabajo	\N	income	\N	1	t	briefcase	2026-04-22 22:36:30.97655+00
42	Extra	\N	income	\N	1	t	gift	2026-04-22 22:36:30.97655+00
43	Finanzas	\N	income	\N	1	t	trending-up	2026-04-22 22:36:30.97655+00
44	Salario	\N	income	41	1	t	wallet	2026-04-22 22:36:31.009658+00
45	Billetazo	\N	income	42	1	t	banknote	2026-04-22 22:36:31.009658+00
46	Bizum	\N	income	42	1	t	smartphone	2026-04-22 22:36:31.009658+00
47	Intereses	\N	income	43	1	t	percent	2026-04-22 22:36:31.009658+00
48	Dividendos	\N	income	43	1	t	line-chart	2026-04-22 22:36:31.009658+00
49	Vida básica	\N	expense	\N	1	t	shopping-cart	2026-04-22 22:36:31.040548+00
50	Ocio	\N	expense	\N	1	t	party-popper	2026-04-22 22:36:31.040548+00
52	Tecnología	\N	expense	\N	1	t	monitor	2026-04-22 22:36:31.040548+00
67	Recambios	\N	expense	51	1	t	wrench	2026-04-22 22:36:31.102811+00
109	Comida	\N	expense	108	1	f	cookie	2026-04-30 08:49:29.707087+00
69	Inversión	Bloque de inversiones financieras	invest	\N	1	f	trending-up	2026-04-22 22:40:06.186316+00
70	ETF	Fondos cotizados	invest	69	1	f	chart-candlestick	2026-04-22 22:40:06.204328+00
71	Fondos indexados	Fondos indexados a largo plazo	invest	69	1	f	chart-line	2026-04-22 22:40:06.219895+00
72	Acciones	Acciones individuales (Tesla, Nvidia, etc.)	invest	69	1	f	building-2	2026-04-22 22:40:06.234612+00
73	Crypto	Criptomonedas	invest	69	1	f	bitcoin	2026-04-22 22:40:06.25517+00
74	Rentabilidad	Intereses, TAE, cuentas remuneradas	invest	69	1	f	percent	2026-04-22 22:40:06.270658+00
110	Cuidados	\N	expense	108	1	f	stethoscope	2026-04-30 08:49:50.949534+00
51	Transporte	\N	expense	\N	1	t	car	2026-04-22 22:36:31.040548+00
60	Viajes	\N	expense	50	1	t	plane	2026-04-22 22:36:31.079877+00
111	Juguetes	\N	expense	108	1	f	smile	2026-04-30 08:50:02.609211+00
105	Coche	\N	expense	51	1	f	car	2026-04-23 21:28:35.696067+00
104	Moto	\N	expense	51	1	f	motorbike	2026-04-23 21:28:29.560284+00
101	Salud y Belleza	\N	expense	49	1	f	heart	2026-04-23 21:26:11.573841+00
106	Ropa	\N	expense	49	1	f	shirt	2026-04-24 07:07:38.510514+00
62	Terrazeo	\N	expense	50	1	t	sun	2026-04-22 22:36:31.079877+00
102	Hardware	\N	expense	52	1	f	laptop	2026-04-23 21:26:48.46324+00
107	Subscripciones	\N	expense	52	1	f	receipt	2026-04-24 07:29:49.029913+00
103	Aliexpress / Amazon	\N	expense	52	1	f	shopping-bag	2026-04-23 21:27:39.521755+00
22	Hotel	\N	expense	50	1	f	building	2026-07-04 07:54:53.648147+00
23	Cosas Casa	\N	expense	49	1	f	house	2026-07-04 09:07:04.326741+00
25	Donación 	\N	income	42	1	f	coins	2026-08-10 06:27:21.679277+00
26	Público	\N	expense	51	1	f	train	2026-08-10 11:13:08.170022+00
\.


--
-- Data for Name: monthly_budgets; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.monthly_budgets (id, user_id, year, month, amount) FROM stdin;
\.


--
-- Data for Name: transactions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.transactions (id, type, amount, date, category_id, description, notes, is_paid, frequency, user_id, created_at, updated_at) FROM stdin;
62	expense	13.90	2026-04-19 00:00:00+00	62	Desayuno Milla	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 09:32:01.079668+00
63	expense	10.78	2026-04-18 00:00:00+00	102	Mando Ps4	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 09:32:26.653604+00
65	invest	50.00	2026-04-16 00:00:00+00	72	IONQ 	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 09:32:39.956505+00
66	expense	7.20	2026-04-14 00:00:00+00	62	Tardeo Milla	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 09:32:46.935627+00
59	expense	19.45	2026-04-19 00:00:00+00	103	Visor Casco	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 09:35:45.817966+00
52	expense	1.70	2026-04-22 00:00:00+00	56	Pan	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
53	expense	12.00	2026-04-22 00:00:00+00	101	Corte Pelo	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
60	income	50.00	2026-04-19 00:00:00+00	45	Papá	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
64	invest	25.00	2026-04-16 00:00:00+00	73	ETH x 0,012147	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
58	expense	4.80	2026-04-19 00:00:00+00	62	Refrescos Milla	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 09:40:55.040131+00
51	expense	4.80	2026-04-23 00:00:00+00	62	Refrescos Milla	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 09:42:59.682486+00
54	income	301.32	2026-04-20 00:00:00+00	44	Nómina Audasa Abril	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 18:28:02.127146+00
61	expense	16.30	2026-04-19 00:00:00+00	104	Gasolina	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-28 16:19:21.61084+00
55	invest	50.00	2026-05-04 00:00:00+00	70	Nuclear Technologies IE000M7V94E1	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-05-04 06:59:20.806216+00
57	invest	20.00	2026-05-04 00:00:00+00	71	Fidelity MSCI Emerging Markets IE00BYX5M476	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-05-09 15:26:41.215029+00
56	invest	70.00	2026-05-04 00:00:00+00	71	Fidelity S&P 500  IE00BYX5MX67	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-05-09 15:26:52.665941+00
68	expense	1.50	2026-04-14 00:00:00+00	52	Venta HealthCare Basurón	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
71	income	76.93	2026-04-10 00:00:00+00	45	Renta 2025	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
73	expense	5.00	2026-04-09 00:00:00+00	105	Parking Parlamento OTTO	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
77	expense	7.80	2026-04-06 00:00:00+00	56	Mercadona	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
78	income	50.00	2026-04-04 00:00:00+00	45	Papá	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
79	income	4.30	2026-04-04 00:00:00+00	45	Propinas	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
80	income	4.90	2026-04-03 00:00:00+00	45	Propinas	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
81	income	2.00	2026-04-03 00:00:00+00	45	Propinas	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
82	expense	15.00	2026-04-03 00:00:00+00	105	Gasolina	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
84	expense	3.40	2026-04-02 00:00:00+00	50	Tardeo	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
85	expense	22.72	2026-04-02 00:00:00+00	67	Recambios Bici + Complementos Ropa Moto	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
87	invest	20.00	2026-04-02 00:00:00+00	71	Fidelity MSCI Emerging Markets IE00BYX5M476	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
88	invest	30.00	2026-04-02 00:00:00+00	70	VanEck Semiconductor	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
91	expense	6.20	2026-03-31 00:00:00+00	50	Tardeo Paz Roja	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
92	expense	12.28	2026-03-31 00:00:00+00	52	Pasta MX4	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
94	expense	0.50	2026-03-31 00:00:00+00	50	Lavado Bici	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
95	expense	16.72	2026-03-30 00:00:00+00	105	Gasolina	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
96	expense	3.95	2026-03-30 00:00:00+00	56	Pan	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
97	income	50.00	2026-03-29 00:00:00+00	45	Papá	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
98	expense	87.11	2026-03-29 00:00:00+00	52	CPU + Placa Base	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
99	expense	8.14	2026-03-27 00:00:00+00	50	Cactus Garden	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
101	expense	5.00	2026-03-26 00:00:00+00	104	Arreglo botas	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
104	expense	6.80	2026-03-23 00:00:00+00	52	Freno 180mm Bici	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
105	expense	1.15	2026-03-23 00:00:00+00	105	ORA	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
107	expense	3.70	2026-03-23 00:00:00+00	52	Correos Separadores Socket	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
108	expense	3.39	2026-03-22 00:00:00+00	107	Spotify	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
110	income	50.00	2026-03-22 00:00:00+00	45	Papá	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
111	expense	1.80	2026-03-20 00:00:00+00	56	Pan	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
112	expense	18.19	2026-03-20 00:00:00+00	52	MX Master 3S 3/3	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
113	expense	24.63	2026-03-19 00:00:00+00	106	Badana y frenos bici	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
115	income	50.00	2026-03-15 00:00:00+00	45	Papá	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
117	expense	14.13	2026-03-13 00:00:00+00	106	5 x Camisetas Básicas	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
118	expense	0.44	2026-03-12 00:00:00+00	106	Chaqueta Dainese	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
119	expense	3.40	2026-03-12 00:00:00+00	50	Tardeo Milla	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
121	expense	4.60	2026-03-11 00:00:00+00	50	Tardeo Milla	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
122	expense	16.00	2026-03-11 00:00:00+00	105	Gasolina	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
125	expense	40.00	2026-03-10 00:00:00+00	105	Diesel	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
126	expense	5.10	2026-03-08 00:00:00+00	50	Tardeo Santiago	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
127	income	80.00	2026-03-07 00:00:00+00	45	Abuelos	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
128	income	50.00	2026-03-07 00:00:00+00	45	Papá	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
131	invest	70.00	2026-03-02 00:00:00+00	71	Fidelity MSCI Emerging Markets IE00BYX5M476	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
132	invest	60.00	2026-03-02 00:00:00+00	70	VanEck Semiconductor	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
133	invest	20.00	2026-03-02 00:00:00+00	73	BTC x 0,000344	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
134	invest	10.00	2026-03-02 00:00:00+00	73	ETH x 0,005866	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
135	income	6.28	2026-03-01 00:00:00+00	47	Efectivo 2%	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
136	income	50.00	2026-03-01 00:00:00+00	45	Papá	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
137	expense	2.40	2026-02-28 00:00:00+00	50	Velas	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
70	expense	8.40	2026-04-10 00:00:00+00	62	Comida Playa	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 09:33:21.207157+00
93	expense	3.00	2026-03-31 00:00:00+00	102	Pasta Térmica	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 09:33:28.377954+00
103	expense	1.60	2026-03-25 00:00:00+00	62	Desayuno	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 09:36:54.716153+00
114	expense	3.20	2026-03-16 00:00:00+00	62	Desayuno Milla	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 09:37:33.632224+00
75	expense	15.00	2026-04-08 00:00:00+00	59	Comida Cañiza	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 09:37:45.982435+00
120	expense	20.00	2026-03-12 00:00:00+00	59	Comidita Milla	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 09:37:53.44669+00
83	expense	15.40	2026-04-02 00:00:00+00	59	Cena cotón	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 09:38:49.191678+00
116	expense	7.40	2026-03-13 00:00:00+00	62	Desayuno San Lázaro	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 09:38:59.51291+00
129	expense	5.08	2026-03-03 00:00:00+00	62	Desayuno San Lázaro	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 09:39:10.455295+00
89	expense	6.40	2026-04-01 00:00:00+00	62	Cafés	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 09:40:00.711251+00
72	income	553.00	2026-04-10 00:00:00+00	44	Subsidio	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-08-21 12:22:19.626571+00
100	expense	3.20	2026-03-26 00:00:00+00	62	Café Mañana	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 09:40:10.063398+00
106	expense	3.10	2026-03-23 00:00:00+00	62	Café Nómada	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 09:40:33.163181+00
123	expense	3.00	2026-03-11 00:00:00+00	62	Café Sta Marta	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 09:40:37.678644+00
102	expense	4.50	2026-03-25 00:00:00+00	62	Refrescos Mañana	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 09:41:04.99258+00
130	invest	210.00	2026-03-02 00:00:00+00	71	Fidelity S&P 500  IE00BYX5MX67	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-05-09 15:27:04.838435+00
76	expense	2.99	2026-04-08 00:00:00+00	107	iCloud	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-28 16:17:30.177659+00
109	expense	30.00	2026-03-22 00:00:00+00	105	Diésel	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-28 16:18:06.26108+00
74	expense	35.00	2026-04-08 00:00:00+00	105	Diésel	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-28 16:19:34.572116+00
90	income	8.85	2026-03-31 00:00:00+00	47	TAE	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-05-13 09:13:42.400541+00
138	expense	21.67	2026-02-28 00:00:00+00	50	Churrasco Milongas	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
139	expense	10.00	2026-02-25 00:00:00+00	59	Tarta	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
140	expense	3.30	2026-02-24 00:00:00+00	50	Tardeo Cumple	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
141	expense	10.49	2026-02-23 00:00:00+00	107	Spotify	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
142	expense	12.00	2026-02-23 00:00:00+00	101	Corte Pelo	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
143	expense	21.50	2026-02-21 00:00:00+00	50	Kebabs Berta	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
144	expense	5.60	2026-02-21 00:00:00+00	50	Tardeo Berta	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
145	income	70.00	2026-02-21 00:00:00+00	45	Papá	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
146	expense	46.00	2026-02-20 00:00:00+00	50	Balneario	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
147	expense	1.50	2026-02-20 00:00:00+00	50	Prueba Ventas	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
148	income	752.02	2026-02-20 00:00:00+00	44	Finiquito	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
149	expense	18.20	2026-02-20 00:00:00+00	52	MX Master 3S 2/3	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
150	expense	40.00	2026-02-19 00:00:00+00	105	Diesel	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
151	expense	7.50	2026-02-18 00:00:00+00	50	Tardeo Deivid Dani	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
152	expense	1.05	2026-02-18 00:00:00+00	105	ORA	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
154	expense	20.00	2026-02-16 00:00:00+00	67	Secado Agua Coche	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
155	expense	0.93	2026-02-16 00:00:00+00	52	Venta XEON	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
156	invest	8.00	2026-02-16 00:00:00+00	73	ETH x 0,000301	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
157	invest	8.00	2026-02-16 00:00:00+00	73	BTC x  0,004663	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
158	expense	3.05	2026-02-15 00:00:00+00	105	Parking Analítica	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
160	income	50.00	2026-02-15 00:00:00+00	45	Papá	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
161	expense	10.00	2026-02-15 00:00:00+00	105	Diesel	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
163	expense	5.80	2026-02-14 00:00:00+00	50	Tarde S Valentin	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
164	expense	37.29	2026-02-13 00:00:00+00	52	Entrada LareiraConf	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
165	income	170.00	2026-02-12 00:00:00+00	45	Regalo Cumple	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
167	income	50.00	2026-02-08 00:00:00+00	45	Papá	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
169	expense	4.30	2026-02-07 00:00:00+00	50	Tardeo	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
170	expense	3.89	2026-02-05 00:00:00+00	67	Insignia Volante BMW	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
171	expense	7.45	2026-02-05 00:00:00+00	52	TRS Altavoces + 2x Pads MX Master 3S	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
173	expense	1.06	2026-02-03 00:00:00+00	56	Pan	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
175	expense	0.70	2026-02-02 00:00:00+00	105	ORA	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
176	expense	35.00	2026-02-02 00:00:00+00	105	Diesel	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
177	invest	8.00	2026-02-02 00:00:00+00	73	ETH x 0,004125	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
178	invest	18.00	2026-02-02 00:00:00+00	73	BTC x 0,000268	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
179	income	0.69	2026-02-01 00:00:00+00	47	2 % TAE Enero TR	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
180	income	50.00	2026-02-01 00:00:00+00	45	Papá	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
181	income	363.25	2026-01-30 00:00:00+00	44	Nómina Dixitalia Software	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
182	expense	27.83	2026-01-30 00:00:00+00	106	Shein - 2 Jerseys 5 Corbatas	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
183	expense	0.60	2026-01-30 00:00:00+00	105	ORA	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
184	expense	0.55	2026-01-29 00:00:00+00	105	ORA	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
186	expense	0.20	2026-01-28 00:00:00+00	105	ORA	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
187	expense	0.60	2026-01-27 00:00:00+00	105	ORA	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
188	expense	1.00	2026-01-26 00:00:00+00	52	Comisión Compra ETF	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
189	expense	1.00	2026-01-25 00:00:00+00	105	Lavado	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
190	expense	6.90	2026-01-25 00:00:00+00	50	Tardeo trastienda	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
191	income	50.00	2026-01-25 00:00:00+00	45	Papá	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
192	income	20.00	2026-01-25 00:00:00+00	45	Mama	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
193	expense	1.00	2026-01-25 00:00:00+00	52	Comisión ETH	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
194	invest	10.00	2026-01-25 00:00:00+00	73	ETH x 0,004009	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
195	expense	1.00	2026-01-25 00:00:00+00	52	Comisión BTC	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
196	invest	24.97	2026-01-25 00:00:00+00	73	BTC x 0,000332	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
198	expense	3.89	2026-01-21 00:00:00+00	52	Spotify Familiar	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
199	expense	18.20	2026-01-20 00:00:00+00	52	MX Master 3S 1/3	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
200	income	50.00	2026-01-18 00:00:00+00	45	Papá	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
201	expense	5.10	2026-01-16 00:00:00+00	50	Tardeo	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
202	expense	35.00	2026-01-16 00:00:00+00	50	Noche Milla B&B	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
203	expense	0.30	2026-01-16 00:00:00+00	105	ORA	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
204	expense	7.50	2026-01-16 00:00:00+00	50	Bingo	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
205	expense	15.01	2026-01-15 00:00:00+00	105	Gasolina	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
206	expense	1.05	2026-01-14 00:00:00+00	105	ORA	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
207	expense	40.00	2026-01-14 00:00:00+00	105	Gasolinera	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
209	income	513.00	2026-01-12 00:00:00+00	44	Subsidio SEPE	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
208	expense	13.40	2026-01-14 00:00:00+00	62	Desayuno Cangaceiro	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 09:39:31.267061+00
185	expense	3.80	2026-01-28 00:00:00+00	62	Café La Morena pre exam	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 09:37:18.502478+00
168	expense	20.00	2026-02-07 00:00:00+00	59	Cena  LaCarpantaSCQ	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 09:38:39.226703+00
162	expense	21.20	2026-02-14 00:00:00+00	59	Cena S Valentin	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 09:38:43.742242+00
159	expense	1.50	2026-02-15 00:00:00+00	62	Desayuno Analítica	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 09:39:19.034348+00
174	expense	3.40	2026-02-03 00:00:00+00	62	Cafés Santa Marta	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 09:40:26.577326+00
172	expense	4.70	2026-02-05 00:00:00+00	62	Cafés Trastienda + Agua	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 09:40:41.975545+00
210	income	50.00	2026-01-11 00:00:00+00	45	Papá	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
211	expense	1.05	2026-01-09 00:00:00+00	105	ORA	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
213	expense	2.99	2026-01-09 00:00:00+00	107	iCloud	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
215	expense	7.70	2026-01-07 00:00:00+00	50	Tardeo Milla	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
216	income	50.00	2026-01-04 00:00:00+00	45	Papá	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
217	expense	8.46	2026-01-02 00:00:00+00	52	Hosting eloylozano.es	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
218	expense	13.50	2026-01-01 00:00:00+00	50	Copeo FDA	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 08:50:11.285042+00
67	expense	2.10	2026-04-14 00:00:00+00	62	Café	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 09:33:03.912552+00
275	expense	0.50	2026-05-06 00:00:00+00	102	Tuercas placa base 	Tuercas placa base 	t	variable	1	2026-05-06 14:15:42.121735+00	2026-05-06 14:15:42.121735+00
197	expense	1.50	2026-01-24 00:00:00+00	62	Café Web Bar Sigüeiro	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 09:36:42.556959+00
212	expense	13.50	2026-01-09 00:00:00+00	59	China Ming	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 09:38:05.53546+00
214	expense	7.00	2026-01-09 00:00:00+00	62	Desayuno Milla	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 09:39:41.569017+00
153	expense	5.20	2026-02-16 00:00:00+00	62	Refrescos Espera Secado	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-04-24 09:41:08.980572+00
276	expense	4.09	2026-05-06 00:00:00+00	103	Cables CAT 7	Cables CAT 7	t	variable	1	2026-05-06 20:01:01.911336+00	2026-05-06 20:01:13.228002+00
278	income	70.00	2026-05-07 00:00:00+00	45	Abuelos	Abuelos	t	variable	1	2026-05-07 19:59:16.104789+00	2026-05-07 19:59:16.104789+00
279	expense	2.80	2026-05-08 00:00:00+00	103	Cúter Chino	Cúter Chino	t	variable	1	2026-05-08 20:17:34.879072+00	2026-05-08 20:17:34.879072+00
219	expense	3.39	2026-04-20 00:00:00+00	107	Spotify	Spotify	t	fixed	1	2026-04-24 09:35:24.188424+00	2026-04-24 18:29:47.7494+00
280	expense	1.00	2026-05-08 00:00:00+00	105	ORA	ORA	t	variable	1	2026-05-08 20:54:26.943111+00	2026-05-08 20:54:26.943111+00
224	income	100.00	2026-04-25 00:00:00+00	46	Otto365 Adelanto Web Pomeranias	Otto365 Adelanto Web Pomeranias	t	variable	1	2026-04-25 08:09:35.106161+00	2026-04-25 08:09:35.106161+00
281	income	456.00	2026-05-06 00:00:00+00	44	Subsidio	Subsidio	t	variable	1	2026-05-08 20:54:46.2148+00	2026-05-08 20:54:46.2148+00
225	expense	0.70	2026-04-25 00:00:00+00	105	ORA	ORA	t	variable	1	2026-04-28 12:13:05.329421+00	2026-04-28 12:13:05.329421+00
227	expense	1.60	2026-04-25 00:00:00+00	56	Comida	Comida	t	variable	1	2026-04-28 12:13:42.881552+00	2026-04-28 12:13:42.881552+00
231	expense	1.00	2026-04-26 00:00:00+00	104	Lavado	Lavado	t	variable	1	2026-04-28 12:15:41.625161+00	2026-04-28 12:15:41.625161+00
86	invest	75.00	2026-04-02 00:00:00+00	71	Fidelity S&P 500  IE00BYX5MX67	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-05-09 15:26:59.955721+00
286	income	50.00	2026-05-10 00:00:00+00	45	Papá	Papá	t	variable	1	2026-05-10 06:49:32.423655+00	2026-05-10 06:49:32.423655+00
226	expense	3.00	2026-04-25 00:00:00+00	105	Lavado	Lavado	t	variable	1	2026-04-28 12:13:18.377202+00	2026-04-28 16:17:48.710741+00
228	expense	30.00	2026-04-25 00:00:00+00	105	Diésel	Diésel	t	variable	1	2026-04-28 12:13:57.180435+00	2026-04-28 16:19:06.880483+00
233	expense	5.90	2026-04-30 00:00:00+00	111	Cola para rascador	Cola para rascador	t	variable	1	2026-04-30 09:58:08.651105+00	2026-04-30 09:58:08.651105+00
230	expense	51.76	2026-04-26 00:00:00+00	102	Piezas Server	Piezas Server	t	variable	1	2026-04-28 12:15:18.472778+00	2026-04-30 12:31:41.842871+00
234	expense	3.50	2026-04-30 00:00:00+00	62	Cafés	Cafés	t	variable	1	2026-05-01 08:07:39.864749+00	2026-05-01 08:07:39.864749+00
235	expense	11.95	2026-04-30 00:00:00+00	110	Peines, cortaúñas, pala cacas	Peines, cortaúñas, pala cacas	t	variable	1	2026-05-01 08:08:10.119406+00	2026-05-01 08:08:19.940188+00
236	expense	48.90	2026-05-01 00:00:00+00	110	Comederos, bebederos, peine, tapete, manta y juguetes	Comederos, bebederos, peine, tapete, manta y juguetes	t	variable	1	2026-05-01 16:00:22.013762+00	2026-05-01 16:00:22.013762+00
237	expense	8.00	2026-05-02 00:00:00+00	59	Comida Audasa	Comida Audasa	t	variable	1	2026-05-02 11:48:36.826857+00	2026-05-02 11:48:36.826857+00
270	expense	10.00	2026-05-01 00:00:00+00	59	Cena BurgerKing	Cena BurgerKing	t	variable	1	2026-05-03 08:27:33.7239+00	2026-05-03 08:27:53.063077+00
232	expense	3.20	2026-04-30 00:00:00+00	56	Pan	Pan	t	variable	1	2026-04-30 08:58:12.131246+00	2026-05-03 08:28:22.423354+00
271	income	9.07	2026-05-01 00:00:00+00	47	Interés 2% TAE	Interés 2% TAE	t	variable	1	2026-05-03 08:29:39.462951+00	2026-05-03 08:29:39.462951+00
272	income	50.00	2026-05-03 00:00:00+00	45	Papá	Papá	t	variable	1	2026-05-03 08:36:53.9176+00	2026-05-03 08:36:53.9176+00
222	invest	30.00	2026-05-04 00:00:00+00	70	Semiconductores IE00BMC38736	Seminconductores IE00BMC38736	t	fixed	1	2026-04-24 18:31:29.578071+00	2026-05-04 06:59:25.789064+00
273	expense	5.60	2026-05-06 00:00:00+00	62	Refrescos Milla	Refrescos Milla	t	variable	1	2026-05-06 12:51:01.866062+00	2026-05-06 12:51:01.866062+00
274	expense	4.80	2026-05-06 00:00:00+00	105	Parking	Parking	t	variable	1	2026-05-06 12:51:17.952637+00	2026-05-06 12:51:17.952637+00
292	expense	5.28	2026-05-11 00:00:00+00	103	Conectores multímetro	Conectores multímetro	t	variable	1	2026-05-11 10:41:50.685733+00	2026-05-13 18:38:05.069277+00
285	income	1.88	2026-05-09 00:00:00+00	45	Mamá Comida	Mamá Comida	t	variable	1	2026-05-09 11:00:36.502511+00	2026-05-13 11:28:44.462366+00
295	expense	0.56	2026-05-13 00:00:00+00	102	Cables Cat 7	Cables Cat 7	t	variable	1	2026-05-13 18:37:53.292893+00	2026-05-13 18:38:00.271394+00
290	expense	28.30	2026-05-10 00:00:00+00	103	Piezas Server y estañar	Piezas Server y estañar	t	variable	1	2026-05-10 13:35:52.853734+00	2026-05-13 18:38:24.330392+00
296	expense	0.55	2026-05-11 00:00:00+00	105	ORA	ORA	t	variable	1	2026-05-14 06:49:00.933971+00	2026-05-14 06:49:00.933971+00
297	expense	100.00	2026-05-14 00:00:00+00	110	Reserva Gato	Reserva Gato	t	variable	1	2026-05-14 12:57:06.766673+00	2026-05-14 12:57:06.766673+00
298	expense	6.00	2026-05-14 00:00:00+00	62	Desayuno Milla	Desayuno Milla	t	variable	1	2026-05-14 12:57:19.159797+00	2026-05-14 12:57:19.159797+00
293	expense	28.53	2026-05-12 00:00:00+00	102	Fuente Alimentación 	Fuente Alimentación 	t	variable	1	2026-05-12 20:28:00.678625+00	2026-05-15 14:21:49.501648+00
1	expense	30.00	2026-05-16 00:00:00+00	105	Diésel	Diésel	t	variable	1	2026-05-16 16:02:33.439812+00	2026-05-16 16:02:33.439812+00
2	income	50.00	2026-05-17 00:00:00+00	45	Papá	Papá	t	variable	1	2026-05-16 16:31:54.634702+00	2026-05-16 16:31:54.634702+00
3	expense	3.50	2026-05-16 00:00:00+00	59	Cafés	Cafés	t	variable	1	2026-05-16 23:25:17.92883+00	2026-05-16 23:25:17.92883+00
4	expense	15.00	2026-05-16 00:00:00+00	59	Hamburguesitas	Hamburguesitas	t	variable	1	2026-05-16 23:26:14.293931+00	2026-05-16 23:26:14.293931+00
6	expense	0.70	2026-05-17 00:00:00+00	58	Agua vending	Agua vending	t	variable	1	2026-05-17 07:23:50.602159+00	2026-05-17 07:23:50.602159+00
7	expense	11.75	2026-05-17 00:00:00+00	103	Conectores PS4 AliExpress 	Conectores PS4 AliExpress 	t	variable	1	2026-05-17 08:34:11.457758+00	2026-05-18 06:56:02.314561+00
8	expense	15.42	2026-05-18 00:00:00+00	104	Gasolina	Gasolina	t	variable	1	2026-05-18 17:11:51.940457+00	2026-05-18 17:11:51.940457+00
229	income	50.00	2026-04-26 00:00:00+00	45	Papá\n		t	fixed	1	2026-04-28 12:14:09.367487+00	2026-08-21 12:21:57.441094+00
12	expense	8.15	2026-05-21 00:00:00+00	103	Herramientas chino	Herramientas chino	t	variable	1	2026-05-21 08:34:07.613468+00	2026-05-21 08:34:07.613468+00
9	expense	0.80	2026-05-19 00:00:00+00	105	ORA	ORA	t	variable	1	2026-05-19 13:08:38.501505+00	2026-05-19 22:11:07.159149+00
10	expense	14.16	2026-05-19 00:00:00+00	110	Madera	Madera	t	variable	1	2026-05-19 22:12:08.507409+00	2026-05-19 22:12:08.507409+00
14	expense	5.70	2026-05-23 00:00:00+00	62	Desayuno en busca de michi	Desayuno en busca de michi	t	variable	1	2026-05-23 12:10:46.756889+00	2026-05-23 12:10:46.756889+00
15	expense	3.50	2026-05-23 00:00:00+00	62	Refresco 	Refresco 	t	variable	1	2026-05-23 19:07:22.90619+00	2026-05-23 19:07:22.90619+00
16	expense	15.60	2026-05-23 00:00:00+00	59	Cena burguer	Cena burguer	t	variable	1	2026-05-23 21:39:41.779525+00	2026-05-23 21:39:41.779525+00
17	income	50.00	2026-05-24 00:00:00+00	45	Papá 	Papá 	t	variable	1	2026-05-24 13:39:17.884738+00	2026-05-24 13:39:17.884738+00
18	expense	12.42	2026-05-24 00:00:00+00	111	Peluches	Peluches	t	variable	1	2026-05-24 17:28:04.679857+00	2026-06-21 20:24:13.570502+00
19	expense	3.40	2026-05-25 00:00:00+00	62	Desayuno playa		t	variable	1	2026-05-25 10:02:51.380974+00	2026-05-25 10:03:04.928729+00
22	expense	2.95	2026-05-27 00:00:00+00	110	Empapador	Empapador	t	variable	1	2026-05-27 09:44:56.212391+00	2026-05-27 09:44:56.212391+00
13	expense	3.39	2026-05-23 00:00:00+00	107	Spoty	Spoty	t	fixed	1	2026-05-23 06:55:48.480854+00	2026-05-30 07:15:00.886483+00
220	income	4876.80	2024-12-30 00:00:00+00	44	Balance Inicial	Balance Inicial	t	variable	1	2026-04-24 14:55:11.668692+00	2026-07-28 07:15:08.806217+00
5	invest	40.00	2026-05-17 00:00:00+00	72	IONQ	IONQ	t	variable	1	2026-05-17 07:18:23.000081+00	2026-08-01 09:08:54.478723+00
23	expense	2.00	2026-05-27 00:00:00+00	105	Lavado	Lavado	t	variable	1	2026-05-27 09:45:06.463505+00	2026-05-27 09:45:06.463505+00
20	expense	5.40	2026-05-26 00:00:00+00	62	Refrescos	Terraza	t	variable	1	2026-05-26 15:40:05.915671+00	2026-05-27 09:45:31.255466+00
24	expense	25.00	2026-05-27 00:00:00+00	105	Diesel	Diesel	t	variable	1	2026-05-27 11:28:50.735906+00	2026-05-27 11:28:50.735906+00
25	expense	70.65	2026-05-27 00:00:00+00	110	Comida, arenero y transportín	Comida, arenero y transportín	t	variable	1	2026-05-27 14:31:35.927913+00	2026-05-27 14:31:35.927913+00
28	expense	22.59	2026-05-28 00:00:00+00	110	Arena	Arena	t	variable	1	2026-05-28 19:13:23.690304+00	2026-05-28 19:13:23.690304+00
309	expense	6.30	2026-06-09 00:00:00+00	110	Arneses gato	Arneses gato	t	variable	1	2026-06-09 19:31:20.462402+00	2026-06-09 19:31:20.462402+00
31	expense	24.60	2026-05-30 00:00:00+00	59	Cena Final champions	Cena Final champions	t	variable	1	2026-05-30 20:43:59.723775+00	2026-05-30 20:43:59.723775+00
33	income	50.00	2026-05-31 00:00:00+00	45	Papá	Papá	t	variable	1	2026-06-01 10:36:04.719207+00	2026-06-01 10:36:04.719207+00
32	expense	8.40	2026-05-31 00:00:00+00	62	Refrescos solecito	Refrescos solecito	t	variable	1	2026-05-31 18:50:22.7957+00	2026-06-01 10:36:16.032469+00
34	expense	12.00	2026-06-02 00:00:00+00	101	Corte Pelo	Corte Pelo	t	variable	1	2026-06-02 09:28:45.66327+00	2026-06-02 09:28:45.66327+00
35	expense	2.75	2026-06-02 00:00:00+00	56	Pan	Pan	t	variable	1	2026-06-02 09:28:55.571863+00	2026-06-02 09:31:08.097441+00
36	income	10.29	2026-06-02 00:00:00+00	47	2% TAE	2% TAE	t	variable	1	2026-06-02 10:24:37.314135+00	2026-06-02 10:24:37.314135+00
37	invest	50.00	2026-06-02 00:00:00+00	71	Fidelity S&P 500	Fidelity S&P 500	t	variable	1	2026-06-02 10:25:09.830181+00	2026-06-02 10:25:09.830181+00
38	invest	30.00	2026-06-02 00:00:00+00	71	Fidelity Emerging Markets	Fidelity Emerging Markets	t	variable	1	2026-06-02 10:25:35.338634+00	2026-06-02 10:25:35.338634+00
40	expense	12.82	2026-06-02 00:00:00+00	104	Gasolina	Gasolina	t	variable	1	2026-06-02 18:19:13.914965+00	2026-06-02 18:19:13.914965+00
42	expense	3.40	2026-06-03 00:00:00+00	62	Cafes	Cafes	t	variable	1	2026-06-03 19:46:06.241845+00	2026-06-03 19:46:06.241845+00
43	income	570.00	2026-06-02 00:00:00+00	44	Subsidio 	Subsidio 	t	variable	1	2026-06-03 19:46:28.61092+00	2026-06-03 19:46:28.61092+00
39	invest	40.00	2026-06-02 00:00:00+00	70	Vaneck Semiconductors	Vaneck Semiconductors	t	variable	1	2026-06-02 10:25:52.03152+00	2026-06-03 19:46:49.189349+00
46	expense	3.10	2026-06-04 00:00:00+00	62	Cafe	Cafe	t	variable	1	2026-06-04 18:19:54.684645+00	2026-06-04 18:19:54.684645+00
50	expense	30.26	2026-06-06 00:00:00+00	106	Camiseta fútbol 	Camiseta fútbol 	t	variable	1	2026-06-06 17:27:37.037917+00	2026-06-06 17:27:37.037917+00
48	expense	10.30	2026-06-04 00:00:00+00	103	Maceta Chino	Maceta Chino	t	variable	1	2026-06-06 12:23:41.823592+00	2026-06-06 17:30:24.218443+00
47	income	50.00	2026-06-07 00:00:00+00	45	Papá	Papá	t	variable	1	2026-06-06 12:21:18.105662+00	2026-06-06 17:30:31.136023+00
300	expense	6.00	2026-06-08 00:00:00+00	67	Pinchazos y palancas coche	Pinchazos y palancas coche	t	variable	1	2026-06-08 08:51:06.678222+00	2026-06-08 08:51:06.678222+00
301	expense	1.95	2026-06-08 00:00:00+00	110	Bebedero	Bebedero	t	variable	1	2026-06-08 08:51:18.837755+00	2026-06-08 08:51:18.837755+00
305	expense	10.00	2026-06-08 00:00:00+00	102	Tarjetas Gaby 	Tarjetas Gaby 	t	variable	1	2026-06-09 19:05:57.692778+00	2026-06-09 19:05:57.692778+00
306	expense	30.00	2026-06-09 00:00:00+00	105	Diésel 	Diésel 	t	variable	1	2026-06-09 19:06:10.512832+00	2026-06-09 19:06:10.512832+00
310	expense	7.02	2026-06-09 00:00:00+00	103	Chinadas	Lubricador bici, soporte cámara mochila y tapa cenicero	t	variable	1	2026-06-09 19:33:00.372751+00	2026-06-09 19:33:13.816695+00
311	expense	5.09	2026-06-09 00:00:00+00	103	Soporte Gaby móvil	Soporte Gaby móvil	t	variable	1	2026-06-09 19:33:31.384664+00	2026-06-09 19:33:31.384664+00
312	expense	26.98	2026-06-11 00:00:00+00	107	DAZN Motor + Mundial	DAZN Motor + Mundial	t	variable	1	2026-06-11 07:27:23.642663+00	2026-06-12 08:10:24.999866+00
315	expense	9.00	2026-06-09 00:00:00+00	67	Soporte botella y cable bici 	Soporte botella y cable bici 	t	variable	1	2026-06-12 08:23:31.902276+00	2026-06-12 08:23:31.902276+00
316	expense	4.90	2026-06-12 00:00:00+00	106	Arreglo pantalón 	Arreglo pantalón 	t	variable	1	2026-06-12 08:25:16.036009+00	2026-06-12 08:25:16.036009+00
314	expense	6.04	2026-06-09 00:00:00+00	106	Pantalon bici 	Pantalon bici 	t	variable	1	2026-06-12 08:23:14.904667+00	2026-06-12 08:40:46.730333+00
317	expense	8.80	2026-06-13 00:00:00+00	58	Desayuno La Bañeza 	Desayuno La Bañeza 	t	variable	1	2026-06-13 08:12:36.54241+00	2026-06-13 08:12:36.54241+00
318	expense	78.75	2026-06-13 00:00:00+00	105	Gasolina Gaby	Gasolina	t	variable	1	2026-06-13 13:10:15.037623+00	2026-06-13 15:18:50.021484+00
320	expense	3.00	2026-06-13 00:00:00+00	56	Agua 	Agua 	t	variable	1	2026-06-14 10:25:21.128157+00	2026-06-14 10:25:21.128157+00
319	expense	450.00	2026-06-13 00:00:00+00	110	Mi hijo Romeo	Mi hijo Romeo	t	variable	1	2026-06-13 13:10:40.003123+00	2026-06-14 10:25:28.977396+00
321	income	50.00	2026-06-14 00:00:00+00	45	Papá	Papá	t	variable	1	2026-06-14 12:13:21.548581+00	2026-06-14 12:13:21.548581+00
322	expense	1.58	2026-06-16 00:00:00+00	102	Steam Meccha Chameleon	Steam Meccha Chameleon	t	variable	1	2026-06-16 16:01:59.06356+00	2026-06-16 16:01:59.06356+00
324	expense	2.30	2026-06-19 00:00:00+00	56	Pan 	Pan 	t	variable	1	2026-06-19 09:51:33.997515+00	2026-06-19 09:51:33.997515+00
325	expense	6.05	2026-06-19 00:00:00+00	103	Reposa pies 	Reposa pies 	t	variable	1	2026-06-19 09:51:51.341833+00	2026-06-19 09:51:51.341833+00
326	expense	18.25	2026-06-19 00:00:00+00	111	Cama 	Cama 	t	variable	1	2026-06-19 18:17:31.363361+00	2026-06-19 18:17:31.363361+00
327	expense	3.90	2026-06-19 00:00:00+00	62	Refrescos\n	Refrescos\n	t	variable	1	2026-06-19 20:01:46.804729+00	2026-06-19 20:01:46.804729+00
328	expense	3.70	2026-06-21 00:00:00+00	62	Terraceo al sol 	Terraceo al sol 	t	variable	1	2026-06-21 18:05:54.483331+00	2026-06-21 18:05:54.483331+00
329	income	50.00	2026-06-21 00:00:00+00	45	Papa	Papa	t	variable	1	2026-06-21 20:24:06.587319+00	2026-06-21 20:24:06.587319+00
330	expense	5.60	2026-06-21 00:00:00+00	62	Cafe Bonsai	Cafe Bonsai	t	variable	1	2026-06-21 20:24:35.801178+00	2026-06-21 20:24:35.801178+00
331	expense	1.30	2026-06-22 00:00:00+00	56	Pan	Pan	t	variable	1	2026-06-22 09:23:47.953149+00	2026-06-22 09:23:47.953149+00
349	expense	14.62	2026-06-30 00:00:00+00	104	Gasolina	Gasolina	t	variable	1	2026-06-30 09:01:35.69089+00	2026-06-30 09:01:35.69089+00
350	income	1.10	2026-06-30 00:00:00+00	45	Propinas	Propinas	t	variable	1	2026-06-30 10:39:20.145484+00	2026-06-30 10:39:20.145484+00
323	expense	19.00	2026-06-18 00:00:00+00	110	Veterinario Romeo Ácaros	Estrellas 	t	variable	1	2026-06-18 12:17:27.269332+00	2026-06-23 11:50:21.515959+00
336	expense	19.90	2026-06-24 00:00:00+00	110	Evicare Romeo	Evicare Romeo	t	variable	1	2026-06-24 09:03:12.166815+00	2026-06-24 09:03:12.166815+00
337	expense	1.50	2026-06-24 00:00:00+00	105	Lavado	Lavado	t	variable	1	2026-06-24 09:03:39.712672+00	2026-06-24 09:03:39.712672+00
338	income	60.00	2026-06-25 00:00:00+00	45	Abuelos 	Abuelos 	t	variable	1	2026-06-25 18:40:31.023899+00	2026-06-25 18:40:31.023899+00
339	expense	25.91	2026-06-26 00:00:00+00	107	Pago mátricula Máster	Pago mátricula Máster	t	variable	1	2026-06-26 07:24:16.496392+00	2026-06-26 07:24:16.496392+00
340	expense	7.50	2026-06-26 00:00:00+00	62	Refrescos	Refrescos	t	variable	1	2026-06-26 17:52:35.285561+00	2026-06-26 17:52:35.285561+00
341	expense	15.23	2026-06-26 00:00:00+00	104	Gasolina 	Gasolina 	t	variable	1	2026-06-26 17:53:02.29731+00	2026-06-26 17:53:02.29731+00
342	expense	8.00	2026-06-27 00:00:00+00	59	Comida Landeira	Comida Landeira	t	variable	1	2026-06-27 17:10:01.32608+00	2026-06-27 17:10:01.32608+00
343	income	0.50	2026-06-27 00:00:00+00	45	Propinas 	Propinas 	t	variable	1	2026-06-27 17:10:24.888071+00	2026-06-27 17:10:24.888071+00
344	income	2.60	2026-06-28 00:00:00+00	45	Propinas	Propinas	t	variable	1	2026-06-28 13:07:37.91393+00	2026-06-28 13:07:37.91393+00
345	income	100.00	2026-06-28 00:00:00+00	45	Papá	Papá	t	variable	1	2026-06-28 16:10:03.125292+00	2026-06-28 16:10:03.125292+00
346	income	271.09	2026-06-29 00:00:00+00	44	Nómina Audasa 	Nómina Audasa 	t	variable	1	2026-06-29 10:19:55.842606+00	2026-06-29 10:19:55.842606+00
347	expense	6.46	2026-06-29 00:00:00+00	56	Chuches Gaby 	Chuches Gaby 	t	variable	1	2026-06-29 10:23:33.314921+00	2026-06-29 10:23:33.314921+00
351	income	10.11	2026-07-01 00:00:00+00	47	2,25% TAE 	2,25% TAE 	t	variable	1	2026-07-01 15:31:44.864116+00	2026-07-01 15:31:44.864116+00
352	expense	9.95	2026-07-01 00:00:00+00	111	Cama	Cama	t	variable	1	2026-07-01 17:18:55.400569+00	2026-07-01 17:18:55.400569+00
353	expense	9.34	2026-07-01 00:00:00+00	106	Soportes calzado 	Soportes calzado 	t	variable	1	2026-07-01 17:19:32.570263+00	2026-07-01 17:19:32.570263+00
354	invest	70.00	2026-07-02 00:00:00+00	71	Fidelity S&P 500	Fidelity S&P 500	t	variable	1	2026-07-02 13:08:25.636586+00	2026-07-02 13:08:25.636586+00
355	invest	30.00	2026-07-02 00:00:00+00	70	VanEck Semiconductors	VanEck Semiconductors	t	variable	1	2026-07-02 13:08:55.441838+00	2026-07-02 13:08:55.441838+00
362	invest	50.00	2026-07-02 00:00:00+00	70	Nuclear Technology	Nuclear Technology	t	variable	1	2026-07-04 07:59:38.309315+00	2026-07-04 07:59:38.309315+00
360	income	228.00	2026-07-02 00:00:00+00	44	Subsidio 	Subsidio 	t	variable	1	2026-07-04 07:56:33.886002+00	2026-07-04 07:56:39.768873+00
348	expense	3.39	2026-06-22 00:00:00+00	107	Spoty 	Spoty 	t	variable	1	2026-06-29 19:50:23.792786+00	2026-07-05 19:36:45.647254+00
357	income	1.00	2026-07-02 00:00:00+00	45	Propina	Propina	t	variable	1	2026-07-02 20:54:49.828588+00	2026-08-21 12:21:20.734814+00
359	expense	6.30	2026-07-03 00:00:00+00	62	Merienda Dpingas	Merienda Dpingas	t	variable	1	2026-07-04 07:56:15.378787+00	2026-07-04 07:56:21.845492+00
358	expense	32.00	2026-07-04 00:00:00+00	22	Eurostars Santa Marta	Eurostars	t	variable	1	2026-07-04 07:53:47.116673+00	2026-07-04 07:56:52.14525+00
361	income	50.00	2026-07-05 00:00:00+00	45	Papá	Papá	t	variable	1	2026-07-04 07:58:52.679022+00	2026-07-04 07:58:52.679022+00
363	income	2.00	2026-07-05 00:00:00+00	45	Propinas	Propinas	t	variable	1	2026-07-05 13:42:29.383571+00	2026-07-05 13:42:35.207644+00
364	expense	35.00	2026-07-05 00:00:00+00	105	Diésel	Diésel	t	variable	1	2026-07-05 13:42:49.032891+00	2026-07-05 13:42:49.032891+00
365	expense	12.90	2026-07-06 00:00:00+00	59	Desayuno	Desayuno	t	variable	1	2026-07-06 10:20:34.5584+00	2026-07-06 10:20:34.5584+00
366	expense	4.01	2026-07-06 00:00:00+00	107	Licencia pesca 	Licencia pesca 	t	variable	1	2026-07-06 10:20:54.18013+00	2026-07-06 10:20:54.18013+00
367	expense	0.60	2026-07-06 00:00:00+00	105	ORA	ORA	t	variable	1	2026-07-06 13:09:12.884152+00	2026-07-06 13:09:12.884152+00
368	expense	3.40	2026-07-07 00:00:00+00	56	Pan 	Pan 	t	variable	1	2026-07-07 08:34:03.294813+00	2026-07-07 08:34:03.294813+00
369	expense	5.50	2026-07-07 00:00:00+00	62	Desayuno 	Desayuno 	t	variable	1	2026-07-07 09:31:44.08181+00	2026-07-07 09:31:44.08181+00
370	expense	5.50	2026-07-07 00:00:00+00	62	Desayuno 	Desayuno 	t	variable	1	2026-07-07 09:31:48.281455+00	2026-07-07 09:31:48.281455+00
371	expense	11.19	2026-07-07 00:00:00+00	109	Rascador	Rascador	t	variable	1	2026-07-07 09:31:59.016896+00	2026-07-07 09:31:59.016896+00
372	expense	36.06	2026-07-07 00:00:00+00	106	Camisa y bañador	Camisa y bañador	t	variable	1	2026-07-07 11:15:02.003565+00	2026-07-07 11:15:02.003565+00
373	expense	7.99	2026-07-07 00:00:00+00	107	Strava premium 	Strava premium 	t	variable	1	2026-07-07 11:15:14.668165+00	2026-07-07 11:15:14.668165+00
356	invest	50.00	2026-07-02 00:00:00+00	70	Nuclear Technology	Nuclear Technology	t	variable	1	2026-07-02 13:09:25.343668+00	2026-07-07 11:15:45.338129+00
374	expense	1.12	2026-07-10 00:00:00+00	101	Seguro  escolar	Seguro  escolar	t	variable	1	2026-07-10 12:19:32.321223+00	2026-07-10 12:19:32.321223+00
375	income	7.00	2026-07-09 00:00:00+00	45	Abuelos	Caña pizzeria	t	variable	1	2026-07-10 12:19:49.541997+00	2026-07-10 12:21:39.249961+00
376	expense	2.99	2026-07-10 00:00:00+00	107	iCloud	iCloud	t	variable	1	2026-07-10 12:22:29.871894+00	2026-07-10 12:22:29.871894+00
378	expense	19.00	2026-07-10 00:00:00+00	62	Cena España Bélgica 	Cena España Bélgica 	t	variable	1	2026-07-10 21:03:21.878957+00	2026-07-10 21:03:21.878957+00
379	expense	6.20	2026-07-10 00:00:00+00	62	Futbolines	Futbolines	t	variable	1	2026-07-10 22:42:40.463302+00	2026-07-11 09:02:02.844464+00
380	expense	5.00	2026-07-11 00:00:00+00	62	Parking Gozo Fest	Parking Gozo Fest	t	variable	1	2026-07-11 17:17:17.297244+00	2026-07-11 17:17:17.297244+00
381	expense	30.00	2026-07-11 00:00:00+00	105	Diésel 	Diésel 	t	variable	1	2026-07-11 22:44:38.373151+00	2026-07-11 22:44:38.373151+00
383	expense	7.55	2026-07-12 00:00:00+00	56	Pan	Pan	t	variable	1	2026-07-12 09:26:15.732705+00	2026-07-12 09:26:15.732705+00
382	expense	1.20	2026-07-11 00:00:00+00	56	Refresco	refresco	t	variable	1	2026-07-11 23:39:00.137518+00	2026-07-12 09:26:28.858914+00
384	expense	13.00	2026-07-12 00:00:00+00	62	Cena Gozo Fest	Cena Gozo Fest	t	variable	1	2026-07-12 09:26:45.534848+00	2026-07-12 09:26:45.534848+00
385	income	50.00	2026-07-12 00:00:00+00	45	Papa	Papa	t	variable	1	2026-07-12 10:30:04.881023+00	2026-07-12 10:30:04.881023+00
386	expense	15.24	2026-07-13 00:00:00+00	104	Gasolina 	Gasolina 	t	variable	1	2026-07-13 15:16:18.116493+00	2026-07-13 15:16:18.116493+00
387	expense	3.00	2026-07-13 00:00:00+00	62	Cafés con hielo	Cafés con hielo	t	variable	1	2026-07-14 09:35:12.738162+00	2026-07-14 09:35:12.738162+00
389	expense	6.99	2026-07-13 00:00:00+00	56	Dazn 	Dazn 	t	variable	1	2026-07-16 19:25:32.110089+00	2026-07-16 19:25:38.903505+00
390	expense	5.00	2026-07-13 00:00:00+00	62	Refrescos 	Refrescos 	t	variable	1	2026-07-16 19:26:15.703729+00	2026-07-16 19:26:15.703729+00
391	income	2.40	2026-07-17 00:00:00+00	45	Propinas	Propinas	t	variable	1	2026-07-17 16:02:32.000045+00	2026-07-17 16:02:32.000045+00
392	income	50.00	2026-07-19 00:00:00+00	45	Papá	Papá	t	variable	1	2026-07-18 07:54:00.238234+00	2026-07-18 07:54:00.238234+00
393	expense	17.65	2026-07-18 00:00:00+00	104	Gasolina 	Gasolina 	t	variable	1	2026-07-18 07:54:19.170037+00	2026-07-18 10:56:33.971146+00
395	expense	8.60	2026-07-19 00:00:00+00	58	Dieta Trabajo 	Dieta Trabajo 	t	variable	1	2026-07-19 14:39:44.363294+00	2026-07-19 14:39:44.363294+00
396	expense	20.80	2026-07-19 00:00:00+00	62	Cena Final Mundial	Cena Final Mundial	t	variable	1	2026-07-19 22:14:03.474745+00	2026-07-19 22:14:03.474745+00
398	income	2.00	2026-07-21 00:00:00+00	45	Propinas	Propinas	t	variable	1	2026-07-21 12:12:54.20083+00	2026-07-21 12:12:54.20083+00
400	expense	12.30	2026-07-22 00:00:00+00	107	Dominio www.romeothebritish.com	Dominio www.romeothebritish.com	t	variable	1	2026-07-22 16:06:13.586175+00	2026-07-22 16:06:13.586175+00
394	expense	16.85	2026-07-18 00:00:00+00	103	Banderitas y camisa España	Banderitas y camisa España	t	variable	1	2026-07-18 14:29:19.28524+00	2026-07-23 18:59:32.447512+00
401	expense	8.39	2026-07-22 00:00:00+00	107	Spotify	Spotify	t	variable	1	2026-07-22 18:41:20.829824+00	2026-07-23 19:00:42.608252+00
402	expense	6.00	2026-07-24 00:00:00+00	109	Churus\n	Desayuno	t	variable	1	2026-07-24 11:00:44.634578+00	2026-07-24 15:28:33.767147+00
404	income	50.00	2026-07-26 00:00:00+00	45	Papá	Papá	t	variable	1	2026-07-26 15:17:45.4311+00	2026-07-26 15:17:45.4311+00
405	income	2.50	2026-07-26 00:00:00+00	45	Propinas	Propinas	t	variable	1	2026-07-26 17:13:34.314241+00	2026-07-26 17:13:34.314241+00
407	expense	3.00	2026-07-27 00:00:00+00	62	Cafés	Cafes 	t	variable	1	2026-07-27 17:19:58.566669+00	2026-07-27 17:20:07.675731+00
408	expense	5.30	2026-07-27 00:00:00+00	62	Refrescos La planta	Refrescos La planta	t	variable	1	2026-07-27 18:16:36.485311+00	2026-07-27 18:16:36.485311+00
409	expense	5.30	2026-07-27 00:00:00+00	62	Refrescos La planta	Refrescos La planta	t	variable	1	2026-07-27 18:16:36.930188+00	2026-07-27 18:16:36.930188+00
411	income	993.03	2026-07-28 00:00:00+00	44	Nómina Audasa Julio	Nómina Audasa Julio	t	variable	1	2026-07-28 07:15:34.414255+00	2026-07-29 09:48:19.900812+00
415	expense	5.60	2026-07-29 00:00:00+00	56	Helados	Helados	t	variable	1	2026-07-29 15:33:00.875007+00	2026-07-29 15:33:00.875007+00
414	income	3.00	2026-07-28 00:00:00+00	45	Propinas	Propinas	t	variable	1	2026-07-28 11:00:24.743279+00	2026-07-30 17:02:18.097315+00
431	expense	8.00	2026-08-04 00:00:00+00	59	Kebabs 	Kebabs 	t	variable	1	2026-08-04 20:10:05.308499+00	2026-08-04 21:15:26.335534+00
455	expense	18.34	2026-08-13 00:00:00+00	104	Gasolina	Gasolina	t	variable	1	2026-08-13 14:37:28.019204+00	2026-08-13 14:37:28.019204+00
421	expense	25.00	2026-07-28 00:00:00+00	105	Diesel	Diesel	t	variable	1	2026-07-31 19:22:56.790356+00	2026-07-31 19:23:04.320503+00
422	expense	18.23	2026-07-27 00:00:00+00	104	Gasolina	Gasolina	t	variable	1	2026-07-31 19:23:16.595857+00	2026-07-31 19:23:16.595857+00
423	income	11.75	2026-08-01 00:00:00+00	47	Interés 2% TAE	Interés 2% TAE	t	variable	1	2026-08-01 09:03:11.99118+00	2026-08-01 09:03:11.99118+00
419	expense	13.00	2026-07-31 00:00:00+00	58	Comida trabajo 	Comida trabajo 	t	variable	1	2026-07-31 19:03:38.892098+00	2026-08-01 19:42:26.616406+00
425	invest	30.00	2026-08-03 00:00:00+00	71	Fidelity MSCI Emerging Markets	Fidelity MSCI Emerging Markets	t	variable	1	2026-08-01 09:03:55.702791+00	2026-08-05 16:45:19.76359+00
437	expense	3.90	2026-08-06 00:00:00+00	62	Cafes 	Cafes 	t	variable	1	2026-08-06 19:44:30.489705+00	2026-08-06 19:44:30.489705+00
427	income	50.00	2026-08-02 00:00:00+00	45	Papá	Papá	t	variable	1	2026-08-02 10:03:24.647648+00	2026-08-02 10:03:24.647648+00
428	expense	1.50	2026-08-02 00:00:00+00	104	Lavado 	Lavado 	t	variable	1	2026-08-02 20:40:06.180891+00	2026-08-02 20:40:06.180891+00
429	expense	8.00	2026-08-02 00:00:00+00	62	Tostadas	Tostadas	t	variable	1	2026-08-02 20:40:33.568975+00	2026-08-02 20:40:33.568975+00
430	expense	9.00	2026-08-03 00:00:00+00	58	Cena	Cena	t	variable	1	2026-08-03 20:49:55.392853+00	2026-08-03 20:49:55.392853+00
438	expense	2.99	2026-08-06 00:00:00+00	107	iCloud	iCloud	t	variable	1	2026-08-07 06:22:15.688141+00	2026-08-07 06:22:15.688141+00
439	expense	15.27	2026-08-07 00:00:00+00	104	Gasolina 	Gasolina 	t	variable	1	2026-08-07 07:22:05.577319+00	2026-08-07 07:22:05.577319+00
440	expense	5.60	2026-08-07 00:00:00+00	62	Cañas	Cañas	t	variable	1	2026-08-07 18:09:11.97731+00	2026-08-07 18:09:19.555248+00
444	income	50.00	2026-08-09 00:00:00+00	45	Papá	Papá	t	variable	1	2026-08-09 10:19:08.712531+00	2026-08-09 10:19:08.712531+00
445	income	1.00	2026-08-07 00:00:00+00	45	Propina	Propina	t	variable	1	2026-08-09 10:19:22.002057+00	2026-08-09 10:19:22.002057+00
446	income	2.21	2026-08-10 00:00:00+00	25	Romeo 	Romeo 	t	variable	1	2026-08-10 06:27:32.546015+00	2026-08-10 06:27:32.546015+00
447	expense	14.23	2026-08-10 00:00:00+00	104	Gasolina 	Gasolina 	t	variable	1	2026-08-10 09:37:13.601378+00	2026-08-10 09:37:13.601378+00
448	expense	1.50	2026-08-10 00:00:00+00	56	Cafe cambio bus 	Cade cambio bus 	t	variable	1	2026-08-10 11:12:04.521305+00	2026-08-10 11:12:18.644117+00
449	expense	1.30	2026-08-10 00:00:00+00	26	Urbano 	Urbano 	t	variable	1	2026-08-10 11:13:30.899279+00	2026-08-10 11:13:30.899279+00
450	expense	2.80	2026-08-10 00:00:00+00	62	Caña	Caña	t	variable	1	2026-08-10 11:47:39.134091+00	2026-08-10 11:47:39.134091+00
451	expense	14.00	2026-08-10 00:00:00+00	58	Burger	Burger	t	variable	1	2026-08-10 18:43:24.803355+00	2026-08-10 18:43:24.803355+00
441	expense	34.57	2026-08-07 00:00:00+00	103	Juguetes	Juguetes	t	variable	1	2026-08-07 19:46:18.671431+00	2026-08-10 18:58:19.623387+00
399	income	2.40	2026-07-22 00:00:00+00	45	Propinas	Propinas	t	variable	1	2026-07-22 15:30:42.96481+00	2026-08-21 12:21:07.519526+00
418	income	50.00	2026-07-30 00:00:00+00	45	Mamá	Mamá	t	variable	1	2026-07-30 17:02:41.487962+00	2026-08-21 12:21:15.147156+00
453	income	3.60	2026-08-12 00:00:00+00	45	Propinas 	Propinas 	t	variable	1	2026-08-12 13:41:51.739635+00	2026-08-15 13:42:43.377621+00
454	expense	23.00	2026-08-12 00:00:00+00	58	Cena	Cena	t	variable	1	2026-08-13 05:05:18.06299+00	2026-08-18 13:57:38.054498+00
424	invest	120.00	2026-08-03 00:00:00+00	71	Fidelity S&P 500	Fidelity S&P 500	t	variable	1	2026-08-01 09:03:38.61145+00	2026-08-13 07:30:09.535713+00
459	expense	25.00	2026-08-15 00:00:00+00	105	Diesel	Diesel	t	variable	1	2026-08-15 17:33:20.025868+00	2026-08-15 17:33:20.025868+00
460	expense	3.00	2026-08-15 00:00:00+00	62	Caña	Caña	t	variable	1	2026-08-15 20:35:28.578125+00	2026-08-15 20:35:28.578125+00
462	income	50.00	2026-08-16 00:00:00+00	45	Papá	Papá	t	variable	1	2026-08-16 13:34:03.796026+00	2026-08-16 13:34:03.796026+00
461	expense	28.00	2026-08-15 00:00:00+00	59	Cena hot pot	Cena hot pot	t	variable	1	2026-08-15 20:35:44.584307+00	2026-08-15 20:35:44.584307+00
464	expense	3.00	2026-08-16 00:00:00+00	62	Caña	Caña	t	variable	1	2026-08-16 14:50:36.708036+00	2026-08-16 14:50:36.708036+00
465	income	1.00	2026-08-16 00:00:00+00	45	Propinas	Propinas	t	variable	1	2026-08-16 21:06:06.705337+00	2026-08-16 21:06:06.705337+00
463	expense	9.00	2026-08-07 00:00:00+00	59	Comida 	Comida 	t	variable	1	2026-08-16 13:50:25.143874+00	2026-08-18 13:57:58.115476+00
467	expense	13.99	2026-08-12 00:00:00+00	107	Dazn	Dazn	t	variable	1	2026-08-18 13:58:27.310312+00	2026-08-18 13:58:27.310312+00
468	income	50.00	2026-08-18 00:00:00+00	45	Abuelos	Abuelos	t	variable	1	2026-08-18 16:18:28.028305+00	2026-08-18 16:18:28.028305+00
469	expense	19.06	2026-08-18 00:00:00+00	104	Gasolina	Gasolina	t	variable	1	2026-08-18 17:30:33.276363+00	2026-08-18 17:30:33.276363+00
472	income	1.00	2026-08-20 00:00:00+00	45	Propinas 	Propinas 	t	variable	1	2026-08-20 12:23:00.615505+00	2026-08-20 12:23:00.615505+00
69	income	50.00	2026-04-12 00:00:00+00	45	Papá	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-08-21 12:20:46.165661+00
124	income	450.00	2026-03-10 00:00:00+00	44	Subsidio	\N	t	fixed	1	2026-04-24 08:50:11.285042+00	2026-08-21 12:22:04.341081+00
166	income	526.00	2026-02-10 00:00:00+00	44	Subsidio Desempleo Enero	\N	t	variable	1	2026-04-24 08:50:11.285042+00	2026-08-21 12:22:13.431899+00
474	expense	13.99	2026-08-21 00:00:00+00	107	Spotify	Spotify	f	fixed	1	2026-08-21 17:33:57.435+00	2026-08-21 17:33:57.435+00
475	income	50.00	2026-08-23 00:00:00+00	45	Papa	Papa	t	variable	1	2026-08-21 20:02:55.432208+00	2026-08-21 20:02:55.432208+00
476	expense	4.60	2026-08-20 00:00:00+00	62	Cafés	Cafes	t	variable	1	2026-08-23 07:59:59.581702+00	2026-08-23 08:00:49.595581+00
477	expense	40.00	2026-08-23 00:00:00+00	105	Diesel	Diesel	t	variable	1	2026-08-23 13:13:46.432576+00	2026-08-23 13:13:46.432576+00
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (id, email, hashed_password, created_at) FROM stdin;
1	user@kaira.local	dummy_password	2026-05-16 12:04:34.678454+00
\.


--
-- Name: backup_settings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.backup_settings_id_seq', 1, true);


--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.categories_id_seq', 26, true);


--
-- Name: monthly_budgets_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.monthly_budgets_id_seq', 1, false);


--
-- Name: transactions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.transactions_id_seq', 477, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_id_seq', 1, false);


--
-- Name: backup_settings backup_settings_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.backup_settings
    ADD CONSTRAINT backup_settings_pkey PRIMARY KEY (id);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- Name: monthly_budgets monthly_budgets_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.monthly_budgets
    ADD CONSTRAINT monthly_budgets_pkey PRIMARY KEY (id);


--
-- Name: transactions transactions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_categories_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_categories_id ON public.categories USING btree (id);


--
-- Name: ix_monthly_budgets_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_monthly_budgets_user_id ON public.monthly_budgets USING btree (user_id);


--
-- Name: ix_transactions_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_transactions_id ON public.transactions USING btree (id);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: categories categories_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.categories(id);


--
-- Name: categories categories_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: transactions transactions_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id);


--
-- Name: transactions transactions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

\unrestrict nCEgyN68D9RYFCfHRhhlFpM0JR85zyr7kXeVqrRVWib5ogC83q1l4o71Q6EXNgV

