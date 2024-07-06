\echo 'Delete and recreate stories db?'
\prompt 'Return for yes or control-C to cancel > ' foo

DROP DATABASE stories;
CREATE DATABASE stories;
\connect stories

\echo 'Delete and recreate stories_test db?'
\prompt 'Return for yes or control-C to cancel > ' foo

DROP DATABASE stories_test;
CREATE DATABASE stories_test;
\connect stories_test