#### Install gulp

~~~~
$ cd {PROJECT PATH}
$ npm init
$ npm install gulp --global
$ npm install gulp --save-dev
~~~~


#### Minify(Uglify) javascript files

~~~~
$ npm install gulp-uglify --save-dev
$ vi gulpfile.js

  var gulp = require('gulp');
  var uglify = require('gulp-uglify');

  // Minify javascript files
  gulp.task('uglify', function () {
    return gulp.src('src/*.js')
      .pipe(uglify())
      .pipe(gulp.dest('dist'));
  });

  // Enroll watch task
  gulp.task('watch', function () {
    gulp.watch('src/*.js', ['uglify']);
  });

  // Run watch task as default
  gulp.task('default', ['uglify', 'watch']);

$ gulp
~~~~


#### Convert SASS to CSS

~~~~
$ npm install gulp-sass --save-dev
$ vi gulpfile.js

  var gulp = require('gulp');
  var sass = require('gulp-sass');
  
  // Convert SASS to CSS
  gulp.task('styles', function() {
    gulp.src('sass/**/*.scss')
      .pipe(sass().on('error', sass.logError))
      .pipe(gulp.dest('./css/'));
  });
  
  // Enroll watch task
  gulp.task('watch', function () {
    gulp.watch('sass/**/*.scss', ['styles']);
  });

  // Run watch task as default
  gulp.task('default', ['styles', 'watch']);
  
$ gulp
~~~~
