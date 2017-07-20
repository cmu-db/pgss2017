-- Temporary table to store HTML for case detail pages
CREATE TABLE rawcases(
	case_id VARCHAR(24) PRIMARY KEY NOT NULL,
	html TEXT NOT NULL
);

-- Actual tables after parsing
CREATE TABLE cases(
	case_id VARCHAR(24) PRIMARY KEY NOT NULL,
	title VARCHAR(128) NOT NULL,
	court_system VARCHAR NOT NULL,
	case_type VARCHAR NOT NULL,
	filing_date DATE NOT NULL,
	status VARCHAR(14) NOT NULL,
	disposition VARCHAR,
	disposition_date DATE,
	violation_county VARCHAR,
	violation_date DATE
);

CREATE TYPE sex AS ENUM(
	'M',
	'F'
);

CREATE TABLE parties(
	case_id VARCHAR(24) REFERENCES cases NOT NULL,
	id BIGSERIAL PRIMARY KEY,
	name VARCHAR,
	type VARCHAR,
	bus_org_name VARCHAR,
	agency_name VARCHAR,
	race VARCHAR,
	sex sex,
	height INT CHECK(height BETWEEN 0 AND 108),
	weight INT CHECK(weight BETWEEN 0 AND 1000),
	dob DATE,
	address VARCHAR,
	city VARCHAR,
	state VARCHAR(2),
	zip VARCHAR(5)
);

CREATE TABLE attorneys(
	party_id INT REFERENCES parties NOT NULL,
	name VARCHAR,
	appearance_date DATE,
	removal_date DATE,
	practice_name VARCHAR,
	address VARCHAR,
	city VARCHAR,
	state VARCHAR(2),
	zip VARCHAR(5)
);

CREATE TABLE events(
	case_id VARCHAR(24) REFERENCES cases NOT NULL,
	type VARCHAR,
	date DATE,
	time VARCHAR(8),
	result VARCHAR,
	result_date DATE
);

CREATE TABLE charges(
	case_id VARCHAR(24) REFERENCES cases NOT NULL,
	statute_code VARCHAR NOT NULL,
	charge_description VARCHAR NOT NULL,
	offense_date_from DATE,
	offense_date_to DATE,
	class VARCHAR(1),
	amended_date VARCHAR,
	cjis_code VARCHAR,
	probable_cause BOOLEAN,
	victim_age INTEGER CHECK(victim_age BETWEEN 0 AND 150),
	speed_limit INTEGER CHECK(speed_limit BETWEEN 0 AND 100),
	recorded_speed INTEGER CHECK(recorded_speed >= 0),
	location_stopped VARCHAR,
	accident_contribution BOOLEAN,
	injuries INTEGER,
	property_damage BOOLEAN,
	seatbelts_used BOOLEAN,
	mandatory_court_appearance BOOLEAN,
	vehicle_tag VARCHAR,
	vehicle_state VARCHAR(2),
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
	case_id VARCHAR(24) REFERENCES cases NOT NULL,
	name VARCHAR NOT NULL,
	filing_date DATE
);

CREATE TABLE judgements(
	case_id VARCHAR(24) REFERENCES cases NOT NULL,
	against VARCHAR,
	in_favor_of VARCHAR,
	type VARCHAR,
	date DATE,
	interest MONEY,
	amt MONEY
);

CREATE TABLE complaints(
	case_id VARCHAR(24) REFERENCES cases NOT NULL,
	type VARCHAR NOT NULL,
	status VARCHAR NOT NULL,
	status_date DATE,
	filing_date DATE,
	amt MONEY
);
