(D:\conda_envs\maguru) PS D:\.maguru\maguru-model> python server.py
INFO:     Will watch for changes in these directories: ['D:\\.maguru\\maguru-model']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [34156] using WatchFiles
INFO:watchfiles.main:4 changes detected
INFO:     Started server process [30264]
INFO:     Waiting for application startup.

     __          ___      .__   __.   _______      _______. _______ .______     ____    ____  _______
    |  |        /   \     |  \ |  |  /  _____|    /       ||   ____||   _  \    \   \  /   / |   ____|
    |  |       /  ^  \    |   \|  | |  |  __     |   (----`|  |__   |  |_)  |    \   \/   /  |  |__
    |  |      /  /_\  \   |  . `  | |  | |_ |     \   \    |   __|  |      /      \      /   |   __|
    |  `----./  _____  \  |  |\   | |  |__| | .----)   |   |  |____ |  |\  \----.  \    /    |  |____
    |_______/__/     \__\ |__| \__|  \______| |_______/    |_______|| _| `._____|   \__/     |_______|
    
LANGSERVE: Playground for chain "/greeting/" is live at:
LANGSERVE:  │
LANGSERVE:  └──> /greeting/playground/
LANGSERVE:
LANGSERVE: Playground for chain "/hint/" is live at:
LANGSERVE:  │
LANGSERVE:  └──> /hint/playground/
LANGSERVE:
LANGSERVE: Playground for chain "/chatbot/" is live at:
LANGSERVE:  │
LANGSERVE:  └──> /chatbot/playground/
LANGSERVE:
LANGSERVE: Playground for chain "/explain-code/" is live at:
LANGSERVE:  │
LANGSERVE:  └──> /explain-code/playground/
LANGSERVE:
LANGSERVE: Playground for chain "/quiz-feedback/" is live at:
LANGSERVE:  │
LANGSERVE:  └──> /quiz-feedback/playground/
LANGSERVE:
LANGSERVE: See all available routes at /docs/
INFO:     Application startup complete.
INFO:watchfiles.main:3 changes detected



(base) PS D:\.maguru\maguru-model> curl http://localhost:8000/health

Security Warning: Script Execution Risk                                                                         Invoke-WebRequest parses the content of the web page. Script code in the web page might be run when the page is  parsed.                                                                                                              RECOMMENDED ACTION:                                                                                       
      Use the -UseBasicParsing switch to avoid script code execution.

      Do you want to continue?
    
[Y] Yes  [A] Yes to All  [N] No  [L] No to All  [S] Suspend  [?] Help (default is "N"): Y


StatusCode        : 200
StatusDescription : OK
Content           : {"status":"ok","service":"Maguru AI API","version":"1.0.0"}
RawContent        : HTTP/1.1 200 OK
                    Content-Length: 59
                    Content-Type: application/json
                    Date: Sun, 15 Feb 2026 08:24:02 GMT
                    Server: uvicorn

                    {"status":"ok","service":"Maguru AI API","version":"1.0.0"}
Forms             : {}
Headers           : {[Content-Length, 59], [Content-Type, application/json], [Date, Sun, 15 Feb 2026 08:24:02 
                    GMT], [Server, uvicorn]}
Images            : {}
InputFields       : {}
Links             : {}
ParsedHtml        : mshtml.HTMLDocumentClass
RawContentLength  : 59



(base) PS D:\.maguru\maguru-model> 