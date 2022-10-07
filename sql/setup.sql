/*
 route: The directory path to locate files
 */
CREATE TABLE IF NOT EXISTS bin_dirs(route TEXT PRIMARY KEY);
CREATE TABLE IF NOT EXISTS states(
    id INT PRIMARY KEY,
    meaning TEXT NOT NULL
);

INSERT INTO states VALUES(0, 'normal');
INSERT INTO states VALUES(1, 'protected');

/*
    name: the name of the interpreter
    active: if the interpreter is currently chosen
*/
CREATE TABLE IF NOT EXISTS interpreters(
    name TEXT PRIMARY KEY,
    active INT CHECK(active = 0 OR active = 1)
);

INSERT INTO interpreters VALUES('bash', 1);
INSERT INTO interpreters VALUES('cmd', 1);
INSERT INTO interpreters VALUES('powershell', 1);
INSERT INTO interpreters VALUES('python', 1);

/*
    name: the link identifier to manipulate it
    file: the path to the linked file
    program: the interpreter of the source or the source if the source is a program
    dir: the bin folder where the link is
    interpreter: the target interpreter
    attribs: the attributes
    state: indicates the link condition
*/
CREATE TABLE IF NOT EXISTS links(
    name TEXT PRIMARY KEY,
    file TEXT NOT NULL,
    program TEXT NOT NULL,
    dir TEXT NOT NULL REFERENCES bin_dirs,
    interpreter TEXT REFERENCES interpreters,
    attribs TEXT NOT NULL,
    state INT REFERENCES states(id)
);

/*
    Arguments that can modify a link based on the name
    linkname: name of the link to match
    position: 0 head, 1 middle, 2 tail
    relative: the index inside position, just for identifying but does not mean an order
    value: the actual value of the argument
*/
CREATE TABLE IF NOT EXISTS arguments(
    linkname TEXT NOT NULL,
    position NUMBER NOT NULL,
    relative NUMBER NOT NULL,
    value TEXT NOT NULL,
    active INT CHECK(active = 0 OR active = 1),
    PRIMARY KEY (linkname, position, relative),
    CHECK (position BETWEEN 0 AND 2) /*position must be between 0 and 2*/
)