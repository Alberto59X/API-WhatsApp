from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import time


driver = webdriver.Chrome()  
driver.get('https://web.whatsapp.com')


def get_last_message():
    
    try:
        messages = driver.find_elements(By.XPATH, '//div[contains(@class,"message-in") or contains(@class,"message-out")]')
        if messages:
            last_message = messages[-1].find_element(By.CSS_SELECTOR, '.copyable-text').text
            return last_message
    except Exception as e:
        print(f"Erro ao capturar a mensagem: {e}")
    return ""

def send_message(text):
   
    try:
        message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
        message_box.send_keys(text)
        message_box.send_keys(Keys.ENTER)
    except Exception as e:
        print(f"Erro ao enviar a mensagem: {e}")


api_key = 'sua-chave-de-api'

def chat_with_gpt(message):
   
    url = 'https://api.openai.com/v1/engines/gpt-4/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
    }
    data = {
        'prompt': message,
        'max_tokens': 150,
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()
        return response_json['choices'][0]['text'].strip()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao se comunicar com a API do ChatGPT: {e}")
        return "Desculpe, não consegui processar sua mensagem agora."


def main():
    print("Por favor, escaneie o QR Code no WhatsApp Web.")
    time.sleep(30)  
    while True:
        try:
            last_message = get_last_message()
            print(f'Mensagem recebida: {last_message}')
            
            if "@" in last_message:  
                response = chat_with_gpt(last_message)
                print(f'Resposta do GPT: {response}')
                send_message(response)
            time.sleep(10)  
        except Exception as e:
            print(f'Erro no loop principal: {e}')
            time.sleep(10)

if __name__ == "__main__":
    main()
