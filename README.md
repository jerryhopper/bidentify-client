# bidentify-client

commandline identification tool for file used by Bohemia Interactive games.



__Bidentify__ ( *Pronounced: Bee-Eye-dentify* ) 

A file identification utility-suite for detecting,finding and archiving usergenerated content for Bohemia Interactive games.

The Bidentity suite consists of several parts.

* The __[Bidentify-client](https://github.com/jerryhopper/bidentify-client)__ is a commandline tool to scan, detect & identify Addons and Missions archives, folders or .pbo's

* The __[Bidentify-server](https://github.com/jerryhopper/bidentify-server)__ is the database/web-backend for use with the bidentify-client,bidentify-node,bidentify-vault.

* The __[Bidentify-vault](https://github.com/jerryhopper/bidentify-vault)__ is a Torrent based file-archive that archives and seeds (ALL!) files which are listed in the Bidentify-server. This package is for dedicated librarians who want to preserve and longterm seed all data on the Bidentify server of your choice. 

* The __[Bidentify-node](https://github.com/jerryhopper/bidentify-node)__ is a Torrent based file-archive that seeds files ( limited to specific size) which are listed in the Bidentify server of your choice.


# What does it do?

The bidentify client scans your local directories, and matches archive files and folders, and matches this against known-filelists downloaded from the a bidentify-server.

# Why?

In the 20+ years that Bohemia Interactive has created games, many user-generated content was created and hosted on community websites like Armaholic.com. When time passes, resources get lost - and so does the content.

In an attempt to keep the old content alive, the bidentify project was started. It enables enthousiasts to find and keep old Bohemia-Interactive related files available to the public.


## Download
Download the executable version from the releases page : 
* https://github.com/jerryhopper/bidentify-client/releases

## Installation

Unpack the zipfile to a directory of your choice.

Add this directory to your windows PATH

Example: ```setx path "%path%;c:\DirectoryWithUnzippedContents"```


## Updates

In case there is a new update, just extract the contents of the zipfile in the exact same folder as you initially installed it.


# Usage

Open a command-prompt and navigate to the folder of your schoice.

Run on the commandline :  bidentify --help




## bidentify scan

Scans the current directory or the directory of choice. 

**bidentify scan** [-d --directory] 

-d or --directory : *Specify a custom directory to scan.* 


## bidentify analyze

Analyzes the current directory or the directory of choice. 

**bidentify analyze** [-d --directory] 

-d or --directory : *Specify a custom directory to scan.* 


## bidentify update

Updates the bidentify file-lists from the server.

**bidentify update** 
