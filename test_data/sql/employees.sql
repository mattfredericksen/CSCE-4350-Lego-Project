insert into Employees (name, username, password, store_id) 
values 
    ('Gizela Borrett', 'Gizela', 'password', 1),
    ('Frederigo Palister', 'Frederigo', 'password', 2),
    ('Dolly Mutch', 'Dolly', 'password', 3),
    ('Dasha Delong', 'Dasha', 'password', 4),
    ('Imojean Brogi', 'Imojean', 'password', 5),
    ('Orazio Ladyman', 'Orazio', 'password', 2),
    ('Meg Mulvagh', 'Meg', 'password', 3),
    ('Karry Tatton', 'Karry', 'password', 4),
    ('Floyd MacCollom', 'Floyd', 'password', 5),
    ('Tedmund Sonner', 'Tedmund', 'password', 1),
    ('Tam Atley', 'Tam', 'password', 2),
    ('Cordell Heady', 'Cordell', 'password', 3),
    ('Cathrin Greated', 'Cathrin', 'password', 4),
    ('Aili Darinton', 'Aili', 'password', 5),
    ('Hamlen Steffens', 'Hamlen', 'password', 1),
    ('Kirbee Errichelli', 'Kirbee', 'password', 2),
    ('Veronika Chaize', 'Veronika', 'password', 3),
    ('Sal Houdmont', 'Sal', 'password', 4),
    ('Trista Weepers', 'Trista', 'password', 5),
    ('Zorina Manchester', 'Zorina', 'password', 1),
    ('Shayne Legges', 'Shayne', 'password', 2),
    ('Barth Ballay', 'Barth', 'password', 3),
    ('Kailey Tomaszewski', 'Kailey', 'password', 4),
    ('Leopold Thonason', 'Leopold', 'password', 5),
    ('Dredi Olyff', 'Dredi', 'password', 1),
    ('Timothea Gocke', 'Timothea', 'password', 2),
    ('Grete Cauley', 'Grete', 'password', 3),
    ('Donavon Grabbam', 'Donavon', 'password', 4),
    ('Standford Waggatt', 'Standford', 'password', 5),
    ('Shell Copner', 'Shell', 'password', 1),
    ('Brandais Blick', 'Brandais', 'password', 2),
    ('Miner McCormack', 'Miner', 'password', 3),
    ('Franky Coultas', 'Franky', 'password', 4),
    ('Berke Birtwell', 'Berke', 'password', 5),
    ('Delainey Joanic', 'Delainey', 'password', 1),
    ('Farrand Payley', 'Farrand', 'password', 2),
    ('Silvie Thinn', 'Silvie', 'password', 3),
    ('Staffard Bacher', 'Staffard', 'password', 4),
    ('Petunia Stockill', 'Petunia', 'password', 5),
    ('Tiffie Faulo', 'Tiffie', 'password', 1),
    ('Kessia Keat', 'Kessia', 'password', 2),
    ('Merell Lazenby', 'Merell', 'password', 3),
    ('Lance Dews', 'Lance', 'password', 4),
    ('Mick Gussin', 'Mick', 'password', 5),
    ('Elvyn Clymer', 'Elvyn', 'password', 1),
    ('Darrelle McOrkill', 'Darrelle', 'password', 2),
    ('Tamarah Bondesen', 'Tamarah', 'password', 3),
    ('Moritz Neller', 'Moritz', 'password', 4),
    ('Brice Grishanin', 'Brice', 'password', 5),
    ('Timi Leaming', 'Timi', 'password', 1);

update stores set manager_id = 5 where store_id = 1;
update stores set manager_id = 1 where store_id = 2;
update stores set manager_id = 2 where store_id = 3;
update stores set manager_id = 3 where store_id = 4;
update stores set manager_id = 4 where store_id = 5;