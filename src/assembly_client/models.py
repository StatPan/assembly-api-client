from pydantic import BaseModel, ConfigDict, Field


class Bill(BaseModel):
    """
    Bill Information Data Model.
    Integrates basic info, detailed content, and processing status.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "bill_id": "PRC_C0Y0T0T0M0X0A1F0H1P5V7G6R2Q5Z2",
                "bill_no": "2100001",
                "bill_name": "국가재정법 일부개정법률안",
                "proposer": "홍길동",
                "proposer_kind_name": "의원",
                "proc_status": "위원회 심사",
                "committee": "기획재정위원회",
                "propose_dt": "2020-05-30",
                "committee_dt": "2020-06-01",
                "proc_dt": None,
                "link_url": "http://likms.assembly.go.kr/bill/billDetail.do?billId=PRC_C0Y0T0T0M0X0A1F0H1P5V7G6R2Q5Z2",
            }
        },
    )

    bill_id: str = Field(..., description="Bill ID (BILL_ID). Unique identifier.")
    bill_no: str | None = Field(None, description="Bill Number (BILL_NO).")
    bill_name: str = Field(..., description="Bill Name (BILL_NAME).")
    proposer: str = Field(..., description="Representative Proposer (PROPOSER). Member or Committee name.")
    proposer_text: str | None = Field(None, description="Original proposer text (e.g., 'Hong Gil-dong and 10 others').")
    primary_proposer: str | None = Field(None, description="Extracted primary proposer name.")
    proposer_count: int | None = Field(None, description="Total number of proposers (derived).")
    proposer_kind_name: str = Field(..., description="Proposer Kind (PROPOSER_KIND). 'Member' or 'Committee'.")
    proc_status: str = Field(..., description="Processing Status (PROC_STATUS). Current stage.")
    committee: str = Field(..., description="Committee Name (COMMITTEE).")
    propose_dt: str | None = Field(None, description="Propose Date (PROPOSE_DT). YYYY-MM-DD.")
    committee_dt: str | None = Field(None, description="Committee Referral Date (COMMITTEE_DT). YYYY-MM-DD.")
    proc_dt: str | None = Field(None, description="Final Process Date (PROC_DT). YYYY-MM-DD.")
    link_url: str = Field(..., description="Detail Link URL (LINK_URL).")


class BillDetail(Bill):
    """
    Detailed Bill Information.
    Adds summary and reason to the basic Bill model.
    """

    summary: str | None = Field(None, description="Major Content (MAJOR_CONTENT). Summary of the bill.")
    reason: str | None = Field(None, description="Propose Reason (PROPOSE_REASON).")


class Committee(BaseModel):
    """
    Committee Information Data Model.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "committee_code": "9700008",
                "committee_name": "Legislation and Judiciary Committee",
                "committee_div": "Standing Committee",
                "chairperson": "Park Kwang-on",
                "member_count": 18,
                "limit_count": 18,
            }
        }
    )

    committee_code: str = Field(..., description="Committee Code (HR_DEPT_CD).")
    committee_name: str = Field(..., description="Committee Name (COMMITTEE_NAME).")
    committee_div: str | None = Field(None, description="Committee Division (CMT_DIV_NM). e.g., Standing Committee.")
    chairperson: str | None = Field(None, description="Chairperson (HG_NM).")
    member_count: int | None = Field(None, description="Current Members (CURR_CNT).")
    limit_count: int | None = Field(None, description="Limit Count (LIMIT_CNT).")


class Member(BaseModel):
    """
    Member Information Data Model.
    """

    member_seq: str = Field(..., description="Member Sequence (HG_NM). Unique ID.")
    name: str = Field(..., description="Member Name (HG_NM).")
    party: str | None = Field(None, description="Political Party (POLY_NM).")
    committee: str | None = Field(None, description="Committee (CMIT_NM).")
    region: str | None = Field(None, description="Region (ORIG_NM).")
    gender: str | None = Field(None, description="Gender (SEX_GBN_NM).")
    elected_count: str | None = Field(None, description="Elected Count (REELE_GBN_NM).")
    units: str | None = Field(None, description="Units (UNITS).")
