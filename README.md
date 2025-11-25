# Assembly API Client (국회 오픈 API 클라이언트)

대한민국 국회 오픈 API(Open API)를 위한 강력하고 유연한 비동기 Python 클라이언트입니다.

## 주요 기능 (Features)

- **동적 스펙 파싱 (Dynamic Spec Parsing)**: 엑셀 명세서를 자동으로 다운로드하고 파싱하여 API 엔드포인트를 동적으로 해결합니다.
- **타입 안정성 (Type Safety)**: Pydantic 모델을 사용하여 데이터 타입을 검증하고 자동 완성 기능을 제공합니다. API의 불규칙한 데이터 타입(문자열/숫자 혼용)에도 유연하게 대응합니다.
- **강력한 복원력 (Resilience)**: 내장된 재시도(Retry) 로직과 에러 핸들링으로 안정적인 데이터 수집이 가능합니다.
- **자동화된 업데이트 (Automated Updates)**: 매주 자동으로 최신 API 명세를 동기화하고 코드를 재생성하는 CI/CD 파이프라인이 포함되어 있습니다.
- **CLI 도구**: API 명세 동기화 및 검색을 위한 커맨드라인 도구를 제공합니다.

## 설치 (Installation)

```bash
pip install assembly-api-client
```

## 사용법 (Usage)

### 기본 데이터 조회

```python
import asyncio
from assembly_client.api import AssemblyAPIClient
from assembly_client.generated import Service

async def main():
    # API 키는 환경 변수 ASSEMBLY_API_KEY로 설정하거나 직접 전달할 수 있습니다.
    async with AssemblyAPIClient(api_key="YOUR_API_KEY") as client:
        
        # 서비스 ID 또는 Enum을 사용하여 데이터 조회
        # 예: 국회의원 발의법률안 조회
        data = await client.get_data(Service.국회의원_발의법률안, params={"AGE": "21"})
        
        for item in data:
            print(f"법안명: {item.BILL_NAME}, 발의자: {item.PROPOSER}")

if __name__ == "__main__":
    asyncio.run(main())
```

### CLI 사용

API 명세 동기화:
```bash
python -m assembly_client.cli sync
```

사용 가능한 API 목록 조회:
```bash
python -m assembly_client.cli list
```

## 개발 및 기여 (Development)

### 테스트 실행
```bash
pytest
```

### 코드 재생성 (수동)
```bash
./scripts/update_client.sh
```

## 라이선스 (License)

MIT License
