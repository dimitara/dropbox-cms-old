# Dropbox-CMS
A Small CMS that downloads all data from Dropbox and generates dynamic content

Dropbox is used as a storage where content managers can upload markdown text files, images and other settings.

It can:

- generate scaffold
- sync with dropbox to download files on server

##Folder structure

```
static                     - will contain all static files that will be served by the website
  admin                    - admin client side files like css, fonts and javascript
  public                   - public client side files like css, fonts, javascript, theme
  resource                 - dynamic content resources that are synced with Dropbox
    gallery                - a folder to contain either only images or subfolders with images
      London               - a subfolder with images and texts
        image1.jpg
        image2.jpg
        ...
        thumb.jpg          - thumbnail image that will be used as website gallery thumbnail
        en                 - localisation folder for English
          image1.txt       - image1 text in English
          image2.txt
        es                 - localisation folder for Spanish
          image1.txt
          image2.txt

        New York           - a subfolder with images and texts
        image1.jpg
        image2.jpg
        ...
        thumb.jpg
        en
          image1.txt
          image2.txt
        es
          image1.txt
          image2.txt

      sections             - a folder containing content data for the different website sections
        About
          content.txt      - a markdown textbased content to show in About section
          image.png        - an image file that will be used as an image for the section
          background.png   - an image file that will be used as a background image for the section
        Articles
          1-Article        - first article in blog
            1-image.jpg    - an image that will be first shown in the article
            2-text.txt     - a markdown based content that will be shown as second item in the article
            ...
            3-image.jpg    - an image that will be shown in order
            4-image.jpg
          2-Article        - second article in blog
          ...
        Contact
          content.txt      - a markdown textbased content to show in About section
          image.png        - an image file that will be used as an image for the section

templates
  admin
    dashboard.html
    login.html
    layout.html
  public
    index.html
    layout.html

website
  settings
    analytics.txt
    en
      description.txt      - the website SEO description in english
      heading.txt          - the website SEO heading in english
      keywords.txt         - the website SEO keywords in english
      title.txt            - the website title in english
      map.json             - a json file defining the map to be used in the contacts section

    es
      description.txt
      heading.txt
      keywords.txt
      title.txt
      map.json

```

##Modules

###Admin

###CMS

###SETTINGS