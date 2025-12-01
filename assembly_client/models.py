from dataclasses import asdict, dataclass
from typing import List


@dataclass
class APIParameter:
    """Represents a single API parameter."""

    name: str
    type: str
    required: bool
    description: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "APIParameter":
        return cls(**data)


@dataclass
class APISpec:
    """Represents a parsed API specification."""

    service_id: str
    endpoint: str
    endpoint_url: str
    basic_params: List[APIParameter]
    request_params: List[APIParameter]

    def to_dict(self) -> dict:
        return {
            "service_id": self.service_id,
            "endpoint": self.endpoint,
            "endpoint_url": self.endpoint_url,
            "basic_params": [p.to_dict() for p in self.basic_params],
            "request_params": [p.to_dict() for p in self.request_params],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "APISpec":
        return cls(
            service_id=data["service_id"],
            endpoint=data["endpoint"],
            endpoint_url=data["endpoint_url"],
            basic_params=[APIParameter.from_dict(p) for p in data["basic_params"]],
            request_params=[APIParameter.from_dict(p) for p in data["request_params"]],
        )
