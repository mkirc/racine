# Mercury Sample Manager

This is Mercury Sample Manager (for now... for the lack of a better name), a sample management tool that enables researchers
to keep track of their samples from any PC in a laboratory. The programme is a Flask-based web service that runs on a
central server on the local network of your research institute and that can be accessed from all other computers on the
same network using the normal web browser (should be a recent browser though).

# Installation of development server

This programme should work an almost any platform (Linux, Windows, MacOS), but I only provide the installation
instructions for Linux. Seeing that you should install it on a server, I suppose Linux is the target OS in most
cases anyways.

You should have python 2.x and pip installed on your system. From there on it's quite straightforward:

    $ sudo pip install virtualenv

installs virtualenv for python. This is not absolutely necessary, but I recommend it. You can now create a folder somewhere
and clone the git repository:

    $ git clone git@github.com:green-mercury/SampleManagerWeb.git

Now you enter this directory and you create a virtual environment for python - and activate it:

    $ cd SampleManagerWeb
    $ virtualenv venv
    $ . venv/bin/activate

Finally, all that remains to do is to install the required python packages:

    $ pip install -r requirements.txt

You can start the development server by simply executing the "run script":

    $ ./run

TODO: explain how to initialise the DB

# Deployment with gunicorn and nginx

Carry out the steps described above in order to set up the development server. Then configure gunicorn by creating
the file /etc/init/msm.conf and copying the following code into it:
 
    description "Gunicorn application server running Mercury Sample Manager"
    
    start on runlevel [2345]
    stop on runlevel [!2345]
    
    respawn
    setuid [user name]
    setgid www-data
    
    env PATH=[path]/SampleManagerWeb/venv/bin
    chdir [path]/SampleManagerWeb
    exec gunicorn --workers 4 --bind unix:msm.sock -m 007 manage:app

Where you will have to replace [user name] by your user name and [path] by the path where you installed the programme.

Now install nginx:

    $ sudo apt-get install nginx

Create an SSL certificate and key in the following folder:

    $ sudo mkdir /etc/nginx/ssl
    $ cd /etc/nginx/ssl

In order to create SSL certificate and key follow the steps given in https://www.digitalocean.com/community/tutorials/how-to-create-a-ssl-certificate-on-nginx-for-ubuntu-12-04

You then want to configure your nginx server. Create a file "msm" in /etc/nginx/sites-available and copy the following content into it:

    server {
        listen 80;
        server_name localhost;
        rewrite        ^ https://$server_name$request_uri? permanent;
    }
    
    
    # HTTPS server
    
    server {
        listen 443;
        server_name localhost;
    
        ssl on;
        ssl_certificate /etc/nginx/ssl/server.crt;
        ssl_certificate_key /etc/nginx/ssl/server.key;
    
        location / {
        include proxy_params;
          proxy_pass http://unix:/home/holger/PycharmProjects/SampleManagerWeb/msm.sock;
        }
    }

Then create a symbolic link to this file in /etc/nginx/sites-enabled and delete the default entry:

    $ sudo ln -s /etc/nginx/sites-available/msm /etc/nginx/sites-enabled
    $ sudo rm /etc/nginx/sites-enabled/default

You can now start your server by executing:
 
    $ sudo start msm
    $ sudo service nginx restart

The server will now automatically - i.e. also after a reboot - be available on localhost.

More details: https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-14-04