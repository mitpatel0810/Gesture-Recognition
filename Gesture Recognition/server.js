const express = require('express');
const body_parser = require('body-parser');
const spawn = require("child_process").spawn;
const fs = require('fs');


var app = express();
app.use(body_parser.json({limit: "50mb"}));
app.use(body_parser.urlencoded({limit: "50mb", extended: true, parameterLimit:50000}));

var PORT = 3000;

app.get('/', function(req, res) {
    res.status(200).send('Hello from Group 13');
});

app.post('/GetPoseLabel', function(req, res) {
    //console.log("REQ Obj", req.body);
    
    fs.writeFile("./key_points.json", JSON.stringify(req.body), function(err) {

        if(err) {
            return console.log(err);
        }
    
        console.log("The file was saved!");
    }); 


    const pythonProcess = spawn('python3',["./server.py"]);
    // console.log("called python file");
    pythonProcess.stdout.on('data', (data) => {
        // data = data.toString();
        // console.log("In Node", data);

        if(data[0]!='{')
            res.status(200).send(data);
        else
            res.status(200).send(JSON.parse(data));
    });
    
});



app.listen(PORT, function() {
    console.log('Server is running on PORT:',PORT);
});