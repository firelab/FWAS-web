from flask import current_app


def test_confirm_test_config_used(app):
    assert app.config['SECRET_KEY'] == 'catcat'
    assert current_app is not None
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'postgresql://docker:docker@localhost:5432/unittests'
    # assert app.config['DEBUG']
