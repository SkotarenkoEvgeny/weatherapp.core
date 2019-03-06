The Weatherapp program can search and compare the weather information from sites:
        accuweather.com/,
        rp5.ua/.
The user can set the location for the weather information.
The program can output information to command line, table, csv file, txt file.
She save information in cache for fast output information.

The command for management:
    'command',

    '-r', '--refresh',
        refresh data in cache
    '--debug',
        set debug level ( WARNING, -v INFO, -vv Debug)
    '-v', '--verbose',

    '-f', '--formatter',
        table, csv data to file, txt data to file
    '-time',
        change time for using data from cache