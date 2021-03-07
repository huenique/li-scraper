class Basic(object):
    url = None
    title = None
    role = None
    company_name = None
    company_loc = None

    def __init__(
        self,
        url=None,
        title=None,
        role=None,
        company_name=None,
        company_loc=None,
    ):
        self.url = url
        self.title = title
        self.role = role
        self.company_name = company_name
        self.company_loc = company_loc

    def __repr__(self):
        return 'URL: {url}, \nTitle: {title}, \nRole: {role}, \nCompany: {company}, \nLocation: {location}'.format(
            url=self.url,
            title=self.title,
            role=self.role,
            company=self.company_name,
            location=self.company_loc)


class Contact(object):
    website = None
    email = None
    twitter = None

    def __init__(self, website=None, email=None, twitter=None):
        self.website = website
        self.email = email
        self.twitter = twitter

    def __repr__(self):
        return 'Website: {website}, \nEmail: {email}, \nTwitter: {twitter}'.format(
            website=self.website, email=self.email, twitter=self.twitter)


class Company(object):
    org_url = None
    industry = None
    company_size = None
    specialties = None

    def __init__(self,
                 industry=None,
                 org_url=None,
                 company_size=None,
                 specialties=None):
        self.industry = industry
        self.org_url = org_url
        self.company_size = company_size
        self.specialties = specialties

    def __repr__(self):
        return 'Org_URL: {url}, \nIndustry: {industry}, \nCompany size: {size}, \nSpecialties: {specialties}'.format(
            url=self.org_url,
            industry=self.industry,
            size=self.company_size,
            specialties=self.specialties)
