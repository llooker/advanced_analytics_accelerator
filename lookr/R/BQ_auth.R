# Provide authentication
## Set GC_BQ_PROJECTID and GC_BQ_DATASETID and environment variables in your .Renviron

provideBQAuthentication <- function(json_path="../service/auth.json",projectid=Sys.getenv("GC_BQ_PROJECTID"),
                                    datasetid=Sys.getenv("GC_BQ_DATASETID"),conn="bq_conn") 
{
  bq_auth(path = json_path)
  bq_auth(use_oob = TRUE)
  df <-  dbConnect(bigquery(),
                        project = projectid,
                        dataset = datasetid,
                        use_legacy_sql = FALSE
  )
  #browser()
  assign(conn, df, envir=.GlobalEnv)
  assign("projectid",projectid, envir=.GlobalEnv)
  assign("datasetid",datasetid, envir=.GlobalEnv)
}
