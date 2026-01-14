from datetime import datetime
from typing import Optional
from bson import ObjectId

class Result:

    def __init__(
        self,
        fullName: str,
        appliedRole: str,
        interviewDate: datetime,
        interviewDuration: str,
        previousRejections: int,
        experienceLevel: str,
        currentRole: str,
        company: str,
        skills: str,
        decision: str,
        shortSummary: str,
        detailedSummary: str,
        mode: str,
        interviewer: str,
        reviewDate: datetime,
        age: int,
        status: str,
        currentCTC: str,
        expectedCTC: str,
        followUpNotes: str,
        scoreTech: int,
        scoreProblemSolving: int,
        scoreCommunication: int,
        scoreSystemDesign: int,
        scoreCultureFit: int,
        scoreRedFlags: int,
        strengths: str,
        weaknesses: str,
        _id: Optional[ObjectId] = None,
        createdAt: Optional[datetime] = None
    ):
        self._id = _id or ObjectId()
        self.fullName = fullName
        self.appliedRole = appliedRole
        self.interviewDate = interviewDate
        self.interviewDuration = interviewDuration
        self.previousRejections = previousRejections
        self.experienceLevel = experienceLevel
        self.currentRole = currentRole
        self.company = company
        self.skills = skills
        self.decision = decision
        self.shortSummary = shortSummary
        self.detailedSummary = detailedSummary
        self.mode = mode
        self.interviewer = interviewer
        self.reviewDate = reviewDate
        self.age = age
        self.status = status
        self.currentCTC = currentCTC
        self.expectedCTC = expectedCTC
        self.followUpNotes = followUpNotes
        self.scoreTech = scoreTech
        self.scoreProblemSolving = scoreProblemSolving
        self.scoreCommunication = scoreCommunication
        self.scoreSystemDesign = scoreSystemDesign
        self.scoreCultureFit = scoreCultureFit
        self.scoreRedFlags = scoreRedFlags
        self.strengths = strengths
        self.weaknesses = weaknesses
        self.createdAt = createdAt or datetime.utcnow()
    
    def to_dict(self) -> dict:
        
        return {
            "_id": self._id,
            "fullName": self.fullName,
            "appliedRole": self.appliedRole,
            "interviewDate": self.interviewDate,
            "interviewDuration": self.interviewDuration,
            "previousRejections": self.previousRejections,
            "experienceLevel": self.experienceLevel,
            "currentRole": self.currentRole,
            "company": self.company,
            "skills": self.skills,
            "decision": self.decision,
            "shortSummary": self.shortSummary,
            "detailedSummary": self.detailedSummary,
            "mode": self.mode,
            "interviewer": self.interviewer,
            "reviewDate": self.reviewDate,
            "age": self.age,
            "status": self.status,
            "currentCTC": self.currentCTC,
            "expectedCTC": self.expectedCTC,
            "followUpNotes": self.followUpNotes,
            "scoreTech": self.scoreTech,
            "scoreProblemSolving": self.scoreProblemSolving,
            "scoreCommunication": self.scoreCommunication,
            "scoreSystemDesign": self.scoreSystemDesign,
            "scoreCultureFit": self.scoreCultureFit,
            "scoreRedFlags": self.scoreRedFlags,
            "strengths": self.strengths,
            "weaknesses": self.weaknesses,
            "createdAt": self.createdAt
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Result':
        
        return Result(
            _id=data.get("_id"),
            fullName=data["fullName"],
            appliedRole=data["appliedRole"],
            interviewDate=data["interviewDate"],
            interviewDuration=data["interviewDuration"],
            previousRejections=data["previousRejections"],
            experienceLevel=data["experienceLevel"],
            currentRole=data["currentRole"],
            company=data["company"],
            skills=data["skills"],
            decision=data["decision"],
            shortSummary=data["shortSummary"],
            detailedSummary=data["detailedSummary"],
            mode=data["mode"],
            interviewer=data["interviewer"],
            reviewDate=data["reviewDate"],
            age=data["age"],
            status=data["status"],
            currentCTC=data["currentCTC"],
            expectedCTC=data["expectedCTC"],
            followUpNotes=data["followUpNotes"],
            scoreTech=data["scoreTech"],
            scoreProblemSolving=data["scoreProblemSolving"],
            scoreCommunication=data["scoreCommunication"],
            scoreSystemDesign=data["scoreSystemDesign"],
            scoreCultureFit=data["scoreCultureFit"],
            scoreRedFlags=data["scoreRedFlags"],
            strengths=data["strengths"],
            weaknesses=data["weaknesses"],
            createdAt=data.get("createdAt")
        )
