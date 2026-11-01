-- Import through phpMyAdmin using a database administrator account.
-- New database name avoids mixing this phase with your older project.
-- No DROP statements. An incompatible existing users table needs review first.
CREATE DATABASE IF NOT EXISTS scholarshipmatch_auth
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE scholarshipmatch_auth;

CREATE TABLE IF NOT EXISTS users (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  full_name VARCHAR(120) NOT NULL,
  email VARCHAR(191) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  is_active TINYINT(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
