from pydantic import BaseModel,Field
from typing import Literal
class AuthIn(BaseModel):
    email:str=Field(min_length=5,max_length=160); password:str=Field(min_length=8,max_length=128)
class TokenOut(BaseModel):
    access_token:str; token_type:str="bearer"
class AssessmentIn(BaseModel):
    patient_name:str=Field(min_length=1,max_length=80); age:int=Field(ge=0,le=120); gender:str="prefer_not_to_say"; symptoms:str=Field(min_length=1,max_length=5000); duration:str="unknown"; severity:int=Field(ge=1,le=10); temperature_c:float|None=Field(default=None,ge=30,le=45); conditions:str=""; medicines:str=""; allergies:str=""; pregnancy_status:str="not_applicable"; previous_similar:str=""; language:Literal["hi","en","hinglish"]="hinglish"; image_attached:bool=False
class ChatIn(BaseModel):
    message:str=Field(min_length=1,max_length=4000); language:Literal["hi","en","hinglish"]="hinglish"; context:str=Field(default="",max_length=5000)
class Analysis(BaseModel):
    summary:str; possible_conditions:list[str]; risk_level:Literal["Low Risk","Moderate Risk","High Risk","Emergency"]; red_flags:list[str]; recommended_action:str; self_care:list[str]; otc_information:list[str]; doctor_required:bool; emergency:bool; follow_up_questions:list[str]; safety_note:str
