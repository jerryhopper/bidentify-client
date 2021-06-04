# bidentify-client

commandline identification tool for file used by Bohemia Interactive games.



__Bidentify__ ( *Pronounced: Bee-Eye-dentify* ) 

A file identification utility-suite for detecting,finding and archiving usergenerated content for Bohemia Interactive games.

The Bidentity suite consists of several parts.

* The __[Bidentify-client](https://github.com/jerryhopper/bidentify-client)__ is a commandline tool to scan, detect & identify Addons and Missions archives, folders or .pbo's

* The __[Bidentify-server](https://github.com/jerryhopper/bidentify-server)__ is the database/web-backend for use with the bidentify-client,bidentify-node,bidentify-vault.

* The __[Bidentify-vault](https://github.com/jerryhopper/bidentify-vault)__ is a Torrent based file-archive that archives and seeds (ALL!) files which are listed in the Bidentify-server. This package is for dedicated librarians who want to preserve and longterm seed all data on the Bidentify server of your choice. 

* The __[Bidentify-node](https://github.com/jerryhopper/bidentify-node)__ is a Torrent based file-archive that seeds files ( limited to specific size) which are listed in the Bidentify server of your choice.


## Download
Download the executable version from the releases page : 
* https://github.com/jerryhopper/bidentify-client/releases

## Installation
Unpack the zipfile.
add to your windows PATH


# Usage
Open a command-prompt and navigate to the folder of your schoice.

Run on the commandline :  bidentify --help

## bidentify scan

Scans the current directory or the directory of choice. 

**bidentify scan** [-o --output] [-d --directory] 


-d or --directory : *Specify a custom directory to scan.* 

-o or --output <name> : *Specify a custom name for the scan-results.* 



## bidentify update

Updates the bidentify file-lists from the server.

**bidentify update** 
