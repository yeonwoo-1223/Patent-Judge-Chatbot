# 나머지 필요한 모듈 한 번에 로드
from langdetect import detect, LangDetectException
import streamlit as st
import speech_recognition as sr
from streamlit_chat import message
from openai import OpenAI
import openai
from dotenv import load_dotenv
import pyttsx3
import os
import json
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnablePassthrough
from langchain.chains import LLMChain
# 비슷한 상황에서 판결된 과실 비율 문서 검색
from difflib import SequenceMatcher
import natsort
import cv2
import numpy as np
from PIL import Image
