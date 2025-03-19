from celery import Celery
from celery.result import AsyncResult
from celery.app.control import Inspect
import grpc
from concurrent import futures
import service_pb2
import service_pb2_grpc
from celery_app import search_task

# Membuat aplikasi Celery
app = Celery('search_service', broker='redis://172.16.9.60:6379/0', backend='redis://172.16.9.60:6379/0')


def get_active_workers():
    """Mengambil jumlah worker aktif menggunakan Celery Inspect."""
    try:
        # Memanggil inspect melalui control dari aplikasi Celery
        i = app.control.inspect()  # Memanggil inspect melalui app.control
        active_workers = i.active() or {}
        return len(active_workers)
    except Exception as e:
        return 1  # Default jika tidak ada worker yang terdeteksi

def distribute_indices(all_indices):
    """Distribusi indeks secara otomatis ke jumlah worker aktif."""
    num_workers = get_active_workers()

    if len(all_indices) < num_workers:
        num_workers = len(all_indices)

    chunk_size = len(all_indices) // num_workers
    distributed = [
        ",".join(all_indices[i * chunk_size: (i + 1) * chunk_size])
        for i in range(num_workers)
    ]
    # Tambahkan sisa indeks ke chunk terakhir
    if len(all_indices) % num_workers != 0:
        distributed[-1] += "," + ",".join(all_indices[num_workers * chunk_size:])
    return distributed

class SearchService(service_pb2_grpc.SearchServiceServicer):
    def SearchHadis(self, request, context):
        try:
            # Distribusi file indeks
            all_indices = request.index_files.split(",")
            distributed_indices = distribute_indices(all_indices)

            # Eksekusi task Celery
            tasks = [search_task.apply_async(args=(indices, request.n, request.query)) for indices in distributed_indices]
            results = []
            for task in tasks:
                try:
                    task_result = task.get(timeout=30)  # Timeout untuk mencegah hang
                    results.extend(task_result)
                except Exception as e:
                    print(f"Task failed: {e}")
                    raise

            return service_pb2.SearchResponse(results=results)
        except Exception as e:
            error_message = f"Error processing search: {e}"
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(error_message)
            return service_pb2.SearchResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_SearchServiceServicer_to_server(SearchService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server is running on port 50051.")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
