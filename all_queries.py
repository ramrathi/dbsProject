Queries
--------
"select * from Users where id = '%s';"%(session['userid'])
"select * from Community where c_id = "+id
'select name,content,time_stamp,p_id,photosrc,p_id from Users,Posts where u_id = id and (u_id in (select u2_id from Friends where u1_id =%s) or u_id = %s)'%(session["userid"],session["userid"])
'select comm_id,post_id, name,content,timestamp from Comments join Users on Users.id = Comments.user_id'
'select name,content,time_stamp,p_id,photosrc,p_id from Users,Posts where community = %s and u_id = id and (u_id in (select u2_id from Friends where u1_id =%s) or u_id = %s)'%(id,session["userid"],session["userid"])
'select comm_id,post_id, name,content,timestamp from Comments join Users on Users.id = Comments.user_id'
"select e_id,host,location,description,mediasrc,count(*) as count from Events join Attending where Attending.event_id = Events.e_id group by e_id;"
"select e_id,user_id from (Events join Attending on Events.e_id = Attending.event_id) where user_id in (select u2_id from Friends where u1_id = %s);"%(session['userid'])
"select event_id from Attending where user_id='%s';"%(session['userid'])
"select name from Users where id=%s;"%(session['fid'])
"select bio from Users where id=%s;"%(session['fid'])
"select picture from Users where id=%s;"%(session['fid'])
"select wallet from Users where id = %s"%(session['userid'])
"select y.name,u2_id from Users join Friends on (Users.id = Friends.u1_id) join (select u2_id,name from Users join Friends on (Users.id = Friends.u2_id)) as y using(u2_id) where id = %s;"%(userdata['userid'])
"select id,name from Users where id not in (select u2_id from Friends where u1_id = %s) and id <> %s and id not in (select u_id2 from Requests where u_id1 = %s);"%(session["userid"],session["userid"],session["userid"])
"select u_id1,name from Requests join Users on Users.id = Requests.u_id1 where u_id2 = %s"%(session["userid"])
"select M.*,Users.name from Users join (select m.m_id,m.From,m.Content,m.media,m.timestamp from Messages m where m.m_id in(select m1.m_id from Messages m1 where m1.To=%s and m1.From=%s UNION select m1.m_id from Messages m1 where m1.To=%s and m1.From=%s)) as M on M.From = Users.id;"%(session["userid"],session["fid"],session["fid"],session["userid"])
"select name from Users where id=%s;"%(i[1])
"select * from Transactions, Users where `from` =%s and `to`=id  order by timestamp desc;"%(session['userid'])
"select * from Users where email = '%s' and password = '%s';"%(email,password)
"select * from Users where email = '%s';"%email
"INSERT INTO `dbsproject`.`Users` (`name`, `password`, `dob`, `gender`, `email`, `wallet`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s');" %(username,password,dob,gender,email,wallet)
'select content,time_stamp,p_id,photosrc from Posts where u_id = %s;'%(session['userid'])
"update Users set bio = '%s' where id = %s"%(status,session['userid'])
"update Users set picture = '%s' where id = %s"%(picture,session['userid'])
"INSERT INTO `dbsproject`.`Posts` (`u_id`, `content`, `time_stamp`,`photosrc`) VALUES ('%s', '%s', CURTIME(),'static/%s');"%(session['userid'],content,f.filename)
"INSERT INTO `dbsproject`.`Posts` (`u_id`, `content`, `time_stamp`) VALUES ('%s', '%s', CURTIME());"%(session['userid'],content)
"INSERT INTO `dbsproject`.`Posts` (`u_id`, `content`, `time_stamp`) VALUES ('%s', '%s', CURTIME());"%(session['userid'],content)
'select i_id,title,description,price,Users.name,seller from Market join Users on Users.id = Market.seller where sold = 0'
"Select * from Market,Payment,Users where id=user_id and item_id=i_id and user_id='%s';"%(session['userid'])
'UPDATE Market set sold= 1 where i_id = %s'%(id)
'UPDATE Market set sold= 1 where i_id = %s'%(id)
"insert into Friends values (%s,%s)"%(id,session['userid'])
"insert into Friends values (%s,%s)"%(session['userid'],id)
"delete from Requests where u_id1 = %s"%(id)
"insert into Requests values (%s,%s)"%(session['userid'],id)
"delete from Friends where (u1_id = %s and u2_id = %s) or (u1_id = %s and u2_id = %s) "%(id,session['userid'],session['userid'],id)
'delete from Posts where p_id = %s'%(id)
"insert into Comments values (NULL,'%s','%s','%s',NULL)"%(id,session['userid'],comment_content)
"delete from Comments where comm_id = %s"%(id)
'UPDATE Users set wallet = wallet-%s where id = %s'%(amount,session['userid'])
'UPDATE Users set wallet = wallet + %s where id = %s'%(amount,f_id)
"INSERT INTO `dbsproject`.`Transactions` (`from`, `to`, `money`, `timestamp`, `message`) VALUES ('%s', '%s', '%s', CURTIME(), '%s');"%(session['userid'],f_id,amount,message)
"INSERT INTO `dbsproject`.`Messages` (`From`, `To`, `Content`, `timestamp`) VALUES ('%s', '%s', '%s', CURTIME());"%(session['userid'],session['fid'],content)
"INSERT INTO `dbsproject`.`Attending` VALUES ('%s', '%s');"%(id,session['userid'])
"select * from Community;"
"select * from Community, Belongs where community_id=c_id and user_id=(%s)"%(session['userid'])
'Select * from Belongs,Users where community_id='+id+' and user_id=id;'
"INSERT INTO `dbsproject`.`Belongs` VALUES('%s','%s');"%(session['userid'],id)
"INSERT INTO `dbsproject`.`Posts` (`u_id`, `content`, `time_stamp`,`photosrc`,`community`) VALUES ('%s', '%s', CURTIME(),'static/%s',%s);"%(session['userid'],content,f.filename,session['currentgroup'])
"INSERT INTO `dbsproject`.`Posts` (`u_id`, `content`, `time_stamp`,`community`) VALUES ('%s', '%s', CURTIME(),%s);"%(session['userid'],content,session['currentgroup'])
"INSERT INTO `dbsproject`.`Posts` (`u_id`, `content`, `time_stamp`,`photosrc`,`community`) VALUES ('%s', '%s', CURTIME(),'static/%s',%s);"%(session['userid'],content,f.filename,session['currentgroup'])
"INSERT INTO `dbsproject`.`Posts` (`u_id`, `content`, `time_stamp`,`community`) VALUES ('%s', '%s', CURTIME(),%s);"%(session['userid'],content,session['currentgroup'])
"INSERT INTO `dbsproject`.`Events` (`host`,`location`,`description`,mediasrc) VALUES('%s','%s','%s','static/%s')"%(session['userid'],location,description,f.filename)
"INSERT INTO `dbsproject`.`Events` (`host`,`location`,`description`) VALUES('%s','%s','%s')"%(session['userid'],location,description)
"select * from Music;"
"select * from Music, Playlist where s_id=song_id and user_id='%s';"%(session['userid'])
"select * from Music where s_id='%s';"%(id)
"select * from Music, Playlist where s_id=song_id and user_id='%s';"%(session['userid'])
"INSERT INTO `dbsproject`.`Playlist`VALUES('%s','%s')"%(session['userid'],s_id)
"INSERT INTO `dbsproject`.`Market` (`title`,`description`,`price`,`seller`,`sold`) VALUES('%s','%s','%s',%s,0)"%(title,description,price,session['userid'])
"INSERT INTO `dbsproject`.`Market` (`title`,`description`,`price`,`seller`,`sold`) VALUES('%s','%s','%s',%s,0)"%(title,description,price,session['userid'])
"INSERT INTO `dbsproject`.`Community` (`name`,`description`) VALUES('%s','%s')"%(title,description)

Triggers
-----------
Delimiter #
create or replace trigger eventgoing
after insert on Events
for each row
begin
insert into Attending values (new.e_id, new.host);
end#


Procedure 1
-----------
Delimiter #
create or replace procedure walletcheck(in userid INT, in money INT, out result INT)
begin
declare currentmoney INT;
select wallet into currentmoney from Users where id = userid;
if money > currentmoney then
	UPDATE Users set wallet = wallet - money where id = userid;
	INSERT into Payment VALUES(userid,money);
end if;
end#

Procedure 2
-----------
Delimiter #
create or replace procedure transactcheck(in userid1 INT, in money INT, in userid2 INT, in message char)
begin
declare currentmoney INT;
select wallet into currentmoney from Users where id = userid1;
if money < currentmoney then
UPDATE Users set wallet = wallet - money where id = userid1;
UPDATE Users set wallet = wallet + money where id = userid2;
INSERT into Transactions(`from`, `to`, `money`, `timestamp`, `message`) VALUES (userid1, userid2, money, CURTIME(), message);
end if;
end#

Cursors
-------
Delimiter #
CREATE OR REPLACE PROCEDURE curdemo(IN id int, OUT nam varchar(20) ,OUT descp varchar(20))
BEGIN
  DECLARE f,g CHAR(16);
  DECLARE h INT;
  DECLARE done INT DEFAULT FALSE;
  DECLARE cur3 CURSOR FOR SELECT c_id FROM Community;
  DECLARE cur1 CURSOR FOR SELECT name FROM Community;
  DECLARE cur2 CURSOR FOR SELECT description FROM Community;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

  OPEN cur1;
  OPEN cur2;
  OPEN cur3;

  read_loop: LOOP
  	FETCH cur1 INTO f;
    FETCH cur2 INTO g;
	FETCH cur3 INTO h;
    IF done THEN
      LEAVE read_loop;
    END IF;
	IF h = id THEN
	SET nam = f;
	SET descp = g;
	END IF;
  END LOOP;
  CLOSE cur1;
  CLOSE cur2;
END#
