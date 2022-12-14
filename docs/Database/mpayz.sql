-- This script was generated by a beta version of the ERD tool in pgAdmin 4.
-- Please log an issue at https://redmine.postgresql.org/projects/pgadmin4/issues/new if you find any bugs, including reproduction steps.
BEGIN;


CREATE TABLE IF NOT EXISTS public."MPayz_admin_data"
(
    id bigint NOT NULL DEFAULT nextval('"MaPayz_admin_data_id_seq"'::regclass),
    key character varying(10) COLLATE pg_catalog."default",
    "values" text COLLATE pg_catalog."default",
    CONSTRAINT "MaPayz_admin_data_pkey" PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
);

CREATE TABLE IF NOT EXISTS public."MPayz_contacts"
(
    id bigint NOT NULL DEFAULT nextval('"MaPayz_contact_id_seq"'::regclass),
    profile_pic character varying(100) COLLATE pg_catalog."default",
    name character varying(60) COLLATE pg_catalog."default" NOT NULL,
    contact_address character varying(60) COLLATE pg_catalog."default" NOT NULL,
    user_id bigint NOT NULL,
    CONSTRAINT "MaPayz_contact_pkey" PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
);

CREATE TABLE IF NOT EXISTS public."MPayz_email_verify"
(
    id bigint NOT NULL DEFAULT nextval('"MaPayz_email_verify_id_seq"'::regclass),
    email_verify_token text COLLATE pg_catalog."default",
    verify boolean NOT NULL,
    "User_id" bigint NOT NULL,
    CONSTRAINT "MaPayz_email_verify_pkey" PRIMARY KEY (id),
    CONSTRAINT "MaPayz_email_verify_User_id_key" UNIQUE ("User_id")
)
WITH (
    OIDS = FALSE
);

CREATE TABLE IF NOT EXISTS public."MPayz_faqs"
(
    id bigint NOT NULL DEFAULT nextval('"MaPayz_faq_id_seq"'::regclass),
    "Questions" text COLLATE pg_catalog."default" NOT NULL,
    "Answer" text COLLATE pg_catalog."default" NOT NULL,
    "is_Active" boolean NOT NULL,
    CONSTRAINT "MaPayz_faq_pkey" PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
);

CREATE TABLE IF NOT EXISTS public."MPayz_healthrecords"
(
    id bigint NOT NULL DEFAULT nextval('"MaPayz_nft_data_id_seq"'::regclass),
    "NFT_id" text COLLATE pg_catalog."default",
    "NFT_trxn_hash" text COLLATE pg_catalog."default",
    "NFT_image" character varying(100) COLLATE pg_catalog."default",
    "User_id" bigint NOT NULL,
    emergency boolean NOT NULL,
    personal boolean NOT NULL,
    "PIN" character varying(4) COLLATE pg_catalog."default",
    CONSTRAINT "MaPayz_nft_data_pkey" PRIMARY KEY (id),
    CONSTRAINT "MaPayz_nft_data_User_id_key" UNIQUE ("User_id")
)
WITH (
    OIDS = FALSE
);

CREATE TABLE IF NOT EXISTS public."MPayz_messages"
(
    id bigint NOT NULL DEFAULT nextval('"MaPayz_direct_message_id_seq"'::regclass),
    body text COLLATE pg_catalog."default",
    date timestamp with time zone NOT NULL,
    is_read boolean NOT NULL,
    "User_id" bigint NOT NULL,
    recipient_id bigint NOT NULL,
    sender_id bigint NOT NULL,
    CONSTRAINT "MaPayz_direct_message_pkey" PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
);

CREATE TABLE IF NOT EXISTS public."MPayz_support"
(
    id bigint NOT NULL DEFAULT nextval('"MaPayz_support_dm_id_seq"'::regclass),
    body text COLLATE pg_catalog."default",
    date timestamp with time zone NOT NULL,
    is_read boolean NOT NULL,
    "User_id" bigint NOT NULL,
    recipient_id bigint NOT NULL,
    sender_id bigint NOT NULL,
    CONSTRAINT "MaPayz_support_dm_pkey" PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
);

CREATE TABLE IF NOT EXISTS public."MPayz_tokenrequests"
(
    token text COLLATE pg_catalog."default",
    date timestamp with time zone NOT NULL,
    is_rejected boolean NOT NULL,
    is_accepted boolean NOT NULL,
    unique_id uuid NOT NULL,
    "User_id" bigint NOT NULL,
    recipient_id bigint NOT NULL,
    sender_id bigint NOT NULL,
    CONSTRAINT "MaPayz_request_token_pkey" PRIMARY KEY (unique_id)
)
WITH (
    OIDS = FALSE
);

CREATE TABLE IF NOT EXISTS public."MPayz_user"
(
    id bigint NOT NULL DEFAULT nextval('"MaPayz_user_id_seq"'::regclass),
    password character varying(128) COLLATE pg_catalog."default" NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) COLLATE pg_catalog."default" NOT NULL,
    first_name character varying(150) COLLATE pg_catalog."default" NOT NULL,
    last_name character varying(150) COLLATE pg_catalog."default" NOT NULL,
    email character varying(254) COLLATE pg_catalog."default" NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    passphrase text COLLATE pg_catalog."default" NOT NULL,
    "Address" character varying(100) COLLATE pg_catalog."default" NOT NULL,
    "privateKey" character varying(100) COLLATE pg_catalog."default" NOT NULL,
    profile_pic character varying(100) COLLATE pg_catalog."default",
    user_token character varying(100) COLLATE pg_catalog."default" NOT NULL,
    role character varying(10) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "MaPayz_user_pkey" PRIMARY KEY (id),
    CONSTRAINT "MaPayz_user_username_key" UNIQUE (username)
)
WITH (
    OIDS = FALSE
);

CREATE TABLE IF NOT EXISTS public."MPayz_user_groups"
(
    id bigint NOT NULL DEFAULT nextval('"MaPayz_user_groups_id_seq"'::regclass),
    user_id bigint NOT NULL,
    group_id integer NOT NULL,
    CONSTRAINT "MaPayz_user_groups_pkey" PRIMARY KEY (id),
    CONSTRAINT "MaPayz_user_groups_user_id_group_id_15c6ff93_uniq" UNIQUE (user_id, group_id)
)
WITH (
    OIDS = FALSE
);

CREATE TABLE IF NOT EXISTS public."MPayz_user_user_permissions"
(
    id bigint NOT NULL DEFAULT nextval('"MaPayz_user_user_permissions_id_seq"'::regclass),
    user_id bigint NOT NULL,
    permission_id integer NOT NULL,
    CONSTRAINT "MaPayz_user_user_permissions_pkey" PRIMARY KEY (id),
    CONSTRAINT "MaPayz_user_user_permiss_user_id_permission_id_1a9c996c_uniq" UNIQUE (user_id, permission_id)
)
WITH (
    OIDS = FALSE
);

CREATE TABLE IF NOT EXISTS public.auth_group
(
    id integer NOT NULL DEFAULT nextval('auth_group_id_seq'::regclass),
    name character varying(150) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT auth_group_pkey PRIMARY KEY (id),
    CONSTRAINT auth_group_name_key UNIQUE (name)
)
WITH (
    OIDS = FALSE
);

CREATE TABLE IF NOT EXISTS public.auth_group_permissions
(
    id bigint NOT NULL DEFAULT nextval('auth_group_permissions_id_seq'::regclass),
    group_id integer NOT NULL,
    permission_id integer NOT NULL,
    CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id),
    CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id)
)
WITH (
    OIDS = FALSE
);

CREATE TABLE IF NOT EXISTS public.auth_permission
(
    id integer NOT NULL DEFAULT nextval('auth_permission_id_seq'::regclass),
    name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT auth_permission_pkey PRIMARY KEY (id),
    CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename)
)
WITH (
    OIDS = FALSE
);

CREATE TABLE IF NOT EXISTS public.dashboard_userdashboardmodule
(
    id bigint NOT NULL DEFAULT nextval('dashboard_userdashboardmodule_id_seq'::regclass),
    title character varying(255) COLLATE pg_catalog."default" NOT NULL,
    module character varying(255) COLLATE pg_catalog."default" NOT NULL,
    app_label character varying(255) COLLATE pg_catalog."default",
    user_id bigint,
    "column" integer NOT NULL,
    "order" integer NOT NULL,
    settings text COLLATE pg_catalog."default" NOT NULL,
    children text COLLATE pg_catalog."default" NOT NULL,
    collapsed boolean NOT NULL,
    CONSTRAINT dashboard_userdashboardmodule_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
);

CREATE TABLE IF NOT EXISTS public.django_admin_log
(
    id integer NOT NULL DEFAULT nextval('django_admin_log_id_seq'::regclass),
    action_time timestamp with time zone NOT NULL,
    object_id text COLLATE pg_catalog."default",
    object_repr character varying(200) COLLATE pg_catalog."default" NOT NULL,
    action_flag smallint NOT NULL,
    change_message text COLLATE pg_catalog."default" NOT NULL,
    content_type_id integer,
    user_id bigint NOT NULL,
    CONSTRAINT django_admin_log_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
);

CREATE TABLE IF NOT EXISTS public.django_content_type
(
    id integer NOT NULL DEFAULT nextval('django_content_type_id_seq'::regclass),
    app_label character varying(100) COLLATE pg_catalog."default" NOT NULL,
    model character varying(100) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT django_content_type_pkey PRIMARY KEY (id),
    CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model)
)
WITH (
    OIDS = FALSE
);

CREATE TABLE IF NOT EXISTS public.django_migrations
(
    id bigint NOT NULL DEFAULT nextval('django_migrations_id_seq'::regclass),
    app character varying(255) COLLATE pg_catalog."default" NOT NULL,
    name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    applied timestamp with time zone NOT NULL,
    CONSTRAINT django_migrations_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
);

CREATE TABLE IF NOT EXISTS public.django_session
(
    session_key character varying(40) COLLATE pg_catalog."default" NOT NULL,
    session_data text COLLATE pg_catalog."default" NOT NULL,
    expire_date timestamp with time zone NOT NULL,
    CONSTRAINT django_session_pkey PRIMARY KEY (session_key)
)
WITH (
    OIDS = FALSE
);

ALTER TABLE IF EXISTS public."MPayz_contacts"
    ADD CONSTRAINT "MaPayz_contact_user_id_d2f794b9_fk_MaPayz_user_id" FOREIGN KEY (user_id)
    REFERENCES public."MPayz_user" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX IF NOT EXISTS "MaPayz_contact_user_id_d2f794b9"
    ON public."MPayz_contacts"(user_id);


ALTER TABLE IF EXISTS public."MPayz_email_verify"
    ADD CONSTRAINT "MaPayz_email_verify_User_id_95388dd0_fk_MaPayz_user_id" FOREIGN KEY ("User_id")
    REFERENCES public."MPayz_user" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX IF NOT EXISTS "MaPayz_email_verify_User_id_key"
    ON public."MPayz_email_verify"("User_id");


ALTER TABLE IF EXISTS public."MPayz_healthrecords"
    ADD CONSTRAINT "MaPayz_nft_data_User_id_8fbb0ac3_fk_MaPayz_user_id" FOREIGN KEY ("User_id")
    REFERENCES public."MPayz_user" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX IF NOT EXISTS "MaPayz_nft_data_User_id_key"
    ON public."MPayz_healthrecords"("User_id");


ALTER TABLE IF EXISTS public."MPayz_messages"
    ADD CONSTRAINT "MaPayz_direct_message_User_id_8d02fe29_fk_MaPayz_user_id" FOREIGN KEY ("User_id")
    REFERENCES public."MPayz_user" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX IF NOT EXISTS "MaPayz_direct_message_User_id_8d02fe29"
    ON public."MPayz_messages"("User_id");


ALTER TABLE IF EXISTS public."MPayz_messages"
    ADD CONSTRAINT "MaPayz_direct_message_recipient_id_96d79160_fk_MaPayz_user_id" FOREIGN KEY (recipient_id)
    REFERENCES public."MPayz_user" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX IF NOT EXISTS "MaPayz_direct_message_recipient_id_96d79160"
    ON public."MPayz_messages"(recipient_id);


ALTER TABLE IF EXISTS public."MPayz_messages"
    ADD CONSTRAINT "MaPayz_direct_message_sender_id_07b3f5b2_fk_MaPayz_user_id" FOREIGN KEY (sender_id)
    REFERENCES public."MPayz_user" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX IF NOT EXISTS "MaPayz_direct_message_sender_id_07b3f5b2"
    ON public."MPayz_messages"(sender_id);


ALTER TABLE IF EXISTS public."MPayz_support"
    ADD CONSTRAINT "MaPayz_support_dm_User_id_cf2ca686_fk_MaPayz_user_id" FOREIGN KEY ("User_id")
    REFERENCES public."MPayz_user" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX IF NOT EXISTS "MaPayz_support_dm_User_id_cf2ca686"
    ON public."MPayz_support"("User_id");


ALTER TABLE IF EXISTS public."MPayz_support"
    ADD CONSTRAINT "MaPayz_support_dm_recipient_id_968f55d9_fk_MaPayz_user_id" FOREIGN KEY (recipient_id)
    REFERENCES public."MPayz_user" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX IF NOT EXISTS "MaPayz_support_dm_recipient_id_968f55d9"
    ON public."MPayz_support"(recipient_id);


ALTER TABLE IF EXISTS public."MPayz_support"
    ADD CONSTRAINT "MaPayz_support_dm_sender_id_730e5cec_fk_MaPayz_user_id" FOREIGN KEY (sender_id)
    REFERENCES public."MPayz_user" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX IF NOT EXISTS "MaPayz_support_dm_sender_id_730e5cec"
    ON public."MPayz_support"(sender_id);


ALTER TABLE IF EXISTS public."MPayz_tokenrequests"
    ADD CONSTRAINT "MaPayz_request_token_User_id_59079dfa_fk_MaPayz_user_id" FOREIGN KEY ("User_id")
    REFERENCES public."MPayz_user" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX IF NOT EXISTS "MaPayz_request_token_User_id_59079dfa"
    ON public."MPayz_tokenrequests"("User_id");


ALTER TABLE IF EXISTS public."MPayz_tokenrequests"
    ADD CONSTRAINT "MaPayz_request_token_recipient_id_40e1b945_fk_MaPayz_user_id" FOREIGN KEY (recipient_id)
    REFERENCES public."MPayz_user" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX IF NOT EXISTS "MaPayz_request_token_recipient_id_40e1b945"
    ON public."MPayz_tokenrequests"(recipient_id);


ALTER TABLE IF EXISTS public."MPayz_tokenrequests"
    ADD CONSTRAINT "MaPayz_request_token_sender_id_8d575276_fk_MaPayz_user_id" FOREIGN KEY (sender_id)
    REFERENCES public."MPayz_user" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX IF NOT EXISTS "MaPayz_request_token_sender_id_8d575276"
    ON public."MPayz_tokenrequests"(sender_id);


ALTER TABLE IF EXISTS public."MPayz_user_groups"
    ADD CONSTRAINT "MaPayz_user_groups_group_id_24fab2ae_fk_auth_group_id" FOREIGN KEY (group_id)
    REFERENCES public.auth_group (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX IF NOT EXISTS "MaPayz_user_groups_group_id_24fab2ae"
    ON public."MPayz_user_groups"(group_id);


ALTER TABLE IF EXISTS public."MPayz_user_groups"
    ADD CONSTRAINT "MaPayz_user_groups_user_id_cf898b2c_fk_MaPayz_user_id" FOREIGN KEY (user_id)
    REFERENCES public."MPayz_user" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX IF NOT EXISTS "MaPayz_user_groups_user_id_cf898b2c"
    ON public."MPayz_user_groups"(user_id);


ALTER TABLE IF EXISTS public."MPayz_user_user_permissions"
    ADD CONSTRAINT "MaPayz_user_user_per_permission_id_7ba30482_fk_auth_perm" FOREIGN KEY (permission_id)
    REFERENCES public.auth_permission (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX IF NOT EXISTS "MaPayz_user_user_permissions_permission_id_7ba30482"
    ON public."MPayz_user_user_permissions"(permission_id);


ALTER TABLE IF EXISTS public."MPayz_user_user_permissions"
    ADD CONSTRAINT "MaPayz_user_user_permissions_user_id_2b9c0472_fk_MaPayz_user_id" FOREIGN KEY (user_id)
    REFERENCES public."MPayz_user" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX IF NOT EXISTS "MaPayz_user_user_permissions_user_id_2b9c0472"
    ON public."MPayz_user_user_permissions"(user_id);


ALTER TABLE IF EXISTS public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id)
    REFERENCES public.auth_permission (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX IF NOT EXISTS auth_group_permissions_permission_id_84c5c92e
    ON public.auth_group_permissions(permission_id);


ALTER TABLE IF EXISTS public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id)
    REFERENCES public.auth_group (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX IF NOT EXISTS auth_group_permissions_group_id_b120cbf9
    ON public.auth_group_permissions(group_id);


ALTER TABLE IF EXISTS public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id)
    REFERENCES public.django_content_type (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX IF NOT EXISTS auth_permission_content_type_id_2f476e4b
    ON public.auth_permission(content_type_id);


ALTER TABLE IF EXISTS public.dashboard_userdashboardmodule
    ADD CONSTRAINT "dashboard_userdashbo_user_id_97c13132_fk_MaPayz_us" FOREIGN KEY (user_id)
    REFERENCES public."MPayz_user" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX IF NOT EXISTS dashboard_userdashboardmodule_user_id_97c13132
    ON public.dashboard_userdashboardmodule(user_id);


ALTER TABLE IF EXISTS public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id)
    REFERENCES public.django_content_type (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX IF NOT EXISTS django_admin_log_content_type_id_c4bce8eb
    ON public.django_admin_log(content_type_id);


ALTER TABLE IF EXISTS public.django_admin_log
    ADD CONSTRAINT "django_admin_log_user_id_c564eba6_fk_MaPayz_user_id" FOREIGN KEY (user_id)
    REFERENCES public."MPayz_user" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX IF NOT EXISTS django_admin_log_user_id_c564eba6
    ON public.django_admin_log(user_id);

END;