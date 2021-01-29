createBigQueryTable = function(table_name, df) {
  assertthat::assert_that(exists("datasetid"), 
                          msg = "`datasetid` variable is not available in .GlobalEnv")
  assertthat::assert_that(exists("projectid"), 
                          msg = "`projectid` variable is not available in .GlobalEnv")
                          
  df.1 = bigrquery::bq_table(.GlobalEnv$projectid, .GlobalEnv$datasetid, table = table_name)
  bigrquery::bq_table_upload(df.1,
                             df,
                             quiet = FALSE,
                             fields = bigrquery::as_bq_fields(df))
}
