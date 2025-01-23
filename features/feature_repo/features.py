from datetime import datetime
from pathlib import Path
from feast import Entity, Feature, ValueType
from feast.feature_view import FeatureView
from feast.infra.offline_stores.file_source import FileSource
from google.protobuf.duration_pb2 import Duration

DATA_DIR = Path(Path().resolve().parent.parent, "data")
# Read data
START_TIME = "2025-01-23"
project_details = FileSource(
    path=str(Path(DATA_DIR, "features.parquet")),
    event_timestamp_column="created_on",
)
project = Entity(
    name="id",
    value_type=ValueType.INT64,
    description="project id",
)


# Define a Feature View for each project
project_details_view = FeatureView(
    name="project_details",
    entities=["id"],
    ttl=Duration(
        seconds=(datetime.today() - datetime.strptime(START_TIME, "%Y-%m-%d")).days * 24 * 60 * 60
    ),
    features=[
        Feature(name="text", dtype=ValueType.STRING),
        Feature(name="tag", dtype=ValueType.STRING),
    ],
    online=True,
    input=project_details,
    tags={},
)