from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 환경변수에서 키 가져오기
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# 1️⃣ 문서 텍스트 로드
with open("doc_text.txt", "r", encoding="utf-8") as f:
    doc_text = f.read()

# 2️⃣ 입력값 (실제 채워넣을 데이터)
fill_data = {
    "성명": "김민수",
    "소속": "(주)에스티이노베이션",
    "직책": "현장조사원",
    "연령": "29세",
    "전문분야": "데이터 기반 사회조사",
    "해당분야근무경력": "4년 6개월",
    "보유자격증": "사회조사분석사 2급",
    "본 사업 참여임무": "표본 추출 및 현장 데이터 검증",
    "본 사업 참여기간": "2025.10.01~2025.10.31",
    "휴대전화": "010-1234-5678",
}

# 3️⃣ Few-shot 예시 (LLM에게 학습할 문맥형 패턴)
few_shot_example = """
예시 1
입력:
참여인력 이력사항

성명
소속
직책
연령
전문분야
해당분야근무경력
보유자격증
본 사업 참여임무
본 사업 참여기간
휴대전화

출력:
참여인력 이력사항

성명 : 홍길동
소속 : (주)에스티이노베이션
직책 : 조사원
연령 : 32세
전문분야 : 사회조사
해당분야근무경력 : 5년 2개월
보유자격증 : 사회조사분석사 2급
본 사업 참여임무 : 현장조사
본 사업 참여기간 : 2025.10.01~2025.10.31
"""

# 4️⃣ 프롬프트 구성
prompt = f"""
아래는 한글 문서에서 추출된 표 형태의 텍스트입니다.
항목 이름 뒤에 알맞은 값을 채워 넣어 완성된 형태로 만들어주세요.
⚠️ 단, 입력 문서에 존재하지 않는 항목은 출력하지 마세요.

{few_shot_example}

문서:
{doc_text}

입력값:
{fill_data}

출력은 완성된 문서 텍스트 형태로만 주세요.
"""

# 5️⃣ LLM 호출
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "너는 문서 자동입력 보조 AI야. 줄바꿈 구조를 이해하고 항목 뒤에 값을 채워 넣어라."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.2,
)

# 6️⃣ 결과 저장
output_text = response.choices[0].message.content

# 결과 파일 저장 경로
output_path = "few_shot_after.txt"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(output_text)

print(f"✅ 완성된 문서 저장 완료 → {output_path}")