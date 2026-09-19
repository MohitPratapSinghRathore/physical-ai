"""Project configuration.

SEC EDGAR fair access policy requires automated requests to declare a real name and
contact email in the User-Agent header, and to stay under 10 requests per second. Supplying
these is compliance with a published access policy, not identification bypass. See
https://www.sec.gov/os/webmaster-faq#developers

Owner authorised the use of this name and address for SEC declaration on 2026-09-19.
"""

OWNER_NAME = "Gunveer Kalsi"
OWNER_EMAIL = "team@oviguide.in"
PROJECT = "physical-ai-research"
VERSION = "0.2"

# SEC wants "Sample Company Name AdminContact@sample.com"
SEC_USER_AGENT = f"{OWNER_NAME} ({OWNER_EMAIL}) {PROJECT}/{VERSION}"

# SEC fair access limit is 10 requests/second. 0.12s ~= 8.3 req/s.
SEC_REQUEST_DELAY_SECONDS = 0.12
