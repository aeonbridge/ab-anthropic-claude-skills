-- Initialize databases for all services

-- Create database for Evolution API
CREATE DATABASE IF NOT EXISTS evolution;

-- Create database for Dify
CREATE DATABASE IF NOT EXISTS dify;

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE evolution TO postgres;
GRANT ALL PRIVILEGES ON DATABASE dify TO postgres;
