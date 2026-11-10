from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User, Position, UserCoin
from api_service.dependencies import get_session
from grpc_service.client import get_recommendation, stream_recommendations
router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])


@router.get("/{username}")
def recommend_params(username: str, session: Session = Depends(get_session)):
    # 1. Ищем пользователя
    user = session.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    positions = (
        session.query(Position)
        .join(UserCoin, Position.usercoin_id == UserCoin.id)
        .filter(UserCoin.user_id == user.id, Position.profit_percent.isnot(None))
        .all()
    )
    # 2. Достаем историю его сделок (считаем профит)
    profit_history = [float(p.profit_percent) for p in positions]

    # 3. Вызываем gRPC-сервис
    try:
        recommendation = get_recommendation(username, profit_history)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка gRPC: {str(e)}")

    return {
        "user": username,
        "trades_count": len(profit_history),
        "recommendation": recommendation
    }

@router.get("/{username}/stream")
def get_stream(username: str):
    """Демонстрация Server Streaming."""
    try:
        results = stream_recommendations(username, ["15m", "1h", "4h"])
        return {"user": username, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка gRPC стриминга: {str(e)}")