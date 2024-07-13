import os
import logging
import random
from datetime import datetime
import aiohttp

class CodingIterationService:
    def __init__(self, openai_api_key, model='gpt-4o'):
        self.openai_api_key = openai_api_key
        self.model = model

    async def get_response(self, system_prompt, user_prompt, retries=3, backoff=2):
        attempt = 0
        while attempt < retries:
            try:
                headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.openai_api_key}'}
                json_data = {
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ]
                }
                async with aiohttp.ClientSession() as session:
                    async with session.post("https://api.openai.com/v1/chat/completions", headers=headers, json=json_data) as response:
                        response.raise_for_status()
                        response_data = await response.json()
                        return response_data['choices'][0]['message']['content'].strip()
            except aiohttp.ClientError as e:
                attempt += 1
                jitter = random.uniform(0, 1)
                sleep_time = backoff * (2 ** (attempt - 1)) + jitter
                logging.error(f"Attempt {attempt}: Error getting response from API - {e}, retrying in {sleep_time:.2f} seconds")
                await asyncio.sleep(sleep_time)
        raise RuntimeError("Failed to get response from OpenAI API after multiple attempts.")

    def save_code_snippet(self, path, code_snippet, language, iteration, topic_summary):
        ext_dict = {
            'Python': '.py',
            'JavaScript': '.js',
            'Java': '.java',
            'C++': '.cpp',
            'Go': '.go',
            'Ruby': '.rb',
            'PHP': '.php'
        }
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        code_extension = ext_dict[language]
        file_name = f'{topic_summary}_snippet_{iteration}_{timestamp}{code_extension}'
        code_path = os.path.join(path, file_name)
        
        try:
            with open(code_path, 'w', encoding='utf-8') as f:
                f.write(code_snippet)
            logging.info(f"Snippet saved to '{file_name}'")
        except IOError as e:
            logging.error(f"Error saving code snippet: {e}")
            raise
