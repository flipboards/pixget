# pixget

Pixget is a quick tool to get pixiv images from its id.

Usage:

    pixget pixid [save_dir] // *if dir is not specified, it is current directory.

There are other two tools now: Infoscraper and Imgscraper. Which are used
as scrapers.

**Infoscraper** downloads image information from a specific tags.

**Imgscraper** downloads images from the information file written by infoscraper.
The two functions are distinguished in the consideration that in many cases the images
are not required to be downloaded.

Usage:

    infoscraper -t [tag] (-s [step]) (-l [limit])
    imgscraper -i [input file] (-o [directory]) (-s [start page]) (-e [end page])

#### Cookies
Cookies here is my cookies, but is recommended to replaced to you own.
Cookies can be found in chrome->settings->privacy settings->contents
(Later I may add login so that no cookie-change is needed)

### libs
Lib **requests** and **bs4** are needed for reading webpage.
