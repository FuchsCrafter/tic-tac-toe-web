# tic-tac-toe-web
This project aims to bring the classic tic-tac-toe-game to the web plattform. Because the backend is written in PHP, this project can be self-hosted on almost every hosting provider.

## Trying it out

You can try the game out by clicking the link on the sidebar (TBD).

## Self-Hosting

To self-host your own instance, you need:

- A MariaDB or MySQL database with read and write acces
- A hosting provider on which you can install your instace

You'll have to download this project and then upload the backend and frontend to your hosting provider. You'll have to create a PHP file called `env.php` in the `backend/api/` folder and put your database information in it like this:

```php

<?
$server = "your.database-server.com";
$username = "Database_Username";
$password = "Database_Password";
$database = "Database_Name";
?>

```

The system will automatically create a table as soon as you start your first game.
