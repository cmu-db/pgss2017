-- Temporary table to store HTML for case detail pages
CREATE TABLE rawcases(
	case_id VARCHAR PRIMARY KEY NOT NULL,
	html TEXT NOT NULL
);

-- Actual tables after parsing
CREATE TABLE cases(
	case_id VARCHAR PRIMARY KEY NOT NULL,
	timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	title VARCHAR,
	court_system VARCHAR,
	type VARCHAR,
	filing_date DATE,
	status VARCHAR,
	disposition VARCHAR,
	disposition_date DATE,
	violation_county VARCHAR,
	violation_date DATE
);

CREATE TABLE parties(
	case_id VARCHAR REFERENCES cases NOT NULL,
	name VARCHAR,
	type VARCHAR,
	bus_org_name VARCHAR,
	agency_name VARCHAR,
	race VARCHAR,
	sex VARCHAR,
	height INT,
	weight INT,
	dob DATE,
	address VARCHAR,
	city VARCHAR,
	state VARCHAR,
	zip VARCHAR
);

CREATE TABLE attorneys(
	case_id VARCHAR REFERENCES cases NOT NULL,
	name VARCHAR,
	type VARCHAR,
	appearance_date DATE,
	removal_date DATE,
	practice_name VARCHAR,
	address VARCHAR,
	city VARCHAR,
	state VARCHAR,
	zip VARCHAR
);

CREATE TABLE events(
	case_id VARCHAR REFERENCES cases NOT NULL,
	type VARCHAR,
	date DATE,
	time TIME,
	result VARCHAR,
	result_date DATE
);

CREATE TABLE charges(
	case_id VARCHAR REFERENCES cases NOT NULL,
	statute_code VARCHAR,
	description VARCHAR,
	offense_date_from DATE,
	offense_date_to DATE,
	class VARCHAR,
	amended_date VARCHAR,
	cjis_code VARCHAR,
	probable_cause BOOLEAN,
	victim_age INTEGER,
	speed_limit INTEGER,
	recorded_speed INTEGER,
	location_stopped VARCHAR,
	accident_contribution BOOLEAN,
	injuries INTEGER,
	property_damage BOOLEAN,
	seatbelts_used BOOLEAN,
	mandatory_court_appearance BOOLEAN,
	vehicle_tag VARCHAR,
	state VARCHAR,
	plea VARCHAR,
	plea_date DATE,
	disposition VARCHAR,
	disposition_date DATE,
	jail_extreme_punishment VARCHAR,
	jail_term INTERVAL,
	jail_suspended_term INTERVAL,
	jail_unsuspended_term INTERVAL,
	probation_term INTERVAL,
	probation_supervised_term INTERVAL,
	probation_unsupervised_term INTERVAL,
	fine_amt MONEY,
	fine_suspended_amt MONEY,
	fine_restitution_amt MONEY,
	fine_due TIMESTAMP,
	fine_first_pmt_due TIMESTAMP,
	cws_hours INTEGER,
	cws_deadline TIMESTAMP,
	cws_location VARCHAR,
	cws_date TIMESTAMP
);

CREATE TABLE documents(
	case_id VARCHAR REFERENCES cases NOT NULL,
	name VARCHAR,
	filing_date DATE
);

CREATE TABLE judgements(
	case_id VARCHAR REFERENCES cases NOT NULL,
	against VARCHAR,
	in_favor_of VARCHAR,
	type VARCHAR,
	date DATE,
	interest MONEY,
	amt MONEY
);

CREATE TABLE complaints(
	case_id VARCHAR REFERENCES cases NOT NULL,
	type VARCHAR,
	against VARCHAR,
	status VARCHAR,
	status_date DATE,
	filing_date DATE,
	amt MONEY
);
