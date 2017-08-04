-- First 5 digits of ZIP codes
UPDATE parties
SET zip = LEFT(zip, 5)
WHERE LENGTH(zip) > 5;
UPDATE attorneys
SET zip = LEFT(zip, 5)
WHERE LENGTH(zip) > 5;

-- Remove random numbers in front of charge dispositions
UPDATE charges
SET disposition = SPLIT_PART(disposition, ';', 2)
WHERE disposition LIKE '%:%';

-- Combine some charge dispositions
UPDATE charges
SET disposition = 'Nolle Prosequi'
WHERE LOWER(disposition) = 'nolle prosequi';
UPDATE charges
SET disposition = 'Stet'
WHERE LOWER(disposition) = 'stet';
UPDATE charges
SET disposition = 'Guilty'
WHERE LOWER(disposition) = 'guilty';
UPDATE charges
SET disposition = 'Not Guilty'
WHERE LOWER(disposition) = 'not guilty';
UPDATE charges
SET disposition = 'Probation Before Judgement'
WHERE LOWER(disposition) LIKE '%probation before judgement%'
OR LOWER(disposition) LIKE '%pbj%';

-- Set height 0 to null
UPDATE parties
SET height = NULL
WHERE height = 0;

-- Set weight 0 to null
UPDATE parties
SET weight = NULL
WHERE weight = 0;

-- Combine some races
UPDATE parties
SET race = 'African American'
WHERE LOWER(race) = 'black'
OR LOWER(race) = 'africanamerican'
OR LOWER(race) = 'african american'
OR LOWER(race) = 'black, african american'
OR LOWER(race) = 'black,african american'
OR LOWER(race) =  'african american/black';
UPDATE parties
SET race = 'Caucasian'
WHERE LOWER(race) = 'white'
OR LOWER(race) = 'caucasian'
OR LOWER(race) = 'caucasion'
OR LOWER(race) = 'white, caucasian, asiatic indian, arab'
OR LOWER(race) = 'white,caucasian,asiatic indian,arab'
OR LOWER(race) = 'white, asiatic indian, arab';
UPDATE parties
SET race = 'American Indian, Alaska Native'
WHERE LOWER(race) = 'american indian, alaska native'
OR LOWER(race) = 'american indian,alaska native';
UPDATE parties
SET race = 'Pacific Islander'
WHERE LOWER(race) = 'asian,native hawaiian,other pacific islander'
OR LOWER(race) = 'asian, native hawaiian,other pacific islander'
OR LOWER(race) = 'native hawaiian or other pacific islander';
UPDATE parties
SET race = null
WHERE LOWER(race) = 'unknown';
UPDATE parties
SET race = 'Other'
WHERE LOWER(race) = 'unknown, other'
OR LOWER(race) = 'unknown,other';
