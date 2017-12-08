module.exports = function(app, passport){
  // Homepage with links to login page
  app.get('/', function(req, res) {
    res.render('index.ejs');
  });

  //Serves CSV files
  app.get('/csvs/:name', function(req, res) {
    var options = {
      root: __dirname + '/../csvs/',
      dotfiles: 'deny',
      headers: {
          'x-timestamp': Date.now(),
          'x-sent': true
      }
    };
    var fileName = req.params.name;
      res.sendFile(fileName, options, function (err) {
	    if (err) {
          //console.log(err);
        } else {
          console.log('Sent:', fileName);
        }
     });
  });

  //Serves SVG files
  app.get('/svgs/:name', function(req, res) {
    var options = {
      root: __dirname + '/../svgs/',
      dotfiles: 'deny',
      headers: {
          'x-timestamp': Date.now(),
          'x-sent': true
      }
    };
    var fileName = req.params.name;
      res.sendFile(fileName, options, function (err) {
	    if (err) {
          //console.log(err);
        } else {
          console.log('Sent:', fileName);
        }
     });
  });

  //file upload
  app.post('/fileupload', function(req, res) {
    var path = require("path");
    if (!req.files)
      return res.status(400).send('No files were uploaded.');
    let csvupload = req.files.csvupload;

    csvupload.mv(path.join(__dirname, '../csvs',req.files.csvupload.name), function(err) {
      if (err)
        return res.status(500).send(err);
       
      //res.send('File uploaded!');
      //req.flash('info','File uploaded successfully');
      res.redirect('/profile')
    });
  });

  // Login form
  app.get('/login', function(req, res) {
    res.render('login.ejs', {message: req.flash('loginMessage') });
  });

  // process login
  app.post('/login', passport.authenticate('local-login', {
    successRedirect : '/profile', //redirect to secure area
    failureRedirect : '/login', //redirect back to signup page
    failureFlash : true //allow flash
  }));

  // Signup
  app.get('/signup', function(req, res) {
    res.render('signup.ejs', { message: req.flash('signupMessage') });
  });

  //Process signup
  app.post('/signup', passport.authenticate('local-signup', {
    successRedirect : '/profile', //redirect to secure area
    failureRedirect : '/signup', // Send back to signup upon error
    failureFlash : true //alowing flash messaging
  }));

  //profile section. Use middleware to verify user is logged in
  app.get('/profile', isLoggedIn, function(req, res){
    res.render('profile.ejs', {
      user : req.user //get user from template
    });
  });

/*
  //This displays the CSVs and SVGs
  app.get('/profile?:csv_name', isLoggedIn, function(req, res){
    var options = {
      root: __dirname + '/../svgs/',
      dotfiles: 'deny',
      headers: {
          'x-timestamp': Date.now(),
          'x-sent': true
      }
    };
    var fileName = req.params.name;
      res.sendFile(fileName, options, function (err) {
	    if (err) {
          console.log(err);
        } else {
          console.log('Sent:', fileName);
        }
     });

	res.render('profile.ejs', {
      user : req.user //get user from template
    });
  });
 */
  
  //logout
  app.get('/logout', function(req, res) {
    req.logout();
    res.redirect('/');
  });
};

//middleware to made sure user is logged in
function isLoggedIn(req, res, next) {

  // if user is authenticated in the session, carry on
  if(req.isAuthenticated())
    return next();

  // if they are not, redirect to home page
  res.redirect('/');
}
