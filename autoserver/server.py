import fastapi.responses
from fastapi import FastAPI
import uvicorn
import jinja2
import pathlib

class AutoServer():
    def __init__(self):
        self.app = FastAPI()
        jinjaPath = pathlib.Path(__file__).resolve().parent / 'resources/'
        jinjaEnv = jinja2.Environment(loader=jinja2.FileSystemLoader(jinjaPath))
        self.homepage = jinjaEnv.get_template("homepage.html.jinja2")
        self.funcList = []

    def addfunc(self, newfunc):
        self.funcList.append(newfunc)

    def run(self):
        @self.app.get("/",response_class=fastapi.responses.HTMLResponse)
        def read_root():
            return self.homepage.render(fnList=self.funcList)

        uvicorn.run(self.app,
                    host="127.0.0.1",
                    port=8000,
                    log_level="debug")

if __name__ == "__main__":
    app = AutoServer()

    @app.addfunc
    def testfunc1(exampleArg):
        pass

    app.run()

