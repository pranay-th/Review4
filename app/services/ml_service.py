from sqlalchemy.orm import Session


def train_model(db: Session) -> dict:
    # TODO: implement once data engineer shares chosen model and feature columns
    raise NotImplementedError


def predict_cost(input_data: dict) -> float:
    # TODO: implement once model is trained and feature set is confirmed
    raise NotImplementedError
