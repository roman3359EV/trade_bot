from celery import Celery
import sys

from src.config.queue import QueueSettings

settings = QueueSettings()

queue_app = Celery(
    main='queue',
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=[
        'src.infrastructure.telegram.telegram'
    ]
)

queue_app.conf.update(broker_connection_retry_on_startup=True)


if __name__ == '__main__':
    queue_app.start(argv=sys.argv[1:])
