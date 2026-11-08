import grpc
from concurrent import futures
from grpc_service import recommendation_pb2
from grpc_service import recommendation_pb2_grpc

class RecommendationServicer(recommendation_pb2_grpc.RecommendationServiceServicer):
    def GetRecommendation(self, request, context):
        # Выводим в консоль, что gRPC получил запрос (это требование ЛР)
        print(f"[gRPC] Получен запрос от пользователя: {request.username}")

        # Простейшая логика: берем средний профит и корректируем параметры
        if request.profit_history:
            avg_profit = sum(request.profit_history) / len(request.profit_history)
        else:
            avg_profit = 0.0

        # Логика рекомендаций (заглушка для примера)
        ema = 20 if avg_profit < 2.0 else 50
        target = 3.0 if avg_profit < 2.0 else 5.0
        stop = 1.5

        msg = f"Средний профит {avg_profit:.2f}%. Рекомендуем EMA={ema}."

        return recommendation_pb2.RecommendationResponse(
            optimal_ema_period=ema,
            optimal_target_pct=target,
            optimal_stop_pct=stop,
            message=msg
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    recommendation_pb2_grpc.add_RecommendationServiceServicer_to_server(
        RecommendationServicer(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC Server запущен на порту 50051...")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()