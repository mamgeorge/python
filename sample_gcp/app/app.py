import os, sys, datetime
import numpy as np
import colorama
from PIL import Image
from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from colorama import Fore, Back, Style, init

print(Back.GREEN + Fore.BLACK + Style.BRIGHT + ' Hello, World! '+ Style.RESET_ALL)
print(f'{Back.CYAN}{Style.BRIGHT} datetime: {datetime.datetime.now()} {Style.RESET_ALL}') 

