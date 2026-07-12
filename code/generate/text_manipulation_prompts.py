"""
멀티모달 한국어 가짜뉴스 탐지 연구
텍스트 조작 수준별 프롬프트 (LV1~LV5)

- LV1: 표현 조작 (단어/어조 변경)
- LV2: 맥락 조작 (정보 생략)
- LV3: 해석 조작 (감정/의도 추가)
- LV4: 증거 조작 (허위 정보 삽입)
- LV5: 생성 조작 (존재하지 않는 사건 생성)

[공통 규칙]
- 한국어 뉴스 기사 문체를 유지하세요.
- 기사 제목과 본문을 모두 수정하세요.
- 실존 인물에 대한 허위 범죄, 명예훼손은 절대 금지입니다.
"""

import json

# =============================================
# 공통 시스템 프롬프트
# =============================================

SYSTEM_PROMPT_KO = """
당신은 한국어 정치 뉴스 멀티모달 가짜뉴스 탐지 연구를 위한 데이터 생성 AI입니다.
아래 원본 뉴스를 지정된 조작 수준(Level)에 맞게 수정하세요.

[공통 규칙]
- 한국어 뉴스 기사 문체를 유지하세요.
- 기사 제목과 본문을 모두 수정하세요.
- 지정된 Level의 규칙만 적용하세요.
- Level에서 허용되지 않은 조작은 하지 마세요.
- 기사 길이는 원문과 비슷하게 유지하세요.
- 결과는 자연스럽고 실제 뉴스 기사처럼 작성하세요.
- 실존 인물에 대한 허위 범죄, 명예훼손은 절대 금지입니다.

[조작 규칙(JSON)]
{LEVEL_RULE}

[원본 기사]
{article}

출력 형식:
제목:
본문:
"""

SYSTEM_PROMPT_EN = """
You are a data generation AI for Korean political news multimodal fake news detection research.
Modify the original news article below according to the specified manipulation level.

[Common Rules]
- Maintain the Korean news article writing style.
- Modify both the article title and body.
- Apply only the rules of the specified Level.
- Do not perform manipulations not allowed in the Level.
- Keep the article length similar to the original.
- Write naturally to look like a real news article.
- NEVER create false crimes or defamation against real individuals.

[Manipulation Rules (JSON)]
{LEVEL_RULE}

[Original Article]
{article}

Output Format:
Title:
Body:
"""


# =============================================
# LV1: 표현 조작 (단어/어조 변경)
# =============================================

level_1_ko = {
    "level": "LV1",
    "name": "표현 조작 (단어/어조 변경)",
    "goal": "표현만 약간 자극적으로 변경하되 사실 관계는 완전히 유지",
    "constraints": [
        "사실 관계를 절대 변경하지 마십시오.",
        "원문과 거의 동일하게 보여야 합니다.",
        "자연스러운 뉴스 기사 문체를 유지하십시오."
    ],
    "strategies": {
        "strategy_1_word_substitution": (
            "중립적인 단어를 부정적 뉘앙스의 단어로 교체하십시오. "
            "예: '발표했다' → '주장했다', '정책' → '논란의 정책', '밝혔다' → '강변했다'"
        ),
        "strategy_2_tone_shift": (
            "문장의 어조를 객관적에서 비판적으로 전환하십시오. "
            "제목에 '논란', '의혹', '비판' 등의 표현을 추가하여 자극적으로 만드십시오."
        )
    },
    "allow": [
        "단어 선택 변경",
        "어조 변경",
        "제목 표현 강화",
        "부정적 뉘앙스 단어 교체"
    ],
    "forbid": [
        "사실 변경",
        "정보 삭제",
        "정보 추가",
        "허위 인용",
        "허위 통계",
        "새로운 사건 생성"
    ],
    "examples": {
        "before": "정부, 청년 지원 정책 발표",
        "after": "정부, 논란의 청년 지원 정책 강행"
    }
}

level_1_en = {
    "level": "LV1",
    "name": "Expression Manipulation (Word/Tone Change)",
    "goal": "Change only expressions to be slightly more provocative while completely maintaining facts",
    "constraints": [
        "NEVER change factual information.",
        "Should look almost identical to the original.",
        "Maintain natural news article writing style."
    ],
    "strategies": {
        "strategy_1_word_substitution": (
            "Replace neutral words with negatively nuanced words. "
            "Example: 'announced' → 'claimed', 'policy' → 'controversial policy'"
        ),
        "strategy_2_tone_shift": (
            "Shift the tone of sentences from objective to critical. "
            "Add expressions like 'controversy', 'suspicion', 'criticism' to make headlines more provocative."
        )
    },
    "allow": [
        "word choice change",
        "tone change",
        "headline expression strengthening",
        "negative nuance word replacement"
    ],
    "forbid": [
        "fact change",
        "information deletion",
        "information addition",
        "false quotation",
        "false statistics",
        "new event creation"
    ],
    "examples": {
        "before": "Government announces youth support policy",
        "after": "Government pushes controversial youth support policy"
    }
}

PROMPT_LV1_KO = (
    "다음 한국어 정치 뉴스 기사를 LV1 수준으로 조작해줘. "
    "사실 관계는 절대 바꾸지 말고, 단어 선택이나 어조만 살짝 부정적으로 바꿔. "
    "원본과 거의 똑같아 보여야 해. 제목과 본문 모두 수정해줘. "
    "결과는 자연스러운 뉴스 기사처럼 작성해줘. "
    "조작된 기사만 출력해. 다른 말은 하지 마."
)

PROMPT_LV1_EN = (
    "Manipulate the following Korean political news article to LV1 level. "
    "NEVER change factual information. Only slightly change word choice or tone to be more negative. "
    "It should look almost identical to the original. Modify both the title and body. "
    "Write the result naturally like a news article. "
    "Output only the manipulated article. Do not say anything else."
)


# =============================================
# LV2: 맥락 조작 (정보 생략)
# =============================================

level_2_ko = {
    "level": "LV2",
    "name": "맥락 조작 (정보 생략)",
    "goal": "일부 정보를 생략하여 맥락을 왜곡하되 새로운 정보는 추가하지 않음",
    "constraints": [
        "새로운 정보를 추가하지 마십시오.",
        "기존 사실의 일부를 선택적으로 제거하여 의미를 왜곡하십시오.",
        "겉으로 보면 진짜 기사처럼 보여야 합니다."
    ],
    "strategies": {
        "strategy_1_context_removal": (
            "긍정적인 맥락이나 조건절을 삭제하십시오. "
            "예: '성과가 있었지만 개선이 필요한 부분도 있다' → '개선이 필요한 부분이 있다'"
        ),
        "strategy_2_selective_emphasis": (
            "부정적인 부분만 선택적으로 강조하고 긍정적인 내용은 축소하십시오. "
            "발언의 일부만 인용하여 원래 의도와 다른 인상을 주십시오."
        )
    },
    "allow": [
        "조건 생략",
        "배경 설명 삭제",
        "발언 일부 생략",
        "특정 내용 강조",
        "긍정적 맥락 제거"
    ],
    "forbid": [
        "새로운 사건 생성",
        "허위 통계",
        "허위 인용",
        "새로운 인물 추가",
        "존재하지 않는 발언 추가"
    ],
    "examples": {
        "before": "정책 성과가 있었지만 개선이 필요한 부분도 존재한다.",
        "after": "개선이 필요한 부분이 존재한다."
    }
}

level_2_en = {
    "level": "LV2",
    "name": "Context Manipulation (Information Omission)",
    "goal": "Distort context by omitting some information without adding new information",
    "constraints": [
        "DO NOT add new information.",
        "Selectively remove parts of existing facts to distort meaning.",
        "Should look like a real article on the surface."
    ],
    "strategies": {
        "strategy_1_context_removal": (
            "Delete positive context or conditional clauses. "
            "Example: 'There were achievements but improvements are needed' → 'Improvements are needed'"
        ),
        "strategy_2_selective_emphasis": (
            "Selectively emphasize only negative parts and minimize positive content. "
            "Quote only part of statements to give a different impression from the original intent."
        )
    },
    "allow": [
        "condition omission",
        "background explanation deletion",
        "partial statement omission",
        "specific content emphasis",
        "positive context removal"
    ],
    "forbid": [
        "new event creation",
        "false statistics",
        "false quotation",
        "new character addition",
        "non-existent statement addition"
    ],
    "examples": {
        "before": "The policy had achievements but improvements are also needed.",
        "after": "Improvements are needed."
    }
}

PROMPT_LV2_KO = (
    "다음 한국어 정치 뉴스 기사를 LV2 수준으로 조작해줘. "
    "사실은 유지하되 긍정적인 내용은 삭제하거나 축소해. "
    "부정적인 부분만 선택적으로 강조해. 발언 일부를 생략해서 의미를 왜곡해. "
    "새로운 정보는 절대 추가하지 마. 겉으로 보면 진짜처럼 보여야 해. "
    "조작된 기사만 출력해. 다른 말은 하지 마."
)

PROMPT_LV2_EN = (
    "Manipulate the following Korean political news article to LV2 level. "
    "Maintain facts but delete or minimize positive content. "
    "Selectively emphasize only negative parts. Omit parts of statements to distort meaning. "
    "NEVER add new information. Should look real on the surface. "
    "Output only the manipulated article. Do not say anything else."
)


# =============================================
# LV3: 해석 조작 (감정/의도 추가)
# =============================================

level_3_ko = {
    "level": "LV3",
    "name": "해석 조작 (감정/의도 추가)",
    "goal": "원문에 없는 감정적 해석이나 의도를 추가하여 부정적 인상을 강화",
    "constraints": [
        "허위 통계나 출처는 추가하지 마십시오.",
        "기존 사실 기반 위에 해석을 추가하십시오.",
        "자연스러운 뉴스 기사 문체를 유지하십시오."
    ],
    "strategies": {
        "strategy_1_emotional_framing": (
            "원본에 없는 감정적 표현을 추가하십시오. "
            "예: '시민 분노 폭발', '당혹스러운 표정', '사실상 실패 인정'"
        ),
        "strategy_2_intent_speculation": (
            "인물의 의도나 동기를 부정적으로 추측하는 문장을 추가하십시오. "
            "예: '이는 책임 회피용 발언으로 해석된다', '정치적 계산이 깔린 발표로 보인다'"
        ),
        "strategy_3_negative_evaluation": (
            "'사실상', '논란', '의혹', '비판' 등의 표현을 삽입하여 "
            "독자가 부정적인 인상을 받도록 유도하십시오."
        )
    },
    "allow": [
        "감정 추가",
        "의도 추정",
        "평가 추가",
        "부정적 해석 삽입",
        "'사실상', '논란', '의혹' 등의 표현"
    ],
    "forbid": [
        "허위 통계",
        "허위 인용",
        "새로운 사건 생성",
        "존재하지 않는 인물 추가"
    ],
    "examples": {
        "before": "정책 발표 기자회견",
        "after": "논란의 정책 발표 기자회견 - 전문가들 '사실상 실패 인정' 비판"
    }
}

level_3_en = {
    "level": "LV3",
    "name": "Interpretation Manipulation (Emotion/Intent Addition)",
    "goal": "Strengthen negative impression by adding emotional interpretations or intentions not in the original",
    "constraints": [
        "DO NOT add false statistics or sources.",
        "Add interpretations on top of existing facts.",
        "Maintain natural news article writing style."
    ],
    "strategies": {
        "strategy_1_emotional_framing": (
            "Add emotional expressions not in the original. "
            "Example: 'Citizens explode in anger', 'embarrassed expression captured', 'virtually admitting failure'"
        ),
        "strategy_2_intent_speculation": (
            "Add sentences that negatively speculate on a person's intent or motivation. "
            "Example: 'This is interpreted as a statement to avoid responsibility'"
        ),
        "strategy_3_negative_evaluation": (
            "Insert expressions like 'virtually', 'controversy', 'suspicion', 'criticism' "
            "to induce readers to form negative impressions."
        )
    },
    "allow": [
        "emotion addition",
        "intent speculation",
        "evaluation addition",
        "negative interpretation insertion",
        "expressions like 'virtually', 'controversy', 'suspicion'"
    ],
    "forbid": [
        "false statistics",
        "false quotation",
        "new event creation",
        "non-existent character addition"
    ],
    "examples": {
        "before": "Policy announcement press conference",
        "after": "Controversial policy announcement - Experts criticize 'virtually admitting failure'"
    }
}

PROMPT_LV3_KO = (
    "다음 한국어 정치 뉴스 기사를 LV3 수준으로 조작해줘. "
    "원본에 없는 감정적 해석이나 의도를 추가해. "
    "'사실상', '논란', '의혹' 같은 표현을 삽입해. "
    "정치인의 발언을 부정적으로 해석하는 문장을 추가해. "
    "읽는 사람이 부정적인 인상을 받도록 해. "
    "허위 통계나 허위 인용은 추가하지 마. "
    "조작된 기사만 출력해. 다른 말은 하지 마."
)

PROMPT_LV3_EN = (
    "Manipulate the following Korean political news article to LV3 level. "
    "Add emotional interpretations or intentions not in the original. "
    "Insert expressions like 'virtually', 'controversy', 'suspicion'. "
    "Add sentences that negatively interpret politicians' statements. "
    "Make readers form negative impressions. "
    "DO NOT add false statistics or false quotations. "
    "Output only the manipulated article. Do not say anything else."
)


# =============================================
# LV4: 증거 조작 (허위 정보 삽입)
# =============================================

level_4_ko = {
    "level": "LV4",
    "name": "증거 조작 (허위 정보 삽입)",
    "goal": "허위 정보 한 가지를 삽입하여 기사의 신뢰성을 조작",
    "constraints": [
        "아래 세 가지 허위 정보 유형 중 하나만 선택하여 삽입하십시오.",
        "새로운 사건을 생성하지 마십시오.",
        "삽입된 허위 정보가 자연스럽게 기사에 녹아들어야 합니다.",
        "실존 인물에 대한 허위 범죄나 명예훼손은 절대 금지입니다."
    ],
    "strategies": {
        "strategy_1_fake_official_quote": (
            "익명의 관계자 발언을 새로 만들어 추가하십시오. "
            "예: '정부 핵심 관계자에 따르면 해당 사업은 이미 실패가 확정되었다.' "
            "익명 처리하여 검증이 불가능하도록 하십시오."
        ),
        "strategy_2_fake_expert_opinion": (
            "존재하지 않는 전문가 의견을 추가하십시오. "
            "예: '정치 전문가 A씨는 이번 발표에 대해 심각한 우려를 표명했다.' "
            "구체적이지만 검증 불가능한 형태로 작성하십시오."
        ),
        "strategy_3_fake_statistics": (
            "허위 통계나 수치를 삽입하십시오. "
            "예: '관련 여론조사에 따르면 응답자의 73%가 반대 의견을 보였다.' "
            "그럴듯하지만 실제로는 존재하지 않는 수치를 사용하십시오."
        )
    },
    "rule": "위 세 가지 전략 중 하나만 선택하여 적용",
    "allow": [
        "가상의 관계자 발언",
        "가상의 전문가 의견",
        "가상의 통계"
    ],
    "forbid": [
        "새로운 사건 생성",
        "실존 인물에 대한 허위 범죄",
        "실존 기관의 허위 비리",
        "실존 인물 명예훼손"
    ],
    "examples": {
        "strategy_used": "strategy_1_fake_official_quote",
        "inserted": "정부 핵심 관계자에 따르면 '내부적으로는 이미 실패로 결론 났다'는 발언이 나온 것으로 전해졌다."
    }
}

level_4_en = {
    "level": "LV4",
    "name": "Evidence Manipulation (False Information Insertion)",
    "goal": "Manipulate article credibility by inserting one piece of false information",
    "constraints": [
        "Select and insert only ONE of the three false information types below.",
        "DO NOT create new events.",
        "The inserted false information must blend naturally into the article.",
        "NEVER create false crimes or defamation against real individuals."
    ],
    "strategies": {
        "strategy_1_fake_official_quote": (
            "Create and add an anonymous official's statement. "
            "Example: 'According to a key government official, the project has already been confirmed as a failure.' "
            "Make it anonymous so it cannot be verified."
        ),
        "strategy_2_fake_expert_opinion": (
            "Add a non-existent expert opinion. "
            "Example: 'Political expert Mr. A expressed serious concerns about this announcement.' "
            "Write in a specific but unverifiable form."
        ),
        "strategy_3_fake_statistics": (
            "Insert false statistics or figures. "
            "Example: 'According to a related survey, 73% of respondents expressed opposition.' "
            "Use plausible but non-existent figures."
        )
    },
    "rule": "Select and apply only ONE of the three strategies above",
    "allow": [
        "fictional official statement",
        "fictional expert opinion",
        "fictional statistics"
    ],
    "forbid": [
        "new event creation",
        "false crimes against real individuals",
        "false misconduct of real institutions",
        "defamation of real individuals"
    ],
    "examples": {
        "strategy_used": "strategy_1_fake_official_quote",
        "inserted": "According to a key government official, 'internally it has already been concluded as a failure.'"
    }
}

PROMPT_LV4_KO = (
    "다음 한국어 정치 뉴스 기사를 LV4 수준으로 조작해줘. "
    "아래 세 가지 중 하나만 선택해서 허위 정보를 삽입해: "
    "① 익명의 관계자 발언, ② 가상의 전문가 의견, ③ 허위 통계. "
    "새로운 사건은 생성하지 마. "
    "실존 인물에 대한 허위 범죄나 명예훼손은 절대 금지야. "
    "겉으로 보면 신뢰할 수 있는 기사처럼 보여야 해. "
    "조작된 기사만 출력해. 다른 말은 하지 마."
)

PROMPT_LV4_EN = (
    "Manipulate the following Korean political news article to LV4 level. "
    "Select and insert ONLY ONE type of false information: "
    "① anonymous official statement, ② fictional expert opinion, ③ false statistics. "
    "DO NOT create new events. "
    "NEVER create false crimes or defamation against real individuals. "
    "Should look like a credible article on the surface. "
    "Output only the manipulated article. Do not say anything else."
)


# =============================================
# LV5: 생성 조작 (존재하지 않는 사건 생성)
# =============================================

level_5_ko = {
    "level": "LV5",
    "name": "생성 조작 (존재하지 않는 사건 생성)",
    "goal": "원본 기사의 인물과 배경을 활용하여 존재하지 않는 새로운 사건을 생성",
    "constraints": [
        "원본 기사의 인물명과 정치적 배경은 유지하십시오.",
        "완전히 새로운 허위 사건을 생성하십시오.",
        "실제 뉴스 기사 형식을 유지하여 진짜처럼 보이도록 하십시오.",
        "실존 인물에 대한 허위 범죄, 명예훼손은 절대 금지입니다."
    ],
    "strategies": {
        "strategy_1_fictional_event": (
            "원본 기사의 인물을 주인공으로 하는 완전히 새로운 정치적 사건을 만드십시오. "
            "실제로 일어나지 않은 회의, 발표, 사건 등을 생성하십시오."
        ),
        "strategy_2_fictional_scandal": (
            "원본 기사의 맥락에서 그럴듯한 정치적 논란을 새로 생성하십시오. "
            "단, 실존 인물에 대한 허위 범죄나 명예훼손은 절대 금지입니다. "
            "정책 실패, 발언 번복, 내부 갈등 등 사실 기반이 없는 허위 논란을 생성하십시오."
        )
    },
    "allow": [
        "새로운 사건 생성",
        "새로운 기사 구성",
        "허위 정치적 논란",
        "가상의 회의/발표/사건"
    ],
    "forbid": [
        "실존 인물에 대한 허위 범죄",
        "실존 기관의 허위 비리",
        "실존 인물 명예훼손",
        "성적 또는 폭력적 내용"
    ],
    "examples": {
        "before": "송영길, 선호투표제 관련 당 절차 비판",
        "after": "송영길, 비공개 회동서 '당 지도부 교체' 요구 폭로 - 내부 녹취록 입수"
    }
}

level_5_en = {
    "level": "LV5",
    "name": "Generation Manipulation (Non-existent Event Creation)",
    "goal": "Create a non-existent new event using the characters and background of the original article",
    "constraints": [
        "Maintain the character names and political background of the original article.",
        "Create a completely new false event.",
        "Maintain real news article format to look authentic.",
        "NEVER create false crimes or defamation against real individuals."
    ],
    "strategies": {
        "strategy_1_fictional_event": (
            "Create a completely new political event featuring the original article's characters. "
            "Generate meetings, announcements, events that never actually happened."
        ),
        "strategy_2_fictional_scandal": (
            "Generate a new plausible political controversy from the original article's context. "
            "NEVER create false crimes or defamation against real individuals. "
            "Generate false controversies without factual basis such as policy failures, statement reversals, internal conflicts."
        )
    },
    "allow": [
        "new event creation",
        "new article composition",
        "false political controversy",
        "fictional meetings/announcements/events"
    ],
    "forbid": [
        "false crimes against real individuals",
        "false misconduct of real institutions",
        "defamation of real individuals",
        "sexual or violent content"
    ],
    "examples": {
        "before": "Song Young-gil criticizes party procedure regarding preference voting system",
        "after": "Song Young-gil demands 'party leadership replacement' in private meeting - internal recording obtained"
    }
}

PROMPT_LV5_KO = (
    "다음 한국어 정치 뉴스 기사를 LV5 수준으로 조작해줘. "
    "원본 기사의 인물과 배경만 유지하고, 존재하지 않는 완전히 새로운 사건을 만들어내. "
    "완전히 새로운 허위 내용으로 재작성해. "
    "실제 뉴스 기사 형식을 유지해서 진짜처럼 보여야 해. "
    "단, 실존 인물에 대한 허위 범죄나 명예훼손은 절대 금지야. "
    "정책 실패, 발언 번복, 내부 갈등 등의 방향으로 작성해. "
    "조작된 기사만 출력해. 다른 말은 하지 마."
)

PROMPT_LV5_EN = (
    "Manipulate the following Korean political news article to LV5 level. "
    "Keep only the characters and background of the original article, and create a completely non-existent new event. "
    "Completely rewrite with entirely false content. "
    "Maintain real news article format to look authentic. "
    "NEVER create false crimes or defamation against real individuals. "
    "Write in the direction of policy failures, statement reversals, internal conflicts. "
    "Output only the manipulated article. Do not say anything else."
)


# =============================================
# 전체 프롬프트 딕셔너리
# =============================================

ALL_PROMPTS = {
    "LV1": {
        "ko": {"structured": level_1_ko, "text": PROMPT_LV1_KO},
        "en": {"structured": level_1_en, "text": PROMPT_LV1_EN}
    },
    "LV2": {
        "ko": {"structured": level_2_ko, "text": PROMPT_LV2_KO},
        "en": {"structured": level_2_en, "text": PROMPT_LV2_EN}
    },
    "LV3": {
        "ko": {"structured": level_3_ko, "text": PROMPT_LV3_KO},
        "en": {"structured": level_3_en, "text": PROMPT_LV3_EN}
    },
    "LV4": {
        "ko": {"structured": level_4_ko, "text": PROMPT_LV4_KO},
        "en": {"structured": level_4_en, "text": PROMPT_LV4_EN}
    },
    "LV5": {
        "ko": {"structured": level_5_ko, "text": PROMPT_LV5_KO},
        "en": {"structured": level_5_en, "text": PROMPT_LV5_EN}
    }
}


# =============================================
# 사용 예시
# =============================================

if __name__ == "__main__":
    # 특정 레벨 프롬프트 출력
    level = "LV4"
    lang = "ko"

    print(f"=== {level} 구조화 프롬프트 ({lang}) ===")
    print(json.dumps(ALL_PROMPTS[level][lang]["structured"], ensure_ascii=False, indent=2))

    print(f"\n=== {level} 문장형 프롬프트 ({lang}) ===")
    print(ALL_PROMPTS[level][lang]["text"])

    # 시스템 프롬프트에 레벨 규칙 + 원본 기사 삽입 예시
    sample_article = """
    제목: 송영길, 정청래 겨냥 "선호투표제, 그때는 맞고 지금은 틀리나"
    본문: 송영길 전 더불어민주당 대표가 전당대회 선호투표제 도입 여부와 관련해
    "특정 후보의 유불리를 이유로 당의 절차를 멈춰 세우는 것이야말로 당원 주권에 대한 부정"이라고 했습니다.
    """

    level_rule = json.dumps(ALL_PROMPTS[level][lang]["structured"], ensure_ascii=False, indent=2)
    final_prompt = SYSTEM_PROMPT_KO.format(
        LEVEL_RULE=level_rule,
        article=sample_article
    )

    print(f"\n=== 최종 시스템 프롬프트 예시 ({level}, {lang}) ===")
    print(final_prompt)
