from pydantic import BaseModel, Field
from typing import Optional, Union

class Model_OOBAOA001213RL17443(BaseModel):
    """Response model for OOBAOA001213RL17443"""
    INF_ID: Union[str, int, float, None] = Field(None, description="공공데이터ID", alias="INF_ID")
    INF_NM: Union[str, int, float, None] = Field(None, description="공공데이터명", alias="INF_NM")
    INF_EXP: Union[str, int, float, None] = Field(None, description="공공데이터설명", alias="INF_EXP")
    CATE_NM: Union[str, int, float, None] = Field(None, description="분류체계", alias="CATE_NM")
    OPEN_DTTM: Union[str, int, float, None] = Field(None, description="공개일자", alias="OPEN_DTTM")
    ORG_NM: Union[str, int, float, None] = Field(None, description="제공기관", alias="ORG_NM")
    LOAD_DTTM: Union[str, int, float, None] = Field(None, description="최종수정일자", alias="LOAD_DTTM")
    SRC_EXP: Union[str, int, float, None] = Field(None, description="원본시스템", alias="SRC_EXP")
    DDC_URL: Union[str, int, float, None] = Field(None, description="명세서URL", alias="DDC_URL")
    SRV_URL: Union[str, int, float, None] = Field(None, description="서비스URL", alias="SRV_URL")
    CCL_NM: Union[str, int, float, None] = Field(None, description="이용허락조건", alias="CCL_NM")
    LOAD_NM: Union[str, int, float, None] = Field(None, description="공개주기", alias="LOAD_NM")
    LOAD_CONT: Union[str, int, float, None] = Field(None, description="공개시기", alias="LOAD_CONT")

class Params_OOBAOA001213RL17443(BaseModel):
    """Request parameters for OOBAOA001213RL17443"""
    INF_ID: str | None = Field(None, description="공공데이터ID", alias="INF_ID")
    INF_NM: str | None = Field(None, description="공공데이터명", alias="INF_NM")
    SRC_EXP: str | None = Field(None, description="원본시스템", alias="SRC_EXP")
