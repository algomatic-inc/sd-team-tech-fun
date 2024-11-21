from boto3.dynamodb.types import TypeSerializer
from decimal import Decimal


def json_to_dynamodb(json_list: list[dict]) -> dict:
    """
    通常のJSONをDynamoDB JSON形式に変換する関数
    """
    result = []
    serializer = TypeSerializer()
    for j in json_list:
        dynamodb_json = {k: serializer.serialize(v) for k, v in j.items()}
        result.append(dynamodb_json)
    return result


# 使用例
sample_data = [
    {
        "shop_lat": Decimal("37.39124887111705"),
        "shop_lng": Decimal("136.90151661513806"),
        "shop_name": "xxx",
        "shop_open_time": "7:30",
        "shop_close_time": "18:00",
        "is_24_hour": False,
        "shop_description": "コンビニエンスストア",
    }
]

# 変換実行
dynamodb_items = json_to_dynamodb(sample_data)
print(dynamodb_items)
