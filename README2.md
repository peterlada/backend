Build status: 
[ ![Codeship Status for easypairings/ep](https://www.codeship.io/projects/492986b0-c389-0131-2fd9-7292fb5ca437/status?branch=master)](https://www.codeship.io/projects/21832)

# EASY PAIRINGS

## SETUP FOR DEVELOPMENT

The production site consists of **assets** and **static site** hosted on _Dreamhost_ and a **Flask application** running on a uwsgi server on _heroku_. We use https to secure sensitive communications on both sites.


### 1. Setup Python

OSX comes with Python 2.7, which is perfect. If you have installed python with homebrew please uninstall it, it's known to break things. You can verify the python location and version:

    $ type python # should say /usr/bin/python
    $ python -V # should say 2.7.5 on OSX Maverick

For Windows, [**download Python**](https://www.python.org/download/windows/), then update your PATH environment variable in System Properties > Advanced > Environment Variables to include 'C:\Python27; C:\Python27\Scripts'

We will need `pip` and `virtualenv` so:

    $ sudo easy_install -U pip
    $ sudo pip install virtualenv

For Windows, [**download PIP**](http://www.pip-installer.org/en/latest/installing.html) and [**Git**](http://git-scm.com/download/win) - choose to 'Run Git and included Unix tools from the Windows Command Prompt'


### 2. Setup Postgres

Install postgres (9.3.4 or later). We like Postgres.app, instruction for that below. Alternatively you can install from official distro.

#### 2.1 Setup Postgres.app

Download and install [postgres.app](http://postgresapp.com/).

Add a line to `~/.bash_profile` for access to postgress command line tools (the path will vary depnding on the version of *Postgres.app*, just because) `export PATH=/Applications/Postgres.app/Contents/Versions/9.3/bin:$PATH`

#### 2.2 Setup Blank DB

Setup a user named `ep` on the command line:

    $ createuser -s -w ep  # superuser, no-password
    $ createdb -E UTF8 -O ep easypairings  # utf-8 encoded, owned by ep
 
Now, from the Postgres terminal window's command line, which should have a `#` as the prompt:

    $ psql
    psql (9.3.4)
    Type "help" for help.
    
    =# 

To verify proper database setup:

    =# \c easypairings ep
    =# \dt

Enable the postgres extension that we use (trigram):
    
    $ psql -c "create extension pg_trgm" -d easypairings

This should report no relations found. If it was incorrectly set up earlier, drop it and repeat it from above:

    =# drop database easypairings;
    =# drop role ep;


### 3. Setup Redis

Redis installation will vary by OS.

#### 3.1 Setup OSX Redis

Note that the location to download the latest redis binary has changed according to the [instruction manual](http://www.js2node.com/redis-io/install-redis-io-2-4-17-on-mac-osx-as-service), but you should use the latest stable version download link at [http://redis.io/download] instead of the old googlecode.com link in the instruction manual.

#### 3.2 Setup Linux Redis

    $ sudo apt-get install redis

#### 3.3 Setup Windows Redis

1. download the latest bins [https://github.com/MSOpenTech/redis/tree/2.6/bin/release]

2. Then unzip to `redisbin/` and include that in your `%PATH%`

3. Then get the `https://github.com/kcherenkov/redis-windows-service`

4. And add it as service:
 
    sc create Redis start= auto DisplayName= Redis binpath= "C:\prj\repo\redisbin\RedisService.exe"

**NOTE:** no redis.conf needed! Based on: [http://www.saltwebsites.com/2012/how-run-redis-service-under-windows]

#### 3.4 Verify Redis Setup

Once installed, make sure redis is running. Use the CLI packaged with redis:

    $ redis-cli ping
    PONG

On production `REDISTOGO_URL` will provide the correct values for accessing the redis instance. If these are not defined the fallback value is `redis://localhost:6379` which will handle the dev setup.


### 4. Setup ImageMagick

Binary package that supports image resizing. Already present on heroku on codeship, thus you only need to run this step on your dev machine:

    $ brew install imagemagick # OSX


### 5. Setup Source Code

Clone the repo (if 1st command `git clone ...` doesn't work make sure you install a public key into your bitbucket account and use the private key in you local lssh config):

    $ git clone git@bitbucket.org:easypairings/ep.git
    $ cd ep
    $ virtualenv venv # to create a new environment in the venv folder

There are several environment variables that you need to customize for the server. These are best set in the virtualenv's activate script, edit the file ``venv/bin/activate`:

    export DEBUG=1 # default is 0, errors are easier to track, also forces http
    export DATABASE_URL=postgresql://ep@localhost/easypairings
    export MAIL_SERVICE=mailtrap
    export MAILTRAP_HOST=mailtrap.io
    export MAILTRAP_PASSWORD=dc893828c3892275
    export MAILTRAP_PORT=2525
    export MAILTRAP_USER_NAME=heroku-9d836ef8cff2aa7e
    export AWS_ACCESS_KEY=AKIAIGKBIFI5VJF6JADQ
    export AWS_SECRET=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
    export AWS_TALENT_BUCKET=flavor_dev
    export PHOTO_BUCKET=epair_dev
    export EP_HOST_BASE=127.0.0.1.xip.io:8080
    export EP_HOST_FOH=foh.127.0.0.1.xip.io:8080
    export SETTINGS=settings.py
    export FILEPREVIEWS_API_KEY=dpPEi5xp9vsrovzWoP6V5GEN3GRg1p
    export FILEPREVIEWS_SECRET=GiRUV9G8bcWVmqJLSDBe2EsXmIG5U9
    export AWS_PREVIEW_TALENT_BUCKET=ep-preview

Then, save the file and close the editor. Back at the command line:

    $ . venv/bin/activate # or venv/Script/activate.bat on windows
    $ pip install -r requirements.txt 

If `pip` fails, as it might on OSX when installing the `easypairings-pages` repo, it might be that your pip is running in strict mode and does not allow alpha versioned packages to install. Simply add the `--pre` option to overcome this.

On **Linux**, you will also need the Postgres developer tools to insure that pip can install psycopg. These tools can be installed one of two ways, depending upon your distro:

    $ sudo yum install postgresql-devel # RPM distros
    $ sudo apt-get install postgresql-dev # DEB distros

On Windows `pip` *will* fail, so you need to install binary packages. These are known to be needed:

- psycopg2 : http://www.stickpeople.com/projects/python/win-psycopg/
- py-bcrypt : https://bitbucket.org/alexandrul/py-bcrypt/downloads
- pycrypto : http://www.voidspace.org.uk/python/modules.shtml#pycrypto

Also needed on Windows: `easy_install pycrypto*.exe` to install into virtualenv.

Having installed postgres and the requisite binaries, run alembic's migration to set up the database schema:

    $ easypairings-manage db upgrade

If it fails to start with failure to `import six` you need to do `pip install six` first. This is known issue with Python installed by `homebrew` on OSX.

#### 5.1 Setup the pages submodule

All code for the static site is in `pages/easypairings_pages` package. The production static site is deployed from the `pages/verify` directory.

You will need node.js that comes with npm. Go download the official here: [node.js](http://nodejs.org/download/)

Verify by:

    $ npm
    ...
    npm@1.3.11 /usr/local/lib/node_modules/npm
    $

Then run this once, to add the local node package from package.json

    $ npm install

Also, need to confirm that Ruby and Sass installed and in your PATH for grunt to work. 
Verify Ruby is installed and on the path by:

    $ ruby -v
    ruby 2.0.0p247 ...
    $
Verify Sass is installed and on the path by:
    
    $ sass -v
    Sass 3.3.14 (Maptastic Maple)
    $

If Sass is not, installed, do that by `sudo gem install sass`. And then follow the instructions at: https://github.com/gruntjs/grunt-contrib-sass

Then you can compile SCSS and generate the static site by:

    $ grunt

Note:

* This package contains the templates that are reused to generate the static site and assets
* The templates here are also used by the Flask application in `web` package  * The email templates reside here as well. 

#### 5.2. Setup eapp submodule

We accept resumes by email, we call these eApps. The repo contains the code in `eapp/easypairings_eapp` package that processes these from an imap inbox to the database. No additional setup is needed.

#### 5.3. Setup web submodule

The dynamic site (aka FOH) is code in `web/easypairings_web` package. This depends on the **pages/** package. No additiona setup needed.


### 6. Setup Testing

We use *nose* with *coverage* and *selenium* test frameworks. You will need to install those manually into your *virtualenv*:

    $ pip install nose coverage selenium

#### 6.1 Add yourself as Staff

Generate staff credentials:

    $ easypairings-manage addstaff <first_name> <last_name> <email> -p <login password> -s true

Flags are for permission to use different staff interfaces: `-sl`=shortlist, `-m`=messages, `-c`=client mgmt, `-s`=staff mgmt. You can add these permission in the HQ/Staff Mgmt interface if you have the `-s` permission. You can also create a test client and the yourself as a supervisor.

### 7. Setup Dev Environment

#### 7.1 IDE

Lot of us use Sublime Text 2. Here are some notes on how to set it up for Python, HTML, CSS and LESS development:

1. Install Package Control <https://sublime.wbond.net/>
2. emmet        - zen coding
3. gitgutter       - git diff in gutter
4. jinja2          - jinja2 editor type
5. live reload     - live reload support
6. markdown preview    - markdown preview and build
7. markdownediting - markdown editing
8. pyv8            - ?
9. sublimecodeintel    - better autocomplete
10. sublimelinter       - interactive linting
11. sublimerepl     - interpreter inside sublime
12. sublime rope        - better completions
13. theme - flatland    - less chrome


## DEVELOPMENT

We use xip.io for accessing local servers. It's a great and free service. Servers are accessible at [static: http://127.0.0.1.xip.io:8080/](http://127.0.0.1.xip.io:8080/) [dynamic: https://foh.127.0.0.1.xip.io:8080/](https://foh.127.0.0.1.xip.io:8080/).

It is possible to run the server so that it accepts traffic from the local LAN, by figuring out your IP, and setting `EP_HOST_BASE` and `EP_HOST_FOH`:

    $ ipconfig en0
    ...
    $ export EP_HOST_BASE=<ip>.xip.io:8080
    $ export EP_HOST_FOH=foh.<ip>.xip.io:8080


### 1. Run Local Server

    $ easypairings-manage runserver

It will serve pages at [**localhost:8080**] unless `EP_HOST_BASE` or `EP_HOST_FOH` is overridden. Stdout is the log. Bookmark this link for local access: [http://127.0.0.1.xip.io:8080/] This will correctly use http only and will find the flask app at: `http://foh.127.0.0.1.xip.io:8080/`

### 2. Working with HTML/JS/SCSS

We will need a little description here. For now start with this:

    $ grunt watch


### 3. Run Redis Workers

Start up redisworker:

    $ python web/easypairings_web/workers.py
    09:42:50 RQ worker started, version 0.3.8
    09:42:50
    09:42:50 *** Listening on default...


### 4. Run Automated Tests

Make sure you have a running workers.py and a server in the background. Then in an activated virtualenv:

    $ nosetests web/ # all tests
    $ nosetests web/easypairings_web/seleniumtest # functional tests only
    $ nosetests web/easypairings_web/tests.py # unit and integration tests only

This should give you a complete listing of test coverage.


### 5. Run Sanity Check for Pages Package

Regression testing for the static site:

    $ ep site:verify    # either OK or FAIL, compares build/ and verify/

This will fail if there are `url_for()` routes that are not within the static site. These ought to be resolved before promoting. Assets should use `asset_url()` instead of `url_for()`.


### 6. Manual Testing

You access the local server.

This will reset the state of the position buttons on the client dashboard:

    $ easypairings-manage resetopening <supervisor_email>

#### 6.1 Microsoft IE

Best is to install a virtual server and download the virtual image provided by Microsoft at [http://modern.ie]:

1. Install virtualbox: [https://www.virtualbox.org/] under the download navigation.
2. Download and install the Windows7.IE10 VM from: [http://modern.ie] Ray Bango has a good blog entry on how: [http://blog.reybango.com/2013/02/04/making-internet-explorer-testing-easier-with-new-ie-vms/]
3. After the first start of the image, post-configuration, it's a good idea to make a snapshot of the virtualbox.
4. On the ost OS, set `EP_HOST_BASE=10.0.2.2.xip.io:8080` and `EP_HOST_FOH=foh.10.0.2.2.xip.io:8080` and generate the static site with `ep site` and run the local server.
5. On the virtualbox you can navigate to: [http://10.0.2.2.xip.io:8080/]



## DEPLOYMENT

### 1. Deployment Setup

**Do this once** We use two heroku repos, one each for production and one for staging. Their respective names are *ep-prod* and *ep-stage*. You need to add them as a remote git repo:

    $ git remote add prod git@heroku.com:ep-prod.git
    $ git remote add stage git@heroku.com:ep-stage.git
    $ git remote # should report origin, prod and stage

### 2. Deployment Steps

If you have modified the pages package, first, you need to sanity check your changes and promote them:

    $ ep site:verify # compares build/ and verify/ folders, complains if any diff
    $ ep site:promote # will execute only if there are changes to promote

Make sure commit and push changes in `ep` repo and and after that it's up to date with the bitbucket repo:

    $ git status
    $ git add # whatever is needed
    $ git commit -m "meaningful description of changes"
    $ git push

**NOTE:** Remember to clear cache on your browser (or use a private browser) and verify the changes at this point. 

Codeship is configured so that on the push hook it'll run all the tests, including selenium tests. Results will be reported in slack in the #dev-tools channel.

If the master branch is modified this test phase is followed by an automatic deployment to staging at [http://easypairings.co](http://easypairings.co) (Notice: .co not .com). This deployment also takes a latest backup from production and restores it to staging. Your login credentials are thus that of production.

If you are on a git branch, you can initiate a staging deploy with:

    $ make deploy-stage

FINALLY, if all is well, you can deploy you local version to production:

    $ make deploy-prod


## CONFIGURATIONS

### 1. Codeship.io

We use codeship for CI (Continuous Integration) and CD (Continuous Deployment).

Configuration is recorded here, in case we need to recreate it.
**Date** May 28, 2014

Setup Commands:

    pip install -r requirements.txt
    createdb -E UTF8 easypairings
    createuser -w ep
    easypairings-manage db upgrade
    echo "CI_BUILD_NUMBER: $CI_BUILD_NUMBER"
    echo -e "machine api.heroku.com\n  login $HEROKU_LOGIN\n  password $HEROKU_TOKEN\nmachine code.heroku.com\n  login $HEROKU_LOGIN\n  password $HEROKU_TOKEN\n" > ~/.netrc
    chmod 0600 /home/rof/.netrc
    npm install
    grunt

Test Commands:

    cd pages && python setup.py test && sleep 2 && cd ..
    cd eapp && python setup.py test && sleep 2 && cd ..
    nohup bash -c "python web/easypairings_web/workers.py &" > ~/workers.out 2>&1
    nohup bash -c "easypairings-fullweb &" > ~/web.out 2>&1 && sleep 5
    cd web && python setup.py test && sleep 2 && cd ..
    echo "WORKERS LOG:" && cat ~/workers.out
    echo "WEB LOG:" && cat ~/web.out
    # test alembic downgrade
    cd web/easypairings_web/alembic && alembic downgrade base && cd -

Environment Variables::

    DATABASE_URL=postgresql://ep@localhost/easypairings
    DEBUG=1
    AWS_TALENT_BUCKET=flavor_dev
    AWS_ACCESS_KEY=<>
    AWS_SECRET=<>
    AWS_SCREENSHOT_BUCKET=ep-screenshot
    MAIL_SERVICE=mailtrap
    MAILTRAP_HOST=mailtrap.io
    HEROKU_TOKEN=<>
    HEROKU_LOGIN=codeship@easypairings.com
    MAILTRAP_PASSWORD=<>
    MAILTRAP_PORT=2525
    MAILTRAP_USER_NAME=16352050c9f59934f
    EP_HOST_BASE=127.0.0.1.xip.io:8080
    EP_HOST_FOH=foh.127.0.0.1.xip.io:8080
    SETTINGS=settings.py
    PHOTO_BUCKET=epair_dev
    FILEPREVIEWS_API_KEY=dpPEi5xp9vsrovzWoP6V5GEN3GRg1p
    FILEPREVIEWS_SECRET=GiRUV9G8bcWVmqJLSDBe2EsXmIG5U9
    AWS_PREVIEW_TALENT_BUCKET=ep-preview

Deployment of master branch with custom script::

    # record artifacts here by echoing on the terminal
    pip freeze
    # prep
    git remote add stage git@heroku.com:ep-stage.git
    make deploy-stage

#### 1.1 Tunneling the server on codeship

Sshing over and execute the `cs s` and `cs t` commands so that the server is running, and then on the local machine run this:

    $ ssh -L 8080:127.0.0.1.xip.io:8080 rof@54.87.233.153 -p 65503 -N 
    # rof@<ip> -p <port> from the ssh command given by codeship

### 2. Heroku

It is important that we configure the heroku apps to use Python buildpack. Since we have a package.json in the root (for grunt), heroku mistakenly detects a node.js app instead of python. Here's how to fix it:

    heroku config:set BUILDPACK_URL=https://github.com/heroku/heroku-buildpack-python --app=<app>

More info: [Why is my Flask app being detected as node.js on Heroku](http://stackoverflow.com/questions/20171169/why-is-my-flask-app-being-detected-as-node-js-on-heroku)
