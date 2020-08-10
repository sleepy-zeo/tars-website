import bp
import flask
import werkzeug.utils
import config
import os
import database
import utils
import app


@bp.bp_videos.route('/')
def hello_world():
    return 'Hello Videos'


@bp.bp_videos.route('/sample')
def sample():
    return flask.render_template("videos_sample.html")


@bp.bp_videos.route("/selected")
def selected():
    return os.path.join(config.URL_VIDEO_PREFIX, "The_Newsroom_S02E04__HDTVrip_1024x576-YYeTs.mp4")


@bp.bp_videos.route("/upload", methods=["POST"])
def upload():
    file = flask.request.files["file"]
    file_name = werkzeug.utils.secure_filename(file.filename)

    # test
    _file_name = utils.file.get_file_name(file_name)
    _file_type = utils.file.get_file_type(file_name)
    file_name = _file_name.replace(".", "_")+"."+_file_type
    app.app.logger.debug(file_name)

    try:
        # save to database
        tb_videos = database.tb_videos.TB_Videos()
        tb_videos.insert((config.DB_ID_PREFIX + utils.uuid.uuid_ramdom(),
                          utils.file.get_file_name(file_name),
                          utils.file.get_file_name(file_name),
                          os.path.join(config.UPLOAD_PATH_VIDEOS, file_name),
                          utils.file.get_file_type(file_name)))
        file.save(os.path.join(config.UPLOAD_PATH_VIDEOS, file_name))
    except BaseException as e:
        app.app.logger.debug(e)
        return {"code": 400, "status": str(e)}

    return {"code": 200, "status": "success"}


@bp.bp_videos.route("/download", methods=["GET"])
def download():
    return flask.send_from_directory("build/videos", "black_mirror.mp4", as_attachment=True)
