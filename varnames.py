ATTRIBUTE_MAP = {
    'Case Number': 'case_id',
    'Case Type': 'type',
    'Case Disposition': 'disposition',
    'Connection': 'party_type',
    'Business or Organization Name': 'bus_org_name',
    'Agency Name': 'agency_name',
    'Zip Code': 'zip',
    'Event Type': 'type',
    'Event Date': 'date',
    'Event Time': 'time',
    'Probable Cause Indicator': 'probable_cause',
    'Contributed to Accident': 'accident_contribution',
    'Personal Injury': 'injuries',
    'Life/Death': 'extreme_punishment',
    'Suspended Term': 'jail_suspended_term',
    'UnSuspended Term': 'jail_unsuspended_term',
    'Probation': 'probation_term',
    'Supervised': 'probation_supervised_term',
    'UnSupervised Term': 'probation_unsupervised_term',
    'First Pmt Due': 'fine_first_pmt_due',
    'Hours': 'cws_hours',
    'Complete By': 'cws_deadline',
    'Report To': 'cws_location',
    'Report Date': 'cws_date'
    'Document Name': 'name'
    'Entered Date': 'date',
    'Ordered Date': 'date',
    'PreJudgement Interest': 'interest',
    'Amount': 'amt',
    'Amount of Judgement': 'amt',
}

def getAttributeName(label):
    if label.endswith(':'): label = label[:-1]
    attr = ATTRIBUTE_MAP.get(label)
    if not attr: attr = label.lower().replace(' ', '_')
    return attr
