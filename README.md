# Spindown

Takes care of turning off hard drives after a certain time of inactivity.

Originally developed for Raspberry Pi (raspbian), for the sole reason that the _hdparm_ utility in itself (as well as other tools) seemed to be unable to do the job.

## How does it work?

The tool monitors HDD usage through the _/proc/diskstats_ file. Provided the entry for the given disk has not been changed for a while, it puts the drive to standby mode using the _hdparm_ utility. In order for the script to be able to monitor changes countinously, it will have to be executed regularly by e.g. a _cronjob_.

You can find more information about _/proc/diskstats_ on [The Linux Kernel Archives](https://www.kernel.org/doc/Documentation/ABI/testing/procfs-diskstats) .

## Installation and usage

  1. First of all, install _hdparm_. On _debian_ based distributions you can do that by simply issuing the following command in the _Terminal_.

    $ sudo apt-get install hdparm

  2. Run _Spindown_ using the _-i_ (or _--install_) command line switch. This will generate a default configuration file. The configuration file will be generated under the current working directory with the name of _config.cfg_ by default, but this can be changed of course (using the _-c_ or _--config_ switch).

  3. Edit the default configuration, set the drive you would like to control.

  4. Test your configuration using the _Terminal_ and see if it works as expected. (Run `python main.py -c config.cfg`.)

  5. Set up a _cronjob_ to run the script every 2 minutes. Add this _cronjob_ to those jobs of the _root_ user, since _hdparm_ needs _root_ priviliges. (You can save the line below in a file named _spindown_crontab.txt_, then run `sudo crontab spindown_crontab.txt` from the _Terminal_ or run `sudo crontab -e` and paste the line below in the editor that pops up.)

    */2 * * * * /usr/bin/python /var/tmp/spindown/main.py > /dev/null

  6. Finally, do not forget to restart _cron_.

    sudo /etc/init.d/cron restart

## Remarks

This is far from a perfect solution and there are some caveats you should know about.

  1. Once the disk has been put in standby mode the script remembers this fact and will not do anything until new changes do not get detected. It is possible however that the drive spins up for some reason (most likely because another tool such as _udisks-glue_ or _smartmontools_ acquires SMART data) and _Spindown_ will not be notified of this. In this case the only solution is stopping the program that is guilty in spinning up the drive. For _smartmontools_ you can find the ID of the problematic process by issuing the command `ps -ef | grep smartd` and then kill this process as root. If you have no idea on which software is causing the problem, you can use `sudo iotop -Pao` to find that out.

  2. For some drives _hdparm_ does not return `0` (indicating success), even though it puts them in standby mode successfully. In case you experience this issue, set the `check_return_value` configuration option to `False`.

## Development environment

Development was performed in the following environment.

  * Ubuntu 16.06
  * Python 3.5.2

The script has been tested on Raspberry Pi as well.

  * Raspbian GNU/Linux 8 (jessie)
  * Python 3.4.2
