CREATE TABLE cases (
    case_id VARCHAR(24) PRIMARY KEY NOT NULL,
    title VARCHAR(128) NOT NULL,
    court_system VARCHAR(MAX),
    case_type VARCHAR(MAX),
    filing_date DATE,
    status VARCHAR(14),
    disposition VARCHAR(MAX),
    disposition_date DATE,
    violation_county VARCHAR(MAX),
    violation_date DATE,
);

CREATE TABLE parties (
  case_number VARCHAR(24) FOREIGN KEY NOT NULL,
  name VARCHAR(MAX),
  party_type ENUM('DEFENDANT','ATTORNEY','OTHER'),
  business_org VARCHAR(MAX),
  agency_name VARCHAR(MAX),
  race VARCHAR(),
  sex ENUM('M','F'),
  height VARCHAR(7),
  weight int,
  date_of_birth DATE,
  address VARCHAR(MAX),
);

CREATE TABLE attorneys (
  party_id int FOREIGN KEY NOT NULL AUTO_INCREMENT,
  name VARCHAR(MAX),
  appearance_date DATE,
  removal_date DATE,
  practice_name VARCHAR(MAX),
  address VARCHAR(MAX),
);

CREATE TABLE events (
  case_number VARCHAR(24) FOREIGN KEY NOT NULL,
  event_type VARCHAR(MAX),
  event_date DATE,
  event_time VARCHAR(8),
  result VARCHAR(MAX),
  result_date DATE,
);

CREATE TABLE charges(
  case_id VARCHAR(24) REFERENCES cases(case_id),
  statute_code VARCHAR(MAX) NOT NULL,
  charge_description VARCHAR(MAX) NOT NULL,
  offense_date_from VARCHAR(MAX),
  offense_date_to VARCHAR(MAX),
  charge_class VARCHAR(1),
  amended_date VARCHAR(MAX),
  cjis_code VARCHAR(MAX),
  probable_cause BOOLEAN,
  victim_age INTEGER,
  speed_limit INTEGER,
  recorded_speed INTEGER,
  location_stopped VARCHAR(MAX),
  contributed_to_accident BOOLEAN,
  personal_injury INTEGER,
  property_damage BOOLEAN,
  seatbelts_used BOOLEAN,
  mandatory_court_appearance BOOLEAN,
  vehicle_tag VARCHAR(MAX),
  vehicle_state VARCHAR(2),
  plea VARCHAR(MAX),
  plea_date DATE,
  disposition VARCHAR(MAX),
  disposition_date DATE,
  jail_life_death VARCHAR(MAX),
  jail_term DATETIME,
  probation DATETIME,
  fine_amount = VARCHAR(MAX),
  fine_suspended_amount VARCHAR(MAX),
  fine_restitution_amount VARCHAR(MAX),
  fine_due DATETIME,
  first_pmt_due DATETIME,
  community_service_hours INTEGER,
  community_service_complete_by DATE,
  community_service_report_to VARCHAR(MAX),
  community_service_report_date DATETIME
);

CREATE TABLE documents(
  case_id VARCHAR(24) REFERENCES cases(case_id),
  document VARCHAR(MAX) NOT NULL,
  file_date DATE
);

CREATE TABLE judgements(
  case_id VARCHAR(24) REFERENCES cases(case_id),
  against VARCHAR(MAX),
  in_favor_of VARCHAR(MAX),
  type VARCHAR(MAX),
  entered_date DATE,
  interest DOUBLE PRECISION,
  amount DOUBLE PRECISION
);

CREATE TABLE complaints(
  case_id VARCHAR(24) REFERENCES cases(case_id),
  type VARCHAR(MAX) NOT NULL,
  status VARCHAR(MAX) NOT NULL,
  status_date DATE,
  filing_date DATE,
  amount DOUBLE PRECISION
);
