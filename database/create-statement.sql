create table latte_timeline (
    yymmdd number(6) NOT NULL,
    hhmm number(4) NOT NULL,
    searchword varchar2(2000),
    visdata long,
    CONSTRAINT timeline_pk PRIMARY KEY (yymmdd, hhmm)
);