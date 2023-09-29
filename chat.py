import os
import logging
import uuid
import glob
import shutil
from werkzeug.utils import secure_filename
import pandas as pd
import json
from flask import send_from_directory, jsonify, request, flash, redirect, Response, make_response
from pathlib import Path

from Suggestion_Agent import SuggestAgent
from db import Chat
from constants import PDF_DIR
from langchain.callbacks import get_openai_callback
from QA_Agent import QAModule
from collections import defaultdict
from __main__ import app

# check
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        # save f.filename to vector db
        with get_openai_callback() as cb:
            agent = QAModule()
            agent.add_document_to_index(f.filename)
            print(cb)
        return make_response(jsonify({"status":"SUCCESS", "output":f'file uploaded successfully. Session id: {str(uuid.uuid4())}'}), 201)


@app.route("/get-all-messages", methods=['GET'])
def get_all_messages():
    session_id = request.form['session_id']
    chat_objs = Chat.objects(session_id=session_id)
    messages = []
    if chat_objs:
        for chat_obj in chat_objs:
            messages.append(
                {'creation_time': chat_obj.creation_time.strftime("%m/%d/%Y, %H:%M:%S"),
                 'body': {
                     'sender': chat_obj.sender, 
                     'text':chat_obj.text
                     }
                }
            )
    
    return make_response(jsonify({"status":"SUCCESS", "output":f"{json.dumps(messages)}"}), 201)


@app.route("/suggestions", methods=['GET', 'POST'])
def get_suggestions():
    text = request.form['text']
    sa = SuggestAgent()
    suggestions = sa.get_suggestions(text)
    return make_response(jsonify({"status":"SUCCESS", "output":"\n".join(suggestions)}))


@app.route("/chat-message", methods=['GET','POST'])
def post_message():
    
    text = request.form['text']
    session_id = request.form['session_id']
    sender = request.form['sender']
    character = request.form['character']
    chat_objs = Chat.objects(session_id=session_id).order_by('creation_time')
    chat_history = defaultdict(list)
    user_text = ""
    for chat_obj in chat_objs:
        if chat_obj.sender != "agent":
            if user_text:
                user_text += "\n" + chat_obj.text
            else:
                user_text = chat_obj.text
            sender = chat_obj.sender
        else:
            if user_text:
                chat_history[sender].append(user_text)
                user_text = ""
            chat_history[chat_obj.sender].append(chat_obj.text)

    assert len(chat_history[sender]) == len(chat_history["agent"])
    with get_openai_callback() as cb:
        followup_qa = False
        agent = QAModule()
        for user_chat, agent_chat in zip(chat_history[sender], chat_history["agent"]):
            agent.update_chat_history_for_user(sender, user_chat, agent_chat)
        if not agent.get_chat_history_for_user(sender):
            followup_qa = True
        response_message = agent.query_index(text, sender, return_source_docs=False, character=character, followup_qa=followup_qa)
        # print(agent.get_chat_history_for_user(sender))
        # response_message = "call_openai_function(text, chat_history)"
        agent.update_chat_history_for_user(sender, text, response_message)
        print(cb)
    Chat(session_id=session_id, sender=sender, text=text).save()
    Chat(session_id=session_id, sender="agent", text=response_message).save()
    return make_response(jsonify({"status":"SUCCESS", "output":f"{response_message}"}), 201)



@app.route('/image/<filename>', methods=['GET'])
def get_image(filename):
    response = send_from_directory('./images/photosynthesis', filename)

    return response

if __name__ == '__main__':
    app.run()
