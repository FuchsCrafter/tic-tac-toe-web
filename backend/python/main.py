from flask import Flask, request
import json
from functools import wraps
from flask_cors import CORS
import random



app = Flask(__name__)
CORS(app)

global games
games = {}




def check_winner(board):  # returns 'X' or 'O' or None
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]
    
    for a, b, c in winning_combinations:
        if board[a] and board[a] == board[b] and board[a] == board[c]:
            return board[a]
    
    return None  # no winner


def check_game_ended(board):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]
    
    for a, b, c in winning_combinations:
        if board[a] and board[a] == board[b] and board[a] == board[c]:
            return True
    
    return False 


def gamesCleanup():
    global games
    
    raise NotImplementedError("Not implemented yet")
    
    

@app.route('/')
def index():
    return json.dumps({"success": True, "message": "Backend online"})

@app.route('/newgame', methods=['GET'])
def registerNewPlayer():
    global games
    try:
        newGameId = random.randrange(1000000, 9999999)
        playerIds = (random.randrange(1000000, 9999999), random.randrange(1000000, 9999999))
        
        while newGameId in games.keys():
            newGameId = random.randrange(1000000, 9999999)

        if len(games) > 10:
            games = {}
                        
        games[str(newGameId)] = {"gameState": [""] * 9, "playerO": playerIds[0], "playerX": playerIds[1], "playerXconnected": False}
        return json.dumps({"success": True, "message": "New player registered", "gameId": newGameId, "playerId": playerIds[0]}) 
    except:
        return json.dumps({"success": False, "message": "Something went wrong"})


@app.route('/joingame', methods=['POST'])
def joinPlayer():
    global games
    try:
        data = request.get_json()
        if not data or data["gameId"]<1000000 or data["gameId"]>9999999:
            return json.dumps({"success": False, "message": "Something went wrong with the request body"})
        
        playerGameId = str(data["gameId"])
        
        if playerGameId not in games.keys():
            return json.dumps({"success": False, "message": "Unknown Game"})
        
        playerId = games[playerGameId]["playerX"]
        games[playerGameId]["playerXconnected"] = True
        return json.dumps({"success": True, "message": "Game Joined", "gameId": playerGameId, "playerId": playerId})
    except:
        return json.dumps({"success": False, "message": "Something went wrong"})
    
    
    
@app.route('/waitconnection', methods=['POST'])
def waitForSecondPlayer():
    global games
    try:
        data = request.get_json()
        
        if not data["gameId"] or data["gameId"]<1000000 or data["gameId"]>9999999 or str(data["gameId"]) not in games.keys():
            return json.dumps({"success": False, "message": "Something went wrong: Wrong request body"})
        
        gameId = str(data["gameId"])
        playerXconnected = games[gameId]["playerXconnected"]
        
        if playerXconnected:
            return json.dumps({"success": True, "message": "Other player is connected", "otherPlayerConnected": playerXconnected})
        else:
            return json.dumps({"success": True, "message": "Other player is not connected", "otherPlayerConnected": playerXconnected})
    except:
        return json.dumps({"success": False, "message": "Something went wrong: Unknown error"})


@app.route('/makemove', methods=['POST'])
def makeMove():
    global games
    try:
        data = request.get_json()
        
        
        if not data or "gameId" not in data.keys() or "playerId" not in data.keys() or "field" not in data.keys():
            return json.dumps({"success": False, "message": "Something went wrong: Incomplete data!"})       
        
        if not data or data["gameId"]<1000000 or data["gameId"]>9999999 or str(data["gameId"]) not in games.keys():
            return json.dumps({"success": False, "message": "Something went wrong: Wrong game ID"})
        
        if not data or data["playerId"]<1000000 or data["playerId"]>9999999 or data["playerId"] not in games[str(data["gameId"])].values():
            return json.dumps({"success": False, "message": "Something went wrong: Wrong player ID"})
        
        if not data or data["field"] < 0 or data["field"] > 9:
            return json.dumps({"success": False, "message": "Something went wrong: Wrong field"})

        
        gameId = str(data["gameId"])
        playerId = data["playerId"]
        field = data["field"]
        
        playerSymbol = ''
        
        if games[gameId]["playerX"] == playerId:
            playerSymbol = 'X'
        else:
            playerSymbol = 'O'
        
        if games[gameId]["gameState"][field] == '':
            games[gameId]["gameState"][field] = playerSymbol
            return json.dumps({"success": True, "message": "Made a move", "field": field, "gameState": games[gameId]["gameState"]})
        else:
            return json.dumps({"success": False, "message": "Wrong move!"})        
        

    except:
        return json.dumps({"success": False, "message": "Something went wrong: Unknown error"})


@app.route('/gamestate', methods=['POST'])
def getGameState():
    global games
    try:
        data = request.get_json()
        
        if not data["gameId"] or data["gameId"]<1000000 or data["gameId"]>9999999 or str(data["gameId"]) not in games.keys():
            return json.dumps({"success": False, "message": "Something went wrong: Wrong request body"})
        
        gameId = str(data["gameId"])
        
        return json.dumps({"success": True, "message": "Output game state", "gameState": games[gameId]["gameState"]})
        
    except:
        return json.dumps({"success": False, "message": "Something went wrong: Unknown error"})

        


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)