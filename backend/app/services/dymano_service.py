import os
import uuid
from datetime import datetime, timezone
import boto3
from botocore.exceptions import ClientError

class DynamoService:
    def __init__(self):
        self.region = os.getenv("AWS_REGION", "us-east-1")
        self.table_name = os.getenv("TABLE_NAME", "ShortenedURLs")
        self.resource = boto3.resource("dynamodb", region_name=self.region)
        self.table = self.resource.Table(self.table_name)

    def create_link(self, original_url: str) -> dict:
        short_code = str(uuid.uuid4())[:8] # UUID más corto para mejor UX
        item = {
            "short_code": short_code,
            "original_url": original_url,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        self.table.put_item(Item=item)
        return item

    def get_link(self, short_code: str) -> dict | None:
        response = self.table.get_item(Key={"short_code": short_code})
        return response.get("Item")