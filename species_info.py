import os
import streamlit as st

# ✅ 도마뱀 종에 대한 정보를 반환하는 함수
def get_species_info(species_name):
    """ 주어진 도마뱀 종(species_name)에 대한 정보를 반환하는 함수 """
    species_data = {
    "0.개구리(Frog)": {
    "설명": "개구리는 양서류에 속하는 동물로, 물과 육지를 오가며 생활합니다. 유생 시기에는 올챙이로 아가미 호흡을 하며 물에서 살다가, 성체가 되면 폐와 피부 호흡을 하며 주로 육지에서 생활합니다. 개구리는 전 세계적으로 약 5,000종이 알려져 있으며, 크기는 1cm 미만부터 30cm 이상까지 다양합니다. 많은 종이 독특한 울음소리로 의사소통하며, 일부 종은 독성을 가져 포식자로부터 자신을 보호합니다. 개구리는 생태계에서 해충 조절자로서 중요한 역할을 하며, 환경 변화의 지표 역할도 합니다.",
    "서식지": "개구리는 습도가 높고 물가나 습지에 가까운 곳에서 주로 서식합니다. 강, 연못, 습지, 열대우림, 온대 숲 등 다양한 환경에서 발견됩니다. 일부 종은 나무 위에서 생활하거나 사막과 같은 건조한 환경에 적응하기도 했습니다. 개구리는 피부 호흡 때문에 대부분 습한 환경을 선호하지만, 적응력이 뛰어나 다양한 서식지에서 생존할 수 있습니다.",
    "먹이": "개구리는 주로 육식성으로, 곤충, 거미, 지렁이 등 작은 무척추동물을 먹습니다. 큰 종의 경우 작은 어류, 설치류, 새끼 새 등도 잡아먹습니다. 올챙이 시기에는 주로 조류나 수생 식물을 먹지만, 일부 종은 육식성 올챙이도 있습니다. 개구리는 대부분 움직이는 먹이만 포착하며, 긴 점착성 혀를 이용해 빠르게 먹이를 잡아챕니다.",
    "특징": "1.긴 혀를 이용한 빠른 먹이 사냥\n2.피부 호흡 능력\n3.변태 과정을 거치는 생활사\n4.강한 뒷다리를 이용한 뛰어난 점프 능력\n5.수컷의 특징적인 울음소리를 통한 의사소통\n6.눈 뒤의 고막을 통한 청각\n7.일부 종의 독성 분비 능력\n8.환경 변화에 민감한 특성\n9.겨울철 동면 능력 (일부 종)\n10.피부색 변화 능력 (일부 종)",
    "이미지": "images/6 Frog.jpg"
    },
    "1.거북이(Turtle)": {
    "설명": "거북이는 파충류 중 가장 오래된 그룹 중 하나로, 약 2억 2천만 년 전부터 존재해왔습니다. 등딱지(갑)와 배딱지(복갑)로 보호된 독특한 몸 구조를 가지고 있으며, 이는 갈비뼈가 변형된 것입니다. 거북이는 수생, 반수생, 육지 서식 종으로 나뉘며, 대부분 매우 긴 수명을 가집니다. 일부 종은 100년 이상 살 수 있습니다. 거북이는 온도에 따른 성결정 시스템을 가지고 있어, 알이 부화할 때의 온도에 따라 성별이 결정됩니다.",
    "서식지": "거북이는 전 세계의 다양한 환경에 적응하여 살고 있습니다. 해양 거북이는 열대와 아열대 바다에서, 민물 거북이는 강, 호수, 습지에서 서식합니다. 육지 거북이는 사막, 초원, 열대우림 등 다양한 육상 환경에서 발견됩니다. 일부 종은 담수와 해수를 오가며 살기도 합니다. 거북이의 서식지는 종에 따라 매우 다양하며, 각 환경에 특화된 적응을 보입니다.",
    "먹이": "거북이의 식성은 종에 따라 매우 다양합니다. 대부분의 거북이는 잡식성이지만, 일부는 완전한 초식 또는 육식을 하기도 합니다. 해양 거북이는 해조류, 해파리, 물고기를 먹고, 민물 거북이는 수생 식물, 곤충, 물고기, 양서류를 먹습니다. 육지 거북이는 주로 식물성 먹이를 선호하며, 과일, 채소, 풀을 먹습니다. 일부 거북이는 나이에 따라 식성이 변하기도 합니다.",
    "특징": "1. 단단한 등딱지와 배딱지로 보호된 몸체\n2. 매우 긴 수명\n3. 온도에 따른 성결정\n4. 느린 움직임과 높은 인내력\n5. 수중과 육지에서의 적응력\n6. 긴 목을 이용한 호흡과 먹이 섭취\n7. 강한 턱과 부리 모양의 입\n8. 알을 땅에 묻는 산란 습성\n9. 일부 종의 장거리 이동 능력\n10. 환경 변화에 대한 높은 민감성",
    "이미지": "images/9 Turtle.jpg"
    },
    "2.기타(Other)": {
    "설명": "이 카테고리는 데이터베이스에 구체적으로 분류되지 않은 희귀하거나 특이한 양서류 또는 파충류를 포함합니다. 이들은 새롭게 발견된 종이거나, 분류학적으로 논란이 있는 종일 수 있습니다. 또한 특정 지역에만 서식하는 고유종이나 멸종 위기에 처한 종들도 이 카테고리에 포함될 수 있습니다. 이러한 동물들은 종종 특별한 보호와 연구의 대상이 되며, 생물다양성 보존에 중요한 역할을 합니다.",
    "서식지": "이 카테고리에 속하는 동물들의 서식지는 매우 다양할 수 있습니다. 일부는 특정 섬이나 고립된 지역에서만 발견되는 고유종일 수 있으며, 다른 일부는 극한 환경에 적응한 종일 수 있습니다. 열대우림의 나무 꼭대기부터 깊은 동굴, 고산 지대, 심해에 이르기까지 다양한 환경에서 발견될 수 있습니다. 이들의 서식지는 종종 인간의 활동으로 인해 위협받고 있어 보호가 필요합니다.",
    "먹이": "이 카테고리의 동물들은 매우 다양한 식성을 가질 수 있습니다. 일부는 매우 특화된 식성을 가져 특정 종류의 먹이에만 의존할 수 있으며, 다른 일부는 다양한 먹이를 섭취하는 generalist일 수 있습니다. 곤충, 작은 무척추동물, 어류, 양서류, 파충류, 식물 등 다양한 먹이원을 이용할 수 있습니다. 일부 종은 독특한 사냥 방법이나 특수한 소화 시스템을 가지고 있을 수 있습니다.",
    "특징": "1. 희귀성 또는 제한된 분포\n2. 독특한 형태학적 특징\n3. 특수한 생태적 적응\n4. 분류학적 불확실성\n5. 높은 보존 가치\n6. 특이한 행동 패턴\n7. 극한 환경 적응력\n8. 독특한 생식 방식\n9. 특별한 방어 메커니즘\n10. 과학적 연구 가치",
    "이미지": "images/5 Other.jpg"
    },
    "3.뉴트(newt)": {
    "설명": "뉴트는 도롱뇽과에 속하는 양서류로, 수생과 육지 생활을 모두 하는 특징이 있습니다. 성체가 되면 물과 육지를 오가며 생활하지만, 유생 시기에는 완전히 수생 생활을 합니다. 뉴트는 놀라운 재생 능력을 가지고 있어, 손상된 사지나 기관을 재생할 수 있습니다. 많은 종이 피부에 독성 물질을 분비하여 포식자로부터 자신을 보호합니다. 번식기에는 수컷이 화려한 색상과 지느러미 모양의 등 크레스트를 발달시키는 경우가 많습니다.",
    "서식지": "뉴트는 주로 북반구의 온대 지역에 분포하며, 습지, 연못, 개울, 숲의 습한 지역 등에서 서식합니다. 일부 종은 건조한 환경에서도 살아갈 수 있지만, 대부분은 수분이 풍부한 환경을 선호합니다. 겨울에는 물속이나 땅속에서 동면을 하기도 합니다.",
    "먹이": "뉴트는 주로 육식성으로, 작은 수생 무척추동물, 물벼룩, 곤충 유충, 작은 물고기, 개구리 알 등을 먹습니다. 육상에서는 지렁이, 달팽이, 곤충 등을 사냥합니다. 유생 시기에는 주로 플랑크톤을 먹지만, 성장하면서 점차 더 큰 먹이를 섭취하게 됩니다.",
    "특징": "1. 뛰어난 재생 능력\n2. 수생과 육상 생활 겸업\n3. 독성 분비를 통한 자기 방어\n4. 번식기의 성적 이형성 (수컷의 화려한 외모)\n5. 변태 과정을 거치는 생활사\n6. 피부 호흡 능력\n7. 꼬리를 이용한 수영\n8. 겨울철 동면\n9. 페로몬을 통한 의사소통\n10. 일부 종의 네오테니 (유생 형태로 성체가 됨)",
    "이미지": "images/newt.jpg"
    },
    "4.도롱뇽(Salamander)": {
    "설명": "도롱뇽은 꼬리가 있는 양서류로, 습한 환경을 선호합니다. 대부분의 종은 육상 생활을 하지만, 일부는 완전한 수생 생활을 합니다. 도롱뇽은 뉴트와 마찬가지로 놀라운 재생 능력을 가지고 있어, 손실된 사지나 기관을 재생할 수 있습니다. 많은 종이 밝은 색상이나 무늬로 포식자에게 자신의 독성을 경고합니다. 일부 대형 종은 폐가 퇴화되어 전적으로 피부와 입천장을 통해 호흡합니다.",
    "서식지": "도롱뇽은 주로 북반구의 온대 및 아열대 지역에 분포하며, 습지, 숲, 동굴, 고산 지대 등 다양한 환경에서 발견됩니다. 대부분의 종은 습한 환경을 필요로 하지만, 일부는 건조한 지역에 적응하기도 했습니다. 많은 종이 낙엽 아래나 통나무 속, 바위 밑 등 은신처를 이용합니다.",
    "먹이": "도롱뇽은 주로 육식성으로, 곤충, 거미, 지렁이, 달팽이, 작은 갑각류 등 다양한 무척추동물을 먹습니다. 큰 종의 경우 작은 척추동물도 사냥합니다. 수생 종은 물벼룩, 곤충 유충, 작은 물고기 등을 주로 먹습니다. 도롱뇽은 대개 야행성이며, 밤에 활발히 먹이 활동을 합니다.",
    "특징": "1. 뛰어난 재생 능력\n2. 독성 피부 분비물\n3. 다양한 서식 환경 적응\n4. 변태 과정을 거치는 생활사\n5. 피부 호흡\n6. 일부 종의 네오테니 (유생 형태로 성체가 됨)\n7. 야행성 습성\n8. 느린 대사율과 긴 수명\n9. 페로몬을 통한 의사소통\n10. 환경 오염에 대한 높은 민감성",
    "이미지": "images/7 Salamander.jpg"
    },
    "5.두꺼비(Toad)": {
    "설명": "두꺼비는 개구리와 비슷하지만 피부가 더 건조하고 거칠며, 주로 육상 생활에 적응했습니다. 대부분의 두꺼비는 뒷다리가 짧아 뛰는 것보다는 걷는 것을 선호합니다. 많은 종이 이어(귀샘)라는 특별한 샘을 통해 독성 물질을 분비하여 포식자로부터 자신을 보호합니다. 두꺼비는 주로 밤에 활동하며, 낮에는 돌 밑이나 땅속에 숨어 지냅니다. 번식기에는 물가로 모여들어 긴 끈 모양의 알을 낳습니다.",
    "서식지": "두꺼비는 남극을 제외한 모든 대륙에 분포하며, 다양한 서식지에 적응했습니다. 습한 숲, 초원, 정원, 농경지, 사막 등에서 발견됩니다. 많은 종이 인간의 주거 지역 근처에서도 잘 적응하여 살아갑니다. 번식기에는 물가로 이동하지만, 대부분의 시간을 육지에서 보냅니다.",
    "먹이": "두꺼비는 주로 육식성으로, 곤충, 지렁이, 달팽이, 거미 등 다양한 무척추동물을 먹습니다. 큰 종의 경우 작은 설치류나 도마뱀도 잡아먹을 수 있습니다. 두꺼비는 주로 움직이는 먹이를 포착하며, 긴 점착성 혀를 이용해 빠르게 먹이를 잡아챕니다. 농업에서 해충 통제에 도움을 주는 이로운 동물로 여겨집니다.",
    "특징": "1. 거칠고 마른 피부\n2. 독성 분비물을 생성하는 이어(귀샘)\n3. 야행성 습성\n4. 육상 생활에 적응된 짧은 뒷다리\n5. 긴 혀를 이용한 사냥\n6. 번식기의 집단 산란\n7. 변태 과정을 거치는 생활사\n8. 동면 또는 하면 능력\n9. 강한 환경 적응력\n10. 농업에서의 해충 통제 역할",
    "이미지": "images/toad.jpg"
    }
    ,
    "6.레오파드 게코(Leopardgeko)": {
    "설명": "레오파드 게코는 인기 있는 애완용 도마뱀으로, 이름은 그들의 특징적인 반점 무늬에서 유래했습니다. 야행성이며 온순한 성격으로 관리가 비교적 쉽습니다. 이 게코는 꼬리를 자발적으로 떼어내는 자할(autotomy) 능력이 있어, 위험 시 포식자의 주의를 분산시킬 수 있습니다. 떨어진 꼬리는 재생되지만, 원래의 꼬리와는 약간 다른 모양과 색상을 가집니다. 레오파드 게코는 눈꺼풀이 있어 대부분의 다른 게코 종과 구별됩니다.",
    "서식지": "레오파드 게코의 원산지는 아프가니스탄, 파키스탄, 인도 북서부의 건조한 암석 지대입니다. 이들은 바위가 많은 사막, 초원, 관목 지대에서 서식합니다. 자연 서식지에서는 바위 틈이나 나무 껍질 아래에 숨어 지내며, 밤에 활동합니다. 애완동물로 키울 때는 이러한 자연 환경을 모방한 테라리움을 제공해야 합니다.",
    "먹이": "레오파드 게코는 주로 육식성으로, 다양한 곤충을 먹습니다. 주요 먹이로는 귀뚜라미, 밀웜, 왁스웜, 바퀴벌레 등이 있습니다. 때때로 작은 설치류나 다른 도마뱀도 잡아먹을 수 있습니다. 사육 시에는 칼슘과 비타민 D3를 보충해 주어야 합니다. 야생에서는 과일이나 꽃蜜도 섭취하는 것으로 알려져 있습니다.",
    "특징": "1. 특징적인 표범 무늬 피부\n2. 자할 능력 (위험 시 꼬리 분리)\n3. 야행성 습성\n4. 온순한 성격으로 애완동물로 인기\n5. 눈꺼풀 존재 (다른 게코와 구별되는 특징)\n6. 발톱이 있어 암벽 등반 가능\n7. 긴 수명 (15-20년)\n8. 온도에 따른 성결정\n9. 울음소리를 통한 의사소통\n10. 재생 능력 (꼬리, 피부 등)",
    "이미지": "images/3 Leopardgeko.jpg"
    },
    "7.뱀(Snake)": {
    "설명": "뱀은 비늘로 덮인 긴 몸을 가진 파충류로, 전 세계적으로 3,500여 종이 알려져 있습니다. 다리가 없지만 근육을 이용해 효율적으로 이동할 수 있으며, 일부 종은 나무를 타거나 물속에서 헤엄칠 수 있습니다. 뱀은 턱이 매우 유연하여 자신의 몸보다 큰 먹이도 통째로 삼킬 수 있습니다. 대부분의 뱀은 독이 없지만, 약 600종은 독성을 가지고 있습니다. 뱀은 주기적으로 허물을 벗어 성장하며, 일부 종은 열 감지 기관을 통해 따뜻한 피를 가진 동물을 감지할 수 있습니다.",
    "서식지": "뱀은 남극을 제외한 모든 대륙에 분포하며, 다양한 환경에 적응했습니다. 사막, 열대우림, 온대 숲, 초원, 습지, 바다 등 거의 모든 서식지에서 발견됩니다. 일부 종은 나무 위에서 생활하고, 다른 종들은 땅 위나 땅속에서 살며, 해양 뱀은 바다에서 생활합니다. 뱀은 바위 틈, 나무 구멍, 땅속 굴 등을 은신처로 이용합니다.",
    "먹이": "뱀은 대부분 육식성입니다. 작은 종은 주로 곤충이나 다른 작은 무척추동물을 먹고, 큰 종은 설치류, 새, 도마뱀, 개구리, 물고기 등을 잡아먹습니다. 일부 대형 종은 사슴이나 악어 같은 큰 동물도 사냥합니다. 뱀은 먹이를 통째로 삼키며, 강력한 소화 효소로 뼈까지 소화시킵니다. 많은 뱀이 한 번에 큰 먹이를 먹고 긴 시간 동안 소화하며 지냅니다.",
    "특징": "1. 비늘로 덮인 긴 몸\n2. 주기적인 허물 벗기\n3. 유연한 턱으로 큰 먹이 삼킴\n4. 일부 종의 독성\n5. 열 감지 기관 (일부 종)\n6. 분지된 혀로 냄새 감지\n7. 뼈로 된 많은 척추\n8. 다양한 이동 방식 (꿈틀거림, 측방 굽힘 등)\n9. 냉혈 동물로 체온 조절 필요\n10. 일부 종의 의사소통을 위한 소리 내기",
    "이미지": "images/8 Snake.jpg"},
    "8.비어디 드래곤(Beardy)": {
    "설명": "비어디 드래곤은 온순한 성격을 가진 도마뱀으로, 호주의 사막 지역에서 서식합니다. 특징적인 턱 아래 수염 모양의 비늘을 가지고 있으며, 체온 조절을 위해 수염을 펼치기도 합니다. 몸길이는 보통 30cm~60cm 정도이며, 수명은 적절한 관리 시 8~10년 이상 생존할 수 있습니다. 비어디 드래곤은 매우 호기심이 강하고 지능이 뛰어나며, 주인과의 교감을 즐기는 특성이 있습니다1.",
    "서식지": "호주의 건조지대, 사바나, 사막 지역이 주 서식지입니다. 자연 환경에서는 바위나 나무 등의 돌출물 위에서 생활합니다. 사육 시에는 사막과 비슷한 환경을 조성해야 하며, 온도와 습도 조절이 중요합니다. 적절한 태양광 또는 UVB 조명을 제공해야 합니다1.",
    "먹이": "비어디 드래곤은 잡식성으로, 다양한 먹이를 섭취합니다. 주로 곤충류(귀뚜라미, 밀웜, 메뚜기 등)를 먹으며, 채소와 과일도 일부 섭취합니다. 성장 단계에 따라 먹이의 비율을 조절해야 하며, 어릴 때는 단백질 위주로, 성체가 되면 채소의 비중을 늘려야 합니다1.",
    "특징": "1. 온순한 성격과 높은 지능\n2. 체온 조절을 위한 수염 퍼짐\n3. 색상 변화 능력 (감정 표현, 체온 조절)\n4. 강한 호기심과 사회성\n5. 손에 익숙해져 핸들링이 쉬움\n6. 수컷의 번식기 특유의 행동 (꼬리 흔들기)\n7. 자외선을 이용한 비타민 D 합성 능력\n8. 건조한 환경 적응력\n9. 수직 표면 등반 능력\n10. 주기적인 허물 벗기1",
    "이미지": "images/0 Beardy Dragon.jpg"},
    "9.앨리게이터(Alligator)": {
		"설명": "앨리게이터는 대형 파충류로, 강한 턱과 단단한 비늘로 덮인 몸을 가지고 있습니다. 주로 북미와 중국에서 서식하며, 평균 몸길이는 3~4미터에 이릅니다. 앨리게이터는 넓고 둥근 U자 모양의 주둥이를 가지고 있어 크로커다일과 구별됩니다. 수명은 30~50년 정도이며, 수중 생활에 잘 적응한 강력한 포식자입니다1.",
		"서식지": "앨리게이터는 주로 습지, 강, 늪에서 서식합니다. 미국 남동부의 루이지애나, 플로리다, 조지아, 앨라배마, 미시시피, 노스캐롤라이나, 사우스캐롤라이나, 텍사스 등에 널리 분포합니다. 최근에는 테네시주와 같이 더 북쪽으로 서식지를 확장하고 있습니다1.",
		"먹이": "앨리게이터는 기회주의적 포식자로, 다양한 먹이를 섭취합니다. 주로 물고기, 포유류, 조류를 사냥하지만, 크기에 따라 먹이의 종류가 달라집니다. 어린 개체는 주로 작은 물고기와 곤충을 먹고, 성체는 더 큰 동물들을 사냥합니다. 매복 공격 전략을 사용하여 먹이를 잡아 물에 끌어들인 후 익사시키거나 통째로 삼킵니다1.",
		"특징": "1. 강한 턱과 날카로운 이빨\n2. 수중 생활에 적응된 신체 구조\n3. U자형 넓은 주둥이 (크로커다일과의 차이점)\n4. 뛰어난 수영 능력\n5. 체온 조절을 위한 일광욕 습성\n6. 야행성 및 매복 사냥 전략\n7. 긴 수명 (30~50년)\n8. 모성 행동 (둥지 보호 및 새끼 돌봄)\n9. 계절에 따른 활동 변화 (겨울철 활동 감소)\n10. 생태계에서 최상위 포식자로서의 역할1",
		"이미지": "images/alligator.jpg"
		},
    "10.이구아나(Iguana)": {
    "설명": "이구아나는 크기가 크며 초식성이 강한 도마뱀으로, 강한 햇빛을 좋아합니다. 등에 가시 돌기가 있으며 수영 능력이 있습니다. 푸른이구아나의 경우 오직 그랜드캐이먼 섬에서만 발견되며, 인간의 정착과 개발로 인해 서식지가 줄어들고 있습니다2.",
    "서식지": "중남미 열대우림, 건생식물이 자라는 수풀, 경작지, 도로 주변, 정원, 높은 숲 등에서 서식합니다. 일부 종은 해안가 근처에서도 발견됩니다. 바위가 많고 햇볕이 강하게 비치는 마른 숲이나 해안가를 선호합니다2.",
    "먹이": "주로 초식성으로, 잎, 꽃, 과일을 먹습니다. 야생에서는 때때로 경작지나 과수원에서 먹이를 찾기도 합니다. 어린 개체는 일부 곤충류도 섭취할 수 있습니다2.",
    "특징": "1. 등에 가시 돌기 존재\n2. 뛰어난 수영 능력\n3. 강한 햇빛 선호\n4. 나무 위 생활 적응\n5. 긴 꼬리로 균형 유지 및 방어\n6. 체온 조절을 위한 일광욕 습성\n7. 암컷의 산란을 위한 해안가 이동\n8. 성장에 따른 서식 환경 변화 (어린 개체는 나무 선호)\n9. 천적이 거의 없는 성체 (외래종 제외)\n10. 3-4년의 성적 성숙 기간2",
    "이미지": "images/4 Iguana.jpg"},
    "11.카멜레온(Chameleon)": {
		"설명": "카멜레온은 색을 변화시키고 긴 혀를 이용해 먹이를 잡는 능력을 가진 특별한 도마뱀입니다. 독립적인 눈 움직임을 가지고 있으며, 크기는 종에 따라 2.5cm에서 68cm까지 다양합니다. 수명은 종에 따라 다르지만 일반적으로 3~10년 정도입니다. 카멜레온은 주로 나무 위에서 생활하며, 특유의 발 구조로 가지를 잡고 이동합니다1.",
		"서식지": "카멜레온은 주로 아프리카와 마다가스카르에 서식하며, 일부 종은 남부 유럽, 중동, 남아시아, 스리랑카에도 분포합니다. 열대우림, 사바나, 사막, 산림 등 다양한 환경에 적응했습니다. 대부분의 종은 나무 위에서 생활하지만, 일부는 관목이나 지면에서 서식합니다1.",
		"먹이": "카멜레온은 주로 곤충을 먹습니다. 긴 혀를 이용해 빠른 속도로 먹이를 잡아챕니다. 주요 먹이로는 귀뚜라미, 메뚜기, 나방, 파리 등이 있으며, 큰 종의 경우 작은 조류나 도마뱀도 잡아먹을 수 있습니다. 일부 종은 식물의 잎이나 과일도 섭취합니다1.",
		"특징": "1. 빠른 색 변화 능력 (위장, 체온 조절, 의사소통)\n2. 독립적으로 움직이는 눈\n3. 긴 혀를 이용한 먹이 사냥 (체장의 1.5~2배)\n4. 나뭇가지를 잡을 수 있는 특수한 발 구조\n5. 느린 움직임과 독특한 걸음걸이\n6. 자외선을 이용한 비타민 D 합성\n7. 종에 따른 다양한 크기와 외형\n8. 수컷의 화려한 색상과 장식 (번식기)\n9. 단독 생활 습성\n10. 환경 변화에 민감한 특성1",
		"이미지": "images/1 Panther Chamaeleon.jpg"
		},
    "12.크레스티드 게코(Crestedgeko)": {
    "설명": "크레스티드 게코는 나무 위에서 생활하며 점착성 패드를 이용해 벽을 기어오를 수 있습니다. 볏 모양의 돌기가 특징입니다. 중앙아메리카의 남동부에 서식하는 작은 파충류로, 특이한 외모와 성격으로 애완동물로서 인기를 얻고 있습니다3.",
    "서식지": "주로 열대 우림 지역에서 발견되며, 나무와 식물의 잎사귀에 서식합니다. 뉴칼레도니아의 열대우림이 원산지이지만, 현재는 애완동물로 전 세계에서 사육되고 있습니다3.",
    "먹이": "과일과 곤충을 주로 먹습니다. 야생에서는 작은 곤충들과 과일의 즙을 섭취하며, 사육 시에는 특별히 제조된 파우더 사료와 생과일, 작은 곤충을 급여합니다3.",
    "특징": "1.볏 모양의 특징적인 돌기\n2.점착성 패드를 가진 발로 수직 표면 등반 가능\n3.꼬리 자할(탈락) 능력\n4.야행성 습성\n5.온순한 성격으로 핸들링이 쉬움\n6.습도에 민감한 피부\n7.눈을 핥아 청소하는 독특한 습관\n8.색상 변화 능력 (제한적)\n9.소리를 내어 의사소통\n10.긴 수명 (적절한 관리 시 15-20년)3",
    "이미지": "images/2 Crestedgeko.jpg"},
    "13.크로커다일(Crocodile)": {
    "설명": "크로커다일은 대형 파충류로, 강한 턱과 단단한 비늘로 덮인 몸을 가지고 있습니다. 앨리게이터와 유사하지만 주둥이 모양 등에서 차이가 있습니다. 나일악어의 경우 최상위 포식자로서 매우 공격적이며, 범위 내의 거의 모든 동물을 잡아먹을 수 있습니다. 크로커다일은 복병 포식자로, 먹이를 공격하기 위해 오랜 시간 동안 기다릴 수 있습니다.",
    "서식지": "열대 및 아열대 지역의 강, 늪, 습지에서 주로 서식합니다. 나일악어의 경우 아프리카의 다양한 수역에서 발견됩니다. 크로커다일은 수중 생활에 잘 적응되어 있으며, 물속에서 오랜 시간을 보낼 수 있습니다.",
    "먹이": "크로커다일은 주로 물고기, 파충류, 조류, 포유류를 먹이로 삼습니다. 나일악어의 경우 매우 다양한 먹이를 섭취하는 일반주의자입니다. 크기가 큰 먹이도 강력한 턱과 날카로운 이빨을 이용해 사냥할 수 있습니다. 물속에서 큰 먹이를 잡아 익사시키는 능력이 있습니다.",
    "특징": "1. 강한 턱과 날카로운 이빨\n2. 수중 생활에 적응된 신체 구조\n3. V자형 주둥이 (악어와의 차이점)\n4. 복병 사냥 전략\n5. 사회적 행동 (떼를 지어 생활)\n6. 엄격한 서열 체계\n7. 부모의 보살핌 행동\n8. 긴 수명\n9. 체온 조절을 위한 일광욕 습성\n10. 강력한 면역 체계",
    "이미지": "images/crocodile.jpg"},
    "14.팩맨(PacMan)": {
    "설명": "팩맨 개구리(뿔개구리)는 둥글고 큰 입을 가진 개구리로, 작은 먹이를 통째로 삼킵니다. 땅속에 숨는 습성이 있습니다. 이름은 비디오 게임 캐릭터 팩맨과 비슷한 외모 때문에 붙여졌습니다. 주로 야행성이며, 낮에는 나뭇잎처럼 위장하고 밤에 먹이활동을 합니다. 성격이 사납고 자기 영역이 확실하여 주로 혼자 생활합니다.",
    "서식지": "남아메리카의 습한 환경, 특히 볼리비아, 브라질, 콜롬비아, 에콰도르, 프랑스령 기아나, 페루, 수리남 등의 숲의 습지 주변에서 서식합니다. 사육 시에는 23~26도의 온도와 70% 이상의 습도를 유지해야 합니다.",
    "먹이": "야생에서는 육식성으로 새, 뱀, 개구리, 도마뱀, 쥐 등을 잡아먹으며 상황에 따라 동종 포식도 합니다. 사육 시에는 귀뚜라미, 밀웜, 특수 제작된 팩맨 푸드, 그리고 때때로 고영양식으로 파충류용 냉동 쥐(핑키)를 급여할 수 있습니다.",
    "특징": "1. 큰 입과 둥근 몸체\n2. 땅속에 숨는 습성\n3. 야행성 생활\n4. 게으르고 움직임이 적음\n5. 강한 영역성과 단독 생활\n6. 위장 능력 (나뭇잎처럼 보임)\n7. 다양한 체색 변이 (인공 번식으로 인한)\n8. 수컷의 특징적인 울음소리\n9. 암수 간 크기 차이 (암컷이 더 큼)\n10. 물과 흙 환경 모두에서 사육 가능",
    "이미지": "images/pacman_frog.jpg"}
    }

    # ✅ 존재하지 않는 종의 경우 기본 정보 반환
    return species_data.get(species_name, {
        "설명": "해당 종에 대한 설명이 없습니다.",
        "서식지": "미확인",
        "먹이": "미확인",
        "특징": "미확인",
        "이미지": "images/default.jpg"
    })


# ✅ 종 설명을 가져오는 함수
def get_species_description(species_name):
    """종에 대한 설명을 가져오는 함수"""
    return get_species_info(species_name)


# ✅ 종 정보를 UI에 표시하는 함수 (이미지 포함)
def display_species_info(species_name):
    """ 종 정보를 UI에 표시하는 함수 """
    species_info = get_species_info(species_name)
    
    # ✅ 이미지 파일 존재 확인
    image_path = species_info["이미지"]
    if not os.path.exists(image_path):
        image_path = "images/default.jpg"  # 기본 이미지로 변경

    # ✅ UI 디자인 개선
    st.markdown(
        f"""
        <div style="
            background-color: #f8f9fa; 
            padding: 15px; 
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            text-align: center;
            ">
            <h3 style="color: #4CAF50;">🦎 {species_name}</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ✅ 이미지 출력
    st.image(image_path, caption=species_name, use_container_width=True)

    # ✅ 상세 정보 출력
    st.write(f"**설명:** {species_info['설명']}")
    st.write(f"**서식지:** {species_info['서식지']}")
    st.write(f"**먹이:** {species_info['먹이']}")
    st.write(f"**특징:** {species_info['특징']}")


