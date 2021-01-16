<html><head><title>Suggestbot in bnwiki - customized by Shohag</title></head>
<body>This is an exact copy of SuggestBot but in bnwiki opearated by Shohag.<?php ?>
</body></html>
<a href="db.php">See database below. </a>

<?php
$con=mysqli_connect("tools.db.svc.eqiad.wmflabs","s54497","xVrO9dfWMwWiHPyo","s54497__SBB");
// Check connection
if (mysqli_connect_errno())
{
echo "Failed to connect to MySQL: " . mysqli_connect_error();
}

$result = mysqli_query($con,"SELECT * FROM Pages");
// Return the number of rows in result set
  $rowcount=mysqli_num_rows($result);
  printf("There's almost %d articles need help in bnwiki.\n",$rowcount);
echo "<table border='1'>
<tr>
<th>PageName</th>
<th>PageID</th>
<th>Pageviews</th>
<th>Class</th>
<th>Categories</th>
</tr>";

while($row = mysqli_fetch_array($result))
{
echo "<tr>";
echo "<td><a href = 'http://bn.wikipedia.org/wiki/".$row['PageName']."'>" . $row['PageName'] . "</a> </td>";
echo "<td>" . $row['PageID'] . "</td>";
echo "<td>" . $row['Pageviews'] . "</td>";
echo "<td>" . $row['Class'] . "</td>";
echo "<td>" . $row['Categories'] . "</td>";
}
echo "</table>";
mysqli_close($con);
?>


