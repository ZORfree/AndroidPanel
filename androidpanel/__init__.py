#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   socket.py
@Contact :   haruihi@163.com Zorfree
@License :   (C)Copyright 2017-2019, MIT

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/11/13 20:01   Zorfree      1.0         None
'''
import os
from flask import Flask, render_template
from androidpanel.settings import config
from androidpanel.blueprints.main import main_bp
from androidpanel.blueprints.socket import socket_bp
from androidpanel.extensions import socketio, db
import click

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('androidpanel')
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_commands(app)
    return app


def register_extensions(app):
    db.init_app(app)
    socketio.init_app(app, async_mode=None, ping_interval=2, ping_timeout=5)

def register_blueprints(app,):
    app.register_blueprint(main_bp)
    app.register_blueprint(socket_bp)


def register_errorhandlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(413)
    def request_entity_too_large(e):
        return render_template('errors/413.html'), 413

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500


def register_commands(app):
    @app.cli.command()
    def forge():

        db.drop_all()
        db.create_all()
        click.echo('Database initialization completed.')
