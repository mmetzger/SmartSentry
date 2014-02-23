#!/usr/bin/env node

var readline = require('readline');

var M2X = require("m2x");
var apikey = "";
var apikey2 = "";
var feedid = "";


var recentupdates = new Object();

var rl = readline.createInterface({
	input: process.stdin,
	output: process.stdout,
	terminal: false
});

// Need to input tags, api keys, etc.
var tags = ["", ""];
rl.on('line', function(l) {
  tags.forEach( function(tag) {
    if (l.indexOf(tag) > -1)
    {
       if (recentupdates.hasOwnProperty(tag))
       {
           // Tag has been updated in past 15 seconds, do not send further
	   //
	} else {
 	   // Tag not listed, add and send update to M2x
	   //
	   var d = new Date();
           console.log("Saw tag " + tag + " at " + d + "\n");
	   recentupdates[tag] = 1;
   	   setTimeout(function() { delete recentupdates[tag]; var nd = new Date(); console.log("Removing tag " + tag + " from list at " + nd); } , 15000 );

	   var m2x = new M2X(apikey);
	   m2x.feeds.updateStream(feedid, tag.replace(/:/g, ''), { value: 1 }, function(data, error, res) { });
	   console.log("Finished update");
        }	   
    }
  });
});
