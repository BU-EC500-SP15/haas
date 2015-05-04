README.md
=========

This project was completed in fulfillment of requirements for CS 591/EC500, Cloud Computing at Boston University.  The following describes installation instructions for recursive haas.  Other installation instructions can be found in the haas github repo.  Of particular interest is HACKING.rst.


SETTING UP BASE HAAS
--------------------  

First, clone the repo:
<git clone https://github.com/BU-EC500-SP15/haas>

This will create the haas directory locally.  Now set up the virtual environment:

$ <cd haas>
$ <virtualenv .venv> 
$ <source .venv/bin/activate> 
$ <pip install -e .>

Each time you work with haas or recursive haas, enter the virtual environment first by running this command in the haas directory:

$ <source .venv/bin/activate> 

Copy haas.cfg.rhaas-dev-example as haas.cfg.  Make the following amendments:

Uncomment:
<dry_run=True>

Add:
<[recursive]>
<rHaas = False>
<#project => 

$ <haas init_db>

(the following may become deprecated due to the new ENV variable method of choosing endpoints) 
You must use different port numbers on base and recursive haas. By default, recursive haas is configured to listen on port 5001, to differentiate it from the base haas code which defaults to port 5000.  To change the port number on the base instance, you must verify that the port number is changed from 5001 to a different port in two different places:
* the serve function at the bottom of file /haas/moc/rest.py
* the endpoint in the .cfg file


cd back to the /haas parent directory

Start the base haas server:
$ <haas serve>

In another terminal window, cd to the same haas directory and enter the virtual environment:
$ <source .venv/bin/activate>

Create the project for recursive HaaS:
$ <haas project_create BaseProject> 

BaseProject is the base haas project that will contain all nodes assigned to recursive haas.  You can use any name, just be sure to use the same name in the haas.cfg file for recursive haas (see below).



SETTING UP THE RECURSIVE HAAS
-----------------------------

The first part of this is the same as setting up the base haas:

$ <git clone https://github.com/BU-EC500-SP15/haas>

$ <cd haas>

$ <virtualenv .venv> 
$ <source .venv/bin/activate>
$ <pip install -e .>

(Again, you should run 
$ <source .venv/bin/activate>
every time you work with recursive haas.)

$ <cp haas.cfg.rhaas-dev-example haas.cfg>


Make the following amendments to the new haas.cfg file:

Uncomment:
<dry_run=True>

Change “BaseProject” to the project name you used when setting up base HaaS.

run:
$ <haas init_db>
$ <haas serve>

In another terminal, cd to the same haas directory and set the virtual environment:
$ <source .venv/bin/activate>

All recursive calls will be made from the rhass_client directory.  The rhaas_client directory doesn’t have to be inside the haas directory, as long as you activate the virtual environment before changing to the new directory.

$ <cd rhaas_client>

Copy the haas.cfg file from the recursive haas directory to the the rhaas_client directory, then change the client endpoint to point to port 5001.  If in the above steps you changed recursive haas to listen at a different port, use that port number instead.

[client]
<endpoint=http://127.0.0.1:5001>


A Note On [client] Endpoints:
-----------------------------

The client endpoint in haas.cfg should be the IP and port for the *base haas* instance in both base and recursive haas directories.  The only client endpoint pointing to the recursive haas IP/port should be in haas.cfg in the rhaas_client directory.

If you type a haas command from a terminal that is currently inside the recursive haas directory, it will be run on base haas, even if it is a non-recursive call.

For this reason, all commands interacting with rhaas should be run from the rhaas_client directory.



WORKING WITH FAST PROVISIONING
==============================

Download the VM appliance consisting of preconfigured fast provisioning boot loader (FPBL) from here. 
https://drive.google.com/open?id=0B3rQr5rEemfUcnNaTXpqSmpkQ28&authuser=0

You can import this appliance using Virtual Box and boot the VM.
Make sure to enable vboxnet0 in your virtualbox. 

On boot up, the you can SSH into it using the following information

IP address: 192.168.56.13
User: sahil
Password: sahil123

In the home directory /hom/sahil
you will see a directory called “loadingbay”

The custom OS is precopied into loading bay.



Contents of loading bay:
sahil@ubuntu-basic:~$ ls -l loadingbay/
total 236200
-rwx------ 1 sahil sahil       473 May  2 20:23 loadCustomOS.sh
-rw-r--r-- 1 sahil sahil 238742291 May  2 20:23 matrixMult_3.16.0-4-amd64.cgz
-rw------- 1 sahil sahil   3113200 May  2 20:23 vmlinuz-3.16.0-4-amd64

execute the script loadCustomOS.sh using sudo.

sudo ./loadCustomOS.sh

sudo password: sahil123

Once it loads the new kernel successfully,
you can simply switch to the new custom OS using command.

sudo kexec -e

That will switch you into the new Custom OS. 
You can SSH into it using the following information.
IP-Address: 192.168.56.20
username: sahil
password: sahil123

Also,
root username: root
root password: root123

In home directory of sahil /home/sahil here you will see a folder called “compute” and a symlink to the script to switch back to FPBL from customOS: “loadFPBL.sh”
Change directory into “compute”
cd compute

Run the matrix multiplication application: 
    ./matrixmult
It will ask for size of matrices and input matrices.
It will provide the product of the two matrices.

Once you done using the application change back to the home directory /home/sahil
switch user to root
su
password: root123

To load back the FPBL kernel just execute the script 
./loadFPBL.sh

Once it successfully loads the kernel, switch back using
kexec -e 

That will bring you back into FPBL. 









