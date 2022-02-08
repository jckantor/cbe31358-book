# Development Notes

This project is maintained using [JupyterBook](https://jupyterbook.org/intro.html).

## Media

Original versions of video files are maintained in the sub-directory `media` of the main project directory. For deployment, manually save a copy of the video file in `_build/html/_static/media` where it can be linked via the path `../_static/media/`. The reason for deploying a copy is to avoid any potential to overwrite or corrupt a media file in the process of rebuilding the static web pages.

## Building

After completing routine edits to notebooks, data, or configuration files, open a terminal window and navigate to the directory of the local git repository. 

```
jupyterbuild clean ../cbe31358-book
```

Rebuild the book by executing the following command from the terminal window while 

```
jupyterbuild build ../cbe31358-book
```

Commit and push changes to the remote git repository.

```
git add --all
git commit -m "commit message"
git push
```

Move relevant html files to github pages.

```
ghp-import -n -p -f _build/html
```
