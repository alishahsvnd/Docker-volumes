const express = require('express');
const mongoose = require('mongoose');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const cors = require('cors');

// Create an Express application
const app = express();
app.use(cors());

// Connect to the MongoDB server
mongoose.connect('mongodb://mongodb:27017/mydb', {
  useNewUrlParser: true,
  useUnifiedTopology: true
}).then(() => {
  console.log('MongoDB connected');
}).catch((err) => {
  console.error(err);
});

// Define the Person schema
const personSchema = new mongoose.Schema({
  name: String,
  family: String
});
const Person = mongoose.model('Person', personSchema);


// Create a 1KB file with random text data in "/serverdata"
const filePath = path.join(__dirname, 'serverdata', 'file.txt');
const fileData = crypto.randomBytes(1024).toString('hex');

// create a folder for the file if it doesn't exist yet then write the file
if (!fs.existsSync(path.dirname(filePath))) {
  fs.mkdirSync(path.dirname(filePath));
}
fs.writeFileSync(filePath, fileData);


// Define a route for getting the file and its checksum
app.get('/file', (req, res) => {

  const file = fs.readFileSync(filePath);
  const checksum = crypto.createHash('sha256').update(file).digest('hex');
  res.set('Content-Type', 'text/plain');
  res.set('Content-Length', file.length);
  res.set('X-Checksum', checksum);
  res.send(file);

});

// Define a route for inserting a new person
app.post('/persons', express.json(), (req, res) => {
  const { name, family } = req.body;
  const person = new Person({ name, family });
  person.save().then(() => {
    res.status(201).send(person);
  }).catch((err) => {
    console.error(err);
    res.status(500).send(err);
  });
});

// Define a route for getting a list of persons
app.get('/persons', (req, res) => {
  Person.find().then((persons) => {
    res.send(persons);
  }).catch((err) => {
    console.error(err);
    res.status(500).send(err);
  });
});

// Define a route for getting a person by ID
app.get('/persons/:id', (req, res) => {
  const { id } = req.params;
  Person.findById(id).then((person) => {
    if (!person) {
      res.status(404).send();
    } else {
      res.send(person);
    }
  }).catch((err) => {
    console.error(err);
    res.status(500).send(err);
  });
});

// Define a route for removing a person by ID
app.delete('/persons/:id', (req, res) => {
  const { id } = req.params;
  Person.findByIdAndDelete(id).then((person) => {
    if (!person) {
      res.status(404).send();
    } else {
      res.send(person);
    }
  }).catch((err) => {
    console.error(err);
    res.status(500).send(err);
  });
});

// Start the server on port 3000
app.listen(3000, () => {
  console.log('Server started on port 3000');
});
