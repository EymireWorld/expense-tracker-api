from app.schemas import Schema


class RecordAddSchema(Schema):
    amount: float


class RecordUpdateSchema(Schema):
    amount: float
