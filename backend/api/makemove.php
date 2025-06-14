<?
require_once 'env.php';
require_once 'get_payload.php';
require_once 'getGames.php';

try {

$conn = new mysqli($server, $username, $password, $database);
if ($conn->connect_error) 
{
    echo json_encode([
        "success" => false,
        "message" => "Database connection failed"
    ]);
} 


try {
    # gameid, playerid, field
    $gameId = getPayload()["gameId"];
    $playerId = getPayload()["playerId"];
    $field = getPayload()["field"];
} catch (\Throwable $th) {
    echo json_encode([
        "success" => false,
        "message" => "Faulty payload"
    ]);
}

$games = getGames($conn);



if (!isset($games[$gameId]) or $gameId<1000000 or $gameId>9999999) {
    echo json_encode([
        "success" => false,
        "message" => "Incorrect game id"
    ]);
} else {
if ( ($games[$gameId]["playerO"] != $playerId and $games[$gameId]["playerX"] != $playerId ) or $playerId<1000000 or $playerId>9999999) {
    echo json_encode([
        "success" => false,
        "message" => "Incorrect player id"
    ]);
} else {
if ($field < 0 or $field > 9) {
    echo json_encode([
        "success" => false,
        "message" => "Incorrect field"
    ]);
} else {

    if ($games[$gameId]["playerX"] == $playerId) {
        $playerSymbol = "X";
    } else {
        $playerSymbol = "O";
    }

    $gameState = json_decode($games[$gameId]["gameState"]);
    $stmt = $conn->prepare("UPDATE `tictactoe` SET `gameState`=? WHERE `gameId` LIKE ?");
    $stmt->bind_param("si", $gameState, $gameId);


    if ((($playerSymbol == "X" && count(array_keys($gameState, "X")) == count(array_keys($gameState, "O")) - 1) ||
         ($playerSymbol == "O" && count(array_keys($gameState, "X")) == count(array_keys($gameState, "O")))) &&
          $gameState[$field] == ""
        ){
        $gameState[$field] = $playerSymbol;
        $gameState = json_encode($gameState);
        $stmt->execute();
        $stmt->close();

        echo json_encode([
            "success" => true,
            "message" => "Made move",
            "field" => $field,
            "gameState" => json_decode($gameState)
        ]);



    } else {
        echo json_encode([
            "success" => false,
            "message" => "Invalid move!"
        ]);
    }


}
}
}

$conn->close();

} catch (\Throwable $th) {
echo json_encode([
    "success" => false,
    "message" => "Internal Error"
]);
}



?>