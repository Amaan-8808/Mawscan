# mawscan

This malware scanner will first <b>index files</b> and then will perform <b>scanning</b> on select indexed files.

#### WHAT PROCESSES ARE CACHED ?

|  | INDEX | SCAN | 
| - | - | - |
| CACHE | cached | not cached | 

Essentially, the program will not repeat the <b>INDEXING PROCESS</b> for subsequent scans.

#### WHAT PROCESS WILL THE PROGRAM PERFORM ?

|  | INDEX + SCAN | ONLY SCAN | ONLY INDEX |
| - | - | - | - |
| FLAG | with --index flag | default (if db is cached) | with --noscan flag |

If there has been a change in the filesystem then user can force <b>INDEXING PROCESS</b> and update the cache.

If your filesystem is huge and system specs are low then <b>INDEXING + SCANNING</b> can take quite a long time. Refresh cache without committing time for a scan.

#### NOTE - 

`YOU DO NOT REQUIRE --INDEX FLAG FOR YOUR FIRST USE OF THE TOOL`

The tool will automatically index the filesystem. The flag is only required on subsequent scans.

## FLAGS

`python runme.py --help`

`usage: runme.py [-h] [-i] [-ns] [-t THREADS]`

#### `-h` // `--help`

Show this help message and exit

#### `-i` // `--index`

Refresh indexing cache

#### `-t THREADS` // `--threads THREADS`

Specify the number of threads required for scanning (default=10)

#### `-p PROCESSES` // `--processes PROCESSES`

Specify the number of processes required for scanning (default=10)

#### `-ft {application,text,image,video,all}` // `--filetype`

Specify filetype that you want to scan

### SCHEDULE SCANS

#### `--config CONFIG_NAME`

Saves scan by configuration name

#### `--schedule CONFIG_NAME`

Schedule the scan to run at a specific time via configuration name

#### `--time TIME`

Time to run the task (e.g. 14:30)

#### `--daily`

Run the task 

#### `--monthly`

Run the task monthly

#### `--hourly`

Run the task hourly

### CUSTOMISE SCAN TYPE 
**COMPULSORY TO USE ONE OF THESE FLAGS**

#### `--yara`

Utilise YARA rules for scanning

#### `--md5`

Utilise MD5 hash for scanning

#### `--sha1` 

Utilise SHA1 hash for scanning

#### `--sha256`

Utilise SHA256 hash for scanning

#### `-ns` // `--noscan`

Perform only file indexing, no scan

## GITHUB REPOSITORY

Malware Database Repository - `git clone https://github.com/Endermanch/MalwareDatabase`

YARA rules taken from - `git clone https://github.com/Yara-Rules/rules.git`

HASH taken from - `git clone https://github.com/eset/malware-ioc`

malwarescanner - `git clone https://github.com/password123456/malwarescanner`

## SCHEDULE SCANS

**FILE TYPES** - APPLICATION, TEXT, IMAGE, VIDEO, ALL

FILE TYPE ALL SHA256 SCAN

> **`python runme.py --sha256 --type all`**

ACTIVE SERVER FOR SCHEDULER -

> **`python schedule.py`**

EXAMPLE OF SCHEDULING SCANS -

> **`python runme.py --sha256 --config scan_config`**

> **`python runme.py --schedule scan_config --time 02:30 --monthly`**