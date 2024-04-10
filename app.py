from flask import Flask, render_template, flash, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
import mysql.connector
import datetime

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)