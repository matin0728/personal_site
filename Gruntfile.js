var crypto = require('crypto')
var exec   = require('child_process').exec
var path   = require('path')

module.exports = function(grunt) {

  var port = 8981;
  
  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    jade: {
      compile: {
        options: {
          data: {
            debug: false
          }
        },
        files: [
          {
            expand: true,     // Enable dynamic expansion.
            cwd: 'templates/src/',      // Src matches are relative to this path.
            src: ['*.jade', '!block_*.jade'], // Actual pattern(s) to match.
            dest: 'templates/',   // Destination path prefix.
            ext: '.html',   // Dest filepaths will have this extension.
          }

        ]
      }
    },
    less: {
      development: {
        options: {
          paths: ['static/css/less/']
          // paths: ["static/css/less/", "doc/css/bootstrap/"]
        },
        files: {
          // TODO
          // "doc/css/bootstrap.auto.css": "doc/css/bootstrap/bootstrap.less",
          // "doc/css/main.auto.css": "doc/css/less/main.less"
        }
      }
    },
    // For watch service usage.
    connect: {
      dev_server:{
        options: {
          port: 8888,
          base: './',
          keepalive: true 
        } 
      }
    },
    watch: {
      options: {
        // Start a live reload server on the default port 35729
        livereload: true,
      },
      all: {
        files: [
          'templates/src/*.jade'
        ],
        tasks: ["less", "jade"],

      }
    },
    jshint: {
      files: {
        src: [
          // don't tranverse, TODO: move zh-pagelet out to component folder.
          'static/js/*.js', '!static/js/sea-debug.js', '!static/js/sea.js',
        ],
        options: {
          jshintrc: 'static/js/.jshintrc'
        }
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-jade');
  grunt.loadNpmTasks('grunt-contrib-connect');
  // grunt.loadNpmTasks('grunt-contrib-cssmin');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-watch');

  function execCommand(cmd, cb) {
    var child = exec(cmd, cb)
    child.stdout.pipe(process.stdout)
    child.stderr.pipe(process.stderr)
  }

  grunt.event.on('watch', function(action, filepath, target) {
    grunt.log.writeln(target + ': ' + filepath + ' has ' + action);
  });

  // Default task(s).
  grunt.registerTask('default', ['jshint', 'less', 'jade']);
  
};