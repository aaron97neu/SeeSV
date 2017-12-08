module.exports = function(app, passport){
  // Homepage with links to login page
  app.get('/', function(req, res) {
    res.render('index.ejs');
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
