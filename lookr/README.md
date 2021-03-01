# lookr

A quick and dirty implementation of the Looker API for R.  Specifically for importing looks without row limits, and returning dataframes into BigQuery

Returns a data frame (well actually it's a [tibble](https://cran.r-project.org/web/packages/tibble/vignettes/tibble.html)) with all data from specified Look.

## set up

You will first need to create a file ~/.Renviron with the following variables:

```
LOOKER_API_PATH = 'https://???.looker.com:19999/api/3.0'
LOOKER_CLIENT_ID = '???'
LOOKER_CLIENT_SECRET = '???'
```

If deploying via Jupyter notebook, you can alternatively set environment variables inline:

```
Sys.setenv(LOOKER_API_PATH = 'https://???.asoba.co:19999/api/3.1', LOOKER_CLIENT_ID = '???', LOOKER_CLIENT_SECRET = '???')
```

## installation

```
install.packages('devtools')
library('devtools')
install_github('llooker/advanced_analytics_accelerator/lookr')
```

## usage

There are three functions.  The first is the runLook Looker API endpoint, styled here as get_look:

```
library(lookr)

df = get_look(look_id = 123)  # default row limit of 500

df = get_look(look_id = 123, limit = 10000)  # custom row limit

df = get_look(look_id = 123, limit = -1)  # without row limit
```

The second function creates the necessary authentication token for your R environment to connect with your BigQuery instance.  Leveraging the 'bigrquery' package, invoking `provideBQauthentication()` sets the file path of your auth.json token, Cloud project ID and BQ dataset ID as global variables.
```
provideBQauthentication(json_path="~/auth.json",projectid="project-id",datasetid="dataset-id",conn="connection_name")
```

Once authenticated, you can save your dataframe to a table:

```
createBigQueryTable(<desired table name>, <name of R dataframe>)
```


To-do:

Add another function to allow for appending new rows to an existing table, leveraging the table_upload api function a la
```
bq_table_upload(x=players_table, values= players_df_2, create_disposition='CREATE_IF_NEEDED', write_disposition='WRITE_APPEND')
```
