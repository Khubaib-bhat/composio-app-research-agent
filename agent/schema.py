from pydantic import BaseModel, Field
from typing import List, Literal

class Evidence(BaseModel):
    url: str
    claim: str
    snippet: str = ""
    source_type: Literal["official_docs", "official_pricing", "official_mcp", "official_blog", "other"] = "official_docs"

class AppResearch(BaseModel):
    app: str
    category: str
    description: str
    auth_methods: List[str] = Field(default_factory=list)
    credential_access: Literal["self_serve", "trial", "paid_gated", "admin_gated", "partner_gated", "unknown"]
    api_type: List[str] = Field(default_factory=list)
    api_breadth: Literal["broad", "moderate", "narrow", "unknown"]
    existing_mcp: Literal["official", "community", "none_found", "unknown"]
    buildability: Literal["high", "medium", "low", "unknown"]
    blocker: str = ""
    confidence: float = Field(ge=0, le=1)
    evidence: List[Evidence] = Field(default_factory=list)
    notes: str = ""
