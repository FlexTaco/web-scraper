<?php
$host = "localhost";
$username = "user1";
$password = "password";
$database = "products";

define('CheckOut', 'checkout!');
//connect to database
$conn = new mysqli($host, $username, $password, $database);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$productID = isset($_GET['product']) ? $_GET['product'] : null;

if ($productID !== null) {
    // query 
    $complementaryID = ($productID % 2 === 0) ? $productID - 1 : $productID + 1;

    $query = "SELECT * FROM products WHERE id IN ($productID, $complementaryID)";
    $result = $conn->query($query);
    if ($result) {
        echo '<div style="display: flex; justify-content: space-around; padding: 20px;">';
        //high price
        $lowestPrice = PHP_INT_MAX;
        $lowestPriceProductID = null;

        // fetch
        while ($row = $result->fetch_assoc()) {
            if ($row["price"] < $lowestPrice) {
                $lowestPrice = $row["price"];
                $lowestPriceProductID = $row["id"];
            }
        }

        // fetch lowest price product
        // reset
        $result->data_seek(0); 
        while ($row = $result->fetch_assoc()) {
            echo '<div style="text-align: center;';

            // lowest price
            // no border
            if ($row["id"] === $lowestPriceProductID) {
                echo 'border: 2px solid red;'; 
            } elseif ($row["id"] === $highestPriceProductID) {
                
            }

            echo '">';
            echo '<h3>' . $row["title"] . '</h3>';
            echo '<img src="' . $row["image"] . '" width="200" height="200"><br>';
            echo '<p>Description: ' . $row["description"] . '</p>';
            echo '<p>Price: $' . $row["price"] . '</p>';
            echo '<p>Review: ' . $row["review"] . ' out of 5</p>';
            echo '</div>';
        }

        echo '</div>';
        echo '<a href="checkout.php">'.CheckOut.'</a>';
    } else {
        echo "Error";
    }
} else {
    echo "Product ID not ava";
}

// close connection
$conn->close();
?>
