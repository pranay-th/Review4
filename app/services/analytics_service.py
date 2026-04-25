from sqlalchemy.orm import Session


def get_top_countries(db: Session, limit: int = 10) -> list[dict]:
    # TODO: implement once data engineer confirms aggregation logic
    raise NotImplementedError


def get_region_summary(db: Session) -> list[dict]:
    # TODO: implement once data engineer confirms region grouping logic
    raise NotImplementedError


def get_trade_trends(db: Session) -> list[dict]:
    # TODO: implement once data engineer confirms trend analysis approach
    raise NotImplementedError
