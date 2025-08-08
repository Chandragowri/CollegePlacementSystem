-- Create DB and tables for Placement System
CREATE DATABASE IF NOT EXISTS placement_db;
USE placement_db;

-- users / login
DROP TABLE IF EXISTS users;
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  fullname VARCHAR(100),
  username VARCHAR(50) UNIQUE,
  password_hash VARCHAR(255),
  email VARCHAR(100),
  role VARCHAR(30) DEFAULT 'user',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- students
DROP TABLE IF EXISTS Student;
CREATE TABLE Student (
  regNo VARCHAR(20) PRIMARY KEY,
  firstName VARCHAR(150),
  lastName VARCHAR(150),
  dob DATE,
  email VARCHAR(100),
  phoneNo VARCHAR(20),
  address VARCHAR(200),
  gender CHAR(1),
  type VARCHAR(10),
  cgpa FLOAT,
  fa VARCHAR(100),
  date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- UG & PG (optional)
DROP TABLE IF EXISTS UG;
CREATE TABLE UG (
  regNo VARCHAR(20) PRIMARY KEY,
  branch VARCHAR(100),
  semester INT,
  date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS PG;
CREATE TABLE PG (
  regNo VARCHAR(20) PRIMARY KEY,
  branch VARCHAR(100),
  semester INT,
  date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Jobs & specializations
DROP TABLE IF EXISTS Job;
CREATE TABLE Job (
  job_Id VARCHAR(60) PRIMARY KEY,
  company VARCHAR(120),
  position VARCHAR(120),
  eligibility TEXT,
  cgpa FLOAT,
  loc VARCHAR(120),
  type VARCHAR(40),
  posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS fulltime;
CREATE TABLE fulltime (
  job_Id VARCHAR(60) PRIMARY KEY,
  bond VARCHAR(40),
  package INT
);

DROP TABLE IF EXISTS internship;
CREATE TABLE internship (
  job_Id VARCHAR(60) PRIMARY KEY,
  duration VARCHAR(40),
  ppo VARCHAR(40),
  salary INT
);

DROP TABLE IF EXISTS stats;
CREATE TABLE stats (
  regno VARCHAR(100) PRIMARY KEY,
  job_id VARCHAR(60)
);

DROP TABLE IF EXISTS applied;
CREATE TABLE applied (
  regno VARCHAR(100) PRIMARY KEY,
  companies VARCHAR(500)
);

-- sample admin and sample data
INSERT INTO users (fullname, username, password_hash, email, role)
VALUES ('Admin User', 'admin', 'REPLACE_WITH_HASH', 'admin@example.com', 'admin');

INSERT INTO Student (regNo, firstName, lastName, email)
VALUES ('S1001','Alice','Kumar','alice@example.com'),
       ('S1002','Ravi','Patel','ravi@example.com');

INSERT INTO Job (job_Id, company, position, eligibility, type)
VALUES ('JOB001','TechNova','Junior Dev','CSE/B.E., CGPA 6.5 or above','Fulltime'),
       ('JOB002','DataCore','Data Intern','Any stream, interest in data','Internship');
