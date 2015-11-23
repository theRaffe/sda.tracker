delete from cat_environment;
insert into cat_environment values(1, 'maab.des', 'maab dev, fix bugs and new feat.');
insert into cat_environment values(2, 'maab.qas', 'maab release, new future feature');
insert into cat_environment values(3, 'maab.uat', 'maab hotfix, bug on production');
insert into cat_environment values(4, 'maab.qa2', 'maab incognito/broadsoft');
insert into cat_environment values(5, 'maab.prd', 'maab production');
insert into cat_environment values(6, 'izzi.des', 'izzi dev, fix bugs and new feat.');
insert into cat_environment values(7, 'izzi.qas', 'izzi release, new future feature');
insert into cat_environment values(8, 'izzi.uat', 'izzi hotfix, bug on production');
insert into cat_environment values(9, 'izzi.qa2', 'izzi incognito/broadsoft');
insert into cat_environment values(10, 'izzi.prd', 'izzi production');

delete from cat_artifact
insert into cat_artifact values(1, 'cartridge-1', 'cartridge1', 'artifact example');
insert into cat_artifact values(-1, 'unknow artifact', '', 'unregistered directory');

delete form cat_branch_git;
insert into cat_branch_git values(1, 'des', 1, 'development of hotfixes and new feat.');
insert into cat_branch_git values(2, 'qas', 2, 'development of new features');
insert into cat_branch_git values(3, 'uat', 3, 'development of hotfixes for production');
insert into cat_branch_git values(4, 'master', 5, 'production code');
insert into cat_branch_git values(5, 'brs.izzi.develop', 6, 'development of bugfixes and new feat.');
insert into cat_branch_git values(6, 'brs.izzi.release', 7, 'development of new features');
insert into cat_branch_git values(7, 'brs.izzi.hotfixes', 8, 'development of hotfixes');
insert into cat_branch_git values(8, 'brs.izzi.master', 10, 'code production new architecture');

delete from cat_status_ticket;
insert into cat_status_ticket values(1, 'requested', 'ticket requested');
insert into cat_status_ticket values(2,'installed', 'ticket installed at environment');

delete from cat_type_tech;
insert into cat_type_tech values(1, 'java', 'releases from java');
insert into cat_type_tech values(2, 'osb', 'releases from osb');
insert into cat_type_tech values(3, 'db', 'releases from db');
insert into cat_type_tech values(4, 'soa', 'releases from soa');
