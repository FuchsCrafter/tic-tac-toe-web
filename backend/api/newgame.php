<?
require_once 'env.php';



try {


$conn = new mysqli($server, $username, $password, $database);
if ($conn->connect_error) 
{
    echo json_encode([
        "success" => false,
        "message" => "Database connection failed"
    ]);
}else {

$sql = "
CREATE TABLE IF NOT EXISTS tictactoe (
    gameId INT(11) NOT NULL PRIMARY KEY,
    gameState TEXT CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
    playerO INT(11) NOT NULL,
    playerX INT(11) NOT NULL,
    playerXConnected TINYINT(1) NOT NULL DEFAULT 0,
    lastUpdate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
";

$result = $conn->query($sql);

if ($result == false) {
    echo json_encode([
        "success" => false,
        "message" => "Database error"
    ]);
    die("Database error!");
}

// $result->free();

$sql = "SELECT * FROM `tictactoe`";
$result = $conn->query($sql);

$data = [];

if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $gameId = $row['gameId'];
        $data[$gameId] = $row;
    }
}

// $result->free();

$stmt = $conn->prepare("INSERT INTO `tictactoe`(`gameId`, `gameState`, `playerO`, `playerX`, `playerXconnected`) VALUES (?, ?, ?, ?, ?)");
$stmt->bind_param("isiii", $gameId, $gameState, $playerO, $playerX, $playerXconnected);

$gameId = rand(1000000, 9999999);
$gameState = json_encode(["", "", "", "", "", "", "", "", ""]);
$playerO = rand(1000000, 9999999);
$playerX = rand(1000000, 9999999);
$playerXconnected = 0;

if (isset($data[$gameId])) {
    while (isset($data[$gameId])) {
        $gameId = rand(1000000, 9999999);
    }
}

// TODO: check if playerIds already exist in db

if ($stmt->execute()) {
    echo json_encode([
        "success" => true, 
        "message" => "New game registered", 
        "gameId" => $gameId, 
        "playerId" => $playerO
    ]);
} else {
    echo json_encode([
        "success" => false,
        "message" => "Error whilst creating new game (insertion error)"
    ]);
}

$stmt->close();
$conn->close();
}
} catch (\Throwable $th) {
    //throw $th;
echo json_encode([
    "success" => false,
    "message" => "Internal Error"
]);
}

?>