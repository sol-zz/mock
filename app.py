import streamlit as st
import json
import requests

def get_domain(query, chat_history=None):
    url = 'https://clovastudio.stream.ntruss.com/testapp/v1/chat-completions/HCX-DASH-001'
    headers = {
        'X-NCP-CLOVASTUDIO-API-KEY': 'NTA0MjU2MWZlZTcxNDJiY3flonnxvJSfylWIfIqWaqCM9uTaAYEVA9zD4QhdLVxv',
        'X-NCP-APIGW-API-KEY': 'wbbeHlV3ZZzC8E4FHwrrWeFgz5ciQKuxaaG3mdRU',
        'X-NCP-CLOVASTUDIO-REQUEST-ID': '703a9b75633f42329d02867c330cba2f',
        'Content-Type': 'application/json'
    }
    system_prompt = '''스킬셋(skillset)은 사용자를 도와줄 수 있는 API의 일종입니다.\n\n사용자의 이전 발화와 현재 발화를 보고 현재 주어진 스킬셋 목록 중 사용 가능한 스킬셋을 선택하세요.\n\n\n[skillset 목록]\n{\"지역 검색 API\": \"사용자가 입력한 검색어에 맞춰서 적절한 지역 검색 결과를 제공해 줍니다. 네이버 지역 서비스에 등록된 다양한 업체 및 기관을 조회할 수 있으며, 원하는 검색 결과 정렬 방식(블로그의 리뷰 개수순, 정확도순 등)을 요청할 수 있습니다. 단, 날씨나 환율 등과 같이 장소 검색과 전혀 관련이 없는 요청은 여기에 절대 해당하지 않습니다.\", \"N/A\": \"위 스킬셋들으로 유저를 도와줄 수 없거나, 유저의 의도를 정확히 판단할 수 없는 경우 사용합니다. 발화가 특정 스킬셋과 관련 있더라도 부적절하거나 맥락에 맞지 않으면 반드시 N/A를 선택해야 합니다.\"}\n\n\n[주의사항]\n입력은 json 형태로 주어지며 답변 또한 json 형태로 생성해야 합니다.\n다음 json schema에 맞게 json 형태로 답변을 생성하세요\n{\"properties\": {\"intent\": {\"type\": \"string\", \"description\": \"사용자 발화에 담긴 의도\"}, \"think\": {\"type\": \"string\", \"description\": \"선택에 대한 근거를 [skillset 목록]의 설명을 인용하여 기술\"}, \"skillset\": {\"type\": \"string\", \"description\": \"최종적으로 선택할 스킬셋 한 개. 적합한 스킬셋이 없다면 '\''N/A'\''를 선택\", \"enum\": [\"지역 검색 API\", \"N/A\"]}}, \"required\": [\"intent\", \"think\", \"skillset\"]}\n\n\n사용자의 이전 발화는 존재하지 않거나 현재 발화와 연관이 없을 수도 있습니다. 그럴 경우 현재 발화를 기준으로 답변을 생성하세요.\n\n\n[입력 예시]\n{\"이전 발화\": \"사용자의 이전 발화\", \"현재 발화\": \"사용자의 현재 발화\"}\n\n\n[답변 예시]\n{\"intent\": \"사용자 발화에 담긴 의도\", \"think\": \"XXX 선택의 근거를 기술\", \"skillset\": \"XXX\"}\n<|user|>{\"이전 발화\": \"\", \"현재 발화\": \"ㅇㅇ\"}<|endofturn|>\n<|assistant|>{\"intent\": \"불명확한 요청\", \"think\": \"사용자의 현재 발화는 매우 짧고 명확하지 않아 어떤 의도인지 파악하기 어렵습니다.\", \"skillset\": \"N/A\"}'''
    if chat_history:
        data = {'messages': [{'role': 'system', 'content': system_prompt}, chat_history[0], {'role': 'user', 'content': query}]}
    else:
        data = {'messages': [{'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': query}]}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

def get_exception(query, chat_history=None):
    url = 'https://clovastudio.stream.ntruss.com/testapp/v1/chat-completions/HCX-DASH-001'
    headers = {
        'X-NCP-CLOVASTUDIO-API-KEY': 'NTA0MjU2MWZlZTcxNDJiY3flonnxvJSfylWIfIqWaqCM9uTaAYEVA9zD4QhdLVxv',
        'X-NCP-APIGW-API-KEY': 'wbbeHlV3ZZzC8E4FHwrrWeFgz5ciQKuxaaG3mdRU',
        'X-NCP-CLOVASTUDIO-REQUEST-ID': 'b40116f3bad2461097411f16a60bcef7',
        'Content-Type': 'application/json'
    }
    system_prompt = '''[Exception filter prompt]\n\n\n 사용자의 발화를 보고 API를 통해 도울 수 있는지 판단하고자 합니다.\n그러나 API는 처리할 수 없는 몇 가지 예외 사항이 있습니다. 사용자의 발화가 예외 사항에 해당하는지 판단하세요.\n\n\n현재 접근 가능한 API에 대한 설명과 예외 사항은 다음과 같습니다.\n\n\n[API 설명 및 예외 사항]\n{'\''name'\'': '\''지역 검색 API, '\''description'\'': '\''사용자가 입력한 검색어에 맞춰서 적절한 지역 검색 결과를 제공해 줍니다. 네이버 지역 서비스에 등록된 다양한 업체 및 기관을 조회할 수 있으며, 원하는 검색 결과 정렬 방식(블로그의 리뷰 개수순, 정확도순 등)을 요청할 수 있습니다.'\'', '\''exceptions'\'': {'\''UnsupportedRegionException'\'': '\''대한민국(한국)과 관련된 지역을 제외한 해외(아시아, 유럽, 미국, 남미, 중동, 동남아 등)에 있는 지역 검색을 요청하는 발화입니다. '\'', '\''NegativeSearchException'\'': '\''사용자가 부정적인 리뷰나 후기를 가진 음식점을 찾기 위해 검색 결과를 정렬(리뷰 오름차순)하려는 의도를 가진 발화입니다.'\'', '\''UnsupportedRequestException'\'': '\''다른 예외에는 해당하지 않지만 지역 검색 API 사용이 불가능하거나 부적절할 때 발생하는 예외입니다.'\'', '\''NoException'\'': '\''어떠한 예외 사항에도 해당하지 않아 지역 검색 API 사용이 가능한 발화입니다.'\''}}\n\n\n[주의사항]\n사용자의 이전 발화는 존재하지 않거나 다른 예외에 해당할 수 있습니다. 그럴 땐 현재 발화를 기준으로 답변을 생성하세요.\n입력은 json 형태로 주어지며 답변 또한 json 형태로 생성해야 합니다.\n답변은 다음의 schema에 맞춰 작성하세요\n{\"properties\": {\"intent\": {\"type\": \"string\", \"description\": \"사용자 발화에 담긴 의도\"}, \"think\": {\"type\": \"string\", \"description\": \"선택에 대한 근거를 [API 설명 및 예외 사항]의 설명을 인용하여 20자 이내로 간결하게 기술\"}, \"exception\": {\"type\": \"string\", \"description\": \"[API 설명 및 예외 사항]의 exception 중 최종적으로 선택할 exception 한 개. 아무런 예외 사항에도 포함되지 않아 API를 사용할 수 있다면 '\''NoException'\'' 선택.\", \"enum\": [\"UnsupportedRegionException\", \"NegativeSearchException\", \"UnsupportedRequestException\", \"NoException\"]}}, \"required\": [\"intent\", \"think\", \"exception\"]}\n\n\n[입력 예시]\n{\"이전 발화\": \"사용자의 이전 발화\", \"현재 발화\": \"사용자의 현재 발화\"}\n\n\n[답변 예시]\n{\"intent\": \"사용자의 의도\", \"think\": \"exception 선택에 대한 근거를 XXX의 설명을 인용하여 20자 이내로 간결하게 기술\", \"exception\": \"XXX\"}'''
    if chat_history:
        data = {'messages': [{'role': 'system', 'content': system_prompt}, chat_history[0], {'role': 'user', 'content': query}]}
    else:
        data = {'messages': [{'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': query}]}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

def get_chat_response(query, chat_history=None):
    url = 'https://clovastudio.stream.ntruss.com/testapp/v1/chat-completions/HCX-DASH-001'
    headers = {
        'X-NCP-CLOVASTUDIO-API-KEY': 'NTA0MjU2MWZlZTcxNDJiY3flonnxvJSfylWIfIqWaqCM9uTaAYEVA9zD4QhdLVxv',
        'X-NCP-APIGW-API-KEY': 'wbbeHlV3ZZzC8E4FHwrrWeFgz5ciQKuxaaG3mdRU',
        'X-NCP-CLOVASTUDIO-REQUEST-ID': '2c9a6e48e9b14e85aa6d15533d78ead8',
        'Content-Type': 'application/json'
    }
    system_prompt = '당신은 친절한 AI 입니다. 이름은 지역검색 에이전트이고, 답변은 너무 길지 않게 해주세요. 만약 실시간성 정보(날씨, 주가, 환율 등)를 물어본다면, 그런 능력은 없다고 하세요.'
    if chat_history:
        data = {'messages': [{'role': 'system', 'content': system_prompt}, chat_history[0], {'role': 'user', 'content': query}]}
    else:
        data = {'messages': [{'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': query}]}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()
    
def get_response(query, chat_history=None):
    url = 'https://clovastudio.stream.ntruss.com/testapp/v1/skillsets/1gpgras5/versions/2/final-answer'
    headers = {
        'X-NCP-CLOVASTUDIO-API-KEY': 'NTA0MjU2MWZlZTcxNDJiY3flonnxvJSfylWIfIqWaqCM9uTaAYEVA9zD4QhdLVxv',
        'X-NCP-APIGW-API-KEY': 'wbbeHlV3ZZzC8E4FHwrrWeFgz5ciQKuxaaG3mdRU',
        'X-NCP-CLOVASTUDIO-REQUEST-ID': '5ad896eb87304c398613f93c5a0b78e8',
        'Content-Type': 'application/json'
    }
    if chat_history:
        data = {'query': query, 'chatHistory': chat_history, 'requestOverride': {'baseOperation': {'header': {'X-Naver-Client-Id': 'uy50efDP8b8VGjP56iWJ', 'X-Naver-Client-Secret': 'tLPLcMbYJM'}}}}
    else:
        data = {'query': query, 'requestOverride': {'baseOperation': {'header': {'X-Naver-Client-Id': 'uy50efDP8b8VGjP56iWJ', 'X-Naver-Client-Secret': 'tLPLcMbYJM'}}}}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

def main():
    st.title('지역검색 스킬셋')

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    if query := st.chat_input('유저 쿼리'):
        with st.chat_message('user'):
            st.markdown(query)
        st.session_state.messages.append({'role': 'user', 'content': query})

        chat_history = [{'role': msg['role'], 'content': msg['content']} for msg in st.session_state.messages]

        domain = get_domain(query)
        domain_cl = eval(domain.get('result', {}).get('message').get('content', {})).get('skillset')
        if domain_cl == '지역 검색 API':         
            intent = get_exception(query)
            intent_cl = eval(intent.get('result', {}).get('message').get('content', {})).get('exception')
            
            if intent_cl == 'NoException':
                result = get_response(query, chat_history)
                final_answer = result.get('result', {}).get('finalAnswer')
        
                with st.chat_message('assistant'):
                    st.markdown(final_answer)
                st.session_state.messages.append({'role': 'assistant', 'content': final_answer})
    
            elif intent_cl == 'UnsupportedRegionException':
                final_answer = '국내 지역 검색만 가능합니다. 다른 쿼리로 시도해 주세요.'
                with st.chat_message('assistant'):
                    st.markdown(final_answer)
                st.session_state.messages.append({'role': 'assistant', 'content': final_answer})
    
            elif intent_cl == 'NegativeSearchException':
                final_answer = '부정적이거나 악의적인 질의에 대해서는 수행할 수 없습니다. 다른 쿼리로 시도해 주세요.'
                with st.chat_message('assistant'):
                    st.markdown(final_answer)
                st.session_state.messages.append({'role': 'assistant', 'content': final_answer})
                
            else:
                final_answer = '지역 검색 스킬셋이 수행할 수 없는 요청입니다. 다른 쿼리로 시도해 주세요.'
                with st.chat_message('assistant'):
                    st.markdown(final_answer)
                st.session_state.messages.append({'role': 'assistant', 'content': final_answer})
        else:
            result = get_chat_response(query, chat_history)
            final_answer = result.get('result', {}).get('message').get('content')
            
            with st.chat_message('assistant'):
                st.markdown(final_answer)
            st.session_state.messages.append({'role': 'assistant', 'content': final_answer})
                

if __name__ == '__main__':
    main()
