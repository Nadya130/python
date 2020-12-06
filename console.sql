use pp_orm;

create TABLE users(
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(225),
    firstName VARCHAR(255),
    lastName VARCHAR(255),
    password VARCHAR(255),
    phoneNumber VARCHAR(20)
);

create TABLE banks(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    budget BIGINT
);

create TABLE credit(
    id INT PRIMARY KEY AUTO_INCREMENT,
    sum INT,
    data DATETIME,
    status ENUM('unpaid', 'paid'),
    userId INT,
    bankID INT,
    FOREIGN KEY (userId) REFERENCES users (id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (bankID) REFERENCES banks (id) ON UPDATE CASCADE ON DELETE CASCADE
);


insert into users (username, firstName, lastName, password, phoneNumber) VALUES ('nadya', 'Nadiia', 'Horishna', 'root', 0639332137);
insert into banks (name, budget) VALUES ('Privatbank', '157000');
insert into credit (sum, data, status, userId, bankID) VALUES ('100', current_timestamp(), 'unpaid', '1', '1');

