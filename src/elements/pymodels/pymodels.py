import json
from typing import Optional, Union

from pydantic import BaseModel, Field
import pandas as pd
class Evaluation(BaseModel):
    date: str = Field(None)
    user_name: str = Field(None)
    feedback_type: str = Field(None)
    response_type: str = Field(None)
    reason: Union[str, int] = Field(None)
    question: Union[str, int] = Field(None)
    answer: str = Field(None)
    trace: str = Field(None)
    session_id: int = Field(None, alias="session id")
    chat_id: int = Field(None, alias="chat id")
    history_qa: str = Field(None, alias="history qa")
    remark: str = Field(None)
    grass_date: str = Field(None)

df = pd.read_excel("badcase.xlsx", sheet_name=0)
# Convert Timestamp to string
df['date'] = df['date'].astype(str)
df['grass_date'] = df['grass_date'].astype(str)

VOCABULARY_DATA = [Evaluation(**row.dropna().to_dict()) for _, row in df.iterrows()]
print(VOCABULARY_DATA[-2])
    

# print(json.loads(VOCABULARY_DATA[3].history_qa))