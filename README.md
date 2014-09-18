RUSC
====
[...] description goes here [...]

#### Dependencies
Package  | Version | Installation
------------- | ------------- | -------------
Python  | 2.7.3 |
Django  | 1.5 final | pip install django==1.5
social_auth | 0.7.23 | pip install django-social-auth==0.7.23
django_mailbox | ? | pip install django-mailbox
django_filters | 0.7 | pip install django-filter==0.7
embed_video | 1.0.0 dev | pip install django-embed-video
postman | 3.1.0 | pip install django-postman==3.1.0
autocomplete_light | ? | pip install django-autocomplete-light
micawber | ? | pip install micawber
tagging | 0.3.1 | pip install django-tagging==0.3.1
notification | 0.1.5 final | pip install django-notification==0.1.5
registration | 1.0.0 final | pip install django-registration==1.0.0
django_countries | ? | pip install django-countries
pygraphviz | ? | pip install pygraphviz (*1)
nltk | 3.0.0b2 | pip install nltk==3.0.0b2
django-tastypie | 0.12.0 | pip install django-tastypie==0.12.0

For installing dependencies recursively it is as simple as generating a *requirements.txt* file with all the modules listed and execute:

`pip install -r requirements.txt`

(*1a) Follow these steps to install pygraphviz on OS X:
> `brew install graphviz`

> *pygraphviz depends on graphviz and its a wrapper for python*

> `brew install pkg-config`

> *fixes the "Error locating graphviz" exception when installing*

> `pip install pygraphviz`

> If doesn't work after these steps try to do the following:

> `export PKG_CONFIG_PATH=/usr/local/Cellar/graphviz/2.38.0/lib/pkgconfig`

(*1b) Follow these steps to install pygraphviz on Windows8.1:
> Download Graphviz .msi installer from the [project page](http://www.graphviz.org/Download_windows.php) (tested with 2.38)

> Download PyGraphviz sources from [repository](https://pypi.python.org/pypi/pygraphviz) (tested with 1.2)

> Configure `setup.py` from the sources to match:
```python
library_path="C:\Program Files (x86)\Graphviz2.38\lib\debug\lib"
include_path="C:\Program Files (x86)\Graphviz2.38\include\graphviz"
```
> Download and install `mingw-get-inst-20100831.exe` from [SourceForge](http://sourceforge.net/projects/mingw/files/OldFiles/mingw-get-inst/mingw-get-inst-20100831/)

> Add MinGW to the system path `C:\Users\AMARIS\Documents\MinGW\bin`

> Change line 285 from *C:\Users\AMARIS\Documents\Python27\Lib\distutils\unixcompiler.py*:

> `compiler = os.path.basename(sysconfig.get_config_var("CC"))`

> to

> `compiler = "gcc"`

> Change back the line 285 after building pygraphviz

> Copy the content of *build/lib.win32-2.7* directory to virtualenv *site-packages* folder

> Test with `manage.py graph_models -a -g -o my_project_visualized.png`

#### Gitignore
Please add the following files and extensions to the list to be ignored by Git when pushing changes.
Need to create a .gitignore file in the root of your repo:
```
*.pyc
*.pyo
.idea/
.DS_Store
Thumbs.db
```

## Installation
#### OSX 10.9 Devel Environment
* Make *~/Library* directory visible
 > Go to Home folder pressing `shift+cmd+H`

 > Press `cmd+J` and check **Show Library Folder**

* Bash profile setup
 > `vim ~/.bash_profile` and add:

 > ```bash
# Set architecture flags
export ARCHFLAGS="-arch x86_64"
# Ensure user-installed binaries take precedence
export PATH=/usr/local/bin:$PATH
# Load .bashrc if it exists
test -f ~/.bashrc && source ~/.bashrc
 > ```

 > `. ~/.bash_profile`

* Setup the compiler installing latest **XCode Command Line Interface**
 > Open XCode | Menu XCode | Open Developer Tools | More Developer Tools | Download CLI
 > *Checked for XCode 5.1.1 and OSX 10.9*

#### Homebrew
* Install Homebrew
 > `ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"`

 > `brew doctor`

 > `brew update`

* Install **wget**
 > `brew install bash-completion ssh-copy-id wget`

* Activate bash completion
 > `vim ~/.bash_profile` and add:

 > ```bash
 if [ -f $(brew --prefix)/etc/bash_completion ]; then
     . $(brew --prefix)/etc/bash_completion
 fi
 > ```

[Help reference](http://hackercodex.com/guide/mac-osx-mavericks-10.9-configuration/)

#### Python and Django
> Will be using Homebrew Python instead of OS X due to system updates.

> *pip* and *easy_install* are installed by default with Homebrew Python.

> *pip* is restricted to only work with an existing virtualenv

> *pip* directories

> * /usr/local/lib/python2.7/site-packages
> * /usr/local/bin

```bash
brew install python
pip install virtualenv
mkdir ~/Virtualenvs
vim ~/.bashrc
```
and add:

```bash
# pip should only run if there is a virtualenv currently activated
export PIP_REQUIRE_VIRTUALENV=true
# cache pip-installed packages to avoid re-downloading
export PIP_DOWNLOAD_CACHE=$HOME/.pip/cache
```
then:

```
. ~/.bash_profile
cd ~/Virtualenvs
virtualenv foobar
cd foobar
. bin/activate
pip install django==1.7
cd bin
django-admin.py startproject mysite
cd ../mysite
python manage.py runserver
```
Be sure to use the Homebrew version instead of OS X version running:

`which python`

and any result without */usr/bin/...* is OK.

[Help reference Python](http://hackercodex.com/guide/python-development-environment-on-mac-osx/)

[Help reference Django](http://www.computersnyou.com/2960/2014/02/setup-django-virtualenv-macosx-mavericks/)

#### Configuring Git for Github
* Set up credentials
 > ```bash
 git config --global user.name "user_name"
 git config --global user.email "user_email@example.com"
 > ```

* Generate SSH Key
 > `ls -al ~/.ssh`

 > *if exitst id_rsa.pub go to 4th row of the following code*

 > ```bash
 ssh-keygen -t rsa -C "your_email@example.com"
 eval "$(ssh-agent -s)"
 ssh-add ~/.ssh/id_rsa
 pbcopy < ~/.ssh/id_rsa.pub
 > ```

* Go to *Github account > Configuration > SSH Keys > Add*

* Test
 > `ssh -T git@github.com`

[Help reference Git setup](https://help.github.com/articles/set-up-git)

[Help reference SSH Keys](https://help.github.com/articles/generating-ssh-keys)
