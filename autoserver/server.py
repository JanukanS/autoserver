import fastapi.responses
from fastapi import FastAPI
import uvicorn
import jinja2
import pathlib
import inspect
import collections
import pydantic

class TemplateBase():
    jinjaPath = pathlib.Path(__file__).resolve().parent / 'resources/'
    jinjaEnv = jinja2.Environment(loader=jinja2.FileSystemLoader(jinjaPath))
    homepage = jinjaEnv.get_template("homepage.html.jinja2")
    baseform = jinjaEnv.get_template("baseform.html.jinja2")
    frontfunc = jinjaEnv.get_template("frontfunc.html.jinja2")

class funcData(TemplateBase):
    formDatum = collections.namedtuple("formDatum", "varName varType")
    def __init__(self, newfunc):
        self.fn = newfunc
        self.name = newfunc.__name__
        self.typeDict = self.inputTypeDict(newfunc)
        self.frontEndPoint = f"/front/{newfunc.__name__}"
        self.backEndPoint = f"/back/{newfunc.__name__}"
        self.form = self.createForm(newfunc)
        self.frontpage = self.frontfunc.render(funcForm=self.form)
        self.model = self.createModel(newfunc)

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
        return cls.baseform.render(formRows=formData,
                                   backEndPoint=f"/back/{newfunc.__name__}")

    @classmethod
    def createModel(cls, newfunc):
        typeDict = cls.inputTypeDict(newfunc)
        modelTypeDict = {varName: (typeDict[varName], ...) for varName in typeDict}
        return pydantic.create_model(f"{newfunc.__name__}_model", **modelTypeDict)





class AutoServer(TemplateBase):
    def __init__(self):
        self.app = FastAPI()
        self.funcDataList = []

    def addfunc(self, newfunc):
        fData = funcData(newfunc)
        self.funcDataList.append(fData)

        @self.app.get(fData.frontEndPoint, response_class=fastapi.responses.HTMLResponse)
        def show_page():
            return fData.frontpage

        @self.app.post(fData.backEndPoint)
        def back_endpoint(inputData: fData.model):
            return newfunc(**inputData.__dict__)

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
    def TaxCalc(province:str, cost: float, taxrate:int):
        tax = cost*float(taxrate)/100
        output = f"The tax in {province} for an item worth ${cost} is {tax}."
        output += f"The total cost is ${cost + tax}."
        return output

    @app.addfunc
    def TargetPrice(province: str, targetcost: float, taxrate:int):
        targetRatio = 1.0 + float(taxrate)/100
        output = f"To have a final cost of ${targetcost} in {province},"
        output += f"the pretax price should be ${targetcost/targetRatio}"
        return output

    app.run()

