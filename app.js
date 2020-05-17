const express = require('express')
const mysqlx = require('@mysql/xdevapi');
var session;

const app = express()
app.get('', (req, res) => {
    res.send('<h1>Resource Manager</h1>')
})

app.get('/show_database', (req, res) => {
  let result = '';
  mysqlx
  .getSession({
    user: 'root',
    password: 'pw',
    host: 'localhost'
  })
  .then(function (s) {
    session = s;
    return session.getSchema('resource_manager');
  })
  .then(function () {
    return session.sql('USE resource_manager').execute();
  })
  .then(() => {
    return session.sql('SHOW TABLES').execute(function (row) {
      // Print result
      console.log(row);
      result += row + ','
      return row;
    });
  })
  .then(() => {
    console.log(result)
    res.send(result)
  })
  .catch(function (err) {
    // Handle error
    console.log(err)
  });

})
app.listen(3000, () => {
    console.log('Server is up on port 3000.')
})