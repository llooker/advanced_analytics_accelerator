# lookr

A quick way to get data out of Looker without row limits.

Returns a data frame (well actually it's a [tibble](https://cran.r-project.org/web/packages/tibble/vignettes/tibble.html)) with all data from specified Look.

## set up

You will first need to create a file ~/.Renviron with the following variables:

```
LOOKER_API_PATH = 'https://???.looker.com:19999/api/3.0'
LOOKER_CLIENT_ID = '???'
LOOKER_CLIENT_SECRET = '???'
```

## installation

```
install.packages('devtools')
library('devtools')
install_github('samudzi/lookr')
```

## usage

There are two functions.  The first is the runLook Looker API endpoint, styled here as get_look:

```
library(lookr)

df = get_look(look_id = 123)  # default row limit of 500

df = get_look(look_id = 123, limit = 10000)  # custom row limit

df = get_look(look_id = 123, limit = -1)  # without row limit
```

The second function allows you to send the results of your analysis back to BigQuery as a net new table.  To use this function, you will need to set two global environment variables, `datasetid` and `projectid`:

```
datasetid = <your BQ dataset id>
projectid = <your GC project id>
```

Once set, you can save your dataframe to a table:

```
createBigQueryTable(<desired table name>, <name of R dataframe>)
```
