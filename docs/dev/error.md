(base) PS D:\.maguru\maguru-model> conda activate D:\conda_envs\maguru
(D:\conda_envs\maguru) PS D:\.maguru\maguru-model> uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
INFO:     Will watch for changes in these directories: ['D:\\.maguru\\maguru-model']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [22016] using WatchFiles
Process SpawnProcess-1:
Traceback (most recent call last):
  File "D:\conda_envs\maguru\Lib\multiprocessing\process.py", line 314, in _bootstrap
    self.run()
  File "D:\conda_envs\maguru\Lib\multiprocessing\process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
  File "D:\conda_envs\maguru\Lib\site-packages\uvicorn\_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
  File "D:\conda_envs\maguru\Lib\site-packages\uvicorn\server.py", line 67, in run
    return asyncio_run(self.serve(sockets=sockets), loop_factory=self.config.get_loop_factory())
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\conda_envs\maguru\Lib\asyncio\runners.py", line 195, in run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File "D:\conda_envs\maguru\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\conda_envs\maguru\Lib\asyncio\base_events.py", line 691, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "D:\conda_envs\maguru\Lib\site-packages\uvicorn\server.py", line 71, in serve
    await self._serve(sockets)
  File "D:\conda_envs\maguru\Lib\site-packages\uvicorn\server.py", line 78, in _serve
    config.load()
  File "D:\conda_envs\maguru\Lib\site-packages\uvicorn\config.py", line 439, in load
    self.loaded_app = import_from_string(self.app)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\conda_envs\maguru\Lib\site-packages\uvicorn\importer.py", line 22, in import_from_string
    raise exc from None
  File "D:\conda_envs\maguru\Lib\site-packages\uvicorn\importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\conda_envs\maguru\Lib\importlib\__init__.py", line 90, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 999, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "D:\.maguru\maguru-model\app\main.py", line 8, in <module>
    from app.api.router import api_router
  File "D:\.maguru\maguru-model\app\api\__init__.py", line 2, in <module>
    from .router import api_router
  File "D:\.maguru\maguru-model\app\api\router.py", line 2, in <module>
    from app.api.v1.router import api_v1_router
  File "D:\.maguru\maguru-model\app\api\v1\__init__.py", line 2, in <module>
    from .router import api_v1_router
  File "D:\.maguru\maguru-model\app\api\v1\router.py", line 2, in <module>
    from app.api.v1.endpoints import health, ingest, chat, quiz
  File "D:\.maguru\maguru-model\app\api\v1\endpoints\ingest.py", line 3, in <module>
    from app.services.rag_service import ingest_document, ingest_text_content
  File "D:\.maguru\maguru-model\app\services\__init__.py", line 2, in <module>
    from .rag_service import ingest_document, get_course_context
  File "D:\.maguru\maguru-model\app\services\rag_service.py", line 5, in <module>
    from langchain_community.document_loaders import PyPDFLoader, TextLoader
ModuleNotFoundError: No module named 'langchain_community'
