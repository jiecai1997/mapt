INSERT INTO Users VALUES (0, 'sqllover@duke.edu', crypt('password', gen_salt('bf')));
INSERT INTO Users VALUES (1, 'ra4ever@duke.edu', crypt('otherpassword', gen_salt('bf')));

INSERT INTO Trips VALUES(0, 0, 'to internship');
INSERT INTO Trips VALUES(1, 1, 'graduation');
INSERT INTO Trips VALUES(2, 0, 'from internship');


INSERT INTO Airlines VALUES('DL', 'Delta Air Lines');
INSERT INTO Airlines VALUES ('AS', 'Alaska Airlines');

INSERT INTO Airports VALUES ('RDU', 'Raleigh Durham International Airport', 'Raleigh-Durham', 'USA', 35.8776, -78.7875, 'America/ New_York', 'A');
INSERT INTO Airports VALUES ('IAD', 'Washington Dulles International Airport', 'Washington, DC', 'USA', 38.9445, -77.4558, 'America/ New_York', 'A');
INSERT INTO Airports VALUES ('SEA', 'Seattle Tacoma International Airport', 'Seattle', 'USA', 47.4490, -122.309, 'America/ Los_Angeles', 'A');
INSERT INTO Airports VALUES ('BWI', 'Baltimore/Washington International Thurgood Marshall Airport', 'Baltimore', 'USA', 39.1754, -76.6683, 'America/ New_York', 'A');

INSERT INTO Flights VALUES(3, 2, 'AS', 0922, 'SEA', 'BWI', '20190727 08:00:00 AM', '20190727 4:15:00 PM', 315, 2335);
INSERT INTO Flights VALUES(2, 1, 'DL', 2220, 'IAD', 'SEA', '20190609 05:00:00 PM', '20190609 07:39:00 PM', 339, 2306);
INSERT INTO Flights VALUES(1, 1, 'DL', 2680, 'SEA', 'IAD', '20190605 10:45:00 PM', '20190606 06:07:00 AM', 339, 2306);
INSERT INTO Flights VALUES(0, 0, 'DL', 1253, 'RDU', 'SEA', '20190505 07:25:00 AM', '20190505 10:13:00 AM', 348, 2355);

INSERT INTO Details VALUES(1, 1, 'IAD', 'Best place to get boba is TeaDM');
INSERT INTO Details VALUES(0, 1, 'IAD', 'Lots of cool museums to go to!');
