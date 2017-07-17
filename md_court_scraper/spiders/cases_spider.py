import scrapy
import string
import datetime

BASE_URL = 'http://casesearch.courts.state.md.us'
DISCLAIMER_URL = '/casesearch/processDisclaimer.jis'
SEARCH_URL = '/casesearch/inquirySearch.jis'

COMPANY_TYPES = ['Y', 'N']
CASE_TYPES = ['CIVIL', 'CRIMINAL', 'TRAFFIC', 'CP']
COURT_SYSTEMS = ['C', 'D']
LETTER_MAX = 26

START_DATE = datetime.date(year = 1970, month = 1, day = 1)
END_DATE = datetime.date.today()

def daterange( start_date, end_date ):
	if start_date <= end_date:
		for n in range((end_date - start_date).days + 1):
			yield start_date + datetime.timedelta(n)
	else:
		for n in range((start_date - end_date).days + 1):
			yield start_date - datetime.timedelta(n)


class CasesSpider(scrapy.Spider):
	name = 'cases'
	cookie = None

	def start_requests(self):
		return [ scrapy.Request(
			BASE_URL + DISCLAIMER_URL,
			callback = self.acceptDisclaimer
		)]

	def acceptDisclaimer(self, response):
		self.cookie = response.headers['Set-Cookie']

		yield scrapy.FormRequest(
			BASE_URL + DISCLAIMER_URL,
			formdata = {
				'action': 'Continue',
				'disclaimer': 'Y'
			},
			callback = self.doSearches
		 )

	def doSearches(self, response):
		for date in daterange(START_DATE, END_DATE):
			for company in COMPANY_TYPES:
				for letter in range(LETTER_MAX):
					for case in CASE_TYPES:
						for court in COURT_SYSTEMS:
							yield scrapy.FormRequest(
								BASE_URL + SEARCH_URL,
								headers = {
									'Cookie': self.cookie
								},
								formdata = {
									'action': 'Search',
									'company': company,
									'countyName': '',
									'courtSystem': court,
									'filingDate': str(date.month) + '/' + str(date.day) + '/' + str(date.year),
									'filingEnd': '',
									'filingStart': '',
									'firstName': '',
									'lastName': string.ascii_lowercase[letter],
									'middleName':'',
									'partyType': '',
									'site': case,
								},
								callback = self.parseResults
							)

	def parseResults(self, response):
		caseLinks = response.css('table.results a::attr(href)').extract()
		for href in caseLinks:
			if href.startswith(BASE_URL + SEARCH_URL): continue
			else:
				yield response.follow(
					href,
					headers = {
						'Cookie': self.cookie
					},
					callback = self.parseCase
				)

		if not response.meta.get('Sub_Page') and len(caseLinks) > 0:
			pageLinks = set(response.css('span.pagelinks a::attr(href)').extract())
			for href in pageLinks:
				yield response.follow(
					href,
					headers = {
						'Cookie': self.cookie
					},
					meta = {
						'Sub_Page': True
					},
					callback = self.parseResults
				)

	def parseCase(self, response):
		with open('data.txt', 'a') as file:
			file.write(response.url + '\n')
