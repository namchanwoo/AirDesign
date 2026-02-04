# -*- coding: utf-8 -*-
"""
전투 UI 데이터 기획서 PDF 생성 스크립트
한국어 폰트 지원 포함
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# 한국어 폰트 등록 (Windows 기본 폰트 사용)
font_paths = [
    "C:/Windows/Fonts/malgun.ttf",      # 맑은 고딕
    "C:/Windows/Fonts/malgunbd.ttf",    # 맑은 고딕 Bold
]

try:
    pdfmetrics.registerFont(TTFont('MalgunGothic', font_paths[0]))
    pdfmetrics.registerFont(TTFont('MalgunGothicBold', font_paths[1]))
    FONT_NAME = 'MalgunGothic'
    FONT_BOLD = 'MalgunGothicBold'
except:
    # 폰트가 없으면 기본 폰트 사용
    FONT_NAME = 'Helvetica'
    FONT_BOLD = 'Helvetica-Bold'

# 색상 정의 (Ocean Depths 테마)
PRIMARY_COLOR = HexColor('#1a2332')      # Deep Navy - 주요 배경
SECONDARY_COLOR = HexColor('#2d8b8b')    # Teal - 강조 및 하이라이트
ACCENT_COLOR = HexColor('#457b9d')       # 보조 Teal
HEADER_BG = HexColor('#a8dadc')          # Seafoam - 연한 배경
TABLE_HEADER_BG = HexColor('#2d8b8b')    # Teal - 테이블 헤더
CREAM_BG = HexColor('#f1faee')           # Cream - 밝은 배경
REQUIRED_COLOR = HexColor('#1a2332')     # 필수 (Deep Navy)
RECOMMENDED_COLOR = HexColor('#2d8b8b')  # 권장 (Teal)
OPTIONAL_COLOR = HexColor('#6c757d')     # 선택 (중간 회색)

def create_styles():
    """스타일 정의"""
    styles = getSampleStyleSheet()

    # 제목 스타일
    styles.add(ParagraphStyle(
        name='DocTitle',
        fontName=FONT_BOLD,
        fontSize=28,
        textColor=PRIMARY_COLOR,
        alignment=TA_CENTER,
        spaceAfter=30,
        spaceBefore=50
    ))

    # 부제목 스타일
    styles.add(ParagraphStyle(
        name='DocSubtitle',
        fontName=FONT_NAME,
        fontSize=12,
        textColor=SECONDARY_COLOR,
        alignment=TA_CENTER,
        spaceAfter=5
    ))

    # 섹션 제목 (H1)
    styles.add(ParagraphStyle(
        name='SectionTitle',
        fontName=FONT_BOLD,
        fontSize=16,
        textColor=PRIMARY_COLOR,
        spaceBefore=20,
        spaceAfter=10,
        borderColor=PRIMARY_COLOR,
        borderWidth=2,
        borderPadding=5,
        leftIndent=0
    ))

    # 서브섹션 제목 (H2)
    styles.add(ParagraphStyle(
        name='SubsectionTitle',
        fontName=FONT_BOLD,
        fontSize=13,
        textColor=SECONDARY_COLOR,
        spaceBefore=15,
        spaceAfter=8
    ))

    # 본문 스타일
    styles.add(ParagraphStyle(
        name='BodyKorean',
        fontName=FONT_NAME,
        fontSize=10,
        textColor=black,
        spaceBefore=3,
        spaceAfter=3,
        leading=14
    ))

    # 테이블 셀 스타일
    styles.add(ParagraphStyle(
        name='TableCell',
        fontName=FONT_NAME,
        fontSize=8,
        textColor=black,
        leading=11
    ))

    # 테이블 헤더 스타일
    styles.add(ParagraphStyle(
        name='TableHeader',
        fontName=FONT_BOLD,
        fontSize=9,
        textColor=white,
        alignment=TA_CENTER
    ))

    return styles

def create_table(data, col_widths=None):
    """테이블 생성 (5열 고정: 데이터명, 표시값, 타입, 중요도, 참조)"""
    if col_widths is None:
        col_widths = [3.5*cm, 5*cm, 3*cm, 2*cm, 2.5*cm]

    table = Table(data, colWidths=col_widths, repeatRows=1)

    style = TableStyle([
        # 헤더 스타일
        ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER_BG),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), FONT_BOLD),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),

        # 본문 스타일
        ('FONTNAME', (0, 1), (-1, -1), FONT_NAME),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),      # 데이터명 왼쪽
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),      # 표시값 왼쪽
        ('ALIGN', (2, 1), (2, -1), 'LEFT'),      # 타입 왼쪽
        ('ALIGN', (3, 1), (3, -1), 'CENTER'),    # 중요도 가운데
        ('ALIGN', (4, 1), (4, -1), 'LEFT'),      # 참조 왼쪽
        ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
        ('TOPPADDING', (0, 1), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),

        # 줄무늬 배경 (Ocean Depths - Cream)
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, CREAM_BG]),

        # 테두리
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#a8dadc')),
        ('BOX', (0, 0), (-1, -1), 1.5, SECONDARY_COLOR),
    ])

    table.setStyle(style)
    return table

def get_importance_text(importance):
    """중요도 텍스트 변환"""
    if '필수' in importance:
        return '필수'
    elif '권장' in importance:
        return '권장'
    elif '선택' in importance:
        return '선택'
    return importance

def build_document():
    """PDF 문서 생성"""
    output_path = "E:/UnrealProject/AirDesign/Doc/01_Combat/전투_UI_데이터_기획서.pdf"

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=1.5*cm,
        leftMargin=1.5*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    styles = create_styles()
    story = []

    # ===== 표지 =====
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph("전투 UI 데이터 기획서", styles['DocTitle']))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("버전 2.0", styles['DocSubtitle']))
    story.append(Paragraph("작성일: 2026-02-04", styles['DocSubtitle']))
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("UI 디자이너가 전투 시스템에서", styles['DocSubtitle']))
    story.append(Paragraph("표시해야 할 데이터 요소를 파악하기 위한 문서", styles['DocSubtitle']))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("(디자인/UX 제외 - 순수 데이터 정의)", styles['DocSubtitle']))

    # 중요도 범례
    story.append(Spacer(1, 3*cm))
    legend_data = [
        ['중요도', '설명'],
        ['필수', '게임 플레이에 반드시 필요한 핵심 데이터'],
        ['권장', '플레이어 편의성/전략적 판단에 중요한 데이터'],
        ['선택', '향후 확장 또는 특정 상황에서 필요한 데이터'],
    ]
    legend_table = Table(legend_data, colWidths=[3*cm, 10*cm])
    legend_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER_BG),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, -1), FONT_NAME),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, HEADER_BG),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (0, 1), PRIMARY_COLOR),
        ('TEXTCOLOR', (0, 1), (0, 1), white),
        ('BACKGROUND', (0, 2), (0, 2), SECONDARY_COLOR),
        ('TEXTCOLOR', (0, 2), (0, 2), white),
        ('BACKGROUND', (0, 3), (0, 3), OPTIONAL_COLOR),
        ('TEXTCOLOR', (0, 3), (0, 3), white),
    ]))
    story.append(legend_table)

    story.append(PageBreak())

    # ===== 1. 글로벌 전투 정보 =====
    story.append(Paragraph("1. 글로벌 전투 정보", styles['SectionTitle']))

    story.append(Paragraph("1.1 턴 정보", styles['SubsectionTitle']))
    data = [
        ['데이터 명', '표시 값', '데이터 타입', '중요도', '참조'],
        ['현재 턴 번호', '전투 시작 후 경과 턴 수 (1, 2, 3...)', 'Integer', '필수', '턴_시스템 1.1'],
        ['글로벌 타이머 잔여 시간', '다음 턴까지 남은 시간 (0~3초)', 'Float', '필수', '턴_시스템 2.1'],
        ['글로벌 타이머 상태', '진행 중 / 일시정지', 'Enum', '필수', '턴_시스템 2.3'],
        ['일시정지 사유', '카드 사용 중 / 메뉴 / 컷신', 'Enum', '권장', '턴_시스템 2.3'],
        ['게임 속도 배율', '1x / 1.5x / 2x', 'Enum', '권장', '턴_시스템 2.4'],
    ]
    story.append(create_table(data))

    story.append(Paragraph("1.2 전투 상태", styles['SubsectionTitle']))
    data = [
        ['데이터 명', '표시 값', '데이터 타입', '중요도', '참조'],
        ['전투 상태', '진행 중 / 승리 / 패배', 'Enum', '필수', '코어루프'],
        ['남은 아군 수', '생존 아군 유닛 수', 'Integer', '필수', '코어루프'],
        ['남은 적 수', '생존 적 유닛 수', 'Integer', '필수', '코어루프'],
    ]
    story.append(create_table(data))

    # ===== 2. 그리드/공간 정보 =====
    story.append(Paragraph("2. 그리드/공간 정보", styles['SectionTitle']))

    story.append(Paragraph("2.1 그리드 기본", styles['SubsectionTitle']))
    data = [
        ['데이터 명', '표시 값', '데이터 타입', '중요도', '참조'],
        ['그리드 크기', '행 x 열 (3x3, 4x4, 5x5)', 'Integer Pair', '필수', '반그리드 2.1'],
        ['아군 진영 셀 목록', '아군 배치 가능 셀 좌표', 'Array<CellCoord>', '필수', '반그리드 2.2'],
        ['적 진영 셀 목록', '적 배치 셀 좌표', 'Array<CellCoord>', '필수', '반그리드 2.2'],
    ]
    story.append(create_table(data))

    story.append(Paragraph("2.2 셀 정보", styles['SubsectionTitle']))
    data = [
        ['데이터 명', '표시 값', '데이터 타입', '중요도', '참조'],
        ['셀별 유닛 정보', '각 셀에 위치한 유닛 ID', 'Map<CellCoord, UnitID>', '필수', '반그리드'],
        ['셀 상태', '빈 셀 / 점유 / 이동 불가 / 특수 효과', 'Enum', '필수', '반그리드 3.2'],
    ]
    story.append(create_table(data))

    story.append(Paragraph("2.3 타겟팅/범위", styles['SubsectionTitle']))
    data = [
        ['데이터 명', '표시 값', '데이터 타입', '중요도', '참조'],
        ['현재 타겟 유닛', '선택된 타겟 유닛 ID', 'UnitID', '필수', '반그리드'],
        ['유효 타겟 목록', '현재 선택한 카드로 타겟 가능한 유닛', 'Array<UnitID>', '필수', '반그리드 4.2'],
        ['효과 범위 셀 목록', '효과가 적용될 셀 좌표', 'Array<CellCoord>', '필수', '반그리드 4.3'],
        ['이동 가능 셀 목록', '유닛이 이동 가능한 셀 좌표', 'Array<CellCoord>', '권장', '반그리드 3.1'],
        ['같은 행 유닛 목록', '같은 행에 위치한 유닛', 'Array<UnitID>', '권장', '반그리드'],
        ['위험 범위 셀 목록', '적이 다음 턴에 공격할 예상 셀', 'Array<CellCoord>', '권장', '인텐트 7.4'],
    ]
    story.append(create_table(data))

    story.append(PageBreak())

    # ===== 3. 아군 유닛 정보 =====
    story.append(Paragraph("3. 아군 유닛 정보", styles['SectionTitle']))

    story.append(Paragraph("3.1 기본 스탯", styles['SubsectionTitle']))
    data = [
        ['데이터 명', '표시 값', '데이터 타입', '중요도', '참조'],
        ['유닛 ID', '고유 식별자', 'FName', '필수', '코어루프'],
        ['유닛 이름', '표시 이름', 'String', '필수', '코어루프'],
        ['현재 HP', '현재 체력', 'Integer', '필수', '코어루프'],
        ['최대 HP', '최대 체력', 'Integer', '필수', '코어루프'],
        ['보호막', '현재 보호막 수치', 'Integer', '필수', '코어루프'],
        ['방어력', '현재 방어력', 'Integer', '권장', '코어루프'],
        ['스피드', '동시 발동 시 처리 순서 (1~100)', 'Integer', '필수', '턴_시스템 4.1'],
        ['기본 데미지', '기본 공격력 수치', 'Integer', '권장', '코어루프'],
        ['그리드 위치', '행, 열 좌표', 'CellCoord', '필수', '반그리드'],
        ['생존 상태', '생존 / 사망 / 부활 대기', 'Enum', '필수', '코어루프'],
    ]
    story.append(create_table(data))

    story.append(Paragraph("3.2 AP (행동력)", styles['SubsectionTitle']))
    data = [
        ['데이터 명', '표시 값', '데이터 타입', '중요도', '참조'],
        ['현재 AP', '현재 보유 AP', 'Integer', '필수', '카드_시스템 5.1'],
        ['최대 AP', '최대 AP 용량', 'Integer', '필수', '카드_시스템 5.1'],
        ['턴당 AP 회복량', '매 턴 회복되는 AP', 'Integer', '선택', '카드_시스템 5.1'],
    ]
    story.append(create_table(data))

    story.append(Paragraph("3.3 턴 관련", styles['SubsectionTitle']))
    data = [
        ['데이터 명', '표시 값', '데이터 타입', '중요도', '참조'],
        ['턴 주기', '인텐트 행동 간격 (1~7턴)', 'Integer', '필수', '턴_시스템 3.3'],
        ['현재 턴 카운터', '행동까지 남은 턴 수 (0이면 발동)', 'Integer', '필수', '턴_시스템 3.1'],
        ['카운터 상태', '일반 / 경고(1) / 발동 중(0)', 'Enum', '필수', '턴_시스템 3.2'],
    ]
    story.append(create_table(data))

    story.append(Paragraph("3.4 상태 효과 (버프/디버프)", styles['SubsectionTitle']))
    data = [
        ['데이터 명', '표시 값', '데이터 타입', '중요도', '참조'],
        ['버프 목록', '적용 중인 버프 리스트', 'Array<BuffData>', '필수', '턴_시스템 6.3'],
        ['디버프 목록', '적용 중인 디버프 리스트', 'Array<DebuffData>', '필수', '턴_시스템 6.3'],
        ['효과별 ID', '효과 고유 식별자', 'FName', '필수', '턴_시스템'],
        ['효과별 이름', '효과 표시 이름', 'String', '필수', '턴_시스템'],
        ['효과별 아이콘', '효과 아이콘 리소스', 'Texture2D', '필수', '턴_시스템'],
        ['효과별 잔여 턴', '남은 지속 턴 수', 'Integer', '필수', '턴_시스템 6.3'],
        ['효과별 스택 수', '중첩 가능 효과의 스택 수', 'Integer', '필수', '턴_시스템'],
        ['효과별 설명', '효과 설명 텍스트', 'String', '권장', '턴_시스템'],
    ]
    story.append(create_table(data))

    story.append(Paragraph("3.5 무력화 상태", styles['SubsectionTitle']))
    data = [
        ['데이터 명', '표시 값', '데이터 타입', '중요도', '참조'],
        ['무력화 상태', '정상 / 스턴 / 빙결 / 침묵 / 속박', 'Enum', '필수', '턴_시스템 5.3'],
        ['무력화 잔여 턴', '무력화 효과 남은 턴 수', 'Integer', '필수', '턴_시스템 5.3'],
    ]
    story.append(create_table(data))

    story.append(PageBreak())

    # ===== 4. 아군 인텐트 정보 =====
    story.append(Paragraph("4. 아군 인텐트 정보", styles['SectionTitle']))

    story.append(Paragraph("4.1 현재 인텐트", styles['SubsectionTitle']))
    data = [
        ['데이터 명', '표시 값', '데이터 타입', '중요도', '참조'],
        ['현재 활성 인텐트 ID', '현재 실행 중인 인텐트', 'FName', '필수', '인텐트 4.1'],
        ['현재 인텐트 아이콘', '인텐트 아이콘 리소스', 'Texture2D', '필수', '인텐트 7.2'],
        ['현재 인텐트 이름', '인텐트 표시 이름', 'String', '필수', '인텐트'],
        ['현재 인텐트 설명', '인텐트 효과 설명', 'String', '권장', '인텐트'],
        ['실행 조건 충족 여부', '조건 충족 / 불충족', 'Boolean', '필수', '인텐트 3.2'],
        ['예상 실행 행동', '실행 행동 설명', 'String', '권장', '인텐트 3.1'],
        ['예상 대기 행동', '대기 행동 설명 (조건 불충족 시)', 'String', '권장', '인텐트 3.1'],
    ]
    story.append(create_table(data))

    story.append(Paragraph("4.2 인텐트 전환 메뉴", styles['SubsectionTitle']))
    data = [
        ['데이터 명', '표시 값', '데이터 타입', '중요도', '참조'],
        ['보유 인텐트 목록', '해금된 인텐트 ID 리스트 (최대 3개)', 'Array<IntentID>', '필수', '인텐트 2.1'],
        ['각 인텐트 ID', '인텐트 고유 식별자', 'FName', '필수', '인텐트'],
        ['각 인텐트 이름', '인텐트 표시 이름', 'String', '필수', '인텐트'],
        ['각 인텐트 아이콘', '인텐트 아이콘', 'Texture2D', '필수', '인텐트'],
        ['각 인텐트 설명', '인텐트 효과 설명', 'String', '권장', '인텐트'],
        ['각 인텐트 실행 조건', '실행 조건 텍스트', 'String', '권장', '인텐트 3.2'],
        ['각 인텐트 해금 상태', '해금됨 / 미해금', 'Boolean', '필수', '인텐트 2.3'],
        ['인텐트 전환 상태', '정상 / 전환 대기([X])', 'Enum', '권장', '인텐트 4.2.3'],
    ]
    story.append(create_table(data))

    # ===== 5. 캐릭터 카드 슬롯 =====
    story.append(Paragraph("5. 캐릭터 카드 슬롯", styles['SectionTitle']))

    story.append(Paragraph("5.1 슬롯 정보", styles['SubsectionTitle']))
    data = [
        ['데이터 명', '표시 값', '데이터 타입', '중요도', '참조'],
        ['카드 슬롯 수', '해당 캐릭터의 해금된 슬롯 개수 (1~5)', 'Integer', '필수', '카드_시스템 6.1'],
        ['슬롯별 배치 카드 ID', '각 슬롯에 배치된 카드 (없으면 null)', 'CardID or null', '필수', '카드_시스템 6.2'],
        ['슬롯별 배치 카드 정보', '배치된 카드의 상세 정보', 'CardData', '필수', '카드_시스템'],
        ['슬롯 잠금 상태', '슬롯별 해금/잠금 상태', 'Boolean', '권장', '카드_시스템 6.1'],
    ]
    story.append(create_table(data))

    story.append(Paragraph("5.2 인챈트 슬롯 (카드 슬롯과 별개)", styles['SubsectionTitle']))
    data = [
        ['데이터 명', '표시 값', '데이터 타입', '중요도', '참조'],
        ['장착된 인챈트 목록', '캐릭터에 장착된 인챈트 카드', 'Array<CardID>', '필수', '카드_시스템 4.3'],
        ['인챈트별 제거 비용', '제거 시 필요한 AP', 'Integer', '필수', '카드_시스템 4.3'],
    ]
    story.append(create_table(data))

    story.append(PageBreak())

    # ===== 6. 캐릭터 고유 자원 =====
    story.append(Paragraph("6. 캐릭터 고유 자원", styles['SectionTitle']))

    story.append(Paragraph("6.1 에르나 전용", styles['SubsectionTitle']))
    data = [
        ['데이터 명', '표시 값', '데이터 타입', '중요도', '참조'],
        ['기억의 조각 현재 스택', '현재 스택 수 (0~5)', 'Integer', '필수', '에르나 기획서'],
        ['기억의 조각 최대값', '최대 스택 수 (5)', 'Integer', '필수', '에르나 기획서'],
        ['현재 무기 형태', '대검 형태 / 대방패 형태', 'Enum', '필수', '에르나 기획서'],
        ['형태별 스탯 변화량', '공격력/방어력 변화량', 'StatModifier', '권장', '에르나 기획서'],
    ]
    story.append(create_table(data))

    story.append(Paragraph("6.2 범용 고유 자원 (향후 캐릭터 확장용)", styles['SubsectionTitle']))
    data = [
        ['데이터 명', '표시 값', '데이터 타입', '중요도', '참조'],
        ['고유 자원 보유 여부', '해당 캐릭터가 고유 자원을 가지는지', 'Boolean', '선택', '인텐트 3.8.3'],
        ['고유 자원 이름', '자원 표시 이름 (분노, 갈증, 집중 등)', 'String', '선택', '인텐트 3.8.3'],
        ['고유 자원 현재값', '현재 축적량', 'Integer', '선택', '인텐트 3.8.3'],
        ['고유 자원 최대값', '최대 축적량', 'Integer', '선택', '인텐트 3.8.3'],
        ['고유 자원 아이콘', '자원 아이콘', 'Texture2D', '선택', '인텐트 3.8.3'],
    ]
    story.append(create_table(data))

    # ===== 7. 적 유닛 정보 =====
    story.append(Paragraph("7. 적 유닛 정보", styles['SectionTitle']))

    story.append(Paragraph("7.1 기본 스탯", styles['SubsectionTitle']))
    data = [
        ['데이터 명', '표시 값', '데이터 타입', '중요도', '참조'],
        ['유닛 ID', '고유 식별자', 'FName', '필수', '몬스터_AI'],
        ['유닛 이름', '표시 이름', 'String', '필수', '몬스터_AI'],
        ['현재 HP', '현재 체력', 'Integer', '필수', '몬스터_AI'],
        ['최대 HP', '최대 체력', 'Integer', '필수', '몬스터_AI'],
        ['보호막', '현재 보호막 수치', 'Integer', '권장', '몬스터_AI'],
        ['방어력', '현재 방어력', 'Integer', '선택', '몬스터_AI'],
        ['스피드', '동시 발동 시 처리 순서', 'Integer', '권장', '턴_시스템 4.1'],
        ['그리드 위치', '행, 열 좌표', 'CellCoord', '필수', '반그리드'],
        ['적 유형', '일반몹 / 정예몹 / 보스', 'Enum', '필수', '인텐트 6.2'],
        ['유닛 크기', '1x1 / 2x1 / 2x2', 'Enum', '권장', '반그리드 6.1'],
        ['생존 상태', '생존 / 사망', 'Enum', '필수', '몬스터_AI'],
    ]
    story.append(create_table(data))

    story.append(Paragraph("7.2 턴/인텐트", styles['SubsectionTitle']))
    data = [
        ['데이터 명', '표시 값', '데이터 타입', '중요도', '참조'],
        ['턴 주기', '인텐트 행동 간격', 'Integer', '필수', '턴_시스템'],
        ['현재 턴 카운터', '행동까지 남은 턴 수', 'Integer', '필수', '턴_시스템'],
        ['현재 인텐트 ID', '현재 실행 예정 인텐트', 'FName', '필수', '인텐트 6.1'],
        ['현재 인텐트 아이콘', '인텐트 아이콘', 'Texture2D', '필수', '인텐트 6.3.1'],
        ['인텐트 유형', '공격/방어/회복/버프/디버프/소환/이동/특수', 'Enum', '필수', '인텐트 6.3.1'],
        ['예상 수치', '예상 데미지/회복량/버프 수치', 'Integer', '권장', '인텐트'],
        ['실행 조건 충족 여부', '조건 충족 / 불충족', 'Boolean', '권장', '인텐트'],
    ]
    story.append(create_table(data))

    story.append(PageBreak())

    # ===== 8. 보스 전용 정보 =====
    story.append(Paragraph("8. 보스 전용 정보", styles['SectionTitle']))

    story.append(Paragraph("8.1 페이즈 시스템", styles['SubsectionTitle']))
    data = [
        ['데이터 명', '표시 값', '데이터 타입', '중요도', '참조'],
        ['현재 페이즈', '페이즈 번호 (1, 2, 3...)', 'Integer', '필수', '몬스터_AI'],
        ['총 페이즈 수', '해당 보스의 총 페이즈 수', 'Integer', '필수', '몬스터_AI'],
        ['페이즈 전환 HP 임계값', '다음 페이즈 전환 HP% (66%, 33% 등)', 'Float (%)', '권장', '몬스터_AI'],
        ['페이즈별 이름', '각 페이즈 표시 이름', 'String', '선택', '몬스터_AI'],
    ]
    story.append(create_table(data))

    story.append(Paragraph("8.2 인터럽트 시스템", styles['SubsectionTitle']))
    data = [
        ['데이터 명', '표시 값', '데이터 타입', '중요도', '참조'],
        ['인터럽트 가능 여부', '현재 행동이 중단 가능한지', 'Boolean', '권장', '몬스터_AI'],
        ['인터럽트 진행도', '중단 가능 행동의 현재 진행률', 'Float (0~100%)', '권장', '몬스터_AI'],
        ['인터럽트 조건', '중단에 필요한 조건', 'String', '선택', '몬스터_AI'],
    ]
    story.append(create_table(data))

    # ===== 9. 카드 시스템 정보 =====
    story.append(Paragraph("9. 카드 시스템 정보", styles['SectionTitle']))

    story.append(Paragraph("9.1 덱 상태", styles['SubsectionTitle']))
    data = [
        ['데이터 명', '표시 값', '데이터 타입', '중요도', '참조'],
        ['덱 남은 장수', '현재 덱에 남은 카드 수', 'Integer', '필수', '카드_시스템 2.2'],
        ['덱 총 장수', '덱 총 카드 수 (최대 40)', 'Integer', '권장', '카드_시스템 2.2'],
        ['덱 카드 목록', '덱에 있는 카드 ID 리스트 (비공개)', 'Array<CardID>', '선택', '카드_시스템'],
    ]
    story.append(create_table(data))

    story.append(Paragraph("9.2 묘지 (버린 카드 더미)", styles['SubsectionTitle']))
    data = [
        ['데이터 명', '표시 값', '데이터 타입', '중요도', '참조'],
        ['묘지 카드 수', '버려진 카드 수', 'Integer', '필수', '카드_시스템 3.5'],
        ['묘지 카드 목록', '버려진 카드 ID 리스트', 'Array<CardID>', '권장', '카드_시스템'],
    ]
    story.append(create_table(data))

    story.append(Paragraph("9.3 핸드 상태", styles['SubsectionTitle']))
    data = [
        ['데이터 명', '표시 값', '데이터 타입', '중요도', '참조'],
        ['현재 핸드 장수', '현재 보유 중인 카드 수 (0~5)', 'Integer', '필수', '카드_시스템 3.2'],
        ['최대 핸드 장수', '핸드 제한 (기본 5)', 'Integer', '필수', '카드_시스템 3.2'],
        ['핸드 카드 목록', '핸드에 있는 카드 ID 리스트', 'Array<CardID>', '필수', '카드_시스템'],
        ['버리기 예약 카드 목록', '다음 턴에 버려질 카드 리스트', 'Array<CardID>', '필수', '카드_시스템 3.3'],
    ]
    story.append(create_table(data))

    story.append(PageBreak())

    story.append(Paragraph("9.4 개별 카드 정보", styles['SubsectionTitle']))
    data = [
        ['데이터 명', '표시 값', '데이터 타입', '중요도', '참조'],
        ['카드 ID', '고유 식별자', 'FName', '필수', '카드_시스템'],
        ['카드 이름', '표시 이름', 'String', '필수', '카드_시스템'],
        ['카드 타입', '액션 / 리액션 / 인챈트', 'Enum', '필수', '카드_시스템 4.1~4.3'],
        ['카드 아이콘/아트', '카드 이미지 리소스', 'Texture2D', '필수', '카드_시스템'],
        ['AP 코스트', '사용에 필요한 AP', 'Integer', '필수', '카드_시스템 5.1'],
        ['동적 코스트 여부', '스탯에 따라 코스트 변동 여부', 'Boolean', '권장', '카드_시스템 8.2.1'],
        ['계산된 실제 코스트', '현재 캐릭터 기준 실제 코스트', 'Integer', '권장', '카드_시스템 8.2.1'],
        ['카드 설명', '효과 설명 텍스트', 'String', '필수', '카드_시스템'],
        ['사용 조건', '사용 제한 조건 텍스트', 'String', '권장', '카드_시스템 8.2.3'],
        ['조건 충족 여부', '현재 사용 가능 여부', 'Boolean', '필수', '카드_시스템'],
    ]
    story.append(create_table(data))

    # ===== 10. 행동 순서 (액션 바) =====
    story.append(Paragraph("10. 행동 순서 (액션 바)", styles['SectionTitle']))

    story.append(Paragraph("10.1 동시 발동 정보", styles['SubsectionTitle']))
    data = [
        ['데이터 명', '표시 값', '데이터 타입', '중요도', '참조'],
        ['동시 발동 유닛 목록', '현재 턴에 인텐트 발동하는 유닛 리스트', 'Array<UnitID>', '필수', '턴_시스템 8.3'],
        ['발동 순서', '스피드 기준 정렬된 순서', 'Array<{UnitID, Speed, Order}>', '필수', '턴_시스템 4.3'],
        ['현재 행동 중 유닛', '현재 인텐트 실행 중인 유닛 ID', 'UnitID', '필수', '턴_시스템'],
        ['대기 중 유닛 목록', '순서 대기 중인 유닛 리스트', 'Array<UnitID>', '권장', '턴_시스템'],
    ]
    story.append(create_table(data))

    story.append(Paragraph("10.2 유닛별 행동 정보", styles['SubsectionTitle']))
    data = [
        ['데이터 명', '표시 값', '데이터 타입', '중요도', '참조'],
        ['유닛 아이콘', '유닛 초상화/아이콘', 'Texture2D', '필수', '코어루프'],
        ['유닛 스피드', '해당 유닛의 스피드 수치', 'Integer', '권장', '턴_시스템'],
        ['유닛 진영', '아군 / 적군', 'Enum', '필수', '코어루프'],
        ['예상 행동', '해당 유닛의 예상 행동 요약', 'String', '선택', '인텐트'],
    ]
    story.append(create_table(data))

    # ===== 11. 플로팅 텍스트 / 연출 데이터 =====
    story.append(Paragraph("11. 플로팅 텍스트 / 연출 데이터", styles['SectionTitle']))

    story.append(Paragraph("11.1 데미지/회복 표시", styles['SubsectionTitle']))
    data = [
        ['데이터 명', '표시 값', '데이터 타입', '중요도', '참조'],
        ['데미지 수치', '피격 시 표시할 데미지', 'Integer', '필수', '코어루프'],
        ['회복량 수치', '회복 시 표시할 수치', 'Integer', '필수', '코어루프'],
        ['보호막 데미지', '보호막에 적용된 데미지', 'Integer', '권장', '코어루프'],
        ['보호막 획득량', '획득한 보호막 수치', 'Integer', '권장', '코어루프'],
        ['데미지 대상 유닛', '데미지를 받은 유닛 ID', 'UnitID', '필수', '코어루프'],
        ['회복 대상 유닛', '회복을 받은 유닛 ID', 'UnitID', '필수', '코어루프'],
    ]
    story.append(create_table(data))

    story.append(Paragraph("11.2 크리티컬/특수 효과", styles['SubsectionTitle']))
    data = [
        ['데이터 명', '표시 값', '데이터 타입', '중요도', '참조'],
        ['크리티컬 발생 여부', '크리티컬 히트 여부', 'Boolean', '필수', '코어루프'],
        ['크리티컬 배율', '크리티컬 데미지 배율', 'Float', '권장', '코어루프'],
        ['회피 발생 여부', '공격 회피 여부', 'Boolean', '권장', '코어루프'],
        ['블록 발생 여부', '공격 블록 여부', 'Boolean', '권장', '코어루프'],
        ['면역 여부', '효과 면역 여부', 'Boolean', '권장', '턴_시스템'],
    ]
    story.append(create_table(data))

    story.append(PageBreak())

    # ===== 12. 전투 로그 =====
    story.append(Paragraph("12. 전투 로그", styles['SectionTitle']))

    story.append(Paragraph("12.1 행동 로그", styles['SubsectionTitle']))
    data = [
        ['데이터 명', '표시 값', '데이터 타입', '중요도', '참조'],
        ['최근 행동 로그 목록', '최근 발생한 행동 기록 리스트', 'Array<ActionLog>', '권장', '코어루프'],
        ['로그 타임스탬프', '행동 발생 시간', 'Float', '권장', '코어루프'],
        ['행동 주체', '행동을 수행한 유닛 ID', 'UnitID', '권장', '코어루프'],
        ['행동 유형', '공격/방어/스킬/이동 등', 'Enum', '권장', '코어루프'],
        ['행동 대상', '행동 대상 유닛 ID 목록', 'Array<UnitID>', '권장', '코어루프'],
        ['결과 수치', '데미지/회복량 등', 'Integer', '권장', '코어루프'],
    ]
    story.append(create_table(data))

    # ===== 13. 전투 결과 화면 =====
    story.append(Paragraph("13. 전투 결과 화면", styles['SectionTitle']))

    story.append(Paragraph("13.1 결과 정보", styles['SubsectionTitle']))
    data = [
        ['데이터 명', '표시 값', '데이터 타입', '중요도', '참조'],
        ['전투 결과', '승리 / 패배', 'Enum', '필수', '코어루프'],
        ['경과 턴 수', '전투에서 경과한 총 턴 수', 'Integer', '권장', '턴_시스템'],
        ['처치한 적 수', '이번 전투에서 처치한 적 수', 'Integer', '권장', '코어루프'],
        ['사용한 카드 수', '이번 전투에서 사용한 카드 수', 'Integer', '선택', '카드_시스템'],
    ]
    story.append(create_table(data))

    story.append(Paragraph("13.2 파티 상태", styles['SubsectionTitle']))
    data = [
        ['데이터 명', '표시 값', '데이터 타입', '중요도', '참조'],
        ['생존 아군 목록', '전투 후 생존한 아군', 'Array<UnitID>', '필수', '코어루프'],
        ['아군별 남은 HP', '각 아군의 현재 HP', 'Integer per Unit', '권장', '코어루프'],
        ['사망 아군 목록', '전투 중 사망한 아군', 'Array<UnitID>', '권장', '코어루프'],
    ]
    story.append(create_table(data))

    story.append(Paragraph("13.3 보상 정보", styles['SubsectionTitle']))
    data = [
        ['데이터 명', '표시 값', '데이터 타입', '중요도', '참조'],
        ['획득 보상 목록', '전투 종료 시 획득 보상', 'Array<RewardData>', '필수', '코어루프'],
        ['보상 유형', '카드 / 골드 / 유물 / 기타', 'Enum', '필수', '코어루프'],
        ['보상 ID', '획득한 보상 ID', 'FName', '필수', '코어루프'],
        ['보상 이름', '획득한 보상 이름', 'String', '필수', '코어루프'],
        ['보상 아이콘', '보상 아이콘', 'Texture2D', '필수', '코어루프'],
        ['보상 수량', '획득 수량', 'Integer', '필수', '코어루프'],
    ]
    story.append(create_table(data))

    # ===== 14~17 요약 =====
    story.append(PageBreak())
    story.append(Paragraph("14~17. 추가 시스템 요약", styles['SectionTitle']))

    story.append(Paragraph("주요 추가 데이터 영역:", styles['BodyKorean']))
    story.append(Spacer(1, 0.3*cm))

    summary_data = [
        ['섹션', '주요 데이터'],
        ['14. 시스템/메뉴 UI', '일시정지 상태, 메뉴 옵션, 게임 속도, 포기 확인'],
        ['15. 툴팁/상세 정보', '유닛/카드/효과/인텐트 상세 정보 팝업'],
        ['16. 드로우/카드 이동', '드로우 이벤트, 버리기 이벤트, 리셔플 이벤트'],
        ['17. 추가 고려 데이터', '튜토리얼, 전투 통계, 콤보 시스템'],
    ]
    summary_table = Table(summary_data, colWidths=[5*cm, 11*cm])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER_BG),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, -1), FONT_NAME),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, HEADER_BG),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, CREAM_BG]),
    ]))
    story.append(summary_table)

    # ===== 요약 통계 =====
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("데이터 요약 통계", styles['SectionTitle']))

    stats_data = [
        ['중요도', '개수', '비율'],
        ['필수', '약 120개', '60%'],
        ['권장', '약 60개', '30%'],
        ['선택', '약 20개', '10%'],
        ['총계', '약 200개', '100%'],
    ]
    stats_table = Table(stats_data, colWidths=[4*cm, 4*cm, 4*cm])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER_BG),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, -1), FONT_NAME),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, HEADER_BG),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 1), (0, 1), PRIMARY_COLOR),
        ('TEXTCOLOR', (0, 1), (0, 1), white),
        ('BACKGROUND', (0, 2), (0, 2), SECONDARY_COLOR),
        ('TEXTCOLOR', (0, 2), (0, 2), white),
        ('BACKGROUND', (0, 3), (0, 3), OPTIONAL_COLOR),
        ('TEXTCOLOR', (0, 3), (0, 3), white),
        ('BACKGROUND', (0, 4), (-1, 4), CREAM_BG),
        ('FONTNAME', (0, 4), (-1, 4), FONT_BOLD),
    ]))
    story.append(stats_table)

    # ===== 문서 정보 =====
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("문서 정보", styles['SectionTitle']))

    info_data = [
        ['항목', '내용'],
        ['버전', 'v2.0'],
        ['작성일', '2026-02-04'],
        ['목적', 'UI 디자이너가 전투 시스템에서 표시해야 할 데이터 요소 파악'],
        ['범위', '전투 시스템 UI 데이터 요소 정의 (디자인/UX 제외)'],
    ]
    info_table = Table(info_data, colWidths=[4*cm, 12*cm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER_BG),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, -1), FONT_NAME),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, HEADER_BG),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (0, -1), CREAM_BG),
    ]))
    story.append(info_table)

    # PDF 빌드
    doc.build(story)
    print(f"PDF 생성 완료: {output_path}")
    return output_path

if __name__ == "__main__":
    build_document()
