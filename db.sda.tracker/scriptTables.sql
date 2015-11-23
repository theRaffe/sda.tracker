create table cat_environment(
  id_environment tinyint not null,
  code_environment varchar(20) not null unique,
  description varchar(50) not null,
  primary key(id_environment)
);

create table cat_artifact(
  id_artifact tinyint not null,
  code_artifact varchar(20) not null unique,
  path_directory varchar(50) not null,
  description varchar(100) not null,
  primary key(id_artifact)
);

create table cat_branch_git(
  id_branch tinyint not null,
  code_branch varchar(20) not null unique,
  id_environment_def tinyint not null,
  description varchar(50),
  primary key(id_branch),
  foreign key(id_environment_def) references cat_environment(id_environment)
);


create table cat_status_ticket(
  id_status tinyint not null,
  code_status varchar(20) not null unique,
  description varchar(50),
  primary key(id_status)
);

create table cat_type_tech(
  id_type_tech tinyint not null,
  code_type_tech varchar(20) not null unique,
  description varchar(50) not null,
  primary key(id_type_tech)
);

create table ticket_board(
  id_ticket varchar(20) not null,
  id_environment tinyint not null,
  id_status tinyint not null,
  user_request varchar(50) not null,
  date_requested integer not null,
  date_installed integer null,
  primary key(id_ticket),
  foreign key(id_environment) references cat_environment(id_environment),
  foreign key(id_status) references cat_status_ticket(id_status)
);

create table ticket_artifact(
  id_ticket varchar(20) not null,
  id_artifact tinyint not null,
  id_type_tech tinyint not null,
  creation_user varchar(50) not null,
  creation_date integer not null,
  modification_user varchar(50) null,
  modification_date integer null,
  primary key(id_ticket, id_artifact, id_type_tech),
  foreign key(id_ticket) references ticket_board(id_ticket),
  foreign key(id_artifact) references cat_artifact(id_artifact),
  foreign key(id_type_tech) references cat_type_tech(id_type_tech)
);

create table ticket_logging(
  id_ticket varchar(20) not null,
  id_ticket_row tinyint not null,
  creation_user varchar(50) not null,
  id_artifact tinyint null,
  id_commit varchar(100),
  creation_date integer not null,
  primary key(id_ticket, id_ticket_row),
  foreign key(id_ticket) references ticket_board(id_ticket)
);
