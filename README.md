# AWS で始めるサーバレスアーキテクチャ入門

このリポジトリでは、AWS の主要なサーバレスサービスを活用した RESTful な API サーバーを構築する方法を学びます。API Gateway、Lambda、DynamoDB、Cognito、CloudWatch Logs を組み合わせて、タスク管理アプリを構築します。

## **前提条件**

以下のツールや設定が必要です：

1. **AWS CLI**

   - インストール: [公式ドキュメント](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
   - プロファイル設定（`cli-user`を使用します）：
     ```bash
     aws configure --profile cli-user
     ```

2. **AWS SAM CLI**

   - インストール: [公式ドキュメント](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)

3. **AWS アカウント**
   - IAM ユーザーに管理者権限（AdministratorAccess）を付与してください。

## リソースデプロイ（SAM）

### 1. SAM でビルド

```bash
sam build
```

### 2. SAM でデプロイ

```bash
# 初回時
sam deploy --guided --profile cli-user

# 2回目以降
sam deploy
```

## API 使用方法（タスク関連）

### 1. タスクを作成

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <idToken>" \ # 認証機能実装後に必須
  -d '{"title": "Task title"}' \
  "<API Gateway Base URL>/dev/tasks"
```

### 2. タスク一覧を取得

```bash
curl -X GET \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <idToken>" \ # 認証機能実装後に必須
  "<API Gateway Base URL>/dev/tasks"
```

### 3. タスクを更新する

```bash
curl -X PATCH \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <idToken>" \ # 認証機能実装後に必須
  -d '{"title": "New Task title", "taskStatus": "NewStatus"}' \
  "<API Gateway Base URL>/dev/tasks/{taskId}"
```

### 4. タスクを削除する

```bash
curl -X DELETE \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <idToken>" \ # 認証機能実装後に必須
  "<API Gateway Base URL>/dev/tasks/{taskId}"
```

## Cognito 使用方法

### 1. サインアップ

**確認メールが送信されるので注意！**

```bash
curl -X POST https://cognito-idp.ap-northeast-1.amazonaws.com/ \
-H "X-Amz-Target: AWSCognitoIdentityProviderService.SignUp" \
-H "Content-Type: application/x-amz-json-1.1" \
-d '{
  "ClientId" : "<UserPoolClientId>",
  "Username" : "<メールアドレス>",
  "Password" : "<パスワード>"
}'
```

### 2. メール認証

```bash
curl -X POST https://cognito-idp.ap-northeast-1.amazonaws.com/ \
-H "X-Amz-Target: AWSCognitoIdentityProviderService.ConfirmSignUp" \
-H "Content-Type: application/x-amz-json-1.1" \
-d '{
  "ClientId" : "<UserPoolClientId>",
  "Username" : "<メールアドレス>",
  "ConfirmationCode" : "<認証コード>"
}'
```

### 3. ログイン

```bash
curl -X POST https://cognito-idp.ap-northeast-1.amazonaws.com/ \
-H "X-Amz-Target: AWSCognitoIdentityProviderService.InitiateAuth" \
-H "Content-Type: application/x-amz-json-1.1" \
-d '{
  "ClientId" : "<UserPoolClientId>",
  "AuthFlow" : "USER_PASSWORD_AUTH",
  "AuthParameters": {
    "USERNAME" : "<メールアドレス>",
    "PASSWORD" : "<パスワード>"
  }
}'
```

### 4. テスト用ユーザー作成

```bash
# ユーザー作成
aws cognito-idp admin-create-user \
  --user-pool-id <UserPoolId> \
  --username <メールアドレス> \
  --user-attributes Name=email,Value=<メールアドレス> Name=email_verified,Value=true \
  --message-action SUPPRESS \
  --profile cli-user

# パスワードを有効化
aws cognito-idp admin-set-user-password \
  --user-pool-id <UserPoolId> \
  --username <メールアドレス> \
  --password "<パスワード>" \
  --permanent \
  --profile cli-user
```
