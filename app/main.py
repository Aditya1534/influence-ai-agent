from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from linkedin_agent import load_user_profile, generate_post
import traceback

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    profile = load_user_profile()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "profile": profile,
        "post": None
    })

@app.post("/", response_class=HTMLResponse)
async def submit_form(request: Request):
    profile = load_user_profile()
    try:
        post = generate_post(profile)
    except Exception as e:
        print("❌ Error generating post in POST route:", e)
        traceback.print_exc()
        post = "⚠️ Something went wrong during generation."
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "profile": profile,
        "post": post
    })
