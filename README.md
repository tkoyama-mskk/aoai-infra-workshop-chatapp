# aoai-infra-workshop-chatapp
このリポジトリには「インフラアーキテクト向け AOAI 設計考慮点ワークショップ」の演習で使用するプログラムが格納されています。

演習では、本来は以下のプログラムで動作確認します。
 - [sample-app-aoai-chatGPT](https://github.com/microsoft/sample-app-aoai-chatGPT)

しかし、こちらのリポジトリは改修が頻繁に行われており、正しく動作しないタイミングや、そもそも Web アプリをうまくデプロイできないケースがあります。
その様なケースにおいての回避策として、簡単な疎通用のサンプルアプリを用意しました。


## 動作確認手順

### はじめに

- 本演習で使用するサンプルプログラムは疎通確認だけを目的に作成されています。
実運用に耐えられるようには作成されておりません。

- 本サンプルプログラムは Azure OpenAI へのアクセスは API キー認証を使用します
元の演習では、Managed ID を使用した認証になっており、違いがありますのでご注意ください

### STEP1 - Web App リソースのデプロイ

- Azure Portal から [Web アプリ] を作成してください
<img src="figs/01-create-webapp.svg" alt="alt" width="600px" />

- 以下のパラメータで作成します。
  - サブスクリプション - ご利用のサブスクリプションを指定します
  - リソースグループ - 任意です。既存のリソースグループでもいいですし、新規に作成したリソースグループでも大丈夫です。
  - 名前 - お好きな名前を付けてください。ただし、グローバルで一意である必要があります。
  - 公開 - [コード] を選択します
  - ランタイムスタック - [Python 3.12] を選択します
  - オペレーティングシステム - [Linux] を選択します
  - リージョン - 任意ですが、原則として AOAI をデプロイしたリージョンと同じにします
  - Linux プラン - 新規作成してください（名前等は任意）
  - 価格プラン - 任意です。
- その他のタブは既定のままで大丈夫です。
- 最後に「確認および作成]-[作成] をクリックします

### STEP2 - 仮想ネットワーク統合を有効にする
<img src="figs/02-vnet-integ.svg" alt="alt" width="800px" />

- デプロイした Web アプリ（App Service）のリソースに移動して、[ネットワーク] から「仮想ネットワーク統合」を構成します。

### STEP3 - アプリケーションをデプロイします
今回は「外部の Git」からの手動デプロイを利用します。最初に、SCM 基本認証をオンにしておく必要があります。

#### SCM 基本認証を有効にします
<img src="figs/03-config-scm-auth.svg" alt="alt" width="800px" />
- Web アプリ（App Service）の [構成] から、[SCM 基本認証の発行資格情報] を [オン] にします。

#### 外部 Git を指定します
<img src="figs/04-external-git.svg" alt="alt" width="800px" />

- Web アプリ（App Service）の [デプロイセンターから]、[ソース] に「外部 Git」を指定します
  - リポジトリは次を指定してください → https://github.com/tkoyama-mskk/aoai-infra-workshop-chatapp.git
  - ブランチは [main] と指定します
  - リポジトリの種類は [パブリック] です
- 最後に [保存] をクリックしてください
- そのまま暫くまちます。デプロイの進捗は [ログ] のタブから確認できます

### STEP4 - 環境変数を設定します

#### モデルの名前を控えます
<img src="figs/05-model-name.svg" alt="alt" width="400px" />

- モデルの名前は、デプロイしたモデルの名前です。「Azure AI Foundry」のチャットプライグラウンドから確認できます。

#### キーとエンドポイントの値を控えます
<img src="figs/06-key-and-endpoint.svg" alt="alt" width="600px" />

- キーとエンドポイントは、Azure OpenAI の [キーとエンドポイント] から取得可能です

#### 環境変数を設定します
先ほど控えた値を環境変数に設定します
<img src="figs/07-environment-variables.svg" alt="alt" width="600px" />

- Web アプリ（App Service）の [環境変数] から以下の３つの環境変数を追加してください
  - DEPLOYMENT_NAME - 「gpt-35-turbo-16k」などデプロイしたモデル名を指定します
  - ENDPOINT_URL - OpenAI のエンドポイント URL を指定します。
  - AZURE_OPENAI_API_KEY - OpenAI のキーを指定します。
- 最後に[適用]ボタン、[確認] をクリックします

### STEP5 - 動作確認
#### アプリの起動
<img src="figs/08-launch-webapp.svg" alt="alt" width="600px" />
- Web アプリ（App Service）の [概要] から [既定のドメイン]にある URL をクリックするとアプリが起動します

#### 動作確認
<img src="figs/09-sample-app.svg" alt="alt" width="600px" />
- テキストボックスに「国産メインフレームはどのようにして開発されましたか？」と入力すると結果が返ります。（すこし時間がかかります）

	


