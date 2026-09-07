from typing import Literal
from pydantic import BaseModel, Field
Language = Literal["hi", "en", "hinglish"]
RiskLevel = Literal["Low Risk", "Moderate Risk", "High Risk", "Emergency"]
class AssessmentIn(BaseModel):
    patient_name: str = Field(min_length=1, max_length=80)
    age: int = Field(ge=0, le=120)
    gender: str = "prefer_not_to_say"
    symptoms: str = Field(min_length=1, max_length=5000)
    duration: str = Field(default="unknown", max_length=120)
    severity: int = Field(ge=1, le=10)
    temperature_c: float | None = Field(default=None, ge=30, le=45)
    conditions: str = Field(default="", max_length=2000)
    medicines: str = Field(default="", max_length=2000)
    allergies: str = Field(default="", max_length=2000)
    pregnancy_status: str = Field(default="not_applicable", max_length=80)
    previous_similar: str = Field(default="", max_length=1000)
    language: Language = "hinglish"
    image_attached: bool = False
class Analysis(BaseModel):
    summary: str
    possible_conditions: list[str] = Field(default_factory=list, max_length=4)
    risk_level: RiskLevel
    red_flags: list[str] = Field(default_factory=list)
    recommended_action: str
    self_care: list[str] = Field(default_factory=list)
    otc_information: list[str] = Field(default_factory=list)
    doctor_required: bool
    emergency: bool
    follow_up_questions: list[str] = Field(default_factory=list)
    safety_note: str
class ChatIn(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    language: Language = "hinglish"
class RegisterIn(BaseModel):
    email: str = Field(min_length=5, max_length=200)
    password: str = Field(min_length=8, max_length=128)
class LoginIn(RegisterIn): pass
