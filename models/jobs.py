from enum import Enum

class Category(Enum):
    ADMIN = "Admin"
    ANALYTICS = "Analytics"
    ENGINEERING = "Engineering"
    MANUFACTURING = "Manufacturing"
    MARKETING = "Marketing"
    SALES = "Sales"
    OTHER = "Other"
    UNKNOWN = "Unknown"

class Senority(Enum):
    STUDENT = "Student"
    ENTRYLEVEL = "Entry"
    EXPERIENCED = "Experienced"
    UNKNOWN = "Unknown"

class Schedule(Enum):
    FULLTIME = "Full-time"
    PARTTIME = "Part-time"
    UNKNOWN = "Unknown"

class Experience(Enum):
    ENTRY = "Entry"
    JUNIOR = "1-2"
    MID = "2-5"
    SENIOR = "5-7"
    UNKNOWN = "Unknown"

class Job:
    def __init__(self, id, title, category, seniority, experience, schedule, link):
        self.id = str(id)
        self.title = str(title)
        self.category = Category(category)
        self.seniority = Senority(seniority)
        self.experience = Experience(experience)
        self.schedule = Schedule(schedule)
        self.link = link
    
    def __str__(self):
        return f"Title: {self.title}\nCategory: {self.category.value}\nSeniority: {self.seniority.value}\nExperience: {self.experience.value}\nSchedule: {self.schedule.value}\nLink: {self.link}"