from flask import Flask, Blueprint, flash, redirect, render_template, request, url_for, session
from db import pool
import pymysql

likes_bp = Blueprint('likes', __name__, url_prefix='/likes')
@likes_bp.route('/', methods=['GET', 'POST'])
def like_game():
    if 'username' not in session:
        return redirect(url_for('login.login'))

    userid = session['userid']
    connection = pool.raw_connection()
    cursor = connection.cursor()
    
    if request.method == "GET":
        cursor.execute("SELECT gid, title, link, introduction from Likes natural join Games where uid = %s", (userid,))
        like_lists = list(cursor.fetchall())
        return render_template('games.html', games_list=like_lists)
    
    gid = request.form['gid']
    cursor.execute("SELECT gid from Likes where uid = %s", (userid,))
    gids = list(cursor.fetchall())

    # if gid == ():
    #     flash('Game does not exist')
    #     return redirect(url_for('games.game', methods=["GET"]))
    # elif gid in gids:
    #     flash('Game already liked')
    #     return redirect(url_for('games.game', methods=["GET"]))
    # else:
    try:
        cursor.execute("INSERT INTO Likes (uid, gid) VALUES (%s, %s)", (userid, gid))
        connection.commit()
        flash('Successfully added game')
    except pymysql.err.IntegrityError as e:
        flash('Game already liked')
    return redirect(url_for('games.game'))

@likes_bp.route('/remove', methods=["POST"])
def remove_game():
    if 'username' not in session:
        return redirect(url_for('login.login'))
    userid = session['userid']
    connection = pool.raw_connection()
    cursor = connection.cursor()

    gid = request.form['gid']
    cursor.execute("DELETE from Likes WHERE uid=%s and gid=%s", (userid, gid))
    connection.commit()
    flash(f'Successfully removed game')
    return redirect(url_for('games.game'))


