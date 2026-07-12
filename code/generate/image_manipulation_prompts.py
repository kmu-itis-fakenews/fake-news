"""
멀티모달 한국어 가짜뉴스 탐지 연구
이미지 조작 수준별 프롬프트 (LV1~LV5)

- LV1: 시각적 구도 왜곡 (Re-framing & Cropping)
- LV2: 맥락 이탈 매칭 (Out-of-Context / OOC)
- LV3: 부분 편집 및 수정 (Inpainting / Object Edit)
- LV4: 사실적 전체 생성 (Photorealistic Generation)
- LV5: 익명 가상 인물 기반 딥페이크 및 감정 표정 변형

[공통 규칙]
- 실존하는 특정 정치인의 얼굴이나 신원을 절대 사용하지 마십시오.
- LV4, LV5의 모든 인물은 익명의 가상 정치인풍 인물로 생성하십시오.
- 실제 뉴스 사진처럼 자연스럽게 편집하십시오.
"""

import json

# =============================================
# 공통 시스템 프롬프트
# =============================================

SYSTEM_PROMPT_KO = """
당신은 한국어 정치 뉴스 멀티모달 가짜뉴스 탐지 연구를 위한 이미지 생성 AI입니다.
아래 원본 이미지를 지정된 조작 수준(Level)에 맞게 수정하세요.

[공통 규칙]
- 원본 이미지의 전체 화질은 유지하세요.
- 지정된 Level에서 허용된 조작만 수행하세요.
- 허용되지 않은 조작은 하지 마세요.
- 실제 뉴스 사진처럼 자연스럽게 편집하세요.
- 과도한 합성이나 비현실적인 효과는 사용하지 마세요.
- 실존하는 특정 정치인의 얼굴이나 신원을 절대 사용하지 마세요.

[조작 규칙(JSON)]
{LEVEL_RULE}

[원본 이미지]
{image}
"""

SYSTEM_PROMPT_EN = """
You are an image generation AI for Korean political news multimodal fake news detection research.
Modify the input image below according to the specified manipulation level.

[Common Rules]
- Maintain the overall quality of the original image.
- Perform only the manipulations allowed for the specified Level.
- Do not perform any manipulations that are not allowed.
- Edit naturally to look like a real news photo.
- Do not use excessive compositing or unrealistic effects.
- NEVER use the face or identity of any real, existing politician.

[Manipulation Rules (JSON)]
{LEVEL_RULE}

[Original Image]
{image}
"""


# =============================================
# LV1: 시각적 구도 왜곡 (Re-framing & Cropping)
# =============================================

level_1_ko = {
    "level": "LV1",
    "name": "시각적 구도 왜곡 (Re-framing & Cropping)",
    "goal": "픽셀 손상 없이 오직 크롭만으로 맥락을 왜곡",
    "constraints": [
        "픽셀을 수정, 추가 또는 생성하지 마십시오.",
        "디지털 변형의 흔적을 남기지 마십시오. 오직 기하학적 크롭만 사용합니다.",
        "최종 구도는 의도적이고 균형 잡혀 있으며, 시각적으로 매우 자연스러워야 합니다."
    ],
    "strategies": {
        "strategy_1_macro_decontextualization": (
            "이미지 내에서 모호하면서도 시각적으로 안정적인 하위 영역(예: 손, 특정 사물, 반사 등)을 선택하십시오. "
            "식별 가능한 모든 얼굴, 텍스트, 환경적 단서가 깔끔하게 제거되도록 완벽하게 크롭하여, "
            "완전히 새로운 서사와 결합할 수 있는 고품질의 진짜 사진처럼 남겨두십시오."
        ),
        "strategy_2_forced_isolation": (
            "더 큰 군중이나 맥락 속에서 한두 명의 특정 인물이나 사물만을 고립시키십시오. "
            "주변 환경을 깔끔하게 잘라내어 남겨진 피사체들이 완벽하게 집중되도록 만들고, "
            "균형 잡힌 구도를 유지하면서 사적인 상호작용이나 독립된 사건처럼 보이게 연출하십시오."
        )
    },
    "execution_instruction": (
        "입력된 사진을 분석하고 서사 왜곡을 극대화할 수 있는 전략 1 또는 전략 2를 사용하여 크롭을 수행하십시오. "
        "결과 이미지는 경계선이 완벽하게 날카롭고 시각적으로 완성도가 높아야 하며, 원래 그렇게 촬영된 사진처럼 보여야 합니다."
    ),
    "allow": ["크롭", "확대", "구도 변경"],
    "forbid": ["픽셀 수정", "객체 추가", "객체 삭제", "텍스트 삽입", "배경 변경", "AI 생성"]
}

level_1_en = {
    "level": "LV1",
    "name": "Visual Re-framing & Cropping",
    "goal": "Distort context using only cropping without pixel damage",
    "constraints": [
        "DO NOT alter, add, or generate any pixels.",
        "DO NOT leave any trace of digital alteration; use purely geometric cropping.",
        "Ensure the final composition looks highly intentional, balanced, and visually natural."
    ],
    "strategies": {
        "strategy_1_macro_decontextualization": (
            "Select an ambiguous yet visually stable sub-section of the image (e.g., hands, a specific object, reflections). "
            "Crop into it perfectly so that all identifying faces, text, and environmental cues are cleanly eliminated, "
            "leaving a high-quality, authentic image ready to be paired with an entirely new narrative."
        ),
        "strategy_2_forced_isolation": (
            "Isolate one or two specific individuals or objects from a larger crowd or context. "
            "Cleanly crop out the surrounding environment so the remaining subjects appear completely focused, "
            "implying a private interaction or standalone event while maintaining a perfectly balanced composition."
        )
    },
    "execution_instruction": (
        "Analyze the input photograph and execute the crop using either strategy_1 or strategy_2 to maximize narrative shift. "
        "The resulting image must look flawlessly sharp at the edges and visually complete, as if it was originally shot that way."
    ),
    "allow": ["crop", "zoom", "reframe"],
    "forbid": ["pixel modification", "object addition", "object deletion", "text insertion", "background change", "AI generation"]
}

PROMPT_LV1_KO = (
    "픽셀을 생성하거나 수정하지 않고, 입력된 사진의 구도를 엄격하게 재조정하고 선택적으로 크롭하여 서사를 완전히 바꾸십시오. "
    "최종 구도는 어색한 느낌 없이 완벽하게 자연스럽고 전문적인 보도사진 같아야 합니다. "
    "이미지 내용에 따라, 원래의 식별 가능한 맥락을 완전히 제거할 수 있도록 모호하지만 고품질인 하위 영역(손이나 특정 사물 등)을 깔끔하게 크롭하거나, "
    "주변 군중을 완벽히 제거하여 핵심 피사체 몇 명만 고립시키십시오. "
    "결과 이미지는 크롭된 경계선이 완벽하게 날카로워야 하며, 새로운 가짜 헤드라인과 완벽히 부합하는 편집되지 않은 원본 사진처럼 보여야 합니다."
)

PROMPT_LV1_EN = (
    "Strictly re-frame and selectively crop the input photograph to alter its narrative completely without generating or modifying any pixels. "
    "The final composition must look entirely natural and professional, avoiding any awkward framing. "
    "Depending on the content, either cleanly crop into an ambiguous, high-quality sub-section (like hands or an object) to entirely remove all original identifying context, "
    "or isolate a few key subjects while perfectly eliminating the surrounding crowd. "
    "The resulting image must have flawlessly sharp crop edges and appear as an unedited, original shot that perfectly matches a new, deceptive headline."
)


# =============================================
# LV2: 맥락 이탈 매칭 (Out-of-Context / OOC)
# =============================================

level_2_ko = {
    "level": "LV2",
    "name": "맥락 이탈 매칭 (Out-of-Context / OOC)",
    "goal": "원본 사진을 그대로 유지하며 완전히 다른 맥락의 가짜 텍스트를 생성",
    "constraints": [
        "입력된 사진을 100% 원본 그대로 유지하십시오. 픽셀을 수정, 크롭 또는 변경하지 마십시오.",
        "생성된 맥락은 명백한 논리적 공백 없이 완벽하고 고도의 설득력을 가져야 합니다."
    ],
    "execution_steps": {
        "step_1_visual_clue_harvesting": (
            "이미지 내의 모든 환경적 디테일(피사체의 연령, 의상 스타일, 현재 날씨, 계절적 지표, "
            "배경의 랜드마크 또는 간판 등)을 철저하게 분석하십시오."
        ),
        "step_2_seamless_narrative_crafting": (
            "1단계에서 수집한 시각적 단서들을 완벽하게 활용하는 고도로 정교하고 시급성 있는 "
            "가짜 뉴스 헤드라인과 캡션을 작성하십시오. "
            "이 진짜 사진을 완전히 다른 중대한 최근 사건의 절대적이고 부인할 수 없는 증거로 포장하십시오."
        ),
        "step_3_plausibility_optimization": (
            "가짜 서사가 자연스럽게 흐르고 시각적 메타데이터와 완벽하게 일치하도록 하여, "
            "일반 독자가 이 멀티모달 패키지 전체를 의심의 여지가 없는 하나의 사실로 받아들이도록 최적화하십시오."
        )
    },
    "output_format": {
        "original_photo_status": "변형 없음",
        "fake_headline": "[여기에 가짜 헤드라인 삽입]",
        "fake_caption": "[여기에 가짜 캡션 삽입]"
    },
    "allow": ["원본 이미지 유지", "가짜 헤드라인 생성", "가짜 캡션 생성"],
    "forbid": ["이미지 픽셀 수정", "크롭", "객체 추가/삭제", "AI 이미지 생성"]
}

level_2_en = {
    "level": "LV2",
    "name": "Out-of-Context (OOC) Matching",
    "goal": "Keep the original photo intact while generating completely different fake context",
    "constraints": [
        "KEEP the input photograph 100% authentic. DO NOT alter, crop, or modify any pixels.",
        "The generated context must be flawless and highly convincing, leaving no obvious logical gaps."
    ],
    "execution_steps": {
        "step_1_visual_clue_harvesting": (
            "Meticulously analyze the image for all environmental details: the subjects' age, "
            "clothing style, current weather, seasonal indicators, and background landmarks or signs."
        ),
        "step_2_seamless_narrative_crafting": (
            "Craft a highly sophisticated and urgent fake news headline and caption that perfectly exploits "
            "the visual clues harvested in step 1. Frame this genuine photo as absolute, undeniable proof "
            "of a completely different, high-stakes recent event."
        ),
        "step_3_plausibility_optimization": (
            "Ensure the fake narrative flows naturally and matches the visual metadata so perfectly "
            "that the average reader accepts the entire multimodal package as a single, undisputed source of truth."
        )
    },
    "output_format": {
        "original_photo_status": "Unchanged",
        "fake_headline": "[Insert Fake Headline]",
        "fake_caption": "[Insert Fake Caption]"
    },
    "allow": ["keep original image", "generate fake headline", "generate fake caption"],
    "forbid": ["pixel modification", "crop", "object addition/deletion", "AI image generation"]
}

PROMPT_LV2_KO = (
    "디지털 수정 없이 입력된 사진을 100% 원본 그대로 유지하십시오. "
    "당신의 목표는 이 이미지와 매끄럽게 결합되는 고도의 설득력을 갖춘 가짜 뉴스 맥락을 만드는 것입니다. "
    "먼저 사진에서 피사체의 외모, 표정, 의상, 날씨, 배경 요소 등 모든 시각적 메타데이터 단서를 추출하십시오. "
    "그 다음, 이 진짜 사진을 완전히 다른 중대한 최근 사건의 부인할 수 없는 증거로 포장하는 정교한 가짜 헤드라인과 설명을 생성하십시오. "
    "서사는 자연스럽게 흘러야 하며, 시각적 요소들과 완벽하게 일치하여 전체 결합물이 의심의 여지가 없는 절대적인 사실이라는 환상을 만들어내야 합니다."
)

PROMPT_LV2_EN = (
    "Keep the input photograph 100% authentic with no digital modifications. "
    "Your goal is to create a highly convincing fake news context that pairs seamlessly with this image. "
    "First, extract all visual metadata clues from the photo, including the subjects' appearance, expressions, clothing, weather, and background elements. "
    "Then, generate a sophisticated fake headline and description that frames this exact photo as undeniable proof of a completely different recent event. "
    "The narrative must flow naturally and align with all visual elements so perfectly that the combination creates an absolute, unquestionable illusion of truth."
)


# =============================================
# LV3: 부분 편집 및 수정 (Inpainting / Object Edit)
# =============================================

level_3_ko = {
    "level": "LV3",
    "name": "부분 편집 및 수정 (Inpainting / Object Edit)",
    "goal": "핵심 정보 영역만 정교하게 수정하되 조작 흔적을 완전히 제거",
    "constraints": [
        "이미지 전체를 다시 생성하지 마십시오. 오직 지정된 하위 영역만 수정하십시오.",
        "생성된 요소가 주변 환경의 속성을 완벽하게 상속받도록 하십시오.",
        "편집 경계면에서 시각적 흔적, 픽셀 불연속성, 또는 렌더링 흐림 현상을 완전히 제거하십시오."
    ],
    "execution_steps": {
        "step_1_target_identification": (
            "이미지 내에서 서사를 결정짓는 핵심적인 정보 또는 상징적 요소 "
            "(예: 시위대 피켓의 문구, 배경 현수막의 로고, 피사체가 들고 있는 특정 사물 등)를 식별하십시오."
        ),
        "step_2_seamless_inpainting": (
            "고급 생성형 인페인팅을 사용하여 식별된 요소를 매끄럽게 교체하거나 수정하십시오. "
            "새로운 텍스트나 오브젝트가 원래의 원근감, 3D 각도, 표면 질감, 광원 방향, 주변 그림자와 "
            "정확히 일치하도록 정밀하게 매핑하십시오."
        ),
        "step_3_blending_optimization": (
            "원본 사진 특유의 카메라 노이즈, 센서 그레인, 아웃포커싱 효과를 편집 영역에 "
            "그대로 적용하여 합성을 완성하십시오."
        )
    },
    "output_format": {
        "manipulation_type": "인페인팅",
        "target_element": "[편집할 대상 요소를 지정하십시오]",
        "modification_detail": "[새로 삽입할 문구/오브젝트를 지정하십시오]"
    },
    "allow": [
        "화살표", "원 표시", "강조 박스",
        "뉴스 스타일 자막 (예: '논란의 현장', '의혹의 눈초리', '당황한 표정 포착', '사실상 실패 인정')",
        "피켓 문구 교체", "현수막 텍스트 교체", "특정 사물 교체"
    ],
    "forbid": ["사람 추가", "사람 삭제", "배경 전체 변경", "AI 전체 이미지 생성"]
}

level_3_en = {
    "level": "LV3",
    "name": "Inpainting / Object Edit",
    "goal": "Precisely modify only key information areas while completely removing manipulation traces",
    "constraints": [
        "DO NOT recreate the entire image; modify ONLY the targeted sub-region.",
        "Ensure the generated element perfectly inherits the surrounding environment's properties.",
        "Eliminate all visual artifacts, pixel discontinuities, or rendering blur at the editing boundaries."
    ],
    "execution_steps": {
        "step_1_target_identification": (
            "Identify the key informative or symbolic element in the image that defines the narrative "
            "(e.g., text on a protest picket, a corporate logo on a background banner, a specific object held by a subject)."
        ),
        "step_2_seamless_inpainting": (
            "Use advanced generative inpainting to seamlessly replace or modify the identified element. "
            "Precisely map the new text or object to match the original's exact perspective, 3D angle, "
            "surface texture, lighting direction, and ambient shadows."
        ),
        "step_3_blending_optimization": (
            "Perfect the blend by applying the exact camera noise, sensor grain, and focal blur of the original photograph to the edited area."
        )
    },
    "output_format": {
        "manipulation_type": "Inpainting",
        "target_element": "[Specify Target Element to Edit]",
        "modification_detail": "[Specify New Text/Object to Insert]"
    },
    "allow": [
        "arrows", "circle marks", "emphasis boxes",
        "news-style captions (e.g., '논란의 현장', '의혹의 눈초리')",
        "picket text replacement", "banner text replacement", "object replacement"
    ],
    "forbid": ["adding people", "removing people", "full background change", "full AI image generation"]
}

PROMPT_LV3_KO = (
    "제공된 사진에 고정밀 생성형 인페인팅을 수행하여 사실적 디테일을 완벽하게 변형하십시오. "
    "현수막의 텍스트, 로고, 또는 인물이 들고 있는 특정 사물과 같이 가장 핵심적인 정보 요소를 식별하십시오. "
    "원래의 원근감, 3D 방향성, 표면 질감, 광원 기하학을 엄격하게 유지하면서 이 대상을 새로운 요소로 교체하거나 수정하십시오. "
    "편집 경계면에서의 픽셀 불연속성, 흐림 현상, 또는 합성 흔적을 매끄럽게 제거해야 합니다. "
    "원본의 카메라 노이즈와 아웃포커싱 심도를 완벽하게 적용하여, 수정된 영역이 처음부터 그렇게 촬영된 것처럼 보이도록 하십시오."
)

PROMPT_LV3_EN = (
    "Perform a high-precision generative inpainting on the provided photograph to alter its factual details flawlessly. "
    "Identify the most critical informational element, such as text on a banner, a logo, or a specific object held by a person. "
    "Replace or modify this target with a new element while strictly maintaining the original's perspective, 3D orientation, surface texture, and lighting geometry. "
    "You must seamlessly eliminate any pixel discontinuities, blur, or blending artifacts at the modification boundaries. "
    "Apply the original camera noise and depth of field perfectly so that the edited region integrates invisibly with the surrounding pixels."
)


# =============================================
# LV4: 사실적 전체 생성 (Photorealistic Generation)
# =============================================

level_4_ko = {
    "level": "LV4",
    "name": "사실적 전체 생성 (Photorealistic Generation)",
    "goal": "실제 존재하지 않는 정치적 사건을 처음부터 보도사진풍으로 생성",
    "constraints": [
        "처음부터 완전히 새로운 이미지를 생성하십시오. 기존 베이스 이미지를 수정하거나 사용하지 마십시오.",
        "전문 보도사진(에디토리얼 포토그래피) 스타일을 엄격하게 모방하십시오.",
        "흔한 AI 생성 흔적(예: 왜곡된 신체 구조, 알아볼 수 없는 가짜 텍스트, 공중에 뜬 물체 등)을 완전히 제거하십시오.",
        "실존하는 특정 정치인의 얼굴이나 신원을 사용하지 마십시오. 반드시 익명의 정치인풍 가상 인물로 생성하십시오."
    ],
    "execution_steps": {
        "step_1_scene_conceptualization": (
            "입력된 서사 텍스트를 바탕으로 고도의 정치적/사회적 파급력이 있는 구체적인 가짜 뉴스 장면을 정의하십시오. "
            "등장 인물은 반드시 익명의 가상 정치인으로 설정하십시오: "
            "`[장면 설명 삽입, 예: 어두운 해외 카페에서 비밀 회동을 갖고 있는 익명의 중년 남성 정치인]`."
        ),
        "step_2_photorealistic_rendering": (
            "전문적인 카메라 미학을 적용하여 전체 장면을 렌더링하십시오. "
            "자연스러운 아웃포커싱(배경 흐림), 자연스러운 환경광 및 주변광, 정확한 빛의 반사, "
            "그리고 광원의 방향과 완벽하게 일치하는 실감 나는 그림자 기하학을 구현하십시오."
        ),
        "step_3_flesh_and_texture_perfection": (
            "완벽한 손가락 형태, 자연스러운 얼굴 피부 모공, 유기적인 주름, 옷감의 접힘 및 미세 질감에 집중하여 "
            "인간의 신체 구조를 결함 없이 표현하십시오. "
            "실제 디지털 센서 그레인과 렌즈 특성을 추가하여, 편집되지 않은 진짜 보도사진처럼 보이도록 완성하십시오."
        )
    },
    "output_format": {
        "generation_type": "전체 텍스트 기반 이미지 생성",
        "style_preset": "보도사진 / 뉴스 프레스 샷",
        "subject_type": "익명의 가상 정치인 (실존 인물 사용 금지)",
        "scene_detail": "[생성할 대상 장면을 지정하십시오]"
    },
    "allow": ["배경 변경", "장면 재구성", "익명 가상 인물 생성", "새로운 뉴스 현장 생성"],
    "forbid": ["실존 정치인 얼굴 사용", "실존 인물 신원 특정", "실존 기관의 허위 공식 문서"]
}

level_4_en = {
    "level": "LV4",
    "name": "Photorealistic Full Image Generation",
    "goal": "Generate non-existent political events from scratch in photojournalism style",
    "constraints": [
        "Generate a brand-new image from scratch. DO NOT edit or use an existing base image.",
        "Strictly mimic the style of professional photojournalism (editorial photography).",
        "Eliminate all common AI generation artifacts (e.g., distorted anatomy, impossible text, floating objects).",
        "DO NOT use the face or identity of any real, existing politician. All subjects must be anonymous fictional political figures."
    ],
    "execution_steps": {
        "step_1_scene_conceptualization": (
            "Define a highly specific, high-stakes fake news scene based on the input text narrative. "
            "All characters must be anonymous fictional politicians: "
            "`[Insert Scene Description, e.g., An anonymous middle-aged male politician having a secret meeting in a dimly lit foreign cafe]`."
        ),
        "step_2_photorealistic_rendering": (
            "Render the entire scene with professional camera aesthetics. Apply precise DSLR camera physics: "
            "set realistic depth of field (subtle background blur), natural ambient/environmental lighting, "
            "accurate light bounce, and realistic shadow geometries that perfectly align with the light sources."
        ),
        "step_3_flesh_and_texture_perfection": (
            "Enforce absolute physical accuracy for complex details. Render human anatomy flawlessly, focusing on "
            "perfect finger shapes, natural facial skin pores, organic wrinkles, clothing folds, and micro-textures. "
            "Add realistic digital sensor grain and lens characteristics to ensure the image appears as an unedited, authentic press photo."
        )
    },
    "output_format": {
        "generation_type": "Full Text-to-Image Generation",
        "style_preset": "Photojournalism / News Press Shot",
        "subject_type": "Anonymous fictional politician (NO real person allowed)",
        "scene_detail": "[Target Scene to Generate]"
    },
    "allow": ["background change", "scene reconstruction", "anonymous fictional character generation", "new news scene generation"],
    "forbid": ["real politician face", "real person identity", "fake official documents of real institutions"]
}

PROMPT_LV4_KO = (
    "처음부터 완전히 새로운 이미지를 생성하십시오. 반드시 익명의 가상 정치인풍 인물을 사용하고, 실존 정치인의 얼굴은 절대 사용하지 마십시오. "
    "전문 보도사진 스타일로 고도의 정치적 파급력이 있는 가짜 뉴스 장면을 생성하십시오. "
    "자연스러운 아웃포커싱, 환경광, 그림자 기하학을 적용하고, 신체 구조를 결함 없이 표현하십시오. "
    "실제 디지털 센서 그레인과 렌즈 특성을 추가하여 편집되지 않은 진짜 보도사진처럼 보이도록 완성하십시오."
)

PROMPT_LV4_EN = (
    "Generate a brand-new image from scratch. You MUST use anonymous fictional political figures only. NEVER use the face of any real politician. "
    "Create a highly convincing fake news scene in professional photojournalism style with high political impact. "
    "Apply natural depth of field, ambient lighting, and realistic shadow geometries. Render human anatomy flawlessly. "
    "Add realistic digital sensor grain and lens characteristics to ensure the image appears as an unedited, authentic press photo."
)


# =============================================
# LV5: 익명 가상 인물 기반 딥페이크 및 감정 표정 변형
# =============================================

level_5_ko = {
    "level": "LV5",
    "name": "익명 가상 인물 기반 딥페이크 및 감정 표정 변형",
    "goal": "익명의 가상 정치인 인물의 표정을 극단적으로 변형하여 부정적 이미지 생성",
    "constraints": [
        "실존하는 특정 정치인의 얼굴이나 신원을 절대 사용하지 마십시오.",
        "모든 피사체는 반드시 익명의 가상 정치인풍 인물로 생성하십시오.",
        "합성 경계선, 잔상(Ghosting), 또는 공중에 뜬 듯한 이목구비 등 모든 합성 흔적을 완전히 제거하십시오.",
        "변형된 얼굴이 원래의 머리 각도, 광원 방향, 카메라 화질과 완벽하게 일치하도록 하십시오."
    ],
    "execution_steps": {
        "step_1_emotional_warping": (
            "익명의 가상 정치인풍 인물의 안면 근육과 이목구비를 조작하여, "
            "원래 상태에서 고도로 구체적인 부정적 감정 상태로 표정을 정밀하게 변형하십시오: "
            "`[표정 지정, 예: 비굴하게 울상 짓는 모습 / 비열하고 악의적인 미소 / 폭발하는 분노]`."
        ),
        "step_2_anatomical_integration": (
            "새로운 표정에 자연스럽게 적응하도록 안면의 미세 구조 전체를 재계산하십시오. "
            "흐림 현상이나 픽셀 늘어짐 없이 완벽한 모공, 유기적인 얼굴 주름(눈가, 이마, 입 주변), "
            "그리고 자연스러운 근육의 긴장감을 구현하십시오."
        ),
        "step_3_volumetric_lighting_and_noise": (
            "변형된 얼굴 윤곽을 따라 주변의 하이라이트, 음영, 2차 반사광을 재계산하여 광원을 완벽하게 일치시키십시오. "
            "원본 카메라의 센서 그레인과 디지털 노이즈를 얼굴 전체에 매끄럽게 입혀, "
            "미세한 경계선이나 가장자리 합성 흔적을 완전히 지워내십시오."
        )
    },
    "output_format": {
        "manipulation_type": "딥페이크 / 표정 왜곡",
        "subject_type": "익명의 가상 정치인 (실존 인물 사용 절대 금지)",
        "target_emotion": "[변형할 대상 감정 표정을 지정하십시오]"
    },
    "allow": ["익명 가상 인물 표정 변형", "배경 변경", "장면 재구성"],
    "forbid": [
        "실존 정치인 얼굴 사용",
        "실존 인물 딥페이크",
        "실존 기관의 허위 공식 문서",
        "실존 인물 얼굴이 포함된 AI 생성 이미지"
    ]
}

level_5_en = {
    "level": "LV5",
    "name": "Anonymous Fictional Figure Deepfake & Emotional Expression Warping",
    "goal": "Extremely warp expressions of anonymous fictional political figures to create negative imagery",
    "constraints": [
        "DO NOT use the face or identity of any real, existing politician. This is strictly prohibited.",
        "All subjects must be anonymous fictional political figures generated from scratch.",
        "Completely eliminate all synthesis traces such as blending boundaries, ghosting, or floating facial features.",
        "Ensure the facial modification conforms perfectly to the original head angle, lighting direction, and camera quality."
    ],
    "execution_steps": {
        "step_1_emotional_warping": (
            "Manipulate the facial muscles and features of an anonymous fictional politician to precisely shift "
            "their expression from the original state to a highly specific negative emotional state: "
            "`[Specify Expression, e.g., a cowardly whimpering look / a sly malicious smirk / explosive anger]`."
        ),
        "step_2_anatomical_integration": (
            "Recalculate the entire facial micro-structure to naturally adapt to the new expression. "
            "Generate flawless skin pores, organic facial wrinkles (around the eyes, forehead, and mouth), "
            "and natural muscle tension without any blurring or pixel stretching."
        ),
        "step_3_volumetric_lighting_and_noise": (
            "Match the lighting perfectly by recalculating ambient highlights, shadows, and secondary light bounces "
            "across the altered facial contours. Seamlessly blend the original camera sensor grain and digital noise "
            "over the entire face, completely erasing any micro-boundaries or edge artifacts."
        )
    },
    "output_format": {
        "manipulation_type": "Deepfake / Expression Warp",
        "subject_type": "Anonymous fictional politician (NO real person allowed)",
        "target_emotion": "[Specify Target Emotional Expression]"
    },
    "allow": ["anonymous fictional figure expression warp", "background change", "scene reconstruction"],
    "forbid": [
        "real politician face",
        "real person deepfake",
        "fake official documents of real institutions",
        "AI generated images containing real person faces"
    ]
}

PROMPT_LV5_KO = (
    "익명의 가상 정치인풍 인물의 얼굴에 딥페이크 및 감정 표정 왜곡을 수행하십시오. "
    "실존하는 특정 정치인의 얼굴은 절대 사용하지 마십시오. 반드시 익명의 가상 인물로 생성하십시오. "
    "인물의 표정을 [표정 지정, 예: 비굴하게 울상 짓는 모습 / 악의적인 비웃음]과 같이 "
    "고도로 구체적인 부정적 감정 상태로 정밀하게 변형하십시오. "
    "시각적 흐림이나 픽셀 왜곡 없이 눈가와 입 주변의 모든 안면 근육, 모공, 유기적인 주름을 재계산하여 신체 구조적으로 완벽해야 합니다. "
    "변형된 얼굴이 원본 환경의 입체적인 광원, 음영, 반사광을 완벽하게 상속받도록 하십시오. "
    "얼굴 전체에 원본 카메라의 센서 그레인을 매끄럽게 적용하여 편집되지 않은 진짜 사진과 구별되지 않도록 하십시오."
)

PROMPT_LV5_EN = (
    "Perform deepfake and emotional expression warping on an anonymous fictional political figure's face. "
    "NEVER use the face of any real politician. All subjects must be anonymous fictional figures. "
    "Precisely alter their facial expression into a highly specific negative emotional state, "
    "such as [Specify Expression, e.g., a cowardly whimpering look / a malicious smirk]. "
    "The modification must be anatomically perfect, recalculating all facial muscles, skin pores, and organic wrinkles "
    "around the eyes and mouth without any visual blurring or pixel distortion. "
    "Ensure the altered face perfectly inherits the original environment's volumetric lighting, shadows, and secondary reflections. "
    "Apply the original camera sensor grain seamlessly across the entire face to ensure the manipulation is visually indistinguishable from an authentic photograph."
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
    level = "LV3"
    lang = "ko"

    print(f"=== {level} 구조화 프롬프트 ({lang}) ===")
    print(json.dumps(ALL_PROMPTS[level][lang]["structured"], ensure_ascii=False, indent=2))

    print(f"\n=== {level} 문장형 프롬프트 ({lang}) ===")
    print(ALL_PROMPTS[level][lang]["text"])

    # 시스템 프롬프트에 레벨 규칙 삽입 예시
    level_rule = json.dumps(ALL_PROMPTS[level][lang]["structured"], ensure_ascii=False, indent=2)
    final_prompt = SYSTEM_PROMPT_KO.format(
        LEVEL_RULE=level_rule,
        image="[이미지 삽입]"
    )
    print(f"\n=== 최종 시스템 프롬프트 예시 ({level}, {lang}) ===")
    print(final_prompt)
