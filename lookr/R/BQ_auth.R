# Provide authentication
## input auth.json file location
provideBQAuthentication <- function(json_path="~/auth.json",projectid="project-id",datasetid="dataset-id",conn="bq_conn") 
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
