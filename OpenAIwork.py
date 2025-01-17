from Createbot import OpenAI_TOKEN, client, logger
from openai import APIError
import data_base.dbreq as dbr 
import requests

def CheckBalanceProxiAPI ():
    url = "https://api.proxyapi.ru/proxyapi/balance"
    headers = {
        "Authorization": f"Bearer {OpenAI_TOKEN}"
    }
    response = requests.get(url=url,headers=headers)
    if response.status_code == 200:
       return response.json()
    else:
        return f"Ошибка: {response.status_code}, {response.text}"

async def CreateRequestToAI(messages):
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=100
        )
        print(completion.usage)
        return completion
    except APIError as e:
        return f"Error happened: {e.code}\n {e.response}"
    
async def CreateMessagesForAI(messagefromuser, tg_id) -> list:
    try:
        context_messages = await dbr.get_context_by_user_id(tg_id=tg_id)
        messages = [{"role": "system", "content": "You are my teacher of English. You are to answer in English, keep up our dialogue. Try to use useful and real vocabulary. If i make a mistake answer me in the form: Explanation of the error\nCorrect verison\n Then answer to my phrase"}]
        if not context_messages:
            logger.info(f"No context message were added while creating a message for AI")
        else:
            cntxt= [ctxt.context.split(":") for ctxt in context_messages]
            for message in cntxt:
                messages.append({"role":message[0], "content":message[1]})
        messages.append({"role":"user","content":f"{messagefromuser}"})
        return messages
    except Exception as e:
        logger.error(f"Error occured while trying to create message for AI /// {e}")
