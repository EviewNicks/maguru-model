LANGSERVE:  └──> /quiz-feedback/playground/
LANGSERVE:
LANGSERVE: See all available routes at /docs/
INFO:     Application startup complete.
INFO:watchfiles.main:5 changes detected
INFO:watchfiles.main:5 changes detected
INFO:watchfiles.main:1 change detected
INFO:watchfiles.main:3 changes detected
INFO:watchfiles.main:1 change detected
INFO:watchfiles.main:3 changes detected
INFO:watchfiles.main:5 changes detected
INFO:     127.0.0.1:50475 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:62752 - "GET /chatbot/playground/ HTTP/1.1" 200 OK
INFO:     127.0.0.1:62752 - "GET /chatbot/playground/assets/index-400979f0.js HTTP/1.1" 200 OK
INFO:     127.0.0.1:58715 - "GET /chatbot/playground/assets/index-52e8ab2f.css HTTP/1.1" 200 OK
INFO:     127.0.0.1:54388 - "GET /chatbot/playground/ HTTP/1.1" 200 OK
INFO:     127.0.0.1:54388 - "GET /chatbot/playground/assets/index-400979f0.js HTTP/1.1" 200 OK
INFO:     127.0.0.1:63288 - "GET /chatbot/playground/assets/index-52e8ab2f.css HTTP/1.1" 200 OK
INFO:     127.0.0.1:54388 - "GET /chatbot/playground/favicon.ico HTTP/1.1" 200 OK
INFO:     127.0.0.1:54388 - "POST /chatbot/stream_log HTTP/1.1" 200 OK
D:\conda_envs\maguru\Lib\site-packages\sse_starlette\sse.py:245: LangChainDeprecationWarning: astream_log is deprecated. Use astream instead.
  async for data in self.body_iterator:
INFO:app.db.checkpointer:Initialized LangGraph InMemorySaver checkpointer.
INFO:httpx:HTTP Request: POST https://openrouter.ai/api/v1/chat/completions "HTTP/1.1 404 Not Found"
ERROR:app.graphs.qa_graph:Error invoking LLM in qa_graph: Error code: 404 - {'error': {'message': 'No endpoints found for arcee-ai/trinity-mini:free.', 'code': 404}, 'user_id': 'user_2yj39fGOELlTlO6AcLdeMIYF93W'}
Traceback (most recent call last):
  File "D:\.maguru\maguru-model\app\graphs\qa_graph.py", line 96, in generate_answer_node
    response = llm.invoke(conversation_messages)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\conda_envs\maguru\Lib\site-packages\langchain_core\language_models\chat_models.py", line 476, in invoke
    self.generate_prompt(
  File "D:\conda_envs\maguru\Lib\site-packages\langchain_core\language_models\chat_models.py", line 1849, in generate_prompt
    return self.generate(prompt_messages, stop=stop, callbacks=callbacks, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\conda_envs\maguru\Lib\site-packages\langchain_core\language_models\chat_models.py", line 1656, in generate
    self._generate_with_cache(
  File "D:\conda_envs\maguru\Lib\site-packages\langchain_core\language_models\chat_models.py", line 1953, in _generate_with_cache
    for chunk in self._stream(messages, stop=stop, **kwargs):
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\conda_envs\maguru\Lib\site-packages\langchain_openai\chat_models\base.py", line 1367, in _stream
    _handle_openai_api_error(e)
  File "D:\conda_envs\maguru\Lib\site-packages\langchain_openai\chat_models\base.py", line 1340, in _stream
    response = self.client.create(**payload)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\conda_envs\maguru\Lib\site-packages\openai\_utils\_utils.py", line 286, in wrapper        
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "D:\conda_envs\maguru\Lib\site-packages\openai\resources\chat\completions\completions.py", line 1147, in create
    return self._post(
           ^^^^^^^^^^^
  File "D:\conda_envs\maguru\Lib\site-packages\openai\_base_client.py", line 1259, in post
    return cast(ResponseT, self.request(cast_to, opts, stream=stream, stream_cls=stream_cls))        
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\conda_envs\maguru\Lib\site-packages\openai\_base_client.py", line 1047, in request        
    raise self._make_status_error_from_response(err.response) from None
openai.NotFoundError: Error code: 404 - {'error': {'message': 'No endpoints found for arcee-ai/trinity-mini:free.', 'code': 404}, 'user_id': 'user_2yj39fGOELlTlO6AcLdeMIYF93W'}
