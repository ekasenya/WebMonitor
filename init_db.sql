CREATE ROLE web_monitoring NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT LOGIN PASSWORD '12345';


CREATE SEQUENCE public.websites_website_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;


CREATE TABLE public.websites (
	website_id serial NOT NULL,
	url varchar(2048) NOT NULL,
	CONSTRAINT websites_pk PRIMARY KEY (website_id)
);
CREATE INDEX websites_url_idx ON public.websites (url);


CREATE SEQUENCE public.websites_check_results_check_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START 1
	CACHE 1
	NO CYCLE;

CREATE TABLE public.websites_check_results (
	check_id bigserial NOT NULL,
	website_id integer NOT NULL,
	available bool NULL,
	request_ts integer NOT NULL,
	response_time real NULL,
	http_code smallint NULL,
	pattern_matched bool NULL,
	CONSTRAINT websites_check_results_pk PRIMARY KEY (check_id)
);
CREATE INDEX websites_check_results_website_id_idx ON public.websites_check_results (website_id);
CREATE INDEX websites_check_results_request_ts_idx ON public.websites_check_results (request_ts);


GRANT SELECT ON TABLE public.websites TO web_monitoring;
GRANT INSERT ON TABLE public.websites TO web_monitoring;
GRANT UPDATE ON TABLE public.websites TO web_monitoring;
GRANT DELETE ON TABLE public.websites TO web_monitoring;
GRANT SELECT ON TABLE public.websites_check_results TO web_monitoring;
GRANT UPDATE ON TABLE public.websites_check_results TO web_monitoring;
GRANT INSERT ON TABLE public.websites_check_results TO web_monitoring;
GRANT DELETE ON TABLE public.websites_check_results TO web_monitoring;

GRANT USAGE, SELECT ON SEQUENCE websites_website_id_seq TO web_monitoring;
GRANT USAGE, SELECT ON SEQUENCE websites_check_results_check_id_seq TO web_monitoring;
