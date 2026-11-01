-- OPTIONAL: fictional records for a classroom demonstration, not real opportunities.
-- No accounts or passwords are created. Re-import does not duplicate these records.
USE scholarshipmatch_auth;

INSERT INTO scholarships (title, provider, country, degree, field, funding, min_cgpa, deadline, description, is_sample)
SELECT 'Future Builders Fellowship', 'Fictional Northbridge Foundation', 'Germany', 'masters', 'Engineering', 'fully_funded', 3.00, DATE_ADD(CURRENT_DATE(), INTERVAL 90 DAY),
 'Fictional classroom example for engineering graduates. This record demonstrates full funding, academic criteria and a sample deadline. It is not open for real applications.', 1
WHERE NOT EXISTS (SELECT 1 FROM scholarships WHERE title='Future Builders Fellowship' AND is_sample=1);

INSERT INTO scholarships (title, provider, country, degree, field, funding, min_cgpa, deadline, description, is_sample)
SELECT 'Digital Horizons Award', 'Fictional Meridian Institute', 'United Kingdom', 'masters', 'Computer Science', 'partial', 2.80, DATE_ADD(CURRENT_DATE(), INTERVAL 60 DAY),
 'Fictional computing award used to demonstrate search and country filters. The provider, funding and criteria are sample data, not verified scholarship information.', 1
WHERE NOT EXISTS (SELECT 1 FROM scholarships WHERE title='Digital Horizons Award' AND is_sample=1);

INSERT INTO scholarships (title, provider, country, degree, field, funding, min_cgpa, deadline, description, is_sample)
SELECT 'New Chapter Undergraduate Grant', 'Fictional Cedar Learning Trust', 'Pakistan', 'undergraduate', 'All fields', 'tuition_waiver', 2.50, DATE_ADD(CURRENT_DATE(), INTERVAL 120 DAY),
 'Fictional tuition support example for the catalogue. Use this record to demonstrate degree filtering and scholarship details. No actual award or application is offered.', 1
WHERE NOT EXISTS (SELECT 1 FROM scholarships WHERE title='New Chapter Undergraduate Grant' AND is_sample=1);

INSERT INTO scholarships (title, provider, country, degree, field, funding, min_cgpa, deadline, description, is_sample)
SELECT 'Research Pathways Scholarship', 'Fictional Willow Research School', 'Canada', 'phd', 'Social Sciences', 'fully_funded', 3.30, NULL,
 'Fictional research scholarship demonstrating an unknown deadline. A missing date is shown honestly instead of creating a countdown or assuming applications are open.', 1
WHERE NOT EXISTS (SELECT 1 FROM scholarships WHERE title='Research Pathways Scholarship' AND is_sample=1);

INSERT INTO scholarships (title, provider, country, degree, field, funding, min_cgpa, deadline, description, is_sample)
SELECT 'Global Software Scholars', 'Fictional Atlas Education Fund', 'Türkiye', 'masters', 'Software Engineering', 'fully_funded', 3.00, DATE_ADD(CURRENT_DATE(), INTERVAL 45 DAY),
 'Fictional software engineering scholarship. This entry supports a classroom walkthrough of an administrator maintaining structured scholarship records.', 1
WHERE NOT EXISTS (SELECT 1 FROM scholarships WHERE title='Global Software Scholars' AND is_sample=1);

INSERT INTO scholarships (title, provider, country, degree, field, funding, min_cgpa, deadline, description, is_sample)
SELECT 'Enterprise Futures Award', 'Fictional Harbour Business School', 'Australia', 'undergraduate', 'Business', 'partial', 2.70, DATE_SUB(CURRENT_DATE(), INTERVAL 10 DAY),
 'Fictional business award with an expired demonstration deadline. The interface must show it as closed, without suggesting it is currently accepting applications.', 1
WHERE NOT EXISTS (SELECT 1 FROM scholarships WHERE title='Enterprise Futures Award' AND is_sample=1);
