import grpc
from grpc_service import recommendation_pb2
from grpc_service import recommendation_pb2_grpc
def get_recommendation(username: str, profit_history: list):
    # Подключаемся к локальному gRPC-серверу на порту 50051
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = recommendation_pb2_grpc.RecommendationServiceStub(channel)#заглушка

        request = recommendation_pb2.RecommendationRequest(
            username=username,
            profit_history=profit_history
        )#Формирует Protobuf-сообщение

        # Вызываем удаленный метод
        response = stub.GetRecommendation(request)

        return {
            "ema_period": response.optimal_ema_period,
            "target_pct": response.optimal_target_pct,
            "stop_pct": response.optimal_stop_pct,
            "message": response.message
        }


def stream_recommendations(username: str, timeframes: list):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = recommendation_pb2_grpc.RecommendationServiceStub(channel)
        request = recommendation_pb2.StreamRequest(username=username, timeframes=timeframes)

        # stub.StreamRecommendations возвращает итератор
        return [
            {"ema": r.optimal_ema_period, "msg": r.message}
            for r in stub.StreamRecommendations(request)
        ]