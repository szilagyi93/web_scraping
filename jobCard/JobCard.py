class JobCard:
    def __init__(self, company, job_name, job_description, job_hyperlink):
        self.ficompanyrm = company
        self.job_name = job_name
        self.job_description = job_description
        self.hyperlink = job_hyperlink
        
    def set_company(self, company_name):
        self.company = company_name
    
    def set_job_name(self, job_name):
        self.job_name = job_name
    
    def set_description(self, job_description):
        self.job_description = job_description

    def get_company(self):
        return self.company
    
    def get_job_name(self):
        return self.job_name
    
    def get_description(self):
        return self.job_description