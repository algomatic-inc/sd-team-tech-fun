import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
// import * as sqs from 'aws-cdk-lib/aws-sqs';

export class InfraStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // The code that defines your stack goes here

    // example resource
    // const queue = new sqs.Queue(this, 'InfraQueue', {
    //   visibilityTimeout: cdk.Duration.seconds(300)
    // });

    const s3 = new cdk.aws_s3.Bucket(this, 'sd-images', {
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
      blockPublicAccess: cdk.aws_s3.BlockPublicAccess.BLOCK_ALL,
      encryption: cdk.aws_s3.BucketEncryption.S3_MANAGED,
      enforceSSL: true,
    });

    const sdDynamoTable = new cdk.aws_dynamodb.Table(this, 'sd', {
      partitionKey: { name: 'locationId', type: cdk.aws_dynamodb.AttributeType.STRING },
      sortKey: { name: 'category', type: cdk.aws_dynamodb.AttributeType.STRING },
      tableName: 'SatelliteData',
      billingMode: cdk.aws_dynamodb.BillingMode.PAY_PER_REQUEST,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    const personaDynamoTable = new cdk.aws_dynamodb.Table(this, 'persona', {
      partitionKey: { name: 'personaId', type: cdk.aws_dynamodb.AttributeType.STRING },
      tableName: 'Persona',
      billingMode: cdk.aws_dynamodb.BillingMode.PAY_PER_REQUEST,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });
  }
}
