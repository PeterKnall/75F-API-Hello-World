# Hello, world!
A collection of projects serving as "PKs Notes" on how to use various 75F APIs.

---
## Read
Retrieve a value or list of values using one of the following methods:
* Read by filter: ver:"3.0" filter "system and equip and siteRef==@b8a1a5be-3080-40e6-9161-64f39944db9e"
* Read by filter (paged): ver:"3.0" size:25 page:3 filter "system and equip and siteRef==@b8a1a5be-3080-40e6-9161-64f39944db9e"
* Read by filter (arrow operator): ver:"3.0" id,dis,equip,siteRef,system @6d78f1c0-d10a-4482-8058-db328441a669,"System Equip A",M,@b8a1a5be-3080-40e6-9161-64f39944db9e,M @84010772-46ec-4937-9430-71083196f2c4,"System Equip B",M,@b8a1a5be-3080-40e6-9161-64f39944db9e,M
* Read by id: ver:"3.0" id @6d78f1c0-d10a-4482-8058-db328441a669 @84010772-46ec-4937-9430-71083196f2c4
---
## hisReadMany
Used to read time-series (trend) data from points in the Facilisight platform.
Points can be selected with tags or Haystack queries, and the time range can
be defined by specific DateTime ranges or through the use of commonly
defined terms (such as "today").

The request in this example uses an HTTP 1.1 POST Request and Response to
transmit and receive data.  The data is transmitted using Zinc formatted
grid and received as text in JSON format.

### Version
The following text, as shown, must appear as the first argument in the 
Request text to identify the version of Zinc being used:

ver:"3.0"

### Range
Range can be formatted as:
* "today"
* "yesterday"
* "{date}"
* "{date},{date}"
* "{dateTime},{dateTime}"
* "{dateTime}"

Where the dateTime is formatted as:

"2020-01-01T12:00:00-04:00 New_York,2020-01-03T00:00:00-04:00 New_York"

And date is formatted as:

"2020-01-01"

### ids

"ids" are GUIDs for individual points.  Each id must begin with an "@"
symbol, and only one id can appear on each line.

### Example
Note in the example below that there is no extra whitespace.  Extra spaces
may cause the request to crash and return a Zinc error.

ver:"3.0" range="today"\n
@52bdc021-71d3-4479-903e-0b0986a993ee\n
@52b2309a-10ec-4578-af76-8c1130c58044

---
## Zinc
Zinc stands for "Zinc is not CSV".
### Syntax
Every grid has the following "\n" separated lines:
* One line of metadata applied to the entire grid
* One line of column definitions
* Zero ore more lines of rows

https://project-haystack.org/doc/docHaystack/Zinc

---
## JSON
JSON stands for Javascript Object Notation.
