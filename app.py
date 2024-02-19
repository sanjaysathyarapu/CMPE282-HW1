from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def initialize_board():
    return [['' for _ in range(3)] for _ in range(3)]

def check_winner(board, player):
    # Check rows
    for row in board:
        if all([cell == player for cell in row]):
            return True
    # Check columns
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    # Check diagonals
    if all([board[i][i] == player for i in range(3)]) or all([board[i][2-i] == player for i in range(3)]):
        return True
    return False

@app.route('/move/<int:row>/<int:col>')
def move(row, col):
    if session['board'][row][col] == '' and 'winner' not in session:
        current_player = session['turn']
        session['board'][row][col] = current_player
        if check_winner(session['board'], current_player):
            session['winner'] = current_player
        session['turn'] = 'O' if current_player == 'X' else 'X'
    return redirect(url_for('index'))

@app.route('/')
def index():
    board = session.get('board', initialize_board())
    turn = session.get('turn', 'X')
    winner = session.get('winner', None)
    return render_template('index.html', board=board, turn=turn, winner=winner)


if __name__ == '__main__':
    app.run(debug=True)
