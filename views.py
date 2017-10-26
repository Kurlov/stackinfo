from app import app
from flask import render_template, flash, redirect, g, session, request


@app.route('/')
def index():
    return 'hello'
