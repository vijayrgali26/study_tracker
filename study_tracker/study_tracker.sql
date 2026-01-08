CREATE DATABASE study_tracker2;
USE study_tracker2;
DESCRIBE timetable1;

CREATE TABLE goals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    goal_name VARCHAR(255),
    start_date DATE,
    end_date DATE,
    target_hours INT,
    hours_completed FLOAT DEFAULT 0
);

CREATE TABLE timetable1 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE,
    start_time TIME,
    end_time TIME,
    total_hours FLOAT,
    tasks TEXT
);

ALTER TABLE goals ADD COLUMN completed BOOLEAN DEFAULT FALSE;

ALTER TABLE timetable1 ADD COLUMN completed BOOLEAN DEFAULT FALSE;