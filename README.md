# Introduction
May 8 2022 there was Lebanese Elections for Expats
https://www.dgcs.gov.lb/arabic/where-to-vote/expats

There are polling stations everywhere.

I had the personal experience of going to polling station in Philadelphia from Pittsburgh. It was a 5 hour drive on each trip.

I want to see where these polling stations are and where are they.
I might get them and out them on a Google My map

# How The site works
The site seems to take a 12 digit number for the national ID. My

in python we will use
```
str(1).zfill(2)
Out[3]: '01'
```
https://stackoverflow.com/questions/733454/best-way-to-format-integer-as-string-with-leading-zeros

The site is sending post requests to
https://www.dgcs.gov.lb/PollingStations/GetPollingStationExpat

I tried it with ID number 000000000000
The request is URL encoded with
`Type=IDNumber&IDNumber=000000000000`

For a failed request we get the response as follows
`{"success":false,"error":"No result found"}`

For a successful response we get it as follows
```
{
    "success": true,
    "data": {
        "IMMIGRANT_ID": null,
        "COUNTRY_NAME_AR": "الولايات المتحدة الأميركية",
        "MISSION_NAME_AR": "قنصلية لبنان العامة في الولايات المتحدة الأميركية, نيويورك",
        "STATION_Number": null,
        "STATION_NAME": "Saint Maron Hall",
        "STATION_ADDRESS": "1013 Ellsworth Street, Philadelphia PA 19147",
        "MADINA": null,
        "ROOM_SEQ": "58",
        "STATION_ROOM": "Saint Maron Hall - غرفة رقم 1",
        "FIRST_NAME": null,
        "LAST_NAME": null,
        "FATHER_NAME": null,
        "MOTHER_FULL_NAME": null,
        "BIRTH_DAY": null,
        "BIRTH_MONTH": null,
        "BIRTH_YEAR": null,
        "GENDER_NAME": null,
        "REGISTER_NUM1": null,
        "REGISTER_NUM2": null,
        "RELIGION_NAME": null,
        "REG_RELIGION_NAME": null,
        "DEPARTMENT_NAME": null,
        "VILLAGE_NAME_AR": null,
        "QADA_NAME_AR": null,
        "MUHAFAZA_NAME_AR": null,
        "IDENTITY": null
    }
}
```
# Our Scraping
## Getting all the valid Lebanese IDs abroad
we do have a simple algorithm working `getValidIDs.py`.10^11 requests on this thread was going to take a lot of time. So I needed a way to do concurrent requests.

There is a library for python called concurrent which would really make this faster
https://blog.devgenius.io/how-to-send-concurrent-http-requests-in-python-d9cda284c86a

A clear example can be found below
https://docs.python.org/3/library/concurrent.futures.html#module-concurrent.futures

I put an arbitrary number of threads. At the moment, I have 1o threads.(Max workers is set to 10)

Now according to the link below I can do `2 * multiprocessing.cpu_count() + 1`
I have an 8 core machine so I can go as much as 17 workers
https://rednafi.github.io/digressions/python/2020/04/21/python-concurrent-futures.html

### How Long will this take
The national ID is a 12 digit number. It is a hundred billion number.
My current strategy is to check every number and see if it is valid.
This will give me all the foreign residents that voted abroad.

At the current rate, I can do 5000 checks per minute.
To do 100 billion it would take
20000000 minutes

That converts to 38 years.

My national id is only 8 digits.
so assuming we only need to check to 10^8.
We would only need 20000 minutes.
That's only 13 days.

We need to try to amp this up a bit more.

We got (460-158) 302 readings in
5932.092s (100 minutes)

Half a million requests were done in 3 hours and a half (500,000 to one million)
12137.335s
In that time we got 412 more IDs

### What is the distribution of National IDs
I presume not all numbers are present. After checking 2 million IDs we have only around 2200 valid ids.
I did histogram of the ids we have so far and it seemed pretty much uniformly distributed.

### Getting the poll stations
