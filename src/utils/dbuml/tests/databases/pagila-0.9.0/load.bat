@echo on

psql -f pagila-schema.sql -h localhost -p 5432 postgres "postgres" 


