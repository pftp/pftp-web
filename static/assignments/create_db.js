var sqlite3 = require('sqlite3').verbose();
var db = new sqlite3.Database('facts.db');

db.serialize(function() {
  db.run('CREATE TABLE fact_table (fact_str TEXT)');
  db.run('INSERT INTO fact_table VALUES ("The total amount of gold ever mined on Earth would fill about three Olympic-size swimming pools")');
});
