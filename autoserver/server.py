import fastapi.responses
from fastapi import FastAPI
import uvicorn
import jinja2
import pathlib
import inspect
import collections

class TemplateBase():
    jinjaPath = pathlib.Path(__file__).resolve().parent / 'resources/'
    jinjaEnv = jinja2.Environment(loader=jinja2.FileSystemLoader(jinjaPath))
    homepage = jinjaEnv.get_template("homepage.html.jinja2")
    baseform = jinjaEnv.get_template("baseform.html.jinja2")

class funcData(TemplateBase):
    formDatum = collections.namedtuple("formDatum", "varName varType")
    def __init__(self, newfunc):
        self.fn = newfunc
        self.name = newfunc.__name__
        self.typeDict = self.inputTypeDict(newfunc)

    @classmethod
    def inputTypeDict(cls, newfunc):
        argData = inspect.getfullargspec(newfunc)
        argList = argData.args
        typeDict = argData.annotations
        return {argVal: typeDict.get(argVal, str) for argVal in argList}

    @classmethod
    def createForm(cls, newfunc):
        typeDict = cls.inputTypeDict(newfunc)
        formData = [cls.formDatum(argVal, typeDict[argVal].__name__) for argVal in typeDict]
        return cls.baseform.render(formRows=formData)




class AutoServer(TemplateBase):
    def __init__(self):
        self.app = FastAPI()
        self.funcDataList = []

    def addfunc(self, newfunc):
        self.funcDataList.append(funcData(newfunc))
        return newfunc

    def run(self):
        @self.app.get("/",response_class=fastapi.responses.HTMLResponse)
        def read_root():
            return self.homepage.render(fnList=self.funcDataList)

        uvicorn.run(self.app,
                    host="127.0.0.1",
                    port=8000,
                    log_level="debug")

if __name__ == "__main__":
    app = AutoServer()

    @app.addfunc
    def testfunc1(arg1, arg2: int, arg3: float):
        pass

    x=funcData.createForm(testfunc1)
    print(x)

    app.run()

