-- Run in phpMyAdmin as an administrator. Keep the existing database and accounts.
USE scholarshipmatch_auth;

-- MySQL-compatible, repeatable column addition. Existing accounts stay applicants.
SET @role_exists = (SELECT COUNT(*) FROM information_schema.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'users' AND COLUMN_NAME = 'role');
SET @upgrade_sql = IF(@role_exists = 0,
  'ALTER TABLE users ADD COLUMN role VARCHAR(20) NOT NULL DEFAULT ''applicant''',
  'SELECT ''users.role already exists'' AS upgrade_status');
PREPARE upgrade_statement FROM @upgrade_sql;
EXECUTE upgrade_statement;
DEALLOCATE PREPARE upgrade_statement;

CREATE TABLE IF NOT EXISTS profiles (
  user_id INT UNSIGNED NOT NULL PRIMARY KEY,
  degree VARCHAR(20) NOT NULL,
  field VARCHAR(80) NOT NULL,
  cgpa DECIMAL(3,2) NOT NULL,
  nationality VARCHAR(80) NOT NULL,
  age SMALLINT UNSIGNED NOT NULL,
  preferred_country VARCHAR(80) NOT NULL,
  preferred_funding VARCHAR(30) NOT NULL,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  CHECK (cgpa BETWEEN 0 AND 4),
  CHECK (age BETWEEN 16 AND 100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS scholarships (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(140) NOT NULL,
  provider VARCHAR(120) NOT NULL,
  country VARCHAR(80) NOT NULL,
  degree VARCHAR(20) NOT NULL,
  field VARCHAR(80) NOT NULL,
  funding VARCHAR(30) NOT NULL,
  min_cgpa DECIMAL(3,2) NOT NULL,
  deadline DATE NULL,
  official_url VARCHAR(500) NOT NULL DEFAULT '',
  description TEXT NOT NULL,
  is_active TINYINT NOT NULL DEFAULT 1,
  is_sample TINYINT NOT NULL DEFAULT 0,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CHECK (min_cgpa BETWEEN 0 AND 4),
  INDEX catalogue_filters (is_active, country, degree, funding)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
