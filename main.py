from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from schemas.url import UrlResult, UrlsRequest
from services.checker import check_urls


app = FastAPI(
    
    title="SEO Status Checker"
)


app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")



@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


@app.post(
    "/check",
    response_model=list[UrlResult],
)

async def check(request: UrlsRequest):
    return await check_urls(request.urls)
    