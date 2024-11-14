import path = require("path");
import * as fs from "fs";
import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as apigateway from "aws-cdk-lib/aws-apigateway";

export class GeminiApiStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // サービスアカウントの認証情報を読み込む
    const credentialsPath = path.join(
      __dirname,
      "../../credentials/tf-satellite-hackathon-826dd6f95aca.json"
    );
    const credentials = JSON.parse(fs.readFileSync(credentialsPath, "utf8"));

    // Lambda関数の定義
    const geminiFunction = new lambda.Function(this, "GeminiFunction", {
      runtime: lambda.Runtime.PYTHON_3_12,
      handler: "index.lambda_handler",
      code: lambda.Code.fromAsset(path.join(__dirname, "../asset"), {
        bundling: {
          image: lambda.Runtime.PYTHON_3_12.bundlingImage,
          command: [
            "bash",
            "-c",
            "pip install . -t /asset-output && cp -au . /asset-output",
          ],
        },
      }),
      memorySize: 1024,
      timeout: cdk.Duration.seconds(30),
      environment: {
        GOOGLE_CLOUD_PROJECT: credentials.project_id,
        GOOGLE_PRIVATE_KEY_ID: credentials.private_key_id,
        GOOGLE_PRIVATE_KEY: credentials.private_key,
        GOOGLE_CLIENT_EMAIL: credentials.client_email,
        GOOGLE_CLIENT_ID: credentials.client_id,
        GOOGLE_CLIENT_X509_CERT_URL: credentials.client_x509_cert_url,
        VERTEX_LOCATION: "us-central1",
      },
    });

    // API Gatewayの作成
    const api = new apigateway.RestApi(this, "GeminiApi", {
      restApiName: "Gemini API",
      description: "API for Gemini AI interactions",
      defaultCorsPreflightOptions: {
        allowOrigins: apigateway.Cors.ALL_ORIGINS,
        allowMethods: apigateway.Cors.ALL_METHODS,
      },
    });

    // API GatewayにLambdaを統合
    const geminiIntegration = new apigateway.LambdaIntegration(geminiFunction);
    api.root.addMethod("POST", geminiIntegration);

    // APIのURLを出力
    new cdk.CfnOutput(this, "ApiUrl", {
      value: api.url,
      description: "API Gateway endpoint URL",
    });
  }
}