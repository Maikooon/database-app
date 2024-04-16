
create table LoginUser (
	username varchar,
	password varchar,
	birth varchar,
	pict varchar 
);

CREATE TABLE Favorites (
    user_id varchar,
    drink_id varchar
);

CREATE TABLE Favoritesfood (
    user_id varchar,
    food_id varchar
);
  
create table drink (id int primary key, drinkName varchar ,price int,kcal int, size varchar , discription varchar, season varchar ,TypeTempId varchar, pict varchar ,foreign key (season) references season(id),foreign key (TypeTempId) references Typetemp(id) );
create table food (id int primary key, foodName varchar ,price int,kcal int,pict varchar );
create table topping (id int primary key, topName varchar ,price int );
create table Typetemp (id int primary key, typeName varchar ,temp int );
create table drink_food (drink_id int ,food_id int ,primary key (drink_id, food_id ) );
create table drink_topping ( drink_id int ,topping_id int ,primary key (drink_id, topping_id ) );
create table shop (id int primary key, shopName varchar ,region_id varchar, type_id varchar, pict varchar,foreign key (region_id) references region(id),  foreign key (type_id) references ShopType(id) );
create table region (id varchar primary key, regionName varchar ,area varchar );
create table shop_drink (shop_id int, drink_id int, primary key ( shop_id, drink_id)  );
create table shop_food ( shop_id int , food_id  int ,primary key ( shop_id , food_id));
create table ShopType ( id varchar  primary key , typeName varchar , avg_price int );
create table season (id varchar primary key, start_at_month int , end_at_month int );


insert into drink values ( 1 ,"コールドブリューコーヒー" , 440 , 10 , "tall" , "まろやかな味わいのコールド ブリュー コーヒーの上に、パルタナ エキストラバージン オリーブオイルを使用したゴールデン フォームを浮かべたコーヒービバレッジ", "SEA0", "Cof1",'1.png');
insert into drink values ( 2 ,"バニラフラペチーノ" , 575 , 255 , "tall" , "ミルクとバニラのなめらかな組み合わせ", "SEA0", "Frap",'2.png');
insert into drink values ( 3 ,"抹茶ティーラテ" , 500 , 208 , "tall" , "ほろ苦い抹茶をラテに仕上げ深い味わいに", "SEA2", "Tea1",'3.png');
insert into drink values ( 4 ,"ほうじ茶" , 460 , 3 , "tall" , "香ばしく豊かな風味のティー", "SEA0", "Tea2",'4.png');
insert into drink values ( 5 ,"ホワイトモカ" , 530 , 253 , "tall" , "エスプレッソにホワイトモカシロップとミルク、ホイップクリーム", "SEA0", "Cof1",'5.png');
insert into drink values ( 6 ,"ジンジャーブレッドラテ" , 550 , 320 , "tall" , "ジンジャーブレッドクッキーのスパイシーな味わいをイメージした一杯", "SEA4", "Tea2",'6.png');
insert into drink values ( 7 ,"桜フラペチーノ" , 690 , 384 , "tall" , "桜風味の春限定フラペチーノ", "SEA1", "Frap",'7.png');
insert into drink values ( 8 ,"マロンラテ" , 490 , 303 , "tall" , "マロンとエスプレッソの相性の良さに着目し、モンブランをイメージしたビバレッジ", "SEA3", "Cof2",'8.png');
insert into drink values ( 9 ,"シェケラート" , 740 , 10 , "tall" , "ふわふわの泡を楽しむ冷たいエスプレッソ", "SEA0", "Cof1",'9.png');
insert into drink values ( 10 ,"オリアートオーツミルクラテ" , 840 , 267 , "tall" , "オリーブオイルの豊かな風味からインスピレーションを得たオーツミルク ラテ", "SEA0", "Cof2",'10.png');
insert into drink values ( 11 ,"ストロベリーパッションティー" , 605 , 93  , "tall" , "ハイビスカス、オレンジピール等をブレンドしたパッション ティーにストロベリーの果肉とフリーズドライストロベリーを合わせたフラペチーノ", "SEA2", "Tea1",'11.png');


insert into food values ( 100, "ブルーベリーチーズケーキ", 495 , 304 ,'100.png');
insert into food values ( 101, "あんバターサンド", 315 , 267,'101.png' );
insert into food values ( 102, "ドーナツ", 260 , 360 ,'102.png');
insert into food values ( 103, "チョコスコーン", 300 , 358 ,'103.png');
insert into food values ( 104, "ティラミス", 495 , 298,'104.png' );


insert into topping values ("Top1", "ホイップクリーム" , 50);
insert into topping values ("Top2", "チョコレートソース" , 0);
insert into topping values ("Top3", "チョコレートチップ" , 55);
insert into topping values ("Top4", "エスプレッソショット" , 50);


insert into Typetemp values ("Cof1" , "コーヒー", "cold");
insert into Typetemp values ("Cof2" , "コーヒー", "hot");
insert into Typetemp values ("Frap" , "フラペチーノ", "cold");
insert into Typetemp values ("Tea1" , "ティー", "cold");
insert into Typetemp values ("Tea2" , "ティー", "hot");


insert into drink_food values ( 1 , 101 );
insert into drink_food values ( 1 , 104 );
insert into drink_food values ( 3 , 100 );
insert into drink_food values ( 4 , 100 );
insert into drink_food values ( 1 , 102 );
insert into drink_food values ( 1 , 103 );
insert into drink_food values ( 5 , 103 );


insert into drink_topping values (5, "Top4" );
insert into drink_topping values (5, "Top1" );
insert into drink_topping values (2, "Top3" );
insert into drink_topping values (2, "Top2" );
insert into drink_topping values (3, "Top2" );


insert into shop values ("S1", "丸の内オアゾ","R1", "T1",'S1.png');
insert into shop values ("S2", "函館ベイサイド店","R3", "T1",'S2.png');
insert into shop values ("S3", "からすま京都ホテル店","R4", "T1",'S3.png');
insert into shop values ("S4", "銀座マロニエ通り","R1", "T2",'S4.png');
insert into shop values ("S5", "アークヒルズ店","R1", "T2",'S5.png');
insert into shop values ("S6", "名古屋JRゲートタワー","R2", "T2",'S6.png');


insert into region values ( "R1", "東京", "関東");
insert into region values ( "R2", "愛知", "中部");
insert into region values ( "R3", "北海道", "北海道");
insert into region values ( "R4", "京都", "関西");



insert into shop_drink values ("S1", 1 );
insert into shop_drink values ("S1", 2 );
insert into shop_drink values ("S1", 3 );
insert into shop_drink values ("S1", 4 );
insert into shop_drink values ("S1", 5 );
insert into shop_drink values ("S1", 6 );
insert into shop_drink values ("S1", 7 );
insert into shop_drink values ("S1", 8 );

insert into shop_drink values ("S2", 1 );
insert into shop_drink values ("S2", 2 );
insert into shop_drink values ("S2", 3 );
insert into shop_drink values ("S2", 4 );
insert into shop_drink values ("S2", 5 );
insert into shop_drink values ("S2", 6 );
insert into shop_drink values ("S2", 7 );
insert into shop_drink values ("S2", 8 );

insert into shop_drink values ("S3", 1 );
insert into shop_drink values ("S3", 2 );
insert into shop_drink values ("S3", 3 );
insert into shop_drink values ("S3", 4 );
insert into shop_drink values ("S3", 5 );
insert into shop_drink values ("S3", 6 );
insert into shop_drink values ("S3", 7 );
insert into shop_drink values ("S3", 8 );

insert into shop_drink values ("S4", 1 );
insert into shop_drink values ("S4", 2 );
insert into shop_drink values ("S4", 3 );
insert into shop_drink values ("S4", 4 );
insert into shop_drink values ("S4", 5 );
insert into shop_drink values ("S4", 6 );
insert into shop_drink values ("S4", 7 );
insert into shop_drink values ("S4", 8 );
insert into shop_drink values ("S4", 9 );
insert into shop_drink values ("S4", 10 );

insert into shop_drink values ("S5", 1 );
insert into shop_drink values ("S5", 2 );
insert into shop_drink values ("S5", 3 );
insert into shop_drink values ("S5", 4 );
insert into shop_drink values ("S5", 5 );
insert into shop_drink values ("S5", 6 );
insert into shop_drink values ("S5", 7 );
insert into shop_drink values ("S5", 8 );
insert into shop_drink values ("S5", 11 );

insert into shop_drink values ("S6", 1 );
insert into shop_drink values ("S6", 2 );
insert into shop_drink values ("S6", 3 );
insert into shop_drink values ("S6", 4 );
insert into shop_drink values ("S6", 5 );
insert into shop_drink values ("S6", 6 );
insert into shop_drink values ("S6", 7 );
insert into shop_drink values ("S6", 8 );
insert into shop_drink values ("S6", 9 );



insert into shop_food values ( "S1", 100 );
insert into shop_food values ( "S1", 101 );
insert into shop_food values ( "S1", 102 );
insert into shop_food values ( "S1", 103 );
insert into shop_food values ( "S1", 104 );

insert into shop_food values ( "S2", 100 );
insert into shop_food values ( "S2", 101 );
insert into shop_food values ( "S2", 102 );
insert into shop_food values ( "S2", 103 );
insert into shop_food values ( "S2", 104 );

insert into shop_food values ( "S3", 100 );
insert into shop_food values ( "S3", 101 );
insert into shop_food values ( "S3", 102 );
insert into shop_food values ( "S3", 103 );
insert into shop_food values ( "S3", 104 );

insert into shop_food values ( "S4", 100 );
insert into shop_food values ( "S4", 101 );
insert into shop_food values ( "S4", 102 );
insert into shop_food values ( "S4", 103 );
insert into shop_food values ( "S4", 104 );

insert into shop_food values ( "S5", 100 );
insert into shop_food values ( "S5", 101 );
insert into shop_food values ( "S5", 102 );
insert into shop_food values ( "S5", 103 );
insert into shop_food values ( "S5", 104 );

insert into shop_food values ( "S6", 100 );
insert into shop_food values ( "S6", 101 );
insert into shop_food values ( "S6", 102 );
insert into shop_food values ( "S6", 103 );
insert into shop_food values ( "S6", 104 );


insert into ShopType values ( "T1", "一般店舗",430);
insert into ShopType values ( "T2", "Reaserved店舗",1000);


insert into season  values ("SEA0", 1 , 12 );
insert into season  values ("SEA1", 2 , 4 );
insert into season  values ("SEA2", 5 ,8 );
insert into season  values ("SEA3", 9 , 11 );
insert into season  values ("SEA4", 12 , 1 );

create view  drinkview as
select drinkName , price , discription  
from drink;

create view  shopinfo as
select  s.shopName, st.typeName, st.avg_price
from  shop s
join ShopType st on s.type_id = st.id;

create view drinkreccomend as
select d.drinkName, f.foodName
from drink d
inner join drink_food df on d.id = df.drink_id
inner join food f on df.food_id = f.id;
