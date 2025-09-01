import asyncio
import json
import os
import sys
sys.path.append(os.getcwd())
from src.elements.models.models import client, llm

def extract_json(s):
    # 查找第一个左大括号的位置，确保最外层是JSON对象
    start = None
    for i, c in enumerate(s):
        if c == '{':
            start = i
            break
    if start is None:
        return None  # 没有找到可能的JSON对象

    stack = ['{']  # 初始化栈，用于匹配括号
    in_string = False  # 是否在字符串内部
    escape = False  # 是否处理转义字符
    end = None  # 记录结束位置

    # 从start+1开始遍历字符，匹配括号
    for i in range(start + 1, len(s)):
        char = s[i]

        # if in_string:
        #     if escape:
        #         escape = False  # 转义状态结束
        #     else:
        #         if char == '\\':
        #             escape = True  # 下一个字符被转义
        #         elif char == '"':
        #             in_string = False  # 字符串结束
        # else:
        # if char == '"':
        #     in_string = True  # 进入字符串
        #     escape = False
        if char == '{':
            stack.append(char)
        elif char == '}':
            if not stack:
                break  # 栈空，无法匹配
            stack.pop()
            if not stack:  # 栈空，匹配成功
                end = i
                break
        # 继续循环直到找到结束或遍历完字符串

    if end is None:
        return None  # 没有完整的结构

    json_str = s[start:end + 1]
    # print(json_str)
    try:
        import json
        parsed = json.loads(json_str)
        # 确保解析结果是一个字典
        return parsed if isinstance(parsed, dict) else None
    except json.JSONDecodeError:
        return None  # JSON解析失败
    
from langsmith import traceable

@traceable(project_name="get_dict")
def get_dict(s):
    s = s.strip('` \njson')
    import json
    try:
        res = json.loads(s)
        return res
    except:
        return extract_json(s)
    

import time
import random
@traceable(project_name="get_completion_with_retry")
def get_completion_with_retry(user_prompt, max_retries=10, initial_delay=1.0):
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # if trans_model <=50:
            #     completion = client.chat.completions.create(
            #         model="qwen-max-latest",
            #         messages=[
            #             {'role': 'system', 'content': 'you are a helpful assistant.'},
            #             {'role': 'user', 'content': user_prompt}],
            #         # extra_body={"enable_thinking": False}
            #     )
            #     res = get_dict(completion.choices[0].message.content)
            # else:
            model_answer = llm.invoke(user_prompt).content
            
            res = get_dict(model_answer)
                
                
            
            if res is not None:  
                return res
                
        except Exception as e:
            print(f"Attempt {retry_count + 1} failed with error: {str(e)}")
            
            
            # 指数退避 + 随机抖动（避免多个客户端同时重试）
            delay = initial_delay * (2 ** retry_count) + random.uniform(0, 1)
            delay = min(delay, 300)
            print(f"Waiting {delay:.2f} seconds before retry...")
            time.sleep(delay)
            
        retry_count += 1
    
    print(f"Failed to get valid JSON after {max_retries} attempts.")
    return None


count = 0
@traceable(project_name="aget_completion_with_retry")
async def aget_completion_with_retry(user_prompt, max_retries=10, initial_delay=1.0):
    retry_count = 0
    global count
    while retry_count < max_retries:
        try:
            # if trans_model <=50:
            #     completion = client.chat.completions.create(
            #         model="qwen-max-latest",
            #         messages=[
            #             {'role': 'system', 'content': 'you are a helpful assistant.'},
            #             {'role': 'user', 'content': user_prompt}],
            #         # extra_body={"enable_thinking": False}
            #     )
            #     res = get_dict(completion.choices[0].message.content)
            # else:
            model_answer = await chatLLM.ainvoke(user_prompt)
            count += 1
            print(count)
            res = get_dict(model_answer.content)
                
                
            
            if res is not None:  
                return res
                
        except Exception as e:
            print(f"Attempt {retry_count + 1} failed with error: {str(e)}")
            
            
            # 指数退避 + 随机抖动（避免多个客户端同时重试）
            delay = initial_delay * (2 ** retry_count) + random.uniform(0, 1)
            delay = min(delay, 300)
            print(f"Waiting {delay:.2f} seconds before retry...")
            await asyncio.sleep(delay)
            
        retry_count += 1
    
    print(f"Failed to get valid JSON after {max_retries} attempts.")
    return None

import time
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import asyncio

from src.elements.utils.utils import *

async def play_web(search_url: str) -> dict:
    
        
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=False,  # 设为False便于调试
                timeout=60000,
                args=['--start-maximized']
            )
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            )
            page = await context.new_page()
            try:
                # ========== 普通检索 ==========
                for i in range(10):
                    
                    try:
                        await page.goto(search_url, timeout=3000)
                        break
                        
                    except:
                        time.sleep(1)
                await asyncio.sleep(30)
                await page.screenshot(path='debug.png')
                
                # Get the page content and parse with BeautifulSoup
                html_content = await page.content()
                
                soup = BeautifulSoup(html_content, 'html.parser')
                                # Find and click the login button
                
                
                                    
                        
                
                            
            
            finally:
                await browser.close()
        
        return {"status": "success", "message": "Login button clicked"}
if __name__ == "__main__":
    asyncio.run(play_web("http://observe.dibrain.data-infra.shopee.io/project/clwt91c5l0001jlxd484nmens/traces/364dd0a0-4e11-45af-bac7-70c822577f1c"))
    print("done")
    exit()
if __name__ == "__main__":
    s = """{
  "RequestId": "A3D6F5CB-7548-538B-9504-4A8DBC09784D",
  "Data": {
    "Status": "PROCESS_SUCCESS",
    "JobId": "D05EB3F3-C33E-5364-93E8-06810C03397E",
    "Result": "{\\"resultUrl\\":\\"https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/viapi-video/2025-08-05/88588205-7124-45f3-9239-f131af1bc32f/20250805115528112084_style1_0hlt1cqiw4.jpg?Expires=1754452539&OSSAccessKeyId=LTAI5tQZd8AEcZX6KZV4G8qL&Signature=f%2BA55USci6vLYNOrwy9vzYL1guI%3D\\"}"
  }
}
    """
  
    print(extract_json(s))
    
    
    print(None)