## This project is using: ##
  * Python(For parser to convert wiki-text to corresponding html).
  * django for server, url handling.
  * CSV files for indexing articles and there span.

## Target Audience: ##
  * All those who don't have handy internet connection.
  * All those who want to access the content of wikipedia even when they are not connected, like while traveling.
  * All those who are using proprietary encyclopedias available in market

## Issues at hand: ##

  * From my-side, apart from following http://users.softlab.ece.ntua.gr/~ttsiod/buildWikipediaOffline.html, i tried to make it work via django, it posed new problem of writing converter for wiki-markup-text to html, which as of now, is not perfect, needs improvement to utilize all the content available at hand, Here i am ready to trade off with any parser irrespective of language (python/PHP), but it should be better the this one, PHP i avoided, as for that, it will need Apache web server, which would be overkill.
  * I am using django server, it can be replaced by simple python web server which can handle css, other requests, as i am not using any of other features provided by django(like MVC).
  * To make accessibility of individual article fast, am breaking huge file to small, resulting in more then 20k odd files, any way we can skip that, hint idea help would be great.
  * Last years October dump was 4.1G and this years March 09 dump is already 4.6G, making things more difficult.
  * Adding options of going live, searching for articles, making updates readily. available.

## Future targets: ##

  * To keep it updated.
  * To make it editable.
  * To manage different categories of articles, and segregation based on that to make refined and better education/learning tool.