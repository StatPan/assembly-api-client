from pydantic import BaseModel, Field
from typing import Optional, Union

class Model_OWSSC6001134T516707(BaseModel):
    """Response model for OWSSC6001134T516707"""
    HG_NM: Union[str, int, float, None] = Field(None, description="이름", alias="HG_NM")
    HJ_NM: Union[str, int, float, None] = Field(None, description="한자명", alias="HJ_NM")
    ENG_NM: Union[str, int, float, None] = Field(None, description="영문명칭", alias="ENG_NM")
    BTH_GBN_NM: Union[str, int, float, None] = Field(None, description="음/양력", alias="BTH_GBN_NM")
    BTH_DATE: Union[str, int, float, None] = Field(None, description="생년월일", alias="BTH_DATE")
    JOB_RES_NM: Union[str, int, float, None] = Field(None, description="직책명", alias="JOB_RES_NM")
    POLY_NM: Union[str, int, float, None] = Field(None, description="정당명", alias="POLY_NM")
    ORIG_NM: Union[str, int, float, None] = Field(None, description="선거구", alias="ORIG_NM")
    ELECT_GBN_NM: Union[str, int, float, None] = Field(None, description="선거구구분", alias="ELECT_GBN_NM")
    CMIT_NM: Union[str, int, float, None] = Field(None, description="대표 위원회", alias="CMIT_NM")
    CMITS: Union[str, int, float, None] = Field(None, description="소속 위원회 목록", alias="CMITS")
    REELE_GBN_NM: Union[str, int, float, None] = Field(None, description="재선", alias="REELE_GBN_NM")
    UNITS: Union[str, int, float, None] = Field(None, description="당선", alias="UNITS")
    SEX_GBN_NM: Union[str, int, float, None] = Field(None, description="성별", alias="SEX_GBN_NM")
    TEL_NO: Union[str, int, float, None] = Field(None, description="전화번호", alias="TEL_NO")
    E_MAIL: Union[str, int, float, None] = Field(None, description="이메일", alias="E_MAIL")
    HOMEPAGE: Union[str, int, float, None] = Field(None, description="홈페이지", alias="HOMEPAGE")
    STAFF: Union[str, int, float, None] = Field(None, description="보좌관", alias="STAFF")
    SECRETARY: Union[str, int, float, None] = Field(None, description="선임비서관", alias="SECRETARY")
    SECRETARY2: Union[str, int, float, None] = Field(None, description="비서관", alias="SECRETARY2")
    MONA_CD: Union[str, int, float, None] = Field(None, description="국회의원코드", alias="MONA_CD")
    MEM_TITLE: Union[str, int, float, None] = Field(None, description="약력", alias="MEM_TITLE")
    ASSEM_ADDR: Union[str, int, float, None] = Field(None, description="사무실 호실", alias="ASSEM_ADDR")

class Params_OWSSC6001134T516707(BaseModel):
    """Request parameters for OWSSC6001134T516707"""
    HG_NM: str | None = Field(None, description="이름", alias="HG_NM")
    POLY_NM: str | None = Field(None, description="정당명", alias="POLY_NM")
    ORIG_NM: str | None = Field(None, description="선거구", alias="ORIG_NM")
    CMITS: str | None = Field(None, description="소속 위원회 목록", alias="CMITS")
    SEX_GBN_NM: str | None = Field(None, description="성별", alias="SEX_GBN_NM")
    MONA_CD: str | None = Field(None, description="국회의원코드", alias="MONA_CD")

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

class Model_O5MSQF0009823A15643(BaseModel):
    """Response model for O5MSQF0009823A15643"""
    V_TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="V_TITLE")
    URL_LINK: Union[str, int, float, None] = Field(None, description="기사 URL", alias="URL_LINK")
    DATE_LASTMODIFIED: Union[str, int, float, None] = Field(None, description="최종수정일", alias="DATE_LASTMODIFIED")
    DATE_RELEASED: Union[str, int, float, None] = Field(None, description="기사작성일", alias="DATE_RELEASED")
    V_BODY: Union[str, int, float, None] = Field(None, description="기사내용", alias="V_BODY")

class Params_O5MSQF0009823A15643(BaseModel):
    """Request parameters for O5MSQF0009823A15643"""
    V_TITLE: str | None = Field(None, description="제목", alias="V_TITLE")

class Model_OB5IBW001180FQ10640(BaseModel):
    """Response model for OB5IBW001180FQ10640"""
    REG_DATE: Union[str, int, float, None] = Field(None, description="발간일", alias="REG_DATE")
    DEPARTMENT_NAME: Union[str, int, float, None] = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: Union[str, int, float, None] = Field(None, description="보고서명", alias="SUBJECT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크 주소", alias="LINK_URL")

class Params_OB5IBW001180FQ10640(BaseModel):
    """Request parameters for OB5IBW001180FQ10640"""
    DEPARTMENT_NAME: str | None = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: str | None = Field(None, description="보고서명", alias="SUBJECT")

class Model_ORNDP7000993P115502(BaseModel):
    """Response model for ORNDP7000993P115502"""
    HG_NM: Union[str, int, float, None] = Field(None, description="의원이름(한글)", alias="HG_NM")
    HJ_NM: Union[str, int, float, None] = Field(None, description="의원이름(한자)", alias="HJ_NM")
    FRTO_DATE: Union[str, int, float, None] = Field(None, description="활동기간", alias="FRTO_DATE")
    PROFILE_SJ: Union[str, int, float, None] = Field(None, description="위원회 경력", alias="PROFILE_SJ")
    MONA_CD: Union[str, int, float, None] = Field(None, description="국회의원코드", alias="MONA_CD")
    PROFILE_UNIT_CD: Union[str, int, float, None] = Field(None, description="경력대수코드", alias="PROFILE_UNIT_CD")
    PROFILE_UNIT_NM: Union[str, int, float, None] = Field(None, description="경력대수", alias="PROFILE_UNIT_NM")

class Params_ORNDP7000993P115502(BaseModel):
    """Request parameters for ORNDP7000993P115502"""
    HG_NM: str | None = Field(None, description="의원이름(한글)", alias="HG_NM")
    PROFILE_SJ: str | None = Field(None, description="위원회 경력", alias="PROFILE_SJ")
    MONA_CD: str | None = Field(None, description="국회의원코드", alias="MONA_CD")
    PROFILE_UNIT_CD: str | None = Field(None, description="경력대수코드", alias="PROFILE_UNIT_CD")

class Model_OND1KZ0009677M13515(BaseModel):
    """Response model for OND1KZ0009677M13515"""
    BILL_ID: Union[str, int, float, None] = Field(None, description="의안ID", alias="BILL_ID")
    PROC_DT: Union[str, int, float, None] = Field(None, description="처리일", alias="PROC_DT")
    BILL_NO: Union[str, int, float, None] = Field(None, description="의안번호", alias="BILL_NO")
    BILL_NAME: Union[str, int, float, None] = Field(None, description="의안명", alias="BILL_NAME")
    CURR_COMMITTEE: Union[str, int, float, None] = Field(None, description="소관위", alias="CURR_COMMITTEE")
    CURR_COMMITTEE_ID: Union[str, int, float, None] = Field(None, description="소관위코드", alias="CURR_COMMITTEE_ID")
    PROC_RESULT_CD: Union[str, int, float, None] = Field(None, description="표결결과", alias="PROC_RESULT_CD")
    BILL_KIND_CD: Union[str, int, float, None] = Field(None, description="의안종류", alias="BILL_KIND_CD")
    AGE: Union[str, int, float, None] = Field(None, description="대수", alias="AGE")
    MEMBER_TCNT: Union[str, int, float, None] = Field(None, description="재적의원", alias="MEMBER_TCNT")
    VOTE_TCNT: Union[str, int, float, None] = Field(None, description="총투표수", alias="VOTE_TCNT")
    YES_TCNT: Union[str, int, float, None] = Field(None, description="찬성", alias="YES_TCNT")
    NO_TCNT: Union[str, int, float, None] = Field(None, description="반대", alias="NO_TCNT")
    BLANK_TCNT: Union[str, int, float, None] = Field(None, description="기권", alias="BLANK_TCNT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="의안상세정보 URL", alias="LINK_URL")

class Params_OND1KZ0009677M13515(BaseModel):
    """Request parameters for OND1KZ0009677M13515"""
    BILL_ID: str | None = Field(None, description="의안ID", alias="BILL_ID")
    BILL_NO: str | None = Field(None, description="의안번호", alias="BILL_NO")
    BILL_NAME: str | None = Field(None, description="의안명", alias="BILL_NAME")
    CURR_COMMITTEE: str | None = Field(None, description="소관위", alias="CURR_COMMITTEE")
    CURR_COMMITTEE_ID: str | None = Field(None, description="소관위코드", alias="CURR_COMMITTEE_ID")
    PROC_RESULT_CD: str | None = Field(None, description="표결결과", alias="PROC_RESULT_CD")
    BILL_KIND_CD: str | None = Field(None, description="의안종류", alias="BILL_KIND_CD")
    AGE: str = Field(..., description="대수", alias="AGE")

class Model_O4K6HM0012064I15889(BaseModel):
    """Response model for O4K6HM0012064I15889"""
    BILL_ID: Union[str, int, float, None] = Field(None, description="의안ID", alias="BILL_ID")
    BILL_NO: Union[str, int, float, None] = Field(None, description="의안번호", alias="BILL_NO")
    AGE: Union[str, int, float, None] = Field(None, description="대", alias="AGE")
    BILL_NAME: Union[str, int, float, None] = Field(None, description="의안명(한글)", alias="BILL_NAME")
    PROPOSER: Union[str, int, float, None] = Field(None, description="제안자", alias="PROPOSER")
    PROPOSER_KIND: Union[str, int, float, None] = Field(None, description="제안자구분", alias="PROPOSER_KIND")
    PROPOSE_DT: Union[str, int, float, None] = Field(None, description="제안일", alias="PROPOSE_DT")
    CURR_COMMITTEE_ID: Union[str, int, float, None] = Field(None, description="소관위코드", alias="CURR_COMMITTEE_ID")
    CURR_COMMITTEE: Union[str, int, float, None] = Field(None, description="소관위", alias="CURR_COMMITTEE")
    COMMITTEE_DT: Union[str, int, float, None] = Field(None, description="소관위회부일", alias="COMMITTEE_DT")
    COMMITTEE_PROC_DT: Union[str, int, float, None] = Field(None, description="위원회심사_처리일", alias="COMMITTEE_PROC_DT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="의안상세정보_URL", alias="LINK_URL")
    RST_PROPOSER: Union[str, int, float, None] = Field(None, description="대표발의자", alias="RST_PROPOSER")
    LAW_PROC_RESULT_CD: Union[str, int, float, None] = Field(None, description="법사위처리결과", alias="LAW_PROC_RESULT_CD")
    LAW_PROC_DT: Union[str, int, float, None] = Field(None, description="법사위처리일", alias="LAW_PROC_DT")
    LAW_PRESENT_DT: Union[str, int, float, None] = Field(None, description="법사위상정일", alias="LAW_PRESENT_DT")
    LAW_SUBMIT_DT: Union[str, int, float, None] = Field(None, description="법사위회부일", alias="LAW_SUBMIT_DT")
    CMT_PROC_RESULT_CD: Union[str, int, float, None] = Field(None, description="소관위처리결과", alias="CMT_PROC_RESULT_CD")
    CMT_PROC_DT: Union[str, int, float, None] = Field(None, description="소관위처리일", alias="CMT_PROC_DT")
    CMT_PRESENT_DT: Union[str, int, float, None] = Field(None, description="소관위상정일", alias="CMT_PRESENT_DT")
    RST_MONA_CD: Union[str, int, float, None] = Field(None, description="대표발의자코드", alias="RST_MONA_CD")
    PROC_RESULT_CD: Union[str, int, float, None] = Field(None, description="본회의심의결과", alias="PROC_RESULT_CD")
    PROC_DT: Union[str, int, float, None] = Field(None, description="의결일", alias="PROC_DT")

class Params_O4K6HM0012064I15889(BaseModel):
    """Request parameters for O4K6HM0012064I15889"""
    BILL_ID: str | None = Field(None, description="의안ID", alias="BILL_ID")
    BILL_NO: str | None = Field(None, description="의안번호", alias="BILL_NO")
    AGE: str = Field(..., description="대", alias="AGE")
    BILL_NAME: str | None = Field(None, description="의안명(한글)", alias="BILL_NAME")
    PROPOSER: str | None = Field(None, description="제안자", alias="PROPOSER")
    PROPOSER_KIND: str | None = Field(None, description="제안자구분", alias="PROPOSER_KIND")
    CURR_COMMITTEE_ID: str | None = Field(None, description="소관위코드", alias="CURR_COMMITTEE_ID")
    CURR_COMMITTEE: str | None = Field(None, description="소관위", alias="CURR_COMMITTEE")
    PROC_DT: str | None = Field(None, description="의결일", alias="PROC_DT")
    PROC_RESULT_CD: str | None = Field(None, description="본회의심의결과", alias="PROC_RESULT_CD")
    BILL_ID_REF: str | None = Field(None, description="참조의안코드", alias="BILL_ID_REF")

class Model_OPR1MQ000998LC12535(BaseModel):
    """Response model for OPR1MQ000998LC12535"""
    HG_NM: Union[str, int, float, None] = Field(None, description="의원", alias="HG_NM")
    HJ_NM: Union[str, int, float, None] = Field(None, description="한자명", alias="HJ_NM")
    POLY_NM: Union[str, int, float, None] = Field(None, description="정당", alias="POLY_NM")
    ORIG_NM: Union[str, int, float, None] = Field(None, description="선거구", alias="ORIG_NM")
    MEMBER_NO: Union[str, int, float, None] = Field(None, description="의원번호", alias="MEMBER_NO")
    POLY_CD: Union[str, int, float, None] = Field(None, description="소속정당코드", alias="POLY_CD")
    ORIG_CD: Union[str, int, float, None] = Field(None, description="선거구코드", alias="ORIG_CD")
    VOTE_DATE: Union[str, int, float, None] = Field(None, description="의결일자", alias="VOTE_DATE")
    BILL_NO: Union[str, int, float, None] = Field(None, description="의안번호", alias="BILL_NO")
    BILL_NAME: Union[str, int, float, None] = Field(None, description="의안명", alias="BILL_NAME")
    BILL_ID: Union[str, int, float, None] = Field(None, description="의안ID", alias="BILL_ID")
    LAW_TITLE: Union[str, int, float, None] = Field(None, description="법률명", alias="LAW_TITLE")
    CURR_COMMITTEE: Union[str, int, float, None] = Field(None, description="소관위원회", alias="CURR_COMMITTEE")
    RESULT_VOTE_MOD: Union[str, int, float, None] = Field(None, description="표결결과", alias="RESULT_VOTE_MOD")
    DEPT_CD: Union[str, int, float, None] = Field(None, description="부서코드(사용안함)", alias="DEPT_CD")
    CURR_COMMITTEE_ID: Union[str, int, float, None] = Field(None, description="소관위코드", alias="CURR_COMMITTEE_ID")
    DISP_ORDER: Union[str, int, float, None] = Field(None, description="표시정렬순서", alias="DISP_ORDER")
    BILL_URL: Union[str, int, float, None] = Field(None, description="의안URL", alias="BILL_URL")
    BILL_NAME_URL: Union[str, int, float, None] = Field(None, description="의안링크", alias="BILL_NAME_URL")
    SESSION_CD: Union[str, int, float, None] = Field(None, description="회기", alias="SESSION_CD")
    CURRENTS_CD: Union[str, int, float, None] = Field(None, description="차수", alias="CURRENTS_CD")
    AGE: Union[str, int, float, None] = Field(None, description="대", alias="AGE")
    MONA_CD: Union[str, int, float, None] = Field(None, description="국회의원코드", alias="MONA_CD")

class Params_OPR1MQ000998LC12535(BaseModel):
    """Request parameters for OPR1MQ000998LC12535"""
    HG_NM: str | None = Field(None, description="의원", alias="HG_NM")
    POLY_NM: str | None = Field(None, description="정당", alias="POLY_NM")
    MEMBER_NO: str | None = Field(None, description="의원번호", alias="MEMBER_NO")
    VOTE_DATE: str | None = Field(None, description="의결일자", alias="VOTE_DATE")
    BILL_NO: str | None = Field(None, description="의안번호", alias="BILL_NO")
    BILL_NAME: str | None = Field(None, description="의안명", alias="BILL_NAME")
    BILL_ID: str = Field(..., description="의안ID", alias="BILL_ID")
    CURR_COMMITTEE: str | None = Field(None, description="소관위원회", alias="CURR_COMMITTEE")
    RESULT_VOTE_MOD: str | None = Field(None, description="표결결과", alias="RESULT_VOTE_MOD")
    CURR_COMMITTEE_ID: str | None = Field(None, description="소관위코드", alias="CURR_COMMITTEE_ID")
    MONA_CD: str | None = Field(None, description="국회의원코드", alias="MONA_CD")
    AGE: str = Field(..., description="대", alias="AGE")
