CREATE TABLE IF NOT EXISTS Publisher (
    Email VARCHAR(255) PRIMARY KEY,
    Name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Author (
    Email VARCHAR(255) PRIMARY KEY,
    Name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Book (
    ISBN VARCHAR(255) PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    Price DECIMAL(10, 2) NOT NULL,
    PageCount INT,
    Genre VARCHAR(100),
    Publisher_Email VARCHAR(255),
    FOREIGN KEY (Publisher_Email) REFERENCES Publisher(Email)
);

CREATE TABLE IF NOT EXISTS Book_Author (
    ISBN VARCHAR(255),
    Author_Email VARCHAR(255),
    PRIMARY KEY (ISBN, Author_Email),
    FOREIGN KEY (ISBN) REFERENCES Book(ISBN),
    FOREIGN KEY (Author_Email) REFERENCES Author(Email)
);

CREATE TABLE IF NOT EXISTS User (
    ID INT PRIMARY KEY,
    Username VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Role Enum("customer", "admin", "author", "publisher") NOT NULL DEFAULT "customer",
    Status Enum("active", "inactive", "terminated") NOT NULL DEFAULT "active",
    Phone_Number VARCHAR(20),
    Address TEXT
);

CREATE TABLE IF NOT EXISTS Transaction (
    ID INT PRIMARY KEY,
    Date DATE NOT NULL,
    Return_Date DATE,
    Price DECIMAL(10, 2) NOT NULL,
    UserID INT,
    FOREIGN KEY (UserID) REFERENCES User(ID)
);

CREATE TABLE IF NOT EXISTS Book_Transaction (
    ISBN VARCHAR(255),
    Transaction_ID INT,
    Quantity INT,
    PRIMARY KEY (ISBN, Transaction_ID),
    FOREIGN KEY (ISBN) REFERENCES Book(ISBN),
    FOREIGN KEY (Transaction_ID) REFERENCES Transaction(ID)
);

CREATE TABLE IF NOT EXISTS Book_User (
    ISBN VARCHAR(255),
    UserID INT,
    PRIMARY KEY (ISBN, UserID),
    FOREIGN KEY (ISBN) REFERENCES Book(ISBN),
    FOREIGN KEY (UserID) REFERENCES User(ID)
);