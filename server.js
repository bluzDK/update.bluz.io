var express, particle, http, fs, bodyParser, uuid, url, path, download, request, util;

express = require('express');
cors = require('cors');
app = express();
app.use(cors());

bodyParser = require('body-parser')

var Particle = require('particle-api-js');

http = require('http');
fs = require('fs');
uuid = require('node-uuid');
url = require("url");
path = require("path");
download = require('download');
request = require('request');
util = require('util');

app.listen(8081);
console.log("Starting!");

var startUpdate = function(downloadID, device, accessToken, files) {
    console.log("Files Downloaded, Starting Update");

    var fileList = {};
    for (var i = 0; i < files.length; i++) {
        fileList["file" + (i + 1) || ''] = files[i];
    }
    console.log(fileList);

    particle.flashDevice({ deviceId: device, files: fileList, auth: accessToken }).then(function(data) {
        console.log('Device flashing started successfully:', data);
        for (var i = 0; i < files.length; i++) {
            fs.unlinkSync(files[i]);
        }
        fs.writeFileSync('./' + downloadID + '/response.json', util.inspect(data.body, {showHidden: false, depth: null}));
    }, function(err) {
        console.log('An error occurred while flashing the device:', err);
        for (var i = 0; i < files.length; i++) {
            fs.unlinkSync(files[i]);
        }
        fs.writeFileSync('./' + downloadID + '/error.json', util.inspect(err.body, {showHidden: false, depth: null}));
    });
}

app.post('/update/', bodyParser.json(), function (req, res) {

    //if the request comes from staging.particle.io, then we should send the update there
    var origin = req.get('origin');
    if (origin.endsWith('staging.particle.io')) {
        defaults = { baseUrl: 'https://api.staging.particle.io', clientSecret: 'particle-api', clientId: 'particle-api', tokenDuration: 7776000 };
        particle = new Particle(defaults);
    } else {
        particle = new Particle();
    }
    console.log("Particle URL is " + particle.baseUrl);

    var device = req.body.device;
    var accessToken = req.body.accessToken;
    var files = req.body.files;
    var localFiles = [];

    var downloadID = uuid.v4();
    fs.mkdirSync("./" + downloadID);

    console.log("New Request, Starting Downloads");
    //download the files locally
    for (var i = 0; i < files.length; i++) {
        //get base file name
        var parsed = url.parse(files[i]);
        var fileName = path.basename(parsed.pathname);

        //download file
        new download({mode: '755'})
            .get(files[i])
            .dest("./" + downloadID + "/")
            .run( function(err, file){
                if (err) {
                    console.log("File did not exist!");
                    fs.writeFileSync('./' + downloadID + '/error.json', '{"status": 0, "error": "files did not exist"}');
                } else {
                    localFiles.push(file[0].path);
                    if (localFiles.length == files.length) {
                        startUpdate(downloadID, device, accessToken, localFiles);
                    }
                }
            });
    }

    res.send(JSON.stringify({
	    uuid: downloadID
    }));

});

app.get('/update/status/:downloadID', bodyParser.json(), function (req, res) {

    // Check if this one exists
    var dir = null;
    try {
        dir = fs.lstatSync('./' + req.params.downloadID);
    } catch (e) {
        res.send('{"status": 0, "error": "update does not exist"}');
        return;
    }

    // Check if it succeeded
    var response = null;
    try {
        response = fs.lstatSync('./' + req.params.downloadID + '/response.json');
    } catch (e) {

    }
    if (response && response.isFile()) {
        res.send(fs.readFileSync('./' + req.params.downloadID + '/response.json'));
        return;
    }

    // Check if it errored
    var error = null;
    try {
        error = fs.lstatSync('./' + req.params.downloadID + '/error.json');
    } catch (e) {

    }
    if (error && error.isFile()) {
        res.send(fs.readFileSync('./' + req.params.downloadID + '/error.json'));
        return;
    }

    res.send(JSON.stringify({
	    status: 1,
        message: 'update in progress'
    }));
});

//test page
app.get('/test/', function (req, res) {
    var uid = req.params.uid,
        path = req.params[0] ? req.params[0] : 'test.html';
    res.sendfile(path, {root: '.'});
});
