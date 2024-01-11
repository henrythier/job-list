from enum import Enum

class JobTool(Enum):
    PERSONIO = "Personio"

class Company:
    def __init__(self, name, url, jobtool):
        self.name = str(name)
        self.url = str(url)
        self.jobtool = JobTool(jobtool)
    
    def __str__(self):
        return f"Company: {self.name}\nURL: {self.url}\nJob tool: {self.jobtool.value}"