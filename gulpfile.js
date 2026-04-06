const gulp = require('gulp');
const fileinclude = require('gulp-file-include');

gulp.task('html', function() {
  return gulp.src('src/*.html')
    .pipe(fileinclude({
      prefix: '@@',
      basepath: '@file'
    }))
    .pipe(gulp.dest('dist'));
});

gulp.task('copy-assets', function() {
  return gulp.src(['css/**', 'js/**', 'images/**', '*.ico', '*.xml', '*.txt'], { base: '.' })
    .pipe(gulp.dest('dist'));
});

gulp.task('build', gulp.series('html', 'copy-assets'));

gulp.task('watch', function() {
  gulp.watch('src/*.html', gulp.series('html'));
  gulp.watch(['css/**', 'js/**', 'images/**'], gulp.series('copy-assets'));
});

gulp.task('default', gulp.series('build', 'watch'));