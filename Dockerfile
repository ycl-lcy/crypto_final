# Derived from official mysql image (our base image)
FROM mysql
# Add a database
ENV MYSQL_DATABASE crypto_final
# Add the content of the sql-scripts/ directory to your image
# All scripts in docker-entrypoint-initdb.d/ are automatically
# executed during container startup
COPY ./sql-scripts/ /docker-entrypoint-initdb.d/
