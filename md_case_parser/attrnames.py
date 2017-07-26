ATTRIBUTE_MAP = {
    'Case Number': 'case_id',
    'Case Type': 'type',
    'Case Disposition': 'disposition',
    'Connection': 'type',
    'Party Type': 'type',
    'Business or Organization Name': 'bus_org_name',
    'AgencyName': 'agency_name',
    'Zip Code': 'zip',
    'Event Type': 'type',
    'Event Date': 'date',
    'Event Time': 'time',
    'Probable Cause Indicator': 'probable_cause',
    'Contributed to Accident': 'accident_contribution',
    'Personal Injury': 'injuries',
    'Charge Class': 'class',
    'Life/Death': 'jail_extreme_punishment',
    'Suspended Term': 'jail_suspended_term',
    'UnSuspended Term': 'jail_unsuspended_term',
    'Probation': 'probation_term',
    'Supervised': 'probation_supervised_term',
    'UnSupervised Term': 'probation_unsupervised_term',
    'First Pmt Due': 'fine_first_pmt_due',
    'Hours': 'cws_hours',
    'Complete By': 'cws_deadline',
    'Report To': 'cws_location',
    'Report Date': 'cws_date',
    'Document Name': 'name',
    'File Date': 'filing_date',
    'Entered Date': 'date',
    'Ordered Date': 'date',
    'Judgement Interest': 'interest',
    'PreJudgement Interest': 'interest',
    'Amount': 'amt',
    'Amount of Judgement': 'amt',
}

def getAttributeName(label):
    if label.endswith(':'): label = label[:-1]
    attr = ATTRIBUTE_MAP.get(label)
    if not attr: attr = label.lower().replace(' ', '_')
    return attr

HEADER_MAP = {
    'Case Information': 'cases',
    'Plaintiff/Petitioner Information': 'parties',
    'Plaintiff': 'parties',
    'Officer - Arresting/Complainant': 'parties',
    'Attorney(s) for the Plaintiff/Petitioner': 'attorneys',
    'Attorney(s) for the Plaintiff': 'attorneys',
    'Defendant/Respondent Information': 'parties',
    'Defendant': 'parties',
    'Attorney(s) for the Defendant/Respondent': 'attorneys',
    'Attorney(s) for the Defendant': 'attorneys',
    'Court Scheduling Information': 'events',
    'ORIGINAL JUDGMENT': 'judgements',
    'Related Persons Information': 'parties',
    'Attorney(s) for the Related Person': 'attorneys',
    'Charge and Disposition Information': 'charges',
    'Disposition': 'charges',
    'Document Tracking': 'documents',
    'Document Information': 'documents'
}

def getSectionName(title):
    return HEADER_MAP.get(title)
