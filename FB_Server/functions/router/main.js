
var express = require('express');
var router = express.Router();


router.get('/imagematching', function(req, res, next) {
  res.render('imageList',{ title: 'imageList' });
});

router.get('/daumadrapi', function(req, res, next) {
  res.render('daum',{ title: 'daumaddress' });
});


module.exports = router;

/*
module.exports = function(app)
{
     app.get('/imagematching',function(req,res){
        res.render('functions/views/imagematching.html')
     });
     
}
*/
/*
var express1 = require('express');
var router1 = express1.Router();


router1.post('/imagematching', function(req, res){
    res.render('functions/views/imagematching.html');

});

module.exports = router1;
*/