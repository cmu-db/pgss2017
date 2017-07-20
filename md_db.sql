CREATE TABLE cases (
	case_id VARCHAR(24) PRIMARY KEY NOT NULL,
	title VARCHAR(128) NOT NULL,
	court_system VARCHAR(MAX) NOT NULL,
	case_type VARCHAR(MAX) NOT NULL,
	filing_date DATE NOT NULL,
	status VARCHAR(14) NOT NULL,
	disposition VARCHAR(MAX),
	disposition_date DATE,
	violation_county VARCHAR(MAX),
	violation_date DATE,
);

CREATE TABLE parties (
	case_id VARCHAR(24) FOREIGN KEY REFERENCES cases(case_id) NOT NULL,
	id PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(MAX),
	type VARCHAR(MAX),
	bus_org_name VARCHAR(MAX),
	agency_name VARCHAR(MAX),
	race VARCHAR(MAX),
	sex ENUM('M','F'),
	height INT CHECK(height BETWEEN 0 AND 108),
	weight INT CHECK(weight BETWEEN 0 AND 1000),
	dob DATE,
	address VARCHAR(MAX),
	city VARCHAR(MAX),
	state VARCHAR(2),
	zip VARCHAR(5)
);

CREATE TABLE attorneys (
	party_id INT FOREIGN KEY REFERENCES parties(id) NOT NULL,
	name VARCHAR(MAX),
	appearance_date DATE,
	removal_date DATE,
	practice_name VARCHAR(MAX),
	address VARCHAR(MAX),
	city VARCHAR(MAX),
	state VARCHAR(2),
	zip VARCHAR(5)
);

CREATE TABLE events (
	case_id VARCHAR(24) FOREIGN KEY NOT NULL,
	type VARCHAR(MAX),
	date DATE,
	time VARCHAR(8),
	result VARCHAR(MAX),
	result_date DATE,
);

CREATE TABLE charges(
	case_id VARCHAR(24) FOREIGN KEY REFERENCES cases(case_id) NOT NULL,
	statute_code VARCHAR(MAX) NOT NULL,
	charge_description VARCHAR(MAX) NOT NULL,
	offense_date_from DATE,
	offense_date_to DATE,
	class VARCHAR(1),
	amended_date VARCHAR(MAX),
	cjis_code VARCHAR(MAX),
	probable_cause BOOLEAN,
	victim_age INTEGER CHECK(victim_age BETWEEN 0 AND 150),
	speed_limit INTEGER CHECK(speed_limit BETWEEN 0 AND 100),
	recorded_speed INTEGER CHECK(recorded_speed >= 0),
	location_stopped VARCHAR(MAX),
	accident_contribution BOOLEAN,
	injuries INTEGER,
	property_damage BOOLEAN,
	seatbelts_used BOOLEAN,
	mandatory_court_appearance BOOLEAN,
	vehicle_tag VARCHAR(MAX),
	vehicle_state VARCHAR(2),
	plea VARCHAR(MAX),
	plea_date DATE,
	disposition VARCHAR(MAX),
	disposition_date DATE,
	jail_extreme_punishment VARCHAR(MAX),
	jail_term INTERVAL,
	jail_suspended_term INTERVAL,
	jail_unsuspended_term INTERVAL,
	probation_term INTERVAL,
	probation_supervised_term INTERVAL,
	probation_unsupervised_term INTERVAL,
	fine_amt MONEY,
	fine_suspended_amt MONEY,
	fine_restitution_amt MONEY,
	fine_due DATETIME,
	fine_first_pmt_due DATETIME,
	cws_hours INTEGER,
	cws_deadline DATETIME,
	cws_location VARCHAR(MAX),
	cws_date DATETIME
);

CREATE TABLE documents(
	case_id VARCHAR(24) FOREIGN KEY REFERENCES cases(case_id) NOT NULL,
	name VARCHAR(MAX) NOT NULL,
	filing_date DATE
);

CREATE TABLE judgements(
	case_id VARCHAR(24) FOREIGN KEY REFERENCES cases(case_id) NOT NULL,
	against VARCHAR(MAX),
	in_favor_of VARCHAR(MAX),
	type VARCHAR(MAX),
	date DATE,
	interest MONEY,
	amt MONEY
);

CREATE TABLE complaints(
	case_id VARCHAR(24) FOREIGN KEY REFERENCES cases(case_id) NOT NULL,
	type VARCHAR(MAX) NOT NULL,
	status VARCHAR(MAX) NOT NULL,
	status_date DATE,
	filing_date DATE,
	amt MONEY
);
