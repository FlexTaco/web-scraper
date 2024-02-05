<?php
$host = "localhost";
$username = "user1";
$password = "password";
$database = "products";

// connect to database
$conn = new mysqli($host, $username, $password, $database);

// check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// query to fetch data
$query = "SELECT * FROM products";
$result = $conn->query($query);

// close  connection
$conn->close();
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Product Listing</title>
    <style>
        body{
            display: flex;
            flex-wrap: wrap;
            flex-basis: 50%;
            padding:40px;
        }

        div {
            word-wrap: break-word;
            height:300px;
            width:200px;
            display:block;
            text-align: center;
            margin-left: 20px;
            margin-right: 20px;
            border-color: red;
        }
    </style>
</head>
<body>
    <h1>The Cloth Store</h1>
<?php
//query was successful or not
if ($result) {
    while ($row = $result->fetch_assoc()) {
        // maybe later can style
        $divClass = ($row["id"] % 2 === 0) ? 'right' : 'left';
        echo '<div class="product ' . $divClass . '">';
        echo '<h3><a href="compare.php?product=' . $row["id"] . '">' . $row["title"] . '</a></h3>';
        echo '<img src="' . $row["image"] . '" width="200" height="200">';
        echo '</div>';
    }
} else {
    echo "Error";
}
?>
</body>
</html>
