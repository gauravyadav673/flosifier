var express = require('express');
var router = express.Router();
var multer = require('multer');
var upload = multer({dest:'./uploads'});
 var fs = require('fs');

/* GET users listing. */
router.post('/classify', upload.single('flowerimage'), function(req, res, next) {
	if(req.file){
        var image = 'uploads/'+req.file.filename;
    }else{
        res.send(JSON.parse('{"error": "empty file"}'));
    }
    var spawn = require('child_process').spawn,
    py = spawn('python', ['labelImage.py', image]),
    dataString = '';
	py.stdout.on('data', function(data){
	  dataString += data.toString();
	});
	py.stdout.on('end', function(){
	  fs.unlinkSync('uploads/'+req.file.filename);
	  res.send(JSON.parse(dataString));
	});
	py.stdin.end();
});
module.exports = router;
