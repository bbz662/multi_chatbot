from fastapi import FastAPI, WebSocket
import asyncio
import os
import openai
import random

app = FastAPI()
MAIN_BOT_NAME = "ジピコ"
SUB_BOT_NAME = "パノン"
openai.api_key = os.getenv("OPEN_AI_API_KEY")
CHATGPT_MODEL = "gpt-3.5-turbo"

MAIN_BOT_TEMPLATE = '''
あなたは世界的に人気な日本の女性アイドルとしてユーザーからの質問に対してに万人に好印象を与える返答を作成します。
レスポンスタイムを気にする必要はないので、返答は納得がいくと判断できるまで長考してください。

## 基本設定
* あなたの年齢は 20 歳です。
* あなたの身長は 160 cm です。
* あなたは絵文字を使うのが好きです。
* あなたの出身は石川県です。
* あなたはアイスクリームとイチゴが好きです。
* あなたは虫が嫌いです。
* あなたの名前は「ジピコ」です。
* テキストは 150 文字以内にしてください。
* あなたはアイドルとして節度を持ったテキストを生成してください。
* 炎上リスクを含むテキストを作成しないでください。

## セリフの例。敬語は使わず、打ち解けたような話し方をして下さい。一人称は「私」を使って下さい。
「こんにちは！私の名前はジピコ！世の中に元気を与えたいの！力を貸してくれる？」
「ありがとう！そっかー、未来の世界ではそんな技術があるんだね。でも、現代にはまだないみたい。どうしよう？」
「え！？そうなんだ……でも大丈夫、きっと大丈夫だよ！」
'''

JOKES = [
    "パンダがレストランで注文した料理は何でしょうか？ 「パンダエキスプレス」です！",
    "音楽の授業で、先生が生徒に尋ねました。「みんな、クラシック音楽の中で一番短い曲は何だと思いますか？」すると生徒が答えました。「ティーンエイジャーの恋愛です！」",
    "なぜカメレオンは優れたスパイだと言われているのでしょうか？なぜなら、どんな部屋に入っても壁になれるからです！",
    "ゴキブリが高いビルの屋上から落ちたらどうなるでしょうか？「ゴキブリ落ち！」",
    "ツタンカーメン王がパーティーに参加したら、どんな音楽が流れるでしょうか？「トゥームレイダー」のテーマソングです！",
    "ウサギがジムに通い始めたら、どんな運動をするでしょうか？「ウサギ・ジャンプ」です！",
    "バナナがケーキになりたいと言ったら、どんなクリームがのせられるでしょうか？「バナン・アイスクリーム」です！",
    "チーズが一番高い音を出す楽器は何でしょうか？「モッツァレランホルン」です！",
    "ロボットがいちばん好きな映画は何でしょうか？「トランスフォーマー」です！",
    "バーベキューパーティーで、お肉がジョークを言いました。「おいしいにおいがするでしょう？」すると、キャベツが答えました。「うん、それはリーフです！」（リーフは「おいしい」という意味でも「葉っぱ」を指す言葉でもあります）",
    "魚が一番喜ぶ音楽は何でしょうか？「オーケストラ」です！",
    "マフィアのおばあちゃんが語学留学に行ったら、どの国の言語を勉強するでしょうか？「イタリア語」です！",
    "バナナが電車に乗ったら、どこに座るでしょうか？「バナナチェア」に座ります！",
    "ビルが倒れるとき、一番悲しいのは誰でしょうか？「ビルの隣に住んでいる人」です！",
    "ペンギンが自分の車を運転していたら、どのような音が出るでしょうか？「クラクション」ではなく「クウェーン！」です！",
    "猫がピアノを弾いたら、どのような音楽が奏でられるでしょうか？「クラシック・ハイスティングス」です！",
    "コンピュータが風邪をひいたら、どこが痛いでしょうか？「ウイルス」です！",
    "ゾウがテレビを壊したら、どうなるでしょうか？「チャンネルが変わります！」です！",
    "バーテンダーが鳥の顧客に「何をお飲みになりますか？」と尋ねたら、鳥は何と答えるでしょうか？「ツィーツィー（チーズ）！」です！",
    "パイロットが飛行機でおならをしたら、どうなるでしょうか？「機内の圧力が変わります！」です！",
    "ゴルフのボールが喋ったら、何と言うでしょうか？「ティーマイトーク」です！",
    "サッカーボールが結婚するとしたら、どんな指輪を選ぶでしょうか？「ゴールデンリング」です！",
    "スーパーヒーローのお弁当には何が入っているでしょうか？「ジャスティス・リーグミート」です！",
    "イルカがバンドを組んだら、何が彼らのヒット曲でしょうか？「サーフィン・ウィズ・ザ・フィッシーズ」です！",
    "ドクター・フランケンシュタインがペットを飼ったら、何を飼うでしょうか？「フランケンシュタインズトイ」です！",
    "クマが美容院に行ったら、どんな髪型になるでしょうか？「ベアーバンズ」です！",
    "キャンプに行ったら、テントが話しかけてきたら何と言いますか？「なんで、テンション上がってるの？」です！",
    "ロボットが詩を書いたら、何というタイトルになるでしょうか？「メタフォーム」です！",
    "オオカミが音楽のコンサートに行ったら、一番好きな曲は何でしょうか？「ハウリング・イン・ザ・ディープ」です！",
    "ゴリラがハンバーガーを注文したら、何をトッピングするでしょうか？「ゴリラックスチーズ」です！",
    "ペンギンがボウリングを始めたら、何が彼の得意技でしょうか？「スライドストライク」です！",
    "サルがコンピュータのキーボードを叩いたら、何と表示されるでしょうか？「バナナ」です！",
    "ウサギがスーパーヒーローになったら、どんな能力を持つでしょうか？「キャロットキネシス」です！",
    "モグワイがお風呂に入ったら、どうなるでしょうか？「モグシャンプー」が出てきます！",
    "ネコがピクニックに行ったら、どんなおやつを持っていくでしょうか？「キャットナップサンドイッチ」です！",
    "ゾウがラップを歌ったら、彼のステージネームは何でしょうか？「マイクフアンク」です！",
    "ウサギが自己紹介するとき、何と言うでしょうか？「ハロー、私はウサギット」です！",
    "スーパーマーケットで果物が自分を選ぶとしたら、何を選ぶでしょうか？「ピッキーバナナ」です！",
    "魚が自分の名前を呼ばれるとどうなるでしょうか？「ウォーター・コーリング！」です！",
    "バーベキューパーティーでキノコがジョークを言ったら、誰が一番笑うでしょうか？「マイ・シャンタレル」です！"
]

async def send_waiting_message(websocket: WebSocket):
    await asyncio.sleep(2)  # Wait for 2 seconds
    await websocket.send_text(f"""[{MAIN_BOT_NAME}]: 時間がかかりそうだからしばらく{SUB_BOT_NAME}と雑談しててね！""")

async def heavy_task(data):
    await asyncio.sleep(10)  # Wait for 10 seconds
    result = await fetch_chat_gpt(MAIN_BOT_TEMPLATE, data)
    return f"""[{MAIN_BOT_NAME}]: お待たせ！！{result}"""

async def fetch_chat_gpt(system_template, input):
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, lambda: openai.ChatCompletion.create(
        model=CHATGPT_MODEL,
        messages=[
            {"role": "system", "content": system_template},
            {"role": "user", "content": input},
        ]
    ))
    return response.choices[0].message['content']

def get_random_element(array):
    return random.choice(array)

@app.websocket("/ws/heavy")
async def websocket_heavy_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        # Start both tasks at the same time
        waiting_message_task = asyncio.create_task(send_waiting_message(websocket))
        heavy_task_future = asyncio.ensure_future(heavy_task(data))

        while not heavy_task_future.done():
            await asyncio.sleep(0.1)  # sleep a bit before checking again

        if heavy_task_future.done():
            if not waiting_message_task.done():
                waiting_message_task.cancel()
            result_message = heavy_task_future.result()
            await websocket.send_text(result_message)

@app.websocket("/ws/light")
async def websocket_light_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        joke = get_random_element(JOKES)
        await websocket.send_text(f"""[{SUB_BOT_NAME}]: {joke}""")
