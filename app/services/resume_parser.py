import re
import io
from typing import Optional, List, Tuple
import fitz  # PyMuPDF
from datetime import datetime

class ResumeParser:

    COMMON_SKILLS = [
        "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Ruby", "Go", "Rust",
        "React", "Angular", "Vue", "Node.js", "Express", "Django", "Flask", "FastAPI",
        "MongoDB", "PostgreSQL", "MySQL", "Redis", "Elasticsearch",
        "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Jenkins", "CI/CD",
        "Machine Learning", "Deep Learning", "AI", "Data Science", "NLP",
        "Git", "Agile", "Scrum", "REST API", "GraphQL", "Microservices"
    ]
    
    EDUCATION_KEYWORDS = [
        "Bachelor", "Master", "PhD", "B.Tech", "M.Tech", "B.E.", "M.E.",
        "B.Sc", "M.Sc", "BCA", "MCA", "MBA", "Diploma", "B.S.", "M.S."
    ]
    
    @staticmethod
    def pdf_to_text(pdf_binary: bytes) -> str:
        
        try:
            pdf_stream = io.BytesIO(pdf_binary)
            
            doc = fitz.open(stream=pdf_stream, filetype="pdf")
            
            text = ""
            for page in doc:
                text += page.get_text()
            
            doc.close()
            return text.strip()
        
        except Exception as e:
            print(f"Error extracting text from PDF: {str(e)}")
            return ""
    
    @staticmethod
    def extract_email(text: str) -> Optional[str]:
        
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else None
    
    @staticmethod
    def extract_phone(text: str) -> Optional[str]:
        
        phone_pattern = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
        phones = re.findall(phone_pattern, text)
        
        if phones:
            phone = phones[0].strip()
            phone = re.sub(r'[\s\-\(\)]', '', phone)
            return phone
        return None
    
    @staticmethod
    def extract_linkedin(text: str) -> Optional[str]:
        
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        linkedin_matches = re.findall(linkedin_pattern, text.lower())
        
        if linkedin_matches:
            url = linkedin_matches[0]
            if not url.startswith('http'):
                url = f"https://{url}"
            return url
        return None
    
    @staticmethod
    def extract_name(text: str) -> Optional[str]:
        
        lines = text.split('\n')
        
        for line in lines[:5]:
            line = line.strip()
            if not line or len(line) < 3:
                continue
            if line.lower() in ['resume', 'cv', 'curriculum vitae']:
                continue
            
            words = line.split()
            if 2 <= len(words) <= 4:
                if all(word.replace('.', '').isalpha() for word in words):
                    return line
        
        return None
    
    @staticmethod
    def extract_skills(text: str) -> List[str]:
        
        found_skills = []
        text_lower = text.lower()
        
        for skill in ResumeParser.COMMON_SKILLS:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        return found_skills
    
    @staticmethod
    def extract_education(text: str) -> List[dict]:
        
        education_list = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            for keyword in ResumeParser.EDUCATION_KEYWORDS:
                if keyword.lower() in line_lower:
                    year_match = re.search(r'\b(19|20)\d{2}\b', line)
                    year = year_match.group(0) if year_match else None
                    
                    duration_match = re.search(r'\b(19|20)\d{2}\s*[-–]\s*(19|20)\d{2}\b', line)
                    if duration_match:
                        year = duration_match.group(0)
                    
                    education_list.append({
                        "degree": line.strip(),
                        "institution": None,  # Would need more sophisticated parsing
                        "year": year
                    })
                    break
        
        return education_list[:5]  # Limit to 5 entries
    
    @staticmethod
    def extract_experience(text: str) -> List[dict]:
        
        experience_list = []
        
        duration_pattern = r'((?:19|20)\d{2}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* (?:19|20)\d{2})\s*[-–]\s*((?:19|20)\d{2}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* (?:19|20)\d{2}|Present|Current)'
        
        matches = re.finditer(duration_pattern, text, re.IGNORECASE)
        
        for match in matches:
            duration = match.group(0)
            start = max(0, match.start() - 100)
            end = min(len(text), match.end() + 100)
            context = text[start:end]
            
            experience_list.append({
                "company": None,  # Would need more sophisticated parsing
                "role": None,
                "duration": duration,
                "description": context[:100]  # First 100 chars of context
            })
        
        return experience_list[:10]  # Limit to 10 entries
    
    @staticmethod
    def calculate_total_experience(experience_list: List[dict]) -> Optional[float]:
        
        if not experience_list:
            return None
        
        total_years = 0.0
        
        for exp in experience_list:
            duration = exp.get("duration", "")
            if not duration:
                continue
            
            years = re.findall(r'(19|20)\d{2}', duration)
            
            if len(years) >= 2:
                try:
                    start_year = int(years[0])
                    end_year = int(years[1])
                    total_years += (end_year - start_year)
                except ValueError:
                    continue
            elif len(years) == 1 and 'present' in duration.lower():
                try:
                    start_year = int(years[0])
                    current_year = datetime.now().year
                    total_years += (current_year - start_year)
                except ValueError:
                    continue
        
        return round(total_years, 1) if total_years > 0 else None
    
    @staticmethod
    def parse_resume(pdf_binary: bytes) -> dict:
        
        text = ResumeParser.pdf_to_text(pdf_binary)
        
        if not text:
            return {
                "fullName": None,
                "email": None,
                "phone": None,
                "linkedinUrl": None,
                "skills": [],
                "education": [],
                "experience": [],
                "totalExperienceYears": None,
                "rawResumeText": ""
            }
        
        email = ResumeParser.extract_email(text)
        phone = ResumeParser.extract_phone(text)
        linkedin = ResumeParser.extract_linkedin(text)
        name = ResumeParser.extract_name(text)
        skills = ResumeParser.extract_skills(text)
        education = ResumeParser.extract_education(text)
        experience = ResumeParser.extract_experience(text)
        total_exp = ResumeParser.calculate_total_experience(experience)
        
        return {
            "fullName": name,
            "email": email,
            "phone": phone,
            "linkedinUrl": linkedin,
            "skills": skills,
            "education": education,
            "experience": experience,
            "totalExperienceYears": total_exp,
            "rawResumeText": text
        }
