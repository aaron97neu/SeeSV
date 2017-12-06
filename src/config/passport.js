//requires:
var LocalStrategy = require('passport-local').Strategy;
var User = require('../app/models/user');

module.exports = function(passport) {
  
  //passport setup - for persistant login sessions

  //serialize(?) the user
  passport.serializeUser(function(user, done) {
    done(null, user.id);
  });

  //deserialize(?) the user
  passport.deserializeUser(function(id, done) {
    User.findById(id, function(err, user) {
      done(err, user);
    });
  });

  //local signup:
  
  passport.use('local-signup', new LocalStrategy({
    //overriding default username with email
    usernameField : 'email',
    passwordField : 'password',
    passReqToCallback : true // passes entire request to callback
  },
  function(req, email, password, done) {
    
    //async
    process.nextTick(function() {

      //check to see if user already exists
      User.findOne({ 'local.email' : email},  function(err, user) {
        //check for errors
        if(err)
          return done(err);

        if(user) {
          return done(null, false, req.flash('signupMessage', 'That email is already taken.'));
        } else {
          //create new user
          var newUser = new User();
          //set user creds
          
          newUser.local.email = email;
          newUser.local.password = newUser.generateHash(password);

          //save user
          newUser.save(function(err) {
            if(err)
              throw err;
            return done(null, newUser);
          });
        }
      });
    });
  }));
};
