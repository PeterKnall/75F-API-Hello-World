# Hello, world!
A collection of projects serving as "PKs Notes" on how to use various 75F APIs.

---

## Examples are organized as follows:
* Example 00 - List all Site IDs
* Example 01 - List all CCUs on all Sites
* Example 02 - List all the current temperatures on all sites
* Example 03 - List all the current temperatures, heating setpoints, cooling setpoints, and temperature deviations on all sites
* Example 04 - List all equipment with its time zone
* Example 05 - Plot a current temperature
* hisReadMany date - Retrieve trends using a YYYY-MM-DD date
* hisReadMany date_range - Retrieve trends using two YYYY-MM-DD dates
* hisReadMany datetime_range - Retrieve trends using two datetime stamps
* hisReadMany today - Retrieve trends using "today" as the range
* hisReadMany latest - Retrieve the last trend point using the "latest" range
* hisReadMany yesterday - Retrieve yesterday's trend points using the "yesterday" range
* Read by_filter - Retrieve information using a tag filter
* Read by_filter_arrow - Retrieve information using a lambda function
* Read by_filter_paged - Retrieve information with a tag filter and page the results
* Read by_id - Retrieve information using an reference id

Note:  Results may differ based on the access privileges of the account used to log in.

---
## 75F API "Read" Functions
Retrieve a value or list of values using one of the following methods:
* Read by filter
* Read by filter (paged)
* Read by filter (arrow operator)
* Read by id
---
## 75F API "hisReadMany" Functions
Used to read time-series (trend) data from points in the Facilisight platform.
Points can be selected with tags or Haystack queries, and the time range can
be defined by specific DateTime ranges or through the use of commonly
defined terms (such as "today").

The request in this example uses an HTTP 1.1 POST Request and Response to
transmit and receive data.  The data is transmitted using Zinc formatted
grid and received as text in JSON format.

### Zinc formatting of the request body
#### Version
The following text, as shown, must appear as the first argument in the 
Request text to identify the version of Zinc being used:

ver:"3.0"

#### Range
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

#### ids

"ids" are GUIDs for individual points.  Each id must begin with an "@"
symbol, and only one id can appear on each line.

#### Example
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

---
## 75F Haystack Entity Types
Entity Types include:
* Point
* Buildingoccupancy
* Schedule
* Floor
* Room
* Equip
* Device

---

## Response JSON Structure
The response to these queries has three main children from the root:
* metadata
* columns
* rows

The information of interest is usually in "rows" and can be read directly into a Pandas DataFrame by:
```
response = requests.post(url, data=data, headers=hdr, timeout=30)
result = response.post()
df = pd.DataFrame(result["rows"])
```
Which makes things so much easier.

---

