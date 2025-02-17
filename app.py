import os
import base64
from openai import AzureOpenAI  
from flask import (Flask, redirect, render_template, request, send_from_directory, url_for)

app = Flask(__name__)

endpoint = os.getenv("ENDPOINT_URL", "")  
deployment = os.getenv("DEPLOYMENT_NAME", "")  
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "")  

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/answer', methods=['POST'])
def answer():
   message = request.form.get('message')
   if not message:
       return redirect(url_for('index'))

   # キーベースの認証を使用して Azure OpenAI Service クライアントを初期化する    
   client = AzureOpenAI(azure_endpoint=endpoint,api_key=subscription_key,api_version="2024-05-01-preview",)

   #チャット プロンプトを準備する 
   chat_prompt = [
      {
         "role": "system",
         "content": "情報を見つけるのに役立つ AI アシスタントです。"
      },
      {
         "role": "user",
         "content": message
      }
   ] 
   inputdata = chat_prompt  

   # 入力候補を生成する  (同期呼出しの為、画面がフリーズする可能性があります。実アプリでは非同期呼出しをご検討ください）
   completion = client.chat.completions.create(  
      model=deployment,
      messages=inputdata,
      max_tokens=800,  
      temperature=0.7,  
      top_p=0.95,  
      frequency_penalty=0,  
      presence_penalty=0,
      stop=None,  
      stream=False
   )

   print('completion: {}'.format( completion.to_json() ) )

   response = completion.choices[0].message.content
   return render_template('answer.html', message = response)

if __name__ == '__main__':
   app.run()
