from sqlalchemy.orm import Session


def get_top_countries(db: Session, limit: int = 10) -> list[dict]:
    # TODO
    raise NotImplementedError


def get_region_summary(db: Session) -> list[dict]:
    # TODO
    raise NotImplementedError


def get_trade_trends(db: Session) -> list[dict]:
    # TODO
    raise NotImplementedError
