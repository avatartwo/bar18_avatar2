# bar18_avatar2

This repository contains the examples described in "Avatar²: A Multi-target Orchestration Platform" [1],
which is available [here](http://s3.eurecom.fr/docs/bar18_muench.pdf).

It comes with a handy Vagrantfile, which sets up an avatar² environment with 
everything needed to dive into the examples right ahead.
However, if you don't feel like having built anything from scratch, we also
provide an already set up vagrant box on app.vagrantup.com, which can be checked
out with `vagrant init avatar2/bar18_avatar2`.

However two out of the three examples require dedicated hardware, while the third
example requires some manual setup - all of this is described in more detail below.

## Examples
### 01_harvey
This example replicates the proof-of-concept I/O Interception implementation of
Harvey, a rootkit for Programmable Logic Controllers (PLCs) presented in [2].
This example requires the presence of an Allen Bradley CompactLogix 5370 with
an attached JTAG-Debugger.

The scripts in this repository are developed against model version
1769-L16ER-BB1B of the plc, firmware version 30.012 and the usage of an
SEGGER JLINK as debugger. Other configurations will likely require minimal
changes to the scripts in this repository.


### 02_firefox
This examples finds a bug artificially inserted into firefox 52.0, by utilizing
avatar² to execute firefox concretely inside gdb and copying this concrete state
into angr [3] at an interesting function, while symbolizing some of the function
arguments.

It doesn't come with any hardware dependencies, however as compiling firefox
requires a reasonable amount of time, we are hosting a pre-compiled version of firefox
externally, which gets downloaded and extracted by the bootstrap.sh script.
However, we also include a script for automatically building firefox with the inserted bug
from source at `02_firefox/build_firefox.sh`.

For running the actually example, X forwarding has to be enabled to prevent 
firefox from not finding a display during startup:
`vagrant ssh -- -X`
Furthermore, firefox should be at least run once before starting the analysis,
in order to disable the check for using firefox as default browser.

### 03_panda_rr
This example demonstrates the orchestration and  memory forwarding capabilities of
avatar². It utilizes PANDA [4] to create a record of a firmware's execution during
partial emulation, which then can be replayed without the need of having the
physical device attached anymore.

For replicating this example, a NUCLEO STM32L152RE development board is
required. The firmware.bin used here is the same as in the 
[Nucleo-L152RE example](https://github.com/avatartwo/avatar2-examples/tree/master/nucleo_l152re)
and needs to be flashed on the device beforehand.

## References

[1] M. Muench, D. Nisi, A. Francillon, D. Balzarotti. 
"Avatar²: A Multi-target Orchestration Platform."
Workshop on Binary Analysis Research, San Diego, California, February 2018.

[2] L. Garcia, F. Brasser, M. H. Cintuglu, A. R. Sadeghi, O. Mohammed, S. A. Zonouz. 
"Hey, my malware knows physics! attacking plcs with physical model aware rootkit."
Network & Distributed System Security Symposium, San Diego, California, February 2017.

[3] Y. Shoshitaishvili, R. Wang, C. Salls, N. Stephens, M. Polino, A. Dutcher,
J. Grosen, S. Feng, C. Hauser, C. Kruegel, G. Vigna.
"SoK: (State of) The Art of War: Offensive Techniques in Binary Analysis."
IEEE Symposium on Security and Privacy, San Jose, California, May 2016.

[4]  B. Dolan-Gavitt, J. Hodosh, P. Hulin, T. Leek, R. Whelan. 
"Repeatable Reverse Engineering with PANDA."
Program Protection and Reverse Engineering Workshop, Los Angeles, California, December 2015.
