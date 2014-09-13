RUSC
====
[...] description goes here [...]

#### Dependencies:
Package  | Version
------------- | -------------
Python  | 2.7.3
Django  | *unknown*

#### Changelog
Empty

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
 eval "$(ssh-agent -s)
 ssh-add ~/.ssh/id_rsa
 pbcopy < ~/.ssh/id_rsa.pub
 > ```

* Go to *Github account > Configuration > SSH Keys > Add*

* Test
 > `ssh -T git@github.com`

[Help reference Git setup](https://help.github.com/articles/set-up-git)

[Help reference SSH Keys](https://help.github.com/articles/generating-ssh-keys)
