<?php
$host = "localhost";
$username = "user1";
$password = "password";
$database = "products";

$conn = new mysqli($host, $username, $password, $database);

//connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// check form 
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // get info
    $creditCard = $_POST['creditCard'];
    $address = $_POST['address'];
    $pinNumber = $_POST['pinNumber'];

    // insert info
    $insertQuery = "INSERT INTO credit_cards (creditCard, address, pinNumber) VALUES (?, ?, ?)";
    $stmt = $conn->prepare($insertQuery);
    $stmt->bind_param("sss", $creditCard, $address, $pinNumber);

    if ($stmt->execute()) {
        echo "Payment successful!";
    } else {
        echo "Error: " . $stmt->error;
    }

    $stmt->close();
}

$conn->close();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Checkout</title>
</head>
<body>
    <h1>Checkout</h1>
    <form method="post" action="">
        <label for="creditCard">Credit Card:</label>
        <input type="text" name="creditCard" required><br>

        <label for="address">Address:</label>
        <input type="text" name="address" required><br>

        <label for="pinNumber">PIN Number:</label>
        <input type="password" name="pinNumber" required><br>

        <input type="submit" value="Submit">
    </form>
</body>
</html>
