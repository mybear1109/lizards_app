import streamlit as st

# ✅ 표종별 설명 데이터
def get_species_info():
    return {
"Beardy Dragon": "비어디 드래곤은 온순한 성격을 가진 도마뱀으로, 호주의 사막 지역에서 서식합니다. 특징적인 턱 아래 수염 모양의 비늘을 가지고 있으며, 체온 조절을 위해 수염을 펼치기도 합니다. 잡식성으로 곤충과 식물을 모두 먹습니다.",
"Panther Chamaeleon": "팬서 카멜레온은 마다가스카르 출신으로 화려한 색 변화 능력을 가지고 있습니다. 독립적인 눈 움직임과 긴 혀를 이용해 먹이를 사냥합니다. 수컷은 더 화려한 색상을 띠며, 크기도 더 큽니다.",
"Crestedgeko": "크레스티드 게코는 나무 위에서 생활하며 점착성 패드를 이용해 벽을 기어오를 수 있습니다. 머리에서 꼬리까지 이어지는 특징적인 볏을 가지고 있으며, 야행성입니다. 과일과 곤충을 주로 먹습니다.",
"Leopardgeko": "레오파드 게코는 인기 있는 애완용 도마뱀으로 야행성이며 관리가 비교적 쉽습니다. 몸에 표범 무늬 같은 반점이 특징적이며, 꼬리를 자발적으로 떼어낼 수 있는 자할 능력이 있습니다. 주로 곤충을 먹습니다.",
"Iguana": "이구아나는 크기가 크며 초식성이 강한 도마뱀으로, 강한 햇빛을 좋아합니다. 등에 있는 가시 모양의 돌기와 턱 아래의 큰 피부 주름이 특징적입니다. 나무를 잘 타고, 수영도 능숙합니다.",
"Frog": "개구리는 양서류로, 물과 육지를 오가며 생활합니다. 피부로 호흡할 수 있으며, 긴 혀로 먹이를 잡습니다. 올챙이에서 성체로 변태하는 과정을 거칩니다.",
"Salamander": "도롱뇽은 양서류로, 꼬리가 있는 것이 특징입니다. 습한 환경을 선호하며, 피부로 호흡합니다. 일부 종은 네온톤의 화려한 색상을 가지고 있습니다.",
"Snake": "뱀은 다리가 없는 파충류로, 비늘로 덮인 긴 몸을 가지고 있습니다. 독을 가진 종도 있으며, 먹이를 통째로 삼킵니다. 주기적으로 허물을 벗습니다.",
"Turtle": "거북은 등딱지와 배딱지로 보호된 파충류입니다. 수생, 육지, 반수생 종이 있으며, 오랜 수명을 가진 것으로 알려져 있습니다. 대부분의 종이 알을 낳아 번식합니다.",
"Newt": "뉴트는 작은 도롱뇽과 비슷하며 수생과 육지를 오가며 생활합니다. 성체가 되어도 꼬리를 유지하며, 일부 종은 독성 물질을 분비하여 포식자로부터 자신을 보호합니다.",
"Pacman": "팩맨 개구리는 둥글고 큰 입을 가진 개구리로, 작은 먹이를 통째로 삼킵니다. 몸집에 비해 매우 큰 입을 가지고 있어 자신보다 큰 먹이도 잡아먹을 수 있습니다. 땅속에 숨어 지내는 습성이 있습니다.",
"Toad": "두꺼비는 피부가 거칠고 마른 환경에서도 잘 견딜 수 있습니다. 대부분의 종이 독성 물질을 분비하여 포식자로부터 자신을 보호합니다. 주로 밤에 활동하며 곤충을 먹습니다.",
"Leachianus Gecko": "르차이아너스 게코는 세계에서 가장 큰 게코로 알려져 있으며, 나무 위에서 생활합니다. 뉴칼레도니아가 원산지이며, 야행성입니다. 과일과 곤충을 주로 먹습니다.",
"Gecko": "게코는 작은 도마뱀 종류로 벽을 타고 오를 수 있는 강한 접착력을 가진 발을 가지고 있습니다. 대부분의 종이 야행성이며, 독특한 울음소리를 내는 것으로 알려져 있습니다.",
"Chahoua Gecko": "차후아 게코는 뉴칼레도니아에서 발견되며, 독특한 피부 패턴을 가지고 있습니다. 나무 위에서 생활하며, 야행성입니다. 과일과 곤충을 주식으로 합니다.",
"Gargoyle Gecko": "가고일 게코는 독특한 돌출된 눈썹과 강한 점착력을 가진 발을 특징으로 합니다. 뉴칼레도니아가 원산지이며, 나무 위에서 생활합니다. 과일과 곤충을 먹습니다.",
"Skink": "스킨크는 매끄러운 비늘과 강한 꼬리를 가진 도마뱀으로, 다양한 환경에서 살아갑니다. 일부 종은 다리가 퇴화되어 뱀과 비슷한 모습을 하고 있습니다. 주로 곤충을 먹습니다.",
"Chamaeleon": "카멜레온은 색을 변화시키고 긴 혀를 이용해 먹이를 잡는 능력을 가진 특별한 도마뱀입니다. 독립적으로 움직이는 눈과 집게 모양의 발이 특징적입니다. 대부분의 종이 나무 위에서 생활합니다."
    }

# ✅ 표종 설명을 가져오는 함수
def get_species_description(species_name):
    species_info = get_species_info()
    return species_info.get(species_name, "해당 표종에 대한 설명이 없습니다.")