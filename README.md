# Item Catalog - Udacity
### Full Stack Web Development - Caroleen Chen
_____________
# About
This repository contains downloadable code and output for the Udacity "Item Catalog Project".

This is an application that provides a list of snowboards within a variety of brands as well as provides a user registration and authentication system. Registered users will have the ability to post, edit, and delete their own items.

# Prerequisites
* [Python 3](https://www.python.org/downloads/)
* [Vagrant](https://www.vagrantup.com/downloads.html)
* [Virtualbox 3](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
* [Vagrant Files](https://github.com/udacity/fullstack-nanodegree-vm)

# Getting Started
1. Start up and connect to the vagrant machine with the Vagrant File configuration
'''
sudo apt install virtualbox-dkms
sudo dpkg-reconfigure virtualbox-dkms
vagrant up
vagrant ssh
'''
2. Make sure the database is set up by running 'python database_setup.py'.
3. You will need to make sure the site's data (lotsofsnowboards.py) is loaded into the local database. Do this by running 'python lotsofsnowboards.py'
4. Run 'python final-project.py' to access the item catalog on 'localhost:5000/'
