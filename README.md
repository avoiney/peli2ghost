# peli2ghost
Convert article from pelican to ghost format

This  script is a first try and need several improvements  
**/!\ Double check the output before uploaded it to your blog.**

## How to
`$ find PELICAN_BLOG_CONTENT_DIR -iname '*.rst' -exec ./peli2ghost.py {} +`

This will find all the rst files in your pelican blog content folder and output  
them in markdown in the ouptut folder of the git directory.

This is yours to zip them and use the Ghost Importer to add them to your blog.


## TODO
* [ ] handle images
* [ ] detect and use all pelican RST metadata
* [ ] use the ghost public API


## CONTRIBUTE
All contributions are greatly welcome.  
Do not hesitate to fork aand create pull request.
