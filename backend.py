# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, render_template, abort
import json
from helper import InputParser, Token, Dedup, Recover
import db as database
from mail import getMail
from sendemail import sendemail
from generator import FFmapConfig, FastdConfig, aliasMap

app = Flask(__name__)
parser = InputParser()
token = Token()
db = database.DB()
dedup = Dedup()
recover = Recover()
ffmap = FFmapConfig()
fastd = FastdConfig()
alias = aliasMap()

@app.route('/')
def main_site():
        return render_template('index.html')

@app.route('/api/node', methods=['POST'])
def process_new():
    # check for invalid data
    val = parser.getData(request)
    vres = parser.validate(parser.getNodeRegex(), val)
    if vres:
        resp = jsonify(**vres)
        resp.status_code = 400
        return resp
    # check for duplicates
    ddres = dedup.checkDups(val['hostname'], val['mac'], val['key'], None)
    if ddres:
        resp = jsonify(**ddres)
        resp.status_code = 409
        return resp
    # if we reach this part the data should be correct
    resp = val
    resp['token'] = token.getToken()
    db.addNode(resp)
    ffmap.genAliasJson()
    fastd.genFastdConf()
    alias.genAliasMap()
    sendemail(getMail(resp), [resp['email']])
    resp['status'] = 'success'
    return jsonify(**resp)

@app.route('/api/node/<tok>', methods=['GET'])
def process_get(tok):
    vres = parser.validate(parser.getTokenRegex(), {'token': tok})
    if vres:
        resp = jsonify(**vres)
        resp.status_code = 400
        return resp
    tres = token.checkToken(tok)
    if tres:
        resp = jsonify(**tres)
        resp.status_code = 404
        return resp
    return jsonify(**db.getNode(tok))

@app.route('/api/node/<tok>', methods=['PUT'])
def process_update(tok):
    val = parser.getData(request)
    val.update({'token': tok})
    vres = parser.validate(parser.getNodeWithTokenRegex(), val)
    if vres:
        resp = jsonify(**vres)
        resp.status_code = 400
        return resp
    ddres = dedup.checkDups(val['hostname'], val['mac'], val['key'], val['token'])
    if ddres:
        resp = jsonify(**ddres)
        resp.status_code = 409
        return resp
    db.updateNode(val)
    ffmap.genAliasJson()
    fastd.genFastdConf()
    alias.genAliasMap()
    resp = val
    resp['status'] = 'success'
    return jsonify(**resp)

@app.route('/api/recover', methods=['POST'])
def recover_token():
    val = parser.getData(request)
    vres = parser.validate(parser.getRecoveryRegex(), val)
    if vres:
        resp = jsonify(**vres)
        resp.status_code = 400
        return resp
    rres = recover.checkCombination(val['email'],val['mac'])
    if rres:
        resp = jsonify(**rres)
        resp.status_code = 404
        return resp
    else:
        resp_mail = db.getNodeMac(val['mac'])
        sendemail(getMail(resp_mail), [resp_mail['email']])
        resp = val
        resp['status'] = 'success'
        return jsonify(**resp)

if __name__ ==  "__main__":
    app.run(debug=True)
