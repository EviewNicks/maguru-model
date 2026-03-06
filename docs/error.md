[Fast Refresh] done in 103ms
logger.ts:196 2026-03-06T09:54:05.056Z [INFO] [ChatbotAssistant][sendMessage] Starting chatbot request{  "question": "Explain this topic in simple terms",  "aiMessageIndex": 1,  "performance": {    "timestamp": 1772790845056,    "memory": null  }}
logger.ts:196 2026-03-06T09:54:05.056Z [INFO] [LangServeAPI][streamChatbot] Starting chatbot stream{  "url": "http://localhost:8000/chatbot/stream",  "question": "Explain this topic in simple terms",  "performance": {    "timestamp": 1772790845056,    "memory": null  }}
installHook.js:1 2026-03-06T09:54:12.585Z [WARN] [LangServeAPI][streamText] Event is not an object{  "chunk": 1,  "eventType": "string",  "event": "\"\\n\\n**Jangan khawatir, siswa! Mari kita pecahkan topik ini dengan mudah dan santai, seperti mempela",  "performance": {    "timestamp": 1772790852585,    "memory": null  }}
overrideMethod @ installHook.js:1
warn @ logger.ts:220
streamText @ api.ts:216
await in streamText
streamChatbot @ api.ts:303
sendMessage @ ChatbotAssistant.tsx:106
executeDispatch @ react-dom-client.development.js:16970
runWithFiberInDEV @ react-dom-client.development.js:871
processDispatchQueue @ react-dom-client.development.js:17020
(anonymous) @ react-dom-client.development.js:17621
batchedUpdates$1 @ react-dom-client.development.js:3311
dispatchEventForPluginEventSystem @ react-dom-client.development.js:17174
dispatchEvent @ react-dom-client.development.js:21357
dispatchDiscreteEvent @ react-dom-client.development.js:21325Understand this warning
logger.ts:196 2026-03-06T09:54:12.593Z [INFO] [LangServeAPI][streamChatbot] Stream completed successfully{  "totalLength": 0,  "performance": {    "timestamp": 1772790852593,    "memory": null  }}
logger.ts:196 2026-03-06T09:54:12.594Z [INFO] [ChatbotAssistant][sendMessage] Stream completed{  "totalLength": 0,  "performance": {    "timestamp": 1772790852594,    "memory": null  }}