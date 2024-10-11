from app.schemas import Schema


class RecordAddSchema(Schema):
    description: str
    amount: float


class RecordUpdateSchema(Schema):
    description: str | None = None
    amount: float | None = None
